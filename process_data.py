import os
import httpx
import pandas as pd
from openpyxl.styles import Font, PatternFill
from openpyxl.utils import get_column_letter
from dotenv import load_dotenv

load_dotenv()

print("--- Starting Premium DaaS Data Pipeline (Header Inspection Mode) ---")


def fetch_raw_api_sample(city_name: str):
    """
    Fetches raw property objects directly from the live RentCast API.
    """
    target_city = city_name.strip() if city_name else "Dallas"
    print(f"Connecting to live database stream to inspect data headers for: {target_city}...")

    url = "https://api.rentcast.io/v1/listings/rental/long-term"

    query_params = {
        "city": target_city,
        "state": "TX",
        "status": "Active",
        "limit": 5
    }

    api_key = os.getenv("RENTCAST_REAL_ESTATE_API_KEY")
    if not api_key:
        print("CRITICAL ERROR: RENTCAST_REAL_ESTATE_API_KEY environment variable is missing!")
        return []

    headers = {
        "Accept": "application/json",
        "X-Api-Key": api_key
    }

    try:
        response = httpx.get(url, headers=headers, params=query_params, timeout=20)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"API Warning: Status {response.status_code}. Details: {response.text}")
            return []
    except Exception as e:
        print(f"Network error: {e}")
        return []


def extract_raw_headers(raw_properties):
    """
    Inspected data catcher: Unwraps the RentCast API structures safely.
    """
    # RentCast endpoint returns a direct list [] of properties.
    # Handle dictionary fallback wrappers if using different endpoints.
    if isinstance(raw_properties, dict):
        print(f"API returned a Dictionary structure. Available top-level keys: {list(raw_properties.keys())}")
        actual_list = raw_properties.get("listings") or raw_properties.get("data") or []
        raw_properties = actual_list if isinstance(actual_list, list) else [raw_properties]

    if not raw_properties or not isinstance(raw_properties, list) or len(raw_properties) == 0:
        print("Data stream empty or malformed. Ensure your key is active in GitHub Secrets.")
        return pd.DataFrame(
            [{"Available API Column Keys": "ERROR", "Sample Raw Data Example": "No data returned from API."}])

    # Grab the first raw property record
    first_house_sample = raw_properties[0]
    api_header_names = list(first_house_sample.keys())
    print(f"SUCCESS: Successfully isolated {len(api_header_names)} unique database headers!")

    header_tracking_rows = []
    for header in api_header_names:
        sample_value = str(first_house_sample.get(header, "Empty/Null"))
        header_tracking_rows.append({
            "Available API Column Keys": header,
            "Sample Raw Data Example": sample_value[:50]  # Truncate long strings safely
        })

    return pd.DataFrame(header_tracking_rows)


if __name__ == "__main__":
    input_location = os.getenv("FILTER_TEXT", "Dallas")

    # 1. Harvest data
    raw_sample = fetch_raw_api_sample(input_location)

    # 2. Extract schemas
    headers_df = extract_raw_headers(raw_sample)

    file_name = "Premium_Undervalued_Deals.xlsx"

    # 3. Export & style spreadsheet report
    with pd.ExcelWriter(file_name, engine='openpyxl') as writer:
        headers_df.to_excel(writer, sheet_name="API Keys Blueprint", index=False)

        workbook = writer.book
        worksheet = writer.sheets["API Keys Blueprint"]

        # Design system styles
        header_font = Font(name="Arial", size=11, bold=True, color="FFFFFF")
        header_fill = PatternFill(start_color="7030A0", end_color="7030A0", fill_type="solid")  # Purple
        data_fill = PatternFill(start_color="F2F4F7", end_color="F2F4F7", fill_type="solid")  # Light grey

        # Single-pass layout formatting loop
        for col_idx, col in enumerate(worksheet.columns, 1):
            max_len = 0
            col_letter = get_column_letter(col_idx)

            for row_idx, cell in enumerate(col, 1):
                # Calculate text padding dynamically
                max_len = max(max_len, len(str(cell.value or '')))

                # Apply styles based on row placement
                if row_idx == 1:
                    cell.font = header_font
                    cell.fill = header_fill
                else:
                    cell.fill = data_fill

            # Apply widths dynamically
            worksheet.column_dimensions[col_letter].width = max(max_len + 5, 25)

    print(f"Spreadsheet generated securely: {file_name}")
    print("--- Data Pipeline Finished ---")
