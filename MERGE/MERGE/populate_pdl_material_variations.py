import sqlite3
import os
import importlib.util
import sys

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

        # Get all product listings
        cursor.execute("SELECT product_design_listing_id, sku FROM product_design_listings")
        records = cursor.fetchall()

        pdl_material_variation_id = 1  # Start ID counter
        inserted_count = 0  # Track inserted records

        for pdl_id, sku in records:
            material_variations = PRODUCT_LISTING.get(sku, {}).get("variations", {})

            if not material_variations:
                print(f"⚠️ No material variations found for SKU: {sku}")
                continue  # Skip if no variations exist

            for variation_no, (variation_key, variation_data) in enumerate(material_variations.items(), start=1):
                material_codes = variation_data.get("material variation", [])
                
                if not material_codes:
                    print(f"⚠️ No material codes for variation '{variation_key}' in SKU: {sku}")
                    continue
                
                for material_code in material_codes:
                    print(f"🔄 Inserting: pdl_id={pdl_id}, variation_no={variation_no}, material_code={material_code}")
                    
                    cursor.execute("""
                        INSERT OR IGNORE INTO pdl_material_variations (
                            pdl_material_variation_id, pdl_id, pdl_material_variation_no, material_code
                        ) VALUES (?, ?, ?, ?)
                    """, (pdl_material_variation_id, pdl_id, variation_no, material_code))

                    pdl_material_variation_id += 1
                    inserted_count += 1

        conn.commit()
        conn.close()

    except Exception as e:
        print(f"❌ Error populating pdl_material_variations: {e}")

if __name__ == "__main__":
    populate_pdl_material_variations()
