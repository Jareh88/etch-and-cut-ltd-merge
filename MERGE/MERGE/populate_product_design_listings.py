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

def populate_product_design_listings():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Get the highest existing product_design_listing_id to prevent duplicates
        cursor.execute("SELECT COALESCE(MAX(product_design_listing_id), 0) FROM product_design_listings")
        product_design_listing_id = cursor.fetchone()[0] + 1  # Start from next available ID

        # Get unique SKUs from order_items and ensure variation is always a string
        cursor.execute("""
            SELECT DISTINCT sales_channel_id, sku, COALESCE(variation, '') AS variation, SUM(quantity) 
            FROM order_items 
            GROUP BY sales_channel_id, sku, variation
        """)
        records = cursor.fetchall()

        new_records_count = 0

        for sales_channel_id, sku, variation, quantity in records:
            product_data = PRODUCT_LISTING.get(sku, {})
            title = product_data.get("title", None)

            if not title:
                print(f"⚠️ Missing title for SKU: {sku} - Defaulting to 'UNKNOWN'")
                title = "UNKNOWN"

            cursor.execute("""
                INSERT OR IGNORE INTO product_design_listings (
                    product_design_listing_id, sales_channel_id, sku, title, variation, quantity
                ) VALUES (?, ?, ?, ?, ?, ?)
            """, (product_design_listing_id, sales_channel_id, sku, title, variation, quantity))

            product_design_listing_id += 1  # Increment ID
            new_records_count += 1

        conn.commit()
        conn.close()
        print(f"✅ Populated {new_records_count} records into product_design_listings.")

    except Exception as e:
        print(f"❌ Error populating product_design_listings: {e}")

if __name__ == "__main__":
    populate_product_design_listings()
