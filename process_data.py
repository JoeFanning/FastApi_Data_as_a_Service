import pandas as pd
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter  # 🌟 FIXED: Added this utility to fix the cloud bug

print("--- Starting Premium DaaS Data Pipeline ---")

# 1. Mock dataset simulating messy real estate information pulled from the web
messy_data = {
    "Address": ["123 Main St", "456 Oak Ave", "789 Pine Rd", "101 Maple Dr"],
    "Raw_Price": ["$350,000", "$180,000 USD", "$420,000!!", "$250,000"],
    "Neighborhood_Avg": [380000.0, 150000.0, 450000.0, 260000.0],
    "Status": ["active", "FORECLOSURE", "active", "active"]
}

df = pd.DataFrame(messy_data)

# 2. Clean data strings into pure numbers
df['Clean_Price'] = df['Raw_Price'].str.replace(r'[\$,! ]|USD', '', regex=True).astype(float)

# 3. Analytics: Find the mathematical discount percentage
df['Discount_Percentage'] = ((df['Neighborhood_Avg'] - df['Clean_Price']) / df['Neighborhood_Avg'] * 100).round(1)

# 4. Filter out properties that are overpriced (keep only deals)
deals_df = df[df['Discount_Percentage'] > 0].copy()

# 5. Format and rename columns to look polished for business clients
final_report = deals_df[["Address", "Raw_Price", "Neighborhood_Avg", "Discount_Percentage", "Status"]]
final_report.columns = ["Property Address", "Current List Price", "Neighborhood Average", "Est. Discount %", "Market Status"]

file_name = "Premium_Undervalued_Deals.xlsx"

# 6. Build and design the Excel file
with pd.ExcelWriter(file_name, engine='openpyxl') as writer:
    final_report.to_excel(writer, sheet_name="Deals of the Day", index=False)
    
    workbook = writer.book
    worksheet = writer.sheets["Deals of the Day"]
    
    # Visual Styling
    header_font = Font(name="Arial", size=11, bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid") # Corporate Blue
    deal_fill = PatternFill(start_color="E2EFDA", end_color="E2EFDA", fill_type="solid")   # Clean Light Green
    center_align = Alignment(horizontal="center")

    for col_num, column_title in enumerate(final_report.columns, 1):
        cell = worksheet.cell(row=1, column=col_num)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center_align

    for row in worksheet.iter_rows(min_row=2, max_row=len(final_report) + 1, min_col=1, max_col=5):
        for cell in row:
            cell.fill = deal_fill
            if cell.column in [4, 5]:
                cell.alignment = center_align

    # 🌟 FIXED LOOP: Explicitly track index numbers and convert them to letters safely
    for col_idx, col in enumerate(worksheet.columns, 1):
        max_len = max(len(str(cell.value or '')) for cell in col)
        col_letter = get_column_letter(col_idx)  # Safely creates 'A', 'B', 'C', etc.
        worksheet.column_dimensions[col_letter].width = max(max_len + 4, 15)

print(f"Generated Excel report: {file_name}")
print("--- Data Pipeline Finished ---")

print(f"Successfully generated spreadsheet: {file_name}")
print("--- Data Pipeline Finished ---")
