import requests
import os
from typing import Dict, Optional

FIVERR_API_URL = "https://www.fiverr.com/api/v1"  # Placeholder - Fiverr's public API is limited
FIVERR_API_KEY = os.getenv("FIVERR_API_KEY", "")
FIVERR_SELLER_ID = os.getenv("FIVERR_SELLER_ID", "")

def create_gig(title: str, description: str, price_in_cents: int, category: str = "writing") -> Optional[Dict]:
    """
    Create a gig on Fiverr (stub - Fiverr's public API is limited).
    In production, you'd use their GraphQL API or manual submission.
    """
    if not FIVERR_API_KEY or not FIVERR_SELLER_ID:
        return {"error": "Fiverr credentials not configured", "status": "error"}
    
    try:
        payload = {
            "seller_id": FIVERR_SELLER_ID,
            "title": title,
            "description": description,
            "price": price_in_cents / 100,  # Convert cents to dollars
            "category": category,
            "delivery_time": 7  # days
        }
        
        # Note: Actual Fiverr API authentication and endpoint varies
        # This is a placeholder structure for later implementation
        response = requests.post(
            f"{FIVERR_API_URL}/gig/create",
            json=payload,
            headers={"Authorization": f"Bearer {FIVERR_API_KEY}"},
            timeout=10
        )
        
        if response.status_code == 201:
            data = response.json()
            return {
                "status": "success",
                "gig_id": data.get("gig_id"),
                "url": data.get("url")
            }
        else:
            return {"error": response.text, "status": "error"}
    except Exception as e:
        return {"error": str(e), "status": "error"}

def sync_gig_to_fiverr(gig_title: str, gig_description: str, price: float) -> Dict:
    """Sync a NightAnvil gig to Fiverr marketplace."""
    price_cents = int(price * 100)
    return create_gig(gig_title, gig_description, price_cents)

def fetch_fiverr_gigs() -> Optional[list]:
    """Fetch seller's gigs from Fiverr (stub)."""
    if not FIVERR_API_KEY or not FIVERR_SELLER_ID:
        return []
    
    try:
        response = requests.get(
            f"{FIVERR_API_URL}/seller/{FIVERR_SELLER_ID}/gigs",
            headers={"Authorization": f"Bearer {FIVERR_API_KEY}"},
            timeout=10
        )
        if response.status_code == 200:
            return response.json().get("gigs", [])
    except Exception as e:
        print(f"Error fetching Fiverr gigs: {e}")
    
    return []
