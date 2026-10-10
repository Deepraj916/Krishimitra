# scripts/price_scraper.py
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Curated fallback prices for Maharashtra APMC mandis
FALLBACK_PRICES = [
    {"commodity": "Tomato", "market": "Pune", "price": "₹1,800 / Quintal"},
    {"commodity": "Tomato", "market": "Nashik", "price": "₹1,650 / Quintal"},
    {"commodity": "Tomato", "market": "Kolhapur", "price": "₹1,900 / Quintal"},
    {"commodity": "Onion", "market": "Nashik", "price": "₹2,400 / Quintal"},
    {"commodity": "Onion", "market": "Pune", "price": "₹2,550 / Quintal"},
    {"commodity": "Onion", "market": "Ahmednagar", "price": "₹2,300 / Quintal"},
    {"commodity": "Potato", "market": "Pune", "price": "₹1,500 / Quintal"},
    {"commodity": "Potato", "market": "Mumbai", "price": "₹1,700 / Quintal"},
    {"commodity": "Potato", "market": "Nagpur", "price": "₹1,450 / Quintal"},
    {"commodity": "Brinjal", "market": "Satara", "price": "₹2,100 / Quintal"},
    {"commodity": "Brinjal", "market": "Pune", "price": "₹2,200 / Quintal"},
    {"commodity": "Cabbage", "market": "Baramati", "price": "₹1,100 / Quintal"},
    {"commodity": "Cauliflower", "market": "Sangamner", "price": "₹1,750 / Quintal"},
    {"commodity": "Lady's Finger", "market": "Rahuri", "price": "₹3,200 / Quintal"},
    {"commodity": "Bitter Gourd", "market": "Jalgaon", "price": "₹2,800 / Quintal"},
    {"commodity": "Bottle Gourd", "market": "Dhule", "price": "₹1,300 / Quintal"},
    {"commodity": "Cucumber", "market": "Aurangabad", "price": "₹1,600 / Quintal"},
    {"commodity": "Green Chilli", "market": "Nanded", "price": "₹4,500 / Quintal"},
    {"commodity": "Garlic", "market": "Osmanabad", "price": "₹12,000 / Quintal"},
    {"commodity": "Ginger(Green)", "market": "Akola", "price": "₹6,800 / Quintal"},
    {"commodity": "Lemon", "market": "Latur", "price": "₹4,200 / Quintal"},
]

def _filter_fallback_prices(market=None, commodity=None):
    results = FALLBACK_PRICES
    if market:
        results = [item for item in results if item['market'].lower() == market.lower()]
    if commodity:
        results = [item for item in results if item['commodity'].lower() == commodity.lower()]
    return results

def get_market_prices(market=None, commodity=None, date_str=None):
    """
    Fetches agricultural market price data from data.gov.in API with strict timeout,
    falling back to curated market data if API is slow, unreachable, or empty.
    """
    api_key = os.getenv("DATA_GOV_API_KEY")
    if not api_key:
        print("[INFO] DATA_GOV_API_KEY not found; using fallback market prices.")
        return _filter_fallback_prices(market, commodity)

    base_url = f"https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070?api-key={api_key}&format=json"

    filters = "&filters[state]=Maharashtra"
    if market:
        filters += f"&filters[market]={market}"
    if commodity:
        filters += f"&filters[commodity]={commodity}"

    limit = "&limit=50"
    API_URL = base_url + filters + limit

    try:
        # Strict timeout prevents web worker from locking up if government API hangs
        response = requests.get(API_URL, timeout=5)
        if response.status_code == 200:
            data = response.json()
            records = data.get('records', [])
            if records:
                formatted_data = []
                for record in records:
                    formatted_data.append({
                        'commodity': record.get('commodity', '').strip(),
                        'market': record.get('market', '').strip(),
                        'price': f"₹{record.get('modal_price', 'N/A')} / Quintal"
                    })
                return formatted_data

        print("[INFO] Live API returned no records or non-200. Using fallback market data.")
        return _filter_fallback_prices(market, commodity)

    except Exception as e:
        print(f"[WARNING] Market price fetch error (using fallback): {e}")
        return _filter_fallback_prices(market, commodity)