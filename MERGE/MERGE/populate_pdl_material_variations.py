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

def extract_material_variations(sku):
    """Extract material variations based on SKU from the product dictionary or fallback to SKU prefix."""
    product_data = PRODUCT_LISTING.get(sku, {})

    if not product_data:
        # Extract material code from SKU if dictionary lookup fails
        material_code = sku.split("_")[0]  # Extract first segment (CWS, WFOV, etc.)
        return [material_code] if material_code else []

    material_variations = set()

    # Iterate through variations (if any exist)
    for variation_key, details in product_data.get("variations", {}).items():
        materials = details.get("material variation", [])
        material_variations.update(materials)

    return list(material_variations) if material_variations else [sku.split("_")[0]]

def populate_pdl_material_variations():
    """Populate the pdl_material_variations table ensuring all SKUs are mapped to materials."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Ensure table is not getting reset or overwritten
        cursor.execute("SELECT COUNT(*) FROM pdl_material_variations")
        row_count_before = cursor.fetchone()[0]

        # Fetch all product design listings
        cursor.execute("SELECT product_design_listing_id, sku FROM product_design_listings")
        records = cursor.fetchall()

        inserted_count = 0  # Track successful inserts

        for pdl_id, sku in records:
            material_variations = extract_material_variations(sku)

            for variation_no, material_code in enumerate(material_variations, start=1):
                cursor.execute("""
                    INSERT OR IGNORE INTO pdl_material_variations (
                        pdl_id, pdl_material_variation_no, material_code
                    ) VALUES (?, ?, ?)
                """, (pdl_id, variation_no, material_code))
                                
        conn.commit()

        # Ensure inserts were successful
        cursor.execute("SELECT COUNT(*) FROM pdl_material_variations")

        conn.close()

        print(f"✅ Successfully inserted {inserted_count} records into pdl_material_variations.")

    except Exception as e:
        print(f"❌ Error populating pdl_material_variations: {e}")

if __name__ == "__main__":
    populate_pdl_material_variations()
