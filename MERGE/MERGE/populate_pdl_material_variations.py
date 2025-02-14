import sqlite3
import os
import sys
import importlib.util

DB_PATH = os.path.join(os.path.dirname(__file__), "../TEST/DATABASE/EtchCut_DB_DEV")
PRODUCT_LISTING_PATH = os.path.join(os.path.dirname(__file__), "product_design_listing.py")

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
