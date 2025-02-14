import sqlite3
import os
import json
import re

DB_PATH = os.path.join(os.path.dirname(__file__), "../TEST/DATABASE/EtchCut_DB_DEV")
PRODUCT_LISTING_PATH = os.path.join(os.path.dirname(__file__), "product_design_listing.py")

def load_product_data():
    """Extract only the dictionary from product_design_listing.py"""
    with open(PRODUCT_LISTING_PATH, "r", encoding="utf-8") as file:
        content = file.read()

    # Use regex to extract JSON data cleanly
    match = re.search(r"__dictionary__ = ({.*})", content, re.DOTALL)
    if match:
        json_data = match.group(1)
        return json.loads(json_data)
    else:
        raise ValueError("Could not find __dictionary__ in product_design_listing.py")

PRODUCT_LISTING = load_product_data().get("EtsyTM", {})

def populate_pdl_material_variations():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Get the highest existing pdl_material_variation_id to avoid duplicates
        cursor.execute("SELECT COALESCE(MAX(pdl_material_variation_id), 0) FROM pdl_material_variations")
        pdl_material_variation_id = cursor.fetchone()[0] + 1  # Start from next available ID

        # Get all product listings
        cursor.execute("SELECT product_design_listing_id, sku FROM product_design_listings")
        records = cursor.fetchall()

        new_records_count = 0

        for pdl_id, sku in records:
            material_variations = PRODUCT_LISTING.get(sku, {}).get("material_variations", {})

            if not isinstance(material_variations, dict):
                continue  # Skip if it's not a dictionary

            for variation_no, (variation_key, material_code) in enumerate(material_variations.items(), start=1):
                cursor.execute("""
                    INSERT OR IGNORE INTO pdl_material_variations (
                        pdl_material_variation_id, pdl_id, pdl_material_variation_no, material_code
                    ) VALUES (?, ?, ?, ?)
                """, (pdl_material_variation_id, pdl_id, variation_no, material_code))

                pdl_material_variation_id += 1  # Increment ID
                new_records_count += 1

        conn.commit()
        conn.close()
        print(f"✅ Populated {new_records_count} records into pdl_material_variations.")

    except Exception as e:
        print(f"❌ Error populating pdl_material_variations: {e}")

if __name__ == "__main__":
    populate_pdl_material_variations()
