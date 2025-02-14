import sqlite3
import os
import sys
import importlib.util

from system_settings import *

sys_settings: SystemSettings = SystemSettings()

DB_PATH = os.path.join(os.path.dirname(__file__), "../TEST/DATABASE/EtchCut_DB_DEV")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "../TEST/MERGE/OUTPUT/", sys_settings.process_date)
PRODUCT_LISTING_PATH = os.path.join(os.path.dirname(__file__), "product_design_listing.py")

os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_product_data():
    """Dynamically load ProductDesignListing and extract __dictionary__"""
    
    spec = importlib.util.spec_from_file_location("product_design_listing", PRODUCT_LISTING_PATH)
    module = importlib.util.module_from_spec(spec)
    
    sys.modules["product_design_listing"] = module
    spec.loader.exec_module(module)

    if hasattr(module, "ProductDesignListing") and hasattr(module.ProductDesignListing, "__dictionary__"):
        print("✅ Successfully loaded __dictionary__ from ProductDesignListing class")
        return module.ProductDesignListing.__dictionary__.get("EtsyTM", {})  # Get only the EtsyTM part
    else:
        raise ValueError("❌ Error: __dictionary__ not found in ProductDesignListing")

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