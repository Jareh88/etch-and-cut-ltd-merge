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
            pdl.variation, pdlm.material_code, m.private_notes, m.buyer_note,
            m.sales_channel_id, m.product_design_code, m.product_material_code, m.product_type_code
        FROM merge_items m
        LEFT JOIN product_design_listings pdl ON m.sku = pdl.sku
        LEFT JOIN pdl_material_variations pdlm ON pdl.product_design_listing_id = pdlm.pdl_id
    """)
    records = cursor.fetchall()
    conn.close()
    return records

def generate_headers():
    """Dynamically generate column headers based on material and product type data."""
    static_headers = [
        "PLATE_REFERENCE", "PLATE_SEQ", "SALES_CHANNEL_ID", "VALID_ORDER_ID", "INVALID_ORDER_ID",
        "DESIGN_ID", "PRIVATE_NOTES", "BUYER_NOTE", "VARIATION", "PERSONALISATION"
    ]
    dynamic_headers = ["@FOREGROUND_01", "@BACKGROUND_01"]

    # Fetch correct product type codes mapped to materials
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DISTINCT mpt.material_code, mpt.product_type_code
        FROM material_product_types mpt
    """)
    material_product_combos = cursor.fetchall()
    conn.close()

    # Append dynamic material-based headers (e.g., "WS107_T03P01S01F01")
    product_headers = [f"{mat}_{ptype}_T01P01S01F01" for mat, ptype in material_product_combos]
    
    return static_headers + dynamic_headers + product_headers

def generate_text_files():
    """Create text files with extracted data."""
    records = fetch_records()
    headers = generate_headers()

    file_data = {}  # Dictionary to store data for each unique txt file

    for record in records:
        (
            order_no, sku, title, input_pers, merge_pers, variation, material_code, 
            private_notes, buyer_note, sales_channel_id, product_design_code, 
            product_material_code, product_type_code
        ) = record

        # Construct filename
        txt_filename = f"{order_no}_{sku}.txt"
        txt_filepath = os.path.join(OUTPUT_DIR, txt_filename)

        # Construct plate reference ID
        plate_reference = f"{order_no}_{sku}"

        # Construct content row
        content_row = [
            plate_reference, "001", sales_channel_id, order_no, "", product_design_code, 
            private_notes or "", buyer_note or "", variation or "", 
            f"{input_pers or ''} {merge_pers or ''}"
        ]

        # Append @FOREGROUND_XX and @BACKGROUND_XX placeholders
        content_row += [f"S:\\MERGE\\IMAGES\\{sku}\\{sku}_FG.pdf", f"S:\\MERGE\\IMAGES\\{sku}\\{sku}_BG.pdf"]

        # Generate proper product variation identifiers (e.g., "WS107_T03P01S01F01")
        product_variation_id = f"{product_material_code}_{product_type_code}_T01P01S01F01"
        content_row.append(product_variation_id)

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
