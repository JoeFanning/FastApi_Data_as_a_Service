import pandas as pd
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter  # Move the import to the top section

print("--- Starting Premium DaaS Data Pipeline ---")

# 1. Simulate receiving raw, messy internet data
messy_data = {
    "Address": ["123 Main St", "456 Oak Ave", "789 Pine Rd", "101 Maple Dr"],
    "Raw_Price": ["$350,000", "$180,000 USD", "$420,000!!", "$250,000"],
    "Neighborhood_Avg": [400000, 150000, 400000, 300000],
    "Status": ["active", "FORECLOSURE", "active", "active"]
}

df = pd.DataFrame(messy_data)

# 2. Clean data: Strip out symbols ($ , ! USD) and convert prices to numbers
df['Clean_Price'] = df['Raw_Price'].str.replace(r'[\$,! ]|USD', '', regex=True).astype(float)

# 3. Analyze data: Calculate the exact discount percentage for the investor
df['Discount_Percentage'] = ((df['Neighborhood_Avg'] - df['Clean_Price']) / df['Neighborhood_Avg'] * 100).round(1)

# 4. Filter data: Isolate only actual deals (where price is below neighborhood average)
deals_df = df[df['Discount_Percentage'] > 0].copy()

# 5. Format structure: Select and rename columns to look highly professional
final_report = deals_df[["Address", "Raw_Price", "Neighborhood_Avg", "Discount_Percentage", "Status"]]
final_report.columns = ["Property Address", "Current List Price", "Neighborhood Average", "Est. Discount %",
                        "Market Status"]

# 6. Generate a styled Excel Spreadsheet
file_name = "Premium_Undervalued_Deals.xlsx"

with pd.ExcelWriter(file_name, engine='openpyxl') as writer:
    final_report.to_excel(writer, sheet_name="Deals of the Day", index=False)

    workbook = writer.book
    worksheet = writer.sheets["Deals of the Day"]

    # Premium visual design styles
    header_font = Font(name="Arial", size=11, bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")  # Dark Blue
    deal_fill = PatternFill(start_color="E2EFDA", end_color="E2EFDA", fill_type="solid")  # Soft Green
    center_align = Alignment(horizontal="center")

    # Apply headers formatting (Clean and un-nested)
    for col_num, column_title in enumerate(final_report.columns, 1):
        cell = worksheet.cell(row=1, column=col_num)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center_align

    # Highlight data rows in soft green
    for row in worksheet.iter_rows(min_row=2, max_row=len(final_report) + 1, min_col=1, max_col=5):
        for cell in row:
            cell.fill = deal_fill
            if cell.column in [4, 5]:
                cell.alignment = center_align

    # 🌟 FIXED: Moved outside the header loop so it runs exactly ONCE per column track
    for col in worksheet.columns:
        max_len = max(len(str(cell.value or '')) for cell in col)

        # 🌟 FIXED: Safely grab the column index integer out of the first cell item in the column tuple
        col_letter = get_column_letter(col[0].column)

        worksheet.column_dimensions[col_letter].width = max(max_len + 4, 15)

print(f"Successfully generated spreadsheet: {file_name}")
print("--- Data Pipeline Finished ---")
