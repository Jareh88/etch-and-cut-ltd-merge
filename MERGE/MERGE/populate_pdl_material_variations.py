from product_design_listing import ProductDesignListing
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "../TEST/DATABASE/EtchCut_DB_DEV")

def populate_pdl_material_variations():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Fetch product listings
        cursor.execute("SELECT product_design_listing_id, sales_channel_id, sku FROM product_design_listings")
        records = cursor.fetchall()

        if not records:
            print("⚠ No records found in product_design_listings.")
            return

        print(f"🔍 Found {len(records)} product design listings.")

        pdl_material_variation_id = 1  # Start ID counter
        inserted_count = 0  # Track how many insertions occur

        for pdl_id, sales_channel_id, sku in records:
            # Initialize class object
            product_obj = ProductDesignListing(sales_channel_id, sku, None)

            # Extract material variations
            material_variations = product_obj.material_variation if product_obj.material_variation else []

            print(f"🛠 Processing SKU: {sku} | Material Variations: {material_variations}")

            for variation_no, material_code in enumerate(material_variations, start=1):
                cursor.execute("""
                    INSERT OR IGNORE INTO pdl_material_variations (
                        pdl_material_variation_id, pdl_id, pdl_material_variation_no, material_code
                    ) VALUES (?, ?, ?, ?)
                """, (pdl_material_variation_id, pdl_id, variation_no, material_code))
                
                pdl_material_variation_id += 1
                inserted_count += 1  # Count successful inserts

        conn.commit()
        conn.close()
        
        print(f"✅ Successfully inserted {inserted_count} records into pdl_material_variations.")

    except Exception as e:
        print(f"❌ Error populating pdl_material_variations: {e}")

if __name__ == "__main__":
    populate_pdl_material_variations()
