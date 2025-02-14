import sqlite3
import os
import json
import re

from system_settings import *

sys_settings: SystemSettings = SystemSettings()

DB_PATH = os.path.join(os.path.dirname(__file__), "../TEST/DATABASE/EtchCut_DB_DEV")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "../TEST/MERGE/OUTPUT/", sys_settings.process_date)
PRODUCT_LISTING_PATH = os.path.join(os.path.dirname(__file__), "product_design_listing.py")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load product data
def load_product_data():
    with open(PRODUCT_LISTING_PATH, "r", encoding="utf-8") as file:
        content = file.read()

    # **Step 1: Remove all comments (`# ...`)**
    content_no_comments = re.sub(r'#.*', '', content)

    # **Step 2: Find `__dictionary__ = {...}` and extract JSON**
    start_index = content_no_comments.find("__dictionary__ =")  
    if start_index == -1:
        raise ValueError("❌ `__dictionary__` not found in product_design_listing.py")

    # Get everything after "__dictionary__ ="
    json_data = content_no_comments[start_index + len("__dictionary__ ="):].strip()

    # **Step 3: Extract ONLY the JSON dictionary (stop at the first unmatched `}`)**
    bracket_count = 0
    json_dict = ""
    for char in json_data:
        json_dict += char
        if char == "{":
            bracket_count += 1
        elif char == "}":
            bracket_count -= 1
            if bracket_count == 0:
                break  # Stop once the dictionary closes properly

    # **Step 4: Save to debug.json for validation**
    with open("debug.json", "w", encoding="utf-8") as f:
        f.write(json_dict)
    print("📂 JSON saved to debug.json for inspection.")

    # **Step 5: Debugging printout**
    print("Raw JSON Data (first 500 characters):", json_dict[:500])

    # **Step 6: Parse JSON safely**
    try:
        return json.loads(json_dict)
    except json.JSONDecodeError as e:
        print("❌ JSON Decode Error:", e)
        print("Error at character:", e.pos)
        print("Problematic JSON snippet:", json_dict[max(0, e.pos - 50): e.pos + 50])  # Show context around error
        raise  # Re-raise error


PRODUCT_LISTING = load_product_data()

HEADERS = ["PLATE_REFERENCE", "SALES_CHANNEL_ID", "DESIGN_ID", "PERSONALISATION", "@OUTLINE_FRM"]

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute("SELECT * FROM merge_items;")
merge_items_records = cursor.fetchall()
columns = [desc[0] for desc in cursor.description]
conn.close()

for record in merge_items_records:
    order_no = str(record[columns.index("order_no")])
    sku = str(record[columns.index("sku")])
    product_details = PRODUCT_LISTING.get("EtsyTM", {}).get(sku, {})
    product_title = product_details.get("title", "")
    txt_filename = f"{order_no}_{sku}.txt"
    txt_filepath = os.path.join(OUTPUT_DIR, txt_filename)
    txt_content = [str(record[columns.index(col)]) if col in columns else "" for col in HEADERS]
    txt_content.append(product_title)
    with open(txt_filepath, "w", encoding="utf-8") as txt_file:
        txt_file.write(";".join(HEADERS) + "\n")
        txt_file.write(";".join(txt_content) + "\n")

print(f"✅ {len(merge_items_records)} .txt files generated in {OUTPUT_DIR}")