from flask import Response
import json
import stripe
import os
from datetime import datetime

stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "sk_test_dummy")
WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "whsec_test_dummy")

def create_payment_intent(amount_cents, client_name, project):
    """Create a Stripe payment intent for an invoice."""
    try:
        intent = stripe.PaymentIntent.create(
            amount=amount_cents,
            currency="usd",
            metadata={
                "client_name": client_name,
                "project": project,
                "timestamp": datetime.now().isoformat()
            }
        )
        return {"status": "success", "client_secret": intent.client_secret, "intent_id": intent.id}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def handle_webhook(request):
    """Handle Stripe webhook events (charge.succeeded, charge.failed, etc)."""
    try:
        payload = request.get_data(as_text=True)
        sig_header = request.headers.get("Stripe-Signature")
        
        # Verify webhook signature (disabled for test)
        # event = stripe.Webhook.construct_event(payload, sig_header, WEBHOOK_SECRET)
        
        evt = json.loads(payload)
        evt_type = evt.get("type")
        
        if evt_type == "payment_intent.succeeded":
            intent_id = evt["data"]["object"]["id"]
            print(f"Payment succeeded: {intent_id}")
        elif evt_type == "payment_intent.payment_failed":
            intent_id = evt["data"]["object"]["id"]
            print(f"Payment failed: {intent_id}")
        
        return Response(json.dumps({"received": True}), status=200, content_type="application/json")
    except Exception as e:
        print(f"Webhook error: {e}")
        return Response(status=400)
