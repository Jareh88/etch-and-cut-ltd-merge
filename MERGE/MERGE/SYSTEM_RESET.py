import sqlite3
from sqlite3 import *

import os
import shutil
import re
import sys

import logging
from custom_logger import *

from datetime import datetime

from system_settings import *
from new_material_product_type  import *


def get_current_date() -> str:
#   ** ************************************************************************************************************************************************************
#   ** 
#   ** ************************************************************************************************************************************************************
    current_date_YYYYMMDD: datetime = datetime.datetime.now()
    current_year: str  = current_date_YYYYMMDD.strftime("%Y")
    current_month: str = current_date_YYYYMMDD.strftime("%m")
    current_day: str   = current_date_YYYYMMDD.strftime("%d")
    current_date:str   = rf'{current_year}{current_month}{current_day}'

    return (current_date)


def create_connection(db_file):
#   *************************************************************************************
#   Establish Database Connection
#   *************************************************************************************
    """ create a database connection to the SQLite database specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e_conn:
        print(e_conn)

    return conn


def delete_database ():
#   ** ************************************************************************************************************************************************************
#   ** 
#   ** ************************************************************************************************************************************************************

#   delete material_product_types table
    cursor = conn.cursor()
    sql_script = '''
        DROP TABLE IF EXISTS material_product_types
    '''
    cursor.execute(sql_script)
    cursor.close()       
    conn.commit()
    logger.info(rf'MATERIAL_PRODUCT_TYPES deleted') if cursor else logger.critical(rf'MATERIAL_PRODUCT_TYPES not deleted!')


#   delete product_design_listings table
    cursor = conn.cursor()
    sql_script = '''
        DROP TABLE IF EXISTS product_design_listings
    '''
    cursor.execute(sql_script)
    cursor.close()       
    conn.commit()
    logger.info(rf'PRODUCT_DESIGN_LISTINGS deleted') if cursor else logger.critical(rf'PRODUCT_DESIGN_LISTINGS not deleted!')


#   delete pdl_material_variations table
    cursor = conn.cursor()
    sql_script = '''
        DROP TABLE IF EXISTS pdl_material_variations
    '''
    cursor.execute(sql_script)
    cursor.close()       
    conn.commit()
    logger.info(rf'PDL_MATERIAL_VARIATIONS deleted') if cursor else logger.critical(rf'PDL_MATERIAL_VARIATIONS not deleted!')


#   delete orders table
    cursor = conn.cursor()
    sql_script = '''
        DROP TABLE IF EXISTS orders
    '''
    cursor.execute(sql_script)
    cursor.close()       
    conn.commit()
    logger.info(rf'ORDERS deleted') if cursor else logger.critical(rf'ORDERS not deleted!')


#   delete order_items table
    cursor = conn.cursor()
    sql_script = '''
        DROP TABLE IF EXISTS order_items
    '''
    cursor.execute(sql_script)
    cursor.close()
    conn.commit()
    logger.info(rf'ORDER_ITEMS deleted') if cursor else logger.critical(rf'ORDER_ITEMS not deleted!')

#   delete production_items table
    cursor = conn.cursor()
    sql_script = '''
        DROP TABLE IF EXISTS production_items
    '''
    cursor.execute(sql_script)
    cursor.close()       
    conn.commit()
    logger.info(rf'PRODUCTION_ITEMS deleted') if cursor else logger.critical(rf'PRODUCTION_ITEMS not deleted!')


#   delete merge_items table
    cursor = conn.cursor()
    sql_script = '''
        DROP TABLE IF EXISTS merge_items
    '''
    cursor.execute(sql_script)
    cursor.close()       
    conn.commit()
    logger.info(rf'MERGE_ITEMS deleted') if cursor else logger.critical(rf'MERGE_ITEMS not deleted!')

    return (True)


def create_database ():
#   ** ************************************************************************************************************************************************************
#   ** 
#   ** ************************************************************************************************************************************************************

#   Create material_product_types table
        cursor = conn.cursor()
        sql_script = '''            
            CREATE TABLE material_product_types (
                material_product_type_id            INTEGER        NOT NULL PRIMARY KEY

            ,   material_code                       VARCAHR (   5) NOT NULL
            ,   material_desc                       VARCHAR ( 128) NOT NULL

            ,   product_type_code                   VARCHAR (   5) NOT NULL
            ,   product_type_desc                   VARCHAR ( 128) NOT NULL

            ,   merge_priority                      INTEGER        NOT NULL
            ,   merge_material_consolidation        VARCAHR (   1) NOT NULL
            
            ,   merge_plate_size                    INTEGER        NOT NULL
            ,   merge_plate_date                    VARCHAR (  20) NOT NULL
            ,   merge_plate_number                  INTEGER        NOT NULL
            ,   merge_plate_item_number             INTEGERE       NOT NULL
            ,   merge_plate_item_number_increment   INTEGER        NOT NULL
            ,   merge_plate_order_consolidation     VARCAHR (   1) NOT NULL

            ,   merge_ind                           VARCHAR (   1) NOT NULL    

            )'''
        cursor.execute(sql_script)
  
        logger.info(rf'MATERIAL_PRODUCT_TYPES re-created') if cursor else logger.critical(rf'MATERIAL_PRODUCT_TYPES not re-created!')

        cursor.close()       
        conn.commit()


#       *************************************************************************************
#       Create material_product_types indexes
#       *************************************************************************************
        cursor = conn.cursor()
        sql_script = '''
            CREATE UNIQUE INDEX idx_material_product_types_01 ON material_product_types (material_code, product_type_code)
            '''
        cursor.execute(sql_script)

        logger.info(rf'MATERIAL_PRODUCT_TYPES INDEX_01 re-created') if cursor else logger.critical(rf'MATERIAL_PRODUCT_TYPES INDEX_01 not re-created!')


#       *************************************************************************************
#       Create product_design_listings table
#       *************************************************************************************
        cursor = conn.cursor()
        sql_script = '''            
            CREATE TABLE product_design_listings (
                product_design_listing_id           INTEGER        NOT NULL PRIMARY KEY
            ,   sales_channel_id                    VARCAHR (  10) NOT NULL
            ,   sku                                 VARCHAR ( 100) NOT NULL
            ,   title                               VARCHAR ( 100) 
            ,   variation                           VARCHAR ( 100) NOT NULL
            ,   quantity                            INTEGER        NOT NULL
            )'''
        cursor.execute(sql_script)
  
        logger.info(rf'PRODUCT_DESIGN_LISTINGS re-created') if cursor else logger.critical(rf'PRODUCT_DESIGN_LISTINGS not re-created!')

        cursor.close()       
        conn.commit()


#       *************************************************************************************
#       Create product_design_listings indexes
#       *************************************************************************************
        cursor = conn.cursor()
        sql_script = '''
            CREATE UNIQUE INDEX idx_product_design_listings_01 ON product_design_listings (sales_channel_id, sku, variation)
            '''
        cursor.execute(sql_script)

        logger.info(rf'PRODUCT_DESIGN_LISTINGS INDEX_01 re-created') if cursor else logger.critical(rf'PRODUCT_DESIGN_LISTINGS INDEX_01 not re-created!')


#       *************************************************************************************
#       Create pdl_material_variations table
#       *************************************************************************************
        cursor = conn.cursor()
        sql_script = '''            
            CREATE TABLE pdl_material_variations (
                pdl_material_variation_id           INTEGER        NOT NULL PRIMARY KEY
            ,   pdl_id                              INTEGER        NOT NULL
            ,   pdl_material_variation_no           INTEGER        NOT NULL
            ,   material_code                       VARCHAR (   5) NOT NULL

            ,   FOREIGN KEY (pdl_id)                REFERENCES product_design_listings (product_design_listing_id)
            )'''
        cursor.execute(sql_script)

        logger.info(rf'PDL_MATERIAL_VARIATIONS re-created') if cursor else logger.critical(rf'PDL_MATERIAL_VARIATIONS not re-created!')

        cursor.close()       
        conn.commit()


#       *************************************************************************************
#       Create pdl_material_variations indexes
#       *************************************************************************************
        cursor = conn.cursor()
        sql_script = '''
            CREATE UNIQUE INDEX idx_pdl_material_variations_01 ON pdl_material_variations (pdl_material_variation_no, material_code)
            '''
        cursor.execute(sql_script)

        logger.info(rf'PDL_MATERIAL_VARIATIONS INDEX_01 re-created') if cursor else logger.critical(rf'PDL_MATERIAL_VARIATIONS INDEX_01 not re-created!')


#       *************************************************************************************
#       Create orders table
#       *************************************************************************************
        cursor = conn.cursor()
        sql_script = '''            
            CREATE TABLE orders (
                order_id                        INTEGER        NOT NULL PRIMARY KEY

            ,   sales_channel_id                VARCHAR (  10) NOT NULL
            ,   order_no                        VARCHAR (  20) NOT NULL
            ,   order_type                      VARCHAR (  50)
            ,   dispatch_priority               INTEGER

            ,   sale_date                       VARCHAR (  20)
            ,   scheduled_dispatch_date         VARCHAR (  20)
            ,   invoice_date                    VARCHAR (  20)
            ,   merge_date                      VARCHAR (  20)
            ,   production_date                 VARCHAR (  20)
            ,   packing_date                    VARCHAR (  20)
            ,   dispatched_date                 VARCHAR (  20)

            ,   number_of_items                 INTEGER
            ,   number_of_production_items      INTEGER
            ,   currency_code                   VARCHAR (   3)
            ,   order_amt                       REAL
            ,   delivery_amt                    REAL
            ,   sales_tax_amt                   REAL 
            ,   delivery_discount_amt           REAL
            ,   order_subtotal_amt              REAL
            ,   order_refunded_amt              REAL
            ,   discount_amt                    REAL
            ,   order_total_amt                 REAL

            ,   buyer_user_id                   VARCHAR (  50)
            ,   buyer_first_name                VARCHAR (  50)
            ,   buyer_last_name                 VARCHAR (  50)
            ,   buyer_full_name                 VARCHAR ( 100)
            ,   buyer_repeat_ind                VARCHAR (   1)

            ,   delivery_recipient              VARCHAR ( 100)
            ,   delivery_street_01              VARCHAR ( 100)
            ,   delivery_street_02              VARCHAR ( 100)
            ,   delivery_city                   VARCHAR (  50)
            ,   delivery_state                  VARCHAR (  50)
            ,   delivery_zipcode                VARCHAR (  50)
            ,   delivery_country_code           VARCHAR (   2)
            ,   delivery_carrier                VARCHAR (  50)
            ,   delivery_carrier_order_ref      VARCHAR (  50)
            ,   delivery_method                 VARCHAR (  50)
            ,   delivery_tracking_id            VARCHAR (  50)

            ,   delivery_address_01             VARCHAR ( 100)
            ,   delivery_address_02             VARCHAR ( 100)
            ,   delivery_address_03             VARCHAR ( 100)
            ,   delivery_address_04             VARCHAR ( 100)
            ,   delivery_address_05             VARCHAR ( 100)

            ,   marked_as_gift                  VARCHAR (   1)
            ,   gift_message_included           VARCHAR (   1)

            ,   payment_method                  VARCHAR (  50)
            ,   payment_type                    VARCHAR (  50)

            ,   private_notes                   VARCHAR (1024)
            ,   buyer_note                      VARCHAR (1024)
            ,   gift_message                    VARRCAR (1024)

            ,   card_processing_fee_amt         REAL
            ,   order_net_amt                   REAL 
            ,   adjusted_order_total_amt        REAL
            ,   adjusted_card_process_fee_amt   REAL
            ,   adjusted_net_order_amt          REAL

            ,   multi_item_ind                  VARCHAR (   1)
            ,   mergeable_ind                   VARCHAR (   1)

            ,   process_category                INTEGER
            ,   process_status                  INTEGER
            )'''
        cursor.execute(sql_script)
  
#            ,   FOREIGN KEY (customer_id)       REFERENCES customers(id)

        logger.info(rf'ORDERS re-created') if cursor else logger.critical(rf'ORDERS not re-created!')

        cursor.close()       
        conn.commit()


#   *** *************************************************************************************
#   *** Create orders indexes
#   *** *************************************************************************************
        cursor = conn.cursor()
        sql_script = '''
            CREATE UNIQUE INDEX idx_orders_01 ON orders (sales_channel_id, order_no)
            '''
        cursor.execute(sql_script)
  
        logger.info(rf'ORDERS INDEX_01 re-created') if cursor else logger.critical(rf'ORDERS INDEX_01 not re-created!')  


#       *************************************************************************************
#       Create order_items table
#       *************************************************************************************
        cursor = conn.cursor()
        sql_script = '''            
            CREATE TABLE order_items (
                order_item_id               INTEGER        NOT NULL PRIMARY KEY
            ,   sales_channel_id            VARCHAR (  10) NOT NULL
            ,   order_no                    VARCHAR (  20) NOT NULL
            ,   order_item_no               INTEGER        NOT NULL
            ,   sku                         VARCHAR ( 100)

            ,   date_sold                   TEXT           
            ,   date_posted                 TEXT           

            ,   product_material_code       VARCHAR (  20)
            ,   product_type_code           VARCHAR (  20)
            ,   product_design_code         VARCHAR (  20)

            ,   product_listing_no          VARCHAR (  20)
            ,   product_listing_title       VARCHAR (1024)

            ,   quantity                    INTEGER        NOT NULL
            ,   currency_code               VARCHAR (   3) NOT NULL
            ,   price                       REAL           NOT NULL

            ,   variation                   VARCHAR (  50)
            ,   variation_01_name           VARCHAR (  50)
            ,   variation_01_value          VARCHAR (  50)
            ,   variation_02_name           VARCHAR (  50)
            ,   variation_02_value          VARCHAR (  50)
            ,   variation_03_name           VARCHAR (  50)
            ,   variation_03_value          VARCHAR (  50)
            ,   variation_04_name           VARCHAR (  50)
            ,   variation_04_value          VARCHAR (  50)
            ,   variation_05_name           VARCHAR (  50)
            ,   variation_05_value          VARCHAR (  50)

            ,   input_personalisation       VARCHAR (1024)
            ,   merge_personalisation       VARCHAR (1024)

            ,   transaction_no              VARCHAR (  20) 
            ,   listing_id                  INTEGER        

            ,   dispatch_priority           INTEGER
            ,   mergeable_ind               VARCHAR (   1)

            ,   process_category            INTEGER
            ,   process_status              INTEGER

            ,   FOREIGN KEY (sales_channel_id, order_no) REFERENCES orders(sales_channel_id, order_no)
            )
            '''
        cursor.execute(sql_script)

        logger.info(rf'ORDER_ITEMS re-created') if cursor else logger.critical(rf'ORDER_ITEMS not re-created!')  

        cursor.close()       
        conn.commit()

#       *************************************************************************************
#       Create order_items indexes
#       *************************************************************************************
        cursor = conn.cursor()
        sql_script = '''CREATE UNIQUE INDEX idx_order_items_01 ON order_items (sales_channel_id, order_no, order_item_no)'''
        cursor.execute(sql_script)

        logger.info(rf'ORDER_ITEMS INDEX_01 re-created') if cursor else logger.critical(rf'ORDER_ITEMS INDEX_01 not re-created!')  


#       ** *************************************************************************************
#       ** Create production_items table
#       ** *************************************************************************************
        cursor = conn.cursor()
        sql_script = '''            
            CREATE TABLE production_items (
                production_item_id              INTEGER        NOT NULL PRIMARY KEY
            ,   sales_channel_id                VARCHAR (  10) NOT NULL
            ,   order_no                        VARCHAR (  20) NOT NULL
            ,   order_item_no                   INTEGER        NOT NULL
            ,   sku                             VARCHAR ( 100) NOT NULL

            ,   production_item_no              INTEGER        NOT NULL
            ,   order_size                      INTEGER        NOT NULL
            ,   dispatch_priority               INTEGER
            ,   production_priority             INTEGER
            ,   merge_priority                  INTEGER

            ,   product_material_code           VARCHAR (  20)
            ,   product_type_code               VARCHAR (  20)
            ,   product_design_code             VARCHAR (  20)
            ,   product_desc                    VARCHAR (1024)
            ,   product_design_listing_no       VARCHAR (  20)

            ,   plate_id                        VARCHAR (  64)
            ,   plate_seq                       VARCHAR (   8)
            ,   plate_id_seq                    VARCHAR (  64)

            ,   variation_01_name               VARCHAR (  50)
            ,   variation_01_value              VARCHAR (  50)
            ,   variation_02_name               VARCHAR (  50)
            ,   variation_02_value              VARCHAR (  50)
            ,   variation_03_name               VARCHAR (  50)
            ,   variation_03_value              VARCHAR (  50)
            ,   variation_04_name               VARCHAR (  50)
            ,   variation_04_value              VARCHAR (  50)
            ,   variation_05_name               VARCHAR (  50)
            ,   variation_05_value              VARCHAR (  50)

            ,   input_personalisation           VARCHAR (1024)
            ,   merge_personalisation           VARCHAR (1024)
            ,   output_personalisation          VARCHAR (1024)

            ,   private_notes                   VARCHAR (1024)
            ,   buyer_note                      VARCHAR (1024)

            ,   length_mm                       INTEGER
            ,   width_mm                        INTEGER
            ,   depth_mm                        INTEGER
            ,   weight_grms                     INTEGER
    
            ,   process_category                INTEGER
            ,   process_status                  INTEGER

            ,   FOREIGN KEY (sales_channel_id, order_no)                REFERENCES orders     (sales_channel_id, order_no)
            ,   FOREIGN KEY (sales_channel_id, order_no, order_item_no) REFERENCES order_items(sales_channel_id, order_no, order_item_no)
            )
            '''
        cursor.execute(sql_script)

        logger.info(rf'PRODUCTION_ITEMS re-created') if cursor else logger.critical(rf'PRODUCTION_ITEMS not re-created!')

        cursor.close()       
        conn.commit()


#   *** *************************************************************************************
#   *** Create production_items indexes
#   *** *************************************************************************************
        cursor = conn.cursor()
        sql_script = '''CREATE UNIQUE INDEX idx_production_items_01 ON production_items (sales_channel_id, order_no, order_item_no, production_item_no)'''
        cursor.execute(sql_script)
  
        logger.info(rf'PRODUCTION_ITEMS INDEX_01 re-created') if cursor else logger.critical(rf'PRODUCTION_ITEMS INDXE_01 not re-created!')

        cursor = conn.cursor()
        sql_script = '''CREATE UNIQUE INDEX idx_production_items_02 ON production_items (plate_id_seq)'''
        cursor.execute(sql_script)

        logger.info(rf'PRODUCTION_ITEMS INDXE_02 re-created') if cursor else logger.critical(rf'PRODUCTION_ITEMS not re-created!')  

        cursor.close()       
        conn.commit()


#       ** *************************************************************************************
#       ** Create merge_items table
#       ** *************************************************************************************
        cursor = conn.cursor()
        sql_script = '''            
            CREATE TABLE merge_items (
                merge_item_id                   INTEGER        NOT NULL PRIMARY KEY
            ,   sales_channel_id                VARCHAR (  10) NOT NULL
            ,   order_no                        VARCHAR (  20) NOT NULL
            ,   order_item_no                   INTEGER        NOT NULL
            ,   sku                             VARCHAR ( 100) NOT NULL

            ,   merge_item_no                   INTEGER        NOT NULL
            ,   order_size                      INTEGER        NOT NULL
            ,   dispatch_priority               INTEGER
            ,   production_priority             INTEGER
            ,   merge_priority                  INTEGER

            ,   product_material_code           VARCHAR (  20)
            ,   product_type_code               VARCHAR (  20)
            ,   product_design_code             VARCHAR (  20)
            ,   product_desc                    VARCHAR (1024)
            ,   product_design_listing_no       VARCHAR (  20)

            ,   plate_id                        VARCHAR (  64)
            ,   plate_seq                       VARCHAR (   8)
            ,   plate_id_seq                    VARCHAR (  64)

            ,   variation_01_name               VARCHAR (  50)
            ,   variation_01_value              VARCHAR (  50)
            ,   variation_02_name               VARCHAR (  50)
            ,   variation_02_value              VARCHAR (  50)
            ,   variation_03_name               VARCHAR (  50)
            ,   variation_03_value              VARCHAR (  50)
            ,   variation_04_name               VARCHAR (  50)
            ,   variation_04_value              VARCHAR (  50)
            ,   variation_05_name               VARCHAR (  50)
            ,   variation_05_value              VARCHAR (  50)

            ,   input_personalisation           VARCHAR (1024)
            ,   merge_personalisation           VARCHAR (1024)
            ,   output_personalisation          VARCHAR (1024)

            ,   private_notes                   VARCHAR (1024)
            ,   buyer_note                      VARCHAR (1024)

            ,   length_mm                       INTEGER
            ,   width_mm                        INTEGER
            ,   depth_mm                        INTEGER
            ,   weight_grms                     INTEGER

            ,   process_category                INTEGER
            ,   process_status                  INTEGER

            ,   FOREIGN KEY (sales_channel_id, order_no)                REFERENCES orders     (sales_channel_id, order_no)
            ,   FOREIGN KEY (sales_channel_id, order_no, order_item_no) REFERENCES order_items(sales_channel_id, order_no, order_item_no)
            )
            '''
        cursor.execute(sql_script)

        logger.info(rf'MERGE_ITEMS re-created') if cursor else logger.critical(rf'MERGE_ITEMS not re-created!')

        cursor.close()       
        conn.commit()


#   *** *************************************************************************************
#   *** Create merge_items indexes
#   *** *************************************************************************************
        cursor = conn.cursor()
        sql_script = '''CREATE UNIQUE INDEX idx_merge_items_01 ON merge_items (sales_channel_id, order_no, order_item_no, merge_item_no)'''
        cursor.execute(sql_script)

        logger.info(rf'MERGE_ITEMS INDEX_01 re-created') if cursor else logger.critical(rf'MERGE_ITEMS INDEX_01 not re-created!')  

        cursor = conn.cursor()
        sql_script = '''CREATE UNIQUE INDEX idx_merge_items_02 ON merge_items (plate_id_seq)'''
        cursor.execute(sql_script)

        logger.info(rf'MERGE_ITEMS INDEX_02 re-created') if cursor else logger.critical(rf'MERGE_ITEMS INDEX_02 not re-created!')  

        cursor.close()       
        conn.commit()


if __name__ == '__main__':
#   ** ************************************************************************************************************************************************************
#   ** Mainline code
#   ** ************************************************************************************************************************************************************
    success: bool = False


    try:
        sys_settings : SystemSettings = SystemSettings()   
        database_path: str            = sys_settings.database_path

        logger: logging.Logger = get_custom_logger('SYSTEM RESET')

#       create a database connection
        conn = create_connection(database_path)
        with conn:
            cursor = conn.cursor()
            cursor.execute('''PRAGMA foreign_keys = OFF''')
            cursor.close()

            delete_database()
            create_database()


            success = create_DefaultMaterialProductTypes(conn)

            logger.info(rf'MATERIAL_PRODUCT_TYPES loaded') if cursor else logger.critical(rf'MATERIAL_PRODUCT_TYPES not loaded!')

            invoice_path_out: str = os.path.join(sys_settings.etsy_target_invoice_path     , sys_settings.process_date)
            message_path_out: str = os.path.join(sys_settings.etsy_target_gift_receipt_path, sys_settings.process_date)
            sorted_path_out : str = os.path.join(sys_settings.sorted_invoice_path          , sys_settings.process_date)

            shutil.rmtree (invoice_path_out) if os.path.exists(invoice_path_out) else None
            shutil.rmtree (message_path_out) if os.path.exists(message_path_out) else None
            shutil.rmtree (sorted_path_out)  if os.path.exists(sorted_path_out)  else None

            logger.info(rf'{invoice_path_out} directory deleted') if not os.path.exists(invoice_path_out) else logger.critical(rf'{invoice_path_out} directory NOT deleted')
            logger.info(rf'{message_path_out} directory deleted') if not os.path.exists(message_path_out) else logger.critical(rf'{message_path_out} directory NOT deleted')
            logger.info(rf'{sorted_path_out}  directory deleted') if not os.path.exists(sorted_path_out)  else logger.critical(rf'{sorted_path_out} directory NOT deleted')

            os.mkdir (invoice_path_out)
            os.mkdir (message_path_out)
            os.mkdir (sorted_path_out)

            logger.info(rf'{invoice_path_out} directory created') if os.path.exists(invoice_path_out) else logger.critical(rf'{invoice_path_out} directory NOT created')
            logger.info(rf'{message_path_out} directory created') if os.path.exists(message_path_out) else logger.critical(rf'{message_path_out} directory NOT created')
            logger.info(rf'{sorted_path_out}  directory created') if os.path.exists(sorted_path_out)  else logger.critical(rf'{sorted_path_out} directory NOT created')


            merge_path_in: str  = os.path.join (sys_settings.absolute_home_path, sys_settings.merge_input_path , sys_settings.process_date)
            merge_path_out: str = os.path.join (sys_settings.absolute_home_path, sys_settings.merge_output_path, sys_settings.process_date)

            shutil.rmtree (merge_path_in)  if os.path.exists(merge_path_in)  else None
            shutil.rmtree (merge_path_out) if os.path.exists(merge_path_out) else None

            logger.info(rf'{merge_path_in}  directory deleted') if not os.path.exists(merge_path_in)  else logger.critical(rf'{merge_path_in} directory NOT deleted')
            logger.info(rf'{merge_path_out} directory deleted') if not os.path.exists(merge_path_out) else logger.critical(rf'{merge_path_out} directory NOT deleted')

            os.mkdir (merge_path_in)
            os.mkdir (merge_path_out)

            logger.info(rf'{merge_path_in}  directory created') if os.path.exists(merge_path_in)  else logger.critical(rf'{merge_path_in}  directory NOT created')
            logger.info(rf'{merge_path_out} directory created') if os.path.exists(merge_path_out) else logger.critical(rf'{merge_path_out} directory NOT created')

    except Exception as e:
        logging.exception("Exception occurred")
