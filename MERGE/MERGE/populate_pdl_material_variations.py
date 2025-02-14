import sqlite3
import os
from product_design_listing import ProductDesignListing

# Database path
DB_PATH = os.path.join(os.path.dirname(__file__), "../TEST/DATABASE/EtchCut_DB_DEV")

def load_product_data():
    """Load the product dictionary from ProductDesignListing class."""
    try:
        return ProductDesignListing.__dictionary__.get("EtsyTM", {})
    except Exception as e:
        print(f"❌ Error loading product data: {e}")
        return {}

PRODUCT_LISTING = load_product_data()

def extract_material_variations(sku, variation):
    """Extract material variations based on SKU and variation from product dictionary."""
    product_data = PRODUCT_LISTING.get(sku, {})
    
    if not product_data:
        return []
    
    material_variations = set()

    # Iterate through __dictionary__ variations
    for variation_key, details in product_data.get("variations", {}).items():
        if variation_key in variation:
            materials = details.get("material variation", [])
            material_variations.update(materials)
    
    return list(material_variations)

def populate_pdl_material_variations():
    """Populate the pdl_material_variations table."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Fetch all product design listings
        cursor.execute("SELECT product_design_listing_id, sku, variation FROM product_design_listings")
        records = cursor.fetchall()

        pdl_material_variation_id = 1  # ID counter

        inserted_count = 0  # Track successful inserts

        for pdl_id, sku, variation in records:
            material_variations = extract_material_variations(sku, variation)

            print(f"🛠 Processing SKU: {sku} | Variation: {variation} | Material Variations: {material_variations}")

            for variation_no, material_code in enumerate(material_variations, start=1):
                cursor.execute("""
                    INSERT OR IGNORE INTO pdl_material_variations (
                        pdl_material_variation_id, pdl_id, pdl_material_variation_no, material_code
                    ) VALUES (?, ?, ?, ?)
                """, (pdl_material_variation_id, pdl_id, variation_no, material_code))

                pdl_material_variation_id += 1
                inserted_count += 1

        conn.commit()
        conn.close()

        print(f"✅ Successfully inserted {inserted_count} records into pdl_material_variations.")

    except Exception as e:
        print(f"❌ Error populating pdl_material_variations: {e}")

if __name__ == "__main__":
    populate_pdl_material_variations()
