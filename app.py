from flask import Flask, request, send_file, render_template, jsonify, redirect, url_for, session
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from gigforge import utils, payments, ai_stub
from gigforge.models import db, User, Client, Invoice, Gig, InvoiceItem
from gigforge import fiverr_api
import io, os, json
from datetime import datetime

app = Flask(__name__, static_folder="static", template_folder="templates")
app.config['JSON_SORT_KEYS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-prod')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///nightanvil.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def index():
    return render_template("landing.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        business_name = request.form.get('business_name', 'My Business')
        
        if User.query.filter_by(username=username).first():
            return render_template('register.html', error='Username exists')
        
        user = User(username=username, email=email, business_name=business_name)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('dashboard'))
    return render_template('register.html')

@app.route("/dashboard")
@login_required
def dashboard():
    invoices = Invoice.query.filter_by(user_id=current_user.id).all()
    gigs = Gig.query.filter_by(user_id=current_user.id).all()
    clients = Client.query.filter_by(user_id=current_user.id).all()
    total_revenue = sum(inv.amount for inv in invoices if inv.status == 'paid')
    return render_template('dashboard.html', invoices=invoices, gigs=gigs, clients=clients, total_revenue=total_revenue)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/checkout")
def checkout():
    return render_template("checkout.html")

@app.route("/gigs/new", methods=['GET', 'POST'])
@login_required
def create_gig():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        price = float(request.form.get('price', 0))
        
        gig = Gig(user_id=current_user.id, title=title, description=description, price=price)
        db.session.add(gig)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('gig_form.html')

@app.route("/gigs/<int:gig_id>/sync-fiverr", methods=['POST'])
@login_required
def sync_gig_to_fiverr(gig_id):
    gig = Gig.query.get_or_404(gig_id)
    if gig.user_id != current_user.id:
        return jsonify({"error": "Unauthorized"}), 403
    
    result = fiverr_api.sync_gig_to_fiverr(gig.title, gig.description, gig.price)
    if result.get('status') == 'success':
        gig.fiverr_gig_id = result.get('gig_id')
        gig.fiverr_url = result.get('url')
        gig.status = 'fiverr_sync'
        db.session.commit()
        return jsonify({"status": "success", "url": gig.fiverr_url})
    return jsonify(result), 400

@app.route("/api/invoices/new", methods=['POST'])
@login_required
def create_invoice_api():
    data = request.json or {}
    client_id = data.get('client_id')
    project = data.get('project', 'Project')
    items_data = data.get('items', [])
    
    total = sum(item['amount'] for item in items_data)
    invoice = Invoice(user_id=current_user.id, client_id=client_id, project=project, amount=total)
    db.session.add(invoice)
    db.session.flush()
    
    for item in items_data:
        inv_item = InvoiceItem(invoice_id=invoice.id, description=item['desc'], amount=item['amount'])
        db.session.add(inv_item)
    
    db.session.commit()
    return jsonify({"status": "success", "invoice_id": invoice.id})

@app.route("/generate_invoice", methods=["POST"])
def generate_invoice_form():
    client = request.form.get("client","Client")
    project = request.form.get("project","Project")
    items_raw = request.form.get("items","")
    items = []
    for it in items_raw.split(","):
        if ":" in it:
            d,a = it.split(":",1)
            try:
                items.append((d.strip(), float(a)))
            except:
                pass
    pdf_bytes = utils.generate_invoice_pdf_bytes(items, client, project)
    return send_file(io.BytesIO(pdf_bytes), mimetype="application/pdf",
                     as_attachment=True, download_name="invoice.pdf")

@app.route("/api/generate_proposal", methods=["POST"])
def api_proposal():
    payload = request.json or {}
    ctx = utils.build_proposal_context(payload)
    md = utils.render_template("proposal.md.j2", ctx)
    return {"proposal_markdown": md}

@app.route("/api/generate_promo", methods=["POST"])
def api_promo():
    data = request.json or {}
    title = data.get("title","NightAnvil Gig")
    subtitle = data.get("subtitle","Professional services")
    png = utils.generate_promo_image(title, subtitle)
    return send_file(io.BytesIO(png), mimetype="image/png",
                     as_attachment=True, download_name="promo.png")

@app.route("/api/create_payment_intent", methods=["POST"])
def create_payment_intent():
    """API endpoint to create a Stripe payment intent for checkout."""
    data = request.json or {}
    amount = data.get("amount", 0)  # in cents
    client_name = data.get("client_name", "Client")
    project = data.get("project", "Project")
    
    if amount < 50:
        return jsonify({"status": "error", "message": "Amount must be at least $0.50"}), 400
    
    result = payments.create_payment_intent(amount, client_name, project)
    return jsonify(result)

@app.route("/webhook/payments", methods=["POST"])
def webhook_payments():
    return payments.handle_webhook(request)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
