import sqlite3
import os
import json
from system_settings import *

sys_settings = SystemSettings()  # Load system settings

DB_PATH = os.path.join(os.path.dirname(__file__), "../TEST/DATABASE/EtchCut_DB_DEV")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "../TEST/MERGE/OUTPUT/", sys_settings.process_date)

os.makedirs(OUTPUT_DIR, exist_ok=True)

def fetch_records():
    """Retrieve data from multiple tables to generate text file contents."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            m.order_no, m.sku, pdl.title, m.input_personalisation, m.merge_personalisation,
            pdl.variation, pdlm.material_code, m.private_notes, m.buyer_note
        FROM merge_items m
        LEFT JOIN product_design_listings pdl ON m.sku = pdl.sku
        LEFT JOIN pdl_material_variations pdlm ON pdl.product_design_listing_id = pdlm.pdl_id
    """)
    records = cursor.fetchall()
    conn.close()
    return records

def generate_headers():
    """Dynamically generate column headers based on available data."""
    static_headers = [
        "PLATE_REFERENCE", "PLATE_SEQ", "SALES_CHANNEL_ID", "VALID_ORDER_ID", "INVALID_ORDER_ID",
        "DESIGN_ID", "PRIVATE_NOTES", "BUYER_NOTE", "VARIATION", "PERSONALISATION"
    ]
    dynamic_headers = ["@FOREGROUND_01", "@BACKGROUND_01"]

    # Fetch unique product design identifiers (e.g., WS101_T01P01S01F01)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT material_code FROM pdl_material_variations")
    material_codes = [row[0] for row in cursor.fetchall()]
    conn.close()

    # Append dynamic material-based headers
    product_headers = [f"{code}_T01" for code in material_codes]
    
    return static_headers + dynamic_headers + product_headers

def generate_text_files():
    """Create text files with extracted data."""
    records = fetch_records()
    headers = generate_headers()

    file_data = {}  # Dictionary to store data for each unique txt file

    for record in records:
        order_no, sku, title, input_pers, merge_pers, variation, material_code, private_notes, buyer_note = record

        # Construct filename
        txt_filename = f"{order_no}_{sku}.txt"
        txt_filepath = os.path.join(OUTPUT_DIR, txt_filename)

        # Construct content row
        content_row = [
            f"{order_no}_{sku}", "001", "EtsyTM", order_no, "", sku, private_notes or "", buyer_note or "",
            variation or "", f"{input_pers or ''} {merge_pers or ''}"
        ]

        # Append @FOREGROUND_XX and @BACKGROUND_XX placeholders (mocked for now)
        content_row += [f"S:\\MERGE\\IMAGES\\{sku}\\{sku}_FG.pdf", f"S:\\MERGE\\IMAGES\\{sku}\\{sku}_BG.pdf"]

        # Add dynamic material-based fields
        product_variations = [material_code if material_code else ""]
        content_row += product_variations

        # Store data in dictionary, ensuring each file gets multiple rows if necessary
        if txt_filepath not in file_data:
            file_data[txt_filepath] = [headers]  # Add headers once per file
        file_data[txt_filepath].append(content_row)

    # Write to files, ensuring multiple rows per file are saved correctly
    for txt_filepath, rows in file_data.items():
        with open(txt_filepath, "w", encoding="utf-8") as txt_file:
            for row in rows:
                txt_file.write(";".join(row) + "\n")

    print(f"✅ {len(file_data)} .txt files generated in {OUTPUT_DIR}")

if __name__ == "__main__":
    generate_text_files()
