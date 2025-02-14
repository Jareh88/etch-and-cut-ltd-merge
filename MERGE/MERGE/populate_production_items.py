import sqlite3
import os

# Path to database
DB_PATH = os.path.join(os.path.dirname(__file__), "../TEST/DATABASE/EtchCut_DB_DEV")

def populate_production_items():
    query = """
    INSERT INTO production_items (
        sales_channel_id, order_no, order_item_no, sku,
        product_material_code, product_type_code, product_design_code,
        product_desc, product_design_listing_no, production_item_no, order_size,
        dispatch_priority, production_priority, merge_priority,
        variation_01_name, variation_01_value, variation_02_name, variation_02_value,
        variation_03_name, variation_03_value, variation_04_name, variation_04_value,
        variation_05_name, variation_05_value, input_personalisation, merge_personalisation,
        output_personalisation, private_notes, buyer_note, length_mm, width_mm,
        depth_mm, weight_grms, process_category, process_status
    )
    SELECT 
        o.sales_channel_id, o.order_no, o.order_item_no, o.sku, 
        o.product_material_code, o.product_type_code, o.product_design_code, 
        o.product_listing_title, o.product_listing_no, 
        (SELECT COALESCE(MAX(production_item_no), 0) + 1 FROM production_items WHERE order_no = o.order_no) AS production_item_no, 
        o.quantity, o.dispatch_priority, o.dispatch_priority, 1, 
        o.variation_01_name, o.variation_01_value, o.variation_02_name, o.variation_02_value, 
        o.variation_03_name, o.variation_03_value, o.variation_04_name, o.variation_04_value, 
        o.variation_05_name, o.variation_05_value, o.input_personalisation, o.merge_personalisation, 
        NULL, NULL, NULL, 0, 0, 0, 0, o.process_category, o.process_status
    FROM order_items o
    LEFT JOIN production_items p ON o.order_no = p.order_no AND o.order_item_no = p.order_item_no
    WHERE p.order_no IS NULL;
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        conn.close()
        print("✅ Successfully populated production_items.")
    except Exception as e:
        print(f"❌ Error populating production_items: {e}")

if __name__ == "__main__":
    populate_production_items()
