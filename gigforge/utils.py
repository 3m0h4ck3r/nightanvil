import io, datetime, os
from jinja2 import Environment, FileSystemLoader
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from PIL import Image, ImageDraw, ImageFont

PKG_DIR = os.path.dirname(__file__)
TEMPLATES_DIR = os.path.join(PKG_DIR, "templates")
env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

def calc_price(hours=None, rate=None, fixed=None, margin=0.2):
    if fixed is not None:
        base = fixed
    else:
        base = (hours or 0) * (rate or 0)
    return round(base * (1 + margin), 2)

def render_template(tmpl_name, ctx):
    tmpl = env.get_template(tmpl_name)
    return tmpl.render(**ctx)

def build_proposal_context(payload):
    now = datetime.date.today().isoformat()
    return {
        "client": payload.get("client","Client"),
        "project": payload.get("project","Project"),
        "author": payload.get("author","Freelancer"),
        "date": now,
        "summary": payload.get("summary", f"Work to deliver {payload.get('project','Project')}"),
        "deliverables": payload.get("deliverables", ["Design","Dev","Test"]),
        "start_date": payload.get("start_date", now),
        "duration": payload.get("duration", 7),
        "price": payload.get("price", calc_price(payload.get("hours",0), payload.get("rate",0), payload.get("fixed",None))),
        "revisions": payload.get("revisions", 2)
    }

def invoice_pdf(items, client_name, project, out_stream):
    c=canvas.Canvas(out_stream, pagesize=A4)
    w,h = A4
    c.setFont("Helvetica-Bold",16)
    c.drawString(30*mm, h-30*mm, "INVOICE")
    c.setFont("Helvetica",10)
    c.drawString(30*mm,h-40*mm, f"To: {client_name}")
    c.drawString(30*mm,h-46*mm, f"Project: {project}")
    c.drawString(30*mm,h-52*mm, f"Date: {datetime.date.today().isoformat()}")
    y = h - 70*mm
    total = 0.0
    c.setFont("Helvetica-Bold",11)
    c.drawString(30*mm,y, "Description")
    c.drawString(140*mm,y, "Amount")
    c.setFont("Helvetica",10)
    y -= 8*mm
    for desc, amt in items:
        c.drawString(30*mm,y, desc)
        c.drawRightString(200*mm,y, f"${amt:.2f}")
        total += amt; y -= 8*mm
    c.setFont("Helvetica-Bold",12)
    c.drawString(30*mm,y-5*mm, "Total:")
    c.drawRightString(200*mm,y-5*mm, f"${total:.2f}")
    c.showPage(); c.save()
    return total

def generate_invoice_pdf_bytes(items, client_name, project):
    buf = io.BytesIO()
    invoice_pdf(items, client_name, project, buf)
    buf.seek(0); return buf.read()

def generate_promo_image(title, subtitle, bg_color=(6,4,10), size=(1200,630)):
    img = Image.new("RGB", size, bg_color)
    draw = ImageDraw.Draw(img)
    try:
        font_title = ImageFont.truetype("DejaVuSans-Bold.ttf", 72)
        font_sub = ImageFont.truetype("DejaVuSans.ttf", 36)
    except Exception:
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()
    w,h = draw.textsize(title, font=font_title)
    draw.text(((size[0]-w)/2, size[1]*0.22), title, fill=(234,246,255), font=font_title)
    w2,h2 = draw.textsize(subtitle, font=font_sub)
    draw.text(((size[0]-w2)/2, size[1]*0.42), subtitle, fill=(139,92,246), font=font_sub)
    footer = f"NightAnvil • {datetime.date.today().year}"
    draw.text((20, size[1]-40), footer, fill=(153,163,179), font=font_sub)
    out = io.BytesIO(); img.save(out, format="PNG"); out.seek(0); return out.read()
def calc_price(hours=0, rate=0, fixed=None, margin=0.2):
    if fixed is not None:
        base = fixed
    else:
        base = hours * rate
    return round(base * (1+margin),2)
