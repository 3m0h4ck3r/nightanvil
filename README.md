# NightAnvil — Freelancer Business Toolkit

**Forge gigs in the dark — loud, sharp, uncompromising.**

NightAnvil is a complete Python/Flask toolkit for freelancers who want to ship high-converting Fiverr gigs, manage invoices, collect payments via Stripe, and auto-list gigs to multiple platforms.

## Features

✅ **Gig Generator** — AI-powered descriptions, titles, pricing  
✅ **Invoice Management** — Generate PDFs, track payments, Stripe integration  
✅ **User Dashboards** — Manage gigs, clients, invoices, revenue tracking  
✅ **Fiverr Integration** — One-click gig sync to Fiverr marketplace  
✅ **Stripe Payments** — Accept card payments, webhooks, secure checkout  
✅ **Authentication** — User registration, login, secure sessions  
✅ **Dark UI** — Professional NightAnvil brand (Orbitron + neon gradients)  
✅ **GitHub Pages** — Static landing site for business verification  
✅ **CI/CD** — GitHub Actions auto-tests and deploys to Railway  
✅ **Database** — PostgreSQL + SQLAlchemy for user/invoice/gig history  

## Quick Start (Local)

### 1. Clone & Setup

```bash
git clone https://github.com/yourusername/nightanvil.git
cd nightanvil
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your Stripe keys, etc.
```

### 3. Initialize Database & Run

```bash
python -c "from app import app, db; db.create_all()" <<< "from app import app; with app.app_context(): db.create_all()"
export FLASK_APP=app.py
flask run
```

Visit http://127.0.0.1:5000 → **Register** → **Create Gigs** → **Manage Dashboard**

### 4. Test Stripe (Sandbox)

Use test card: `4242 4242 4242 4242` | CVC `111` | Any future date

## CLI Commands

```bash
# Generate a gig description
python -m gigforge.cli gig --title "React Landing Page" --hours 20 --rate 40

# Generate an invoice PDF
python -m gigforge.cli invoice --client "Acme" --project "Site" --items "Design:800" "Dev:1200" --out invoice.pdf

# Create a promo image
python -m gigforge.cli promo --title "React Pro" --subtitle "Fast Delivery" --out promo.png
```

## Deployment

### GitHub Pages (Stripe Business Verification)

```bash
# Enable in repo settings > Pages > Deploy from branch > /docs
# Your site: https://yourusername.github.io/nightanvil/
```

### Railway (Free Tier)

```bash
# 1. Connect GitHub repo to Railway
# 2. Set environment variables (SECRET_KEY, DATABASE_URL, STRIPE_*, FIVERR_*)
# 3. Auto-deploys on push to main branch
# Your site: https://nightanvil-[random].railway.app
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

## Architecture

```
nightanvil/
├── app.py                    # Flask app, routes, auth
├── gigforge/
│   ├── models.py             # SQLAlchemy: User, Client, Invoice, Gig
│   ├── utils.py              # PDF, promo image, pricing
│   ├── payments.py           # Stripe integration
│   ├── fiverr_api.py         # Fiverr gig sync
│   ├── ai_stub.py            # OpenAI hook (optional)
│   ├── cli.py                # CLI commands
│   └── templates/            # Jinja2 templates
├── static/
│   └── css/night_theme.css   # Dark UI theme
├── templates/
│   ├── landing.html          # Public landing
│   ├── login.html            # Auth pages
│   ├── register.html
│   ├── checkout.html         # Stripe payment UI
│   ├── dashboard.html        # User dashboard
│   ├── gig_form.html         # Gig creator
│   └── ...
├── docs/
│   └── index.html            # GitHub Pages landing
├── .github/workflows/
│   └── ci.yml                # GitHub Actions CI/CD
├── Procfile                  # Heroku/Railway deployment
├── requirements.txt
└── README.md
```

## Environment Variables

```bash
# Core
FLASK_ENV=development
SECRET_KEY=your-secure-random-key
DATABASE_URL=postgresql://...  # or sqlite:///nightanvil.db

# Stripe (get from https://dashboard.stripe.com)
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=whsec_test_...

# Fiverr (optional)
FIVERR_API_KEY=...
FIVERR_SELLER_ID=...

# OpenAI (optional for AI descriptions)
OPENAI_API_KEY=...
```

## Business Model

**Sell NightAnvil as a Fiverr gig:**
- "I'll create a high-converting Fiverr gig for your service" ($50–200)
- "Professional invoice + proposal package" ($25–75)
- "Stripe payment integration setup" ($100–300)
- "AI gig description + Fiverr optimization" ($30–100)

**SaaS variant:**
- Deploy to Railway, charge monthly ($9–29/mo)
- Include Stripe sub payments, client management, gig auto-posting

## Tech Stack

- **Backend:** Python 3.11, Flask, SQLAlchemy
- **Database:** PostgreSQL (prod) / SQLite (local)
- **Payments:** Stripe API
- **Frontend:** HTML5, CSS3, Vanilla JS, Orbitron font
- **Deployment:** Railway/Heroku, GitHub Actions, GitHub Pages
- **Integrations:** Fiverr API, Stripe Webhooks

## License

MIT. Use freely, modify, sell gigs using this.

## Support

- **GitHub Issues:** Report bugs, request features
- **Docs:** See DEPLOYMENT.md for deployment guides
- **Examples:** Check CLI commands and API routes in app.py

---

**Built with ⚒ for freelancers who dare to be different.**

