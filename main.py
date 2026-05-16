import os
import httpx
import pandas as pd


def fetch_live_us_listings(city_name: str):
    """
    Fetches actual, real-world active listings from the live RentCast API.
    """
    # Default to Dallas, TX if the user leaves the input blank
    target_city = city_name.strip() if city_name else "Dallas"
    print(f"Connecting to live US MLS stream for: {target_city}...")

    # Official RentCast active listings endpoint
    url = "https://rentcast.io"

    query_params = {
        "city": target_city,
        "state": "TX",  # Hardcoded to Texas for hyper-stable data tracking
        "status": "Active",
        "limit": 50  # Pulls the 50 newest live listings on the market
    }

    headers = {
        "Accept": "application/json",
        # Pulls your secure token from your GitHub repository vault
        "X-Api-Key": os.getenv("REAL_ESTATE_API_KEY")
    }

    try:
        response = httpx.get(url, headers=headers, params=query_params, timeout=20)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"API Warning: Status {response.status_code}. Details: {response.text}")
            return []
    except Exception as e:
        print(f"Network error connecting to US property database: {e}")
        return []


def calculate_undervalued_deals(raw_properties):
    """
    Applies an algorithmic data formula to identify premium, undervalued deals.
    """
    if not raw_properties:
        print("No live listings fetched or API key is unconfigured.")
        return pd.DataFrame()

    analyzed_deals = []

    for house in raw_properties:
        price = house.get("price", 0)
        sqft = house.get("squareFootage", 0)
        beds = house.get("bedrooms", 0)
        baths = house.get("bathrooms", 0)
        property_type = house.get("propertyType", "Single Family")

        if not price or not sqft:
            continue

        # 📊 LIVE MARKET DATA MATH
        price_per_sqft = round(price / sqft, 2)

        # INVESTOR LOGIC CONFIGURATION:
        # Let's say the average price per sqft for standard houses in this target market is $180.
        # If a house hits the market under $150 per sqft, it's heavily undervalued!
        MARKET_AVERAGE_SQFT_PRICE = 180

        is_undervalued = price_per_sqft < (MARKET_AVERAGE_SQFT_PRICE * 0.85)  # 15% below market average

        if is_undervalued:
            deal_label = "🔥 PREMIUM UNDERVALUED DEAL"
        else:
            deal_label = "Standard Market Value"

        analyzed_deals.append({
            "Address": house.get("formattedAddress", "Unknown"),
            "City": house.get("city", "Dallas"),
            "Zip Code": house.get("zipcode", ""),
            "Listing Price": f"${price:,}",
            "Beds/Baths": f"{beds} bds / {baths} ba",
            "Size (Sq Ft)": f"{sqft:,} sqft",
            "Price / SqFt": f"${price_per_sqft}",
            "Property Type": property_type,
            "Investment Analysis": deal_label
        })

    return pd.DataFrame(analyzed_deals)


if __name__ == "__main__":
    # Intercept the exact city parameter typed into your FastAPI browser dashboard
    input_location = os.getenv("FILTER_TEXT", "Dallas")

    # 1. Gather live US real estate records
    raw_listings = fetch_live_us_listings(input_location)

    # 2. Extract and tag the undervalued bargains using Pandas data analytics
    processed_df = calculate_undervalued_deals(raw_listings)

    # 3. Overwrite the tracked tracking spreadsheet in your repo root
    output_excel = "Premium_Undervalued_Deals.xlsx"

    if not processed_df.empty:
        processed_df.to_excel(output_excel, index=False)
        print(f"SUCCESS: Calculated market data! Saved {len(processed_df)} live houses to {output_excel}")
    else:
        # Fallback empty structure to safeguard your automated Git push execution step
        fallback_df = pd.DataFrame(
            [{"System Message": "Data sync empty. Ensure your REAL_ESTATE_API_KEY is active in GitHub Secrets."}])
        fallback_df.to_excel(output_excel, index=False)
        print("WARNING: Live stream data returned empty. Running fallback structure.")
