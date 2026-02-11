# Deployment Guide

## GitHub Pages (For Stripe Business Verification)

GitHub Pages hosts the static landing site at:
```
https://yourusername.github.io/nightanvil/
```

Enable in GitHub repo settings:
1. Go to Settings > Pages
2. Select "Deploy from branch"
3. Choose "main" and "/docs" folder
4. Save

Your GitHub Pages site is now live for Stripe business website verification.

## Railway Deployment (Free Tier)

Railway offers free deployments with generous limits.

### Prerequisites
- GitHub account linked to Railway
- Railway account (https://railway.app)

### Steps

1. **Connect GitHub Repository**
   - Go to https://railway.app/dashboard
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your nightanvil repository
   - Authorize Railway to access GitHub

2. **Set Environment Variables**
   In Railway dashboard:
   ```
   DATABASE_URL=postgresql://[auto-generated]
   SECRET_KEY=[generate a secure random string]
   STRIPE_SECRET_KEY=sk_test_...
   STRIPE_PUBLISHABLE_KEY=pk_test_...
   STRIPE_WEBHOOK_SECRET=whsec_test_...
   FIVERR_API_KEY=[optional]
   FIVERR_SELLER_ID=[optional]
   ```

3. **Deploy**
   Railway auto-deploys on every push to `main` branch.
   - Check logs in Railway dashboard
   - Your app runs at `https://nightanvil-[random].railway.app`

### Database Setup

Railway auto-provisions PostgreSQL. Initialize the database:

```bash
# SSH into Railway container (via CLI or dashboard)
flask db init
flask db migrate
flask db upgrade
```

Or set up a release command in `Procfile`:
```
release: flask db upgrade
```

## Local Development

For PostgreSQL locally:
```bash
# Using Docker
docker run --name nightanvil-db -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres:15

# Then set in .env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/nightanvil
```

## Heroku (Paid After Demo Period)

If deploying to Heroku after free trial ends, use:
```bash
# Install Heroku CLI
brew install heroku/brew/heroku

# Login and deploy
heroku login
heroku create nightanvil
git push heroku main

# Set variables
heroku config:set SECRET_KEY='...'
heroku config:set STRIPE_SECRET_KEY='...'
```

## Stripe Account Setup

1. Go to https://dashboard.stripe.com/register
2. Create account (business verification required)
3. For verification, use your GitHub Pages URL:
   ```
   https://yourusername.github.io/nightanvil/
   ```
4. Once verified, get live API keys
5. Update Railway env vars with live keys:
   ```
   STRIPE_SECRET_KEY=sk_live_...
   STRIPE_PUBLISHABLE_KEY=pk_live_...
   ```

## Monitoring & Logs

**Railway:**
- Dashboard logs: View in web UI
- CLI: `railway logs -f`

**Stripe:**
- Test payments: https://dashboard.stripe.com/test/payments
- Webhooks: https://dashboard.stripe.com/webhooks

## GitHub Actions CI/CD

Tests and deploys run automatically on push to `main`:
- Runs pytest suite
- Linting checks
- Auto-deploys to Railway on pass
