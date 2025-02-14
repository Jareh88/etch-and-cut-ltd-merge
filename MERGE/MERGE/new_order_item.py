import csv, sys, sqlite3, os
from datetime import datetime
from dataclasses import dataclass


# ************************************************************************************************************************************************************
# CLASS: OrderItem
# ************************************************************************************************************************************************************
@dataclass
class NewOrderItem:
    """Etch & Cut OrderItem Class"""

    order_item_id: int = None
    sales_channel_id: str = None
    order_no: str = None
    order_item_no: int = None
    sku: str = None

    date_sold: datetime = None
    date_posted: datetime = None

    product_material_code: str = ''
    product_type_code: str = ''
    product_design_code: str = ''

    product_listing_no: str = ''
    product_listing_title: str = ''

    quantity: int = None
    currency_code: str = None
    price: float = None

    variation: str = None
    variation_01_name: str = None
    variation_01_value: str = None
    variation_02_name: str = None
    variation_02_value: str = None
    variation_03_name: str = None
    variation_03_value: str = None
    variation_04_name: str = None
    variation_04_value: str = None
    variation_05_name: str = None
    variation_05_value: str = None

    input_personalisation: str = None
    merge_personalisation: str = None

    transaction_no: str = None
    listing_id: str = None

    mergeable_ind: str = 'N'
    dispatch_priority: int = 0

    process_category: int = None  # 1 = NEXT DAY, 2 = USA, 3 = MULTI ITEM (DIFFERENT PRODUCT ITEMS), 4 = SINGLE (OR MULTI WITH SAME PRODUCT ITEMS), 5 = UNALLOCATED
    process_status: int = 0  # 0 = unprocessed, 1 = processed, 3 = merged, 4 = plated, 5 = processed, 6 = packed, 7 = dispatched, 99 = ERROR

    def save(self, conn):
        #   *** ************************************************************************************************************************************************************
        #   *** insert order_item database table record
        #   *** ************************************************************************************************************************************************************
        #        print(f'''OrderItem-save_OrderItem: order_no: {self.order_no}, quantity: {self.quantity}, order_item: {self.order_item_no}''')

        cursor = conn.cursor()
        sql = '''
            INSERT
                INTO order_items(
                    order_item_id
                ,   sales_channel_id, order_no, order_item_no, sku
                ,   date_sold, date_posted
                ,   product_material_code, product_type_code, product_design_code
                ,   product_listing_no, product_listing_title
                ,   quantity, currency_code, price
                ,   variation, variation_01_name, variation_01_value, variation_02_name, variation_02_value, variation_03_name, variation_03_value, variation_04_name, variation_04_value, variation_05_name, variation_05_value
                ,   input_personalisation, merge_personalisation
                ,   transaction_no, listing_id
                ,   mergeable_ind, dispatch_priority
                ,   process_category, process_status
                )
                VALUES
                (
                    NULL
                ,   ?, ?, ?, ?
                ,   ?, ?
                ,   ?, ?, ?
                ,   ?, ?
                ,   ?, ?, ?
                ,   ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                ,   ?, ?
                ,   ?, ?
                ,   ?, ?
                ,   ?, ?
                )
            '''
        cursor.execute(
            sql,
            (
                self.sales_channel_id, self.order_no, self.order_item_no, self.sku
                , self.date_sold, self.date_posted
                , self.product_material_code, self.product_type_code, self.product_design_code
                , self.product_listing_no, self.product_listing_title
                , self.quantity, self.currency_code, self.price
                , self.variation, self.variation_01_name, self.variation_01_value, self.variation_02_name,
                self.variation_02_value, self.variation_03_name, self.variation_03_value, self.variation_04_name,
                self.variation_04_value, self.variation_05_name, self.variation_05_value
                , self.input_personalisation, self.merge_personalisation
                , self.transaction_no, self.listing_id
                , self.mergeable_ind, self.dispatch_priority
                , self.process_category, self.process_status)
        )
        if cursor:
            conn.commit()
            cursor.close()
        else:
            print("order_items table insert failed!")
            cursor.close()

    def update(self, conn):
        #   *** ************************************************************************************************************************************************************
        #   *** update order_item database table record
        #   *** ************************************************************************************************************************************************************
        cursor = conn.cursor()
        sql = '''
            UPDATE order_items 
                SET
                    sales_channel_id =?, order_no =?, order_item_no =?, sku =?
                ,   date_sold =?, date_posted =?
                ,   product_material_code =?, product_type_code =?, product_design_code =?
                ,   product_listing_no =?, product_listing_title =?
                ,   quantity =?, currency_code =?, price =?
                ,   variation =?, variation_01_name =?, variation_01_value =?, variation_02_name =?, variation_02_value =?, variation_03_name =?, variation_03_value =?, variation_04_name =?, variation_04_value =?, variation_05_name =?, variation_05_value =?
                ,   input_personalisation =?, merge_personalisation =?
                ,   transaction_no =?, listing_id =?
                ,   mergeable_ind =?, dispatch_priority =?
                ,   process_category =?, process_status =?
                WHERE 
                    order_items.sales_channel_id =? AND
                    order_items.order_no         =? AND
                    order_items.order_item_no    =? 
            '''

        cursor.execute(
            sql,
            (
                self.sales_channel_id, self.order_no, self.order_item_no, self.sku
                , self.date_sold, self.date_posted
                , self.product_material_code, self.product_type_code, self.product_design_code
                , self.product_listing_no, self.product_listing_title
                , self.quantity, self.currency_code, self.price
                , self.variation, self.variation_01_name, self.variation_01_value, self.variation_02_name,
                self.variation_02_value, self.variation_03_name, self.variation_03_value, self.variation_04_name,
                self.variation_04_value, self.variation_05_name, self.variation_05_value
                , self.input_personalisation, self.merge_personalisation
                , self.transaction_no, self.listing_id
                , self.mergeable_ind, self.dispatch_priority
                , self.process_category, self.process_status
                ,
                self.sales_channel_id, self.order_no, self.order_item_no,)
        )
        if cursor:
            conn.commit()
            cursor.close()
        else:
            print("order_item database table update failed!")
            cursor.close()


def get_order_item(conn, sales_channel_id, order_no, order_item_no):
    # ** ************************************************************************************************************************************************************
    # ** get a single order_item database table record
    # ** ************************************************************************************************************************************************************
    cursor = conn.cursor()
    sql = '''
        SELECT
            sales_channel_id, order_no, order_item_no, sku
        ,   date_sold, date_posted
        ,   product_material_code, product_type_code, product_design_code
        ,   product_listing_no, product_listing_title
        ,   quantity, currency_code, price
        ,   variation, variation_01_name, variation_01_value, variation_02_name, variation_02_value, variation_03_name, variation_03_value, variation_04_name, variation_04_value, variation_05_name, variation_05_value
        ,   input_personalisation, merge_personalisation
        ,   transaction_no, listing_id
        ,   mergeable_ind, dispatch_priority
        ,   process_category, process_status
        FROM
            order_items
        WHERE 
            order_items.sales_channel_id =? AND
            order_items.order_no         =? AND
            order_items.order_item_no    =? 
        LIMIT 
            1
        '''
    cursor.execute(sql, (sales_channel_id, order_no, order_item_no,))
    rows = cursor.fetchall()

    if rows is not None:
        for row in rows:
            order_item: NewOrderItem = NewOrderItem()

            order_item.sales_channel_id = row[0]
            order_item.order_no = row[1]
            order_item.order_item_no = row[2]
            order_item.sku = row[3]

            order_item.date_sold = row[4]
            order_item.date_posted = row[5]

            order_item.product_material_code = row[6]
            order_item.product_type_code = row[7]
            order_item.product_design_code = row[8]

            order_item.product_listing_no = row[9]
            order_item.product_listing_title = row[10]

            order_item.quantity = row[11]
            order_item.currency_code = row[12]
            order_item.price = row[13]

            order_item.variation = row[14]
            order_item.variation_01_name = row[15]
            order_item.variation_01_value = row[16]
            order_item.variation_02_name = row[17]
            order_item.variation_02_value = row[18]
            order_item.variation_03_name = row[19]
            order_item.variation_03_value = row[20]
            order_item.variation_04_name = row[21]
            order_item.variation_04_value = row[22]
            order_item.variation_05_name = row[23]
            order_item.variation_05_value = row[24]

            order_item.input_personalisation = row[25]
            order_item.merge_personalisation = row[26]

            order_item.transaction_no = row[27]
            order_item.listing_id = row[28]

            order_item.mergeable_ind = row[29]
            order_item.dispatch_priority = row[30]

            order_item.process_category = row[31]
            order_item.process_status = row[32]

            cursor.close()
            return (order_item)
    else:
        return (None)


def existing_order_item(conn, sales_channel_id, order_no, transaction_no, order_item_no):
    #   ************************************************************************************************************************************************************
    #   determines whether a specific order_item database table record exists
    #   ************************************************************************************************************************************************************
    cursor = conn.cursor()
    sql = '''
        SELECT
            order_items.order_item_id
        FROM
            order_items
        WHERE 
            order_items.sales_channel_id =? AND
            order_items.order_no         =? AND
            order_items.transaction_no   =? AND
            order_items.order_item_no    =?
        LIMIT 
            1
        '''
    cursor.execute(sql, (sales_channel_id, order_no, transaction_no, order_item_no,))
    row = cursor.fetchone()

    if row is not None:
        return (True)
    else:
        return (False)


def count_order_items_by_status(conn, sales_channel_id: str, order_no: str, process_status: int) -> int:
    #   ************************************************************************************************************************************************************
    #   Retrieve all un-processed order_item rows from order_items table and order by order.dispatch_priority
    #   ************************************************************************************************************************************************************
    cursor = conn.cursor()
    sql = '''
        SELECT
            count (*)
        FROM
            order_items
        WHERE
            order_items.sales_channel_id = ? AND
            order_items.order_no         = ? AND
            order_items.process_status   = ?
        '''
    cursor.execute(sql, (sales_channel_id, order_no, process_status,))
    row = cursor.fetchone()

    if row is not None:
        return (row[0])
    else:
        return (0)


def get_last_order_item_no(conn, sales_channel_id: str, order_no: str) -> int:
    #   ************************************************************************************************************************************************************
    #
    #   ************************************************************************************************************************************************************
    cursor = conn.cursor()
    sql = '''
        SELECT
            order_item_no
        FROM
            order_items
        WHERE
            order_items.sales_channel_id = ? AND
            order_items.order_no         = ? 
        ORDER BY
            order_items.order_item_no DESC
        '''
    cursor.execute(sql, (sales_channel_id, order_no,))
    row = cursor.fetchone()

    if row is not None:
        return (row[0])
    else:
        return (None)


def get_order_items_by_status(conn, sales_channel_id: str, order_no: str, process_status: int) -> list[NewOrderItem]:
    #   ************************************************************************************************************************************************************
    #   Retrieve all un-processed order_item rows from order_items table and order by order.dispatch_priority
    #   ************************************************************************************************************************************************************
    cursor = conn.cursor()
    sql = '''
        SELECT
            sales_channel_id, order_no, order_item_no, sku
        ,   date_sold, date_posted
        ,   product_material_code, product_type_code, product_design_code
        ,   product_listing_no, product_listing_title
        ,   quantity, currency_code, price
        ,   variation, variation_01_name, variation_01_value, variation_02_name, variation_02_value, variation_03_name, variation_03_value, variation_04_name, variation_04_value, variation_05_name, variation_05_value
        ,   input_personalisation, merge_personalisation
        ,   transaction_no, listing_id
        ,   mergeable_ind, dispatch_priority
        ,   process_category, process_status
        FROM
            order_items
        WHERE
            order_items.sales_channel_id = ? AND
            order_items.order_no         = ? AND
            order_items.process_status   = ?
        ORDER BY
            order_items.sales_channel_id
        ,   order_items.order_no
        ,   order_items.process_status
        '''
    cursor.execute(sql, (sales_channel_id, order_no, process_status,))
    rows = cursor.fetchall()
    order_items: list[NewOrderItem] = []

    if rows is not None:
        for row in rows:
            order_item: NewOrderItem = NewOrderItem()

            order_item.sales_channel_id = row[0]
            order_item.order_no = row[1]
            order_item.order_item_no = row[2]
            order_item.sku = row[3]

            order_item.date_sold = row[4]
            order_item.date_posted = row[5]

            order_item.product_material_code = row[6]
            order_item.product_type_code = row[7]
            order_item.product_design_code = row[8]

            order_item.product_listing_no = row[9]
            order_item.product_listing_title = row[10]

            order_item.quantity = row[11]
            order_item.currency_code = row[12]
            order_item.price = row[13]

            order_item.variation = row[14]
            order_item.variation_01_name = row[15]
            order_item.variation_01_value = row[16]
            order_item.variation_02_name = row[17]
            order_item.variation_02_value = row[18]
            order_item.variation_03_name = row[19]
            order_item.variation_03_value = row[20]
            order_item.variation_04_name = row[21]
            order_item.variation_04_value = row[22]
            order_item.variation_05_name = row[23]
            order_item.variation_05_value = row[24]

            order_item.input_personalisation = row[25]
            order_item.merge_personalisation = row[26]

            order_item.transaction_no = row[27]
            order_item.listing_id = row[28]

            order_item.mergeable_ind = row[29]
            order_item.dispatch_priority = row[30]

            order_item.process_category = row[31]
            order_item.process_status = row[32]

            order_items.append(order_item)

        cursor.close()
        return (order_items)
    else:
        cursor.close()
        return (None)


def get_sorted_order_items(conn, process_status: int, process_category: int, product_material_code: str,
                           product_type_code: str) -> list[NewOrderItem]:
    #   ************************************************************************************************************************************************************
    #   Retrieve all un-processed order_item rows from order_items table and order by order.dispatch_priority
    #   ************************************************************************************************************************************************************
    cursor = conn.cursor()
    sql = '''
        SELECT
            sales_channel_id, order_no, order_item_no, sku
        ,   date_sold, date_posted
        ,   product_material_code, product_type_code, product_design_code
        ,   product_listing_no, product_listing_title
        ,   quantity, currency_code, price
        ,   variation, variation_01_name, variation_01_value, variation_02_name, variation_02_value, variation_03_name, variation_03_value, variation_04_name, variation_04_value, variation_05_name, variation_05_value
        ,   input_personalisation, merge_personalisation
        ,   transaction_no, listing_id
        ,   mergeable_ind, dispatch_priority
        ,   process_category, process_status
        FROM
            order_items
        WHERE
            order_items.process_status        = ? AND
            order_items.process_category      = ? AND
            order_items.product_material_code = ? AND
            order_items.product_type_code     = ?
        ORDER BY
            order_items.product_material_code
        ,   order_items.product_type_code
        ,   order_items.product_design_code
        ,   order_items.mergeable_ind
        ,   order_items.sales_channel_id
        ,   order_items.order_no
        '''
    cursor.execute(sql, (process_status, process_category, product_material_code, product_type_code,))
    rows = cursor.fetchall()
    order_items: list[NewOrderItem] = []

    if rows is not None:
        for row in rows:
            order_item: NewOrderItem = NewOrderItem()

            order_item.sales_channel_id = row[0]
            order_item.order_no = row[1]
            order_item.order_item_no = row[2]
            order_item.sku = row[3]

            order_item.date_sold = row[4]
            order_item.date_posted = row[5]

            order_item.product_material_code = row[6]
            order_item.product_type_code = row[7]
            order_item.product_design_code = row[8]

            order_item.product_listing_no = row[9]
            order_item.product_listing_title = row[10]

            order_item.quantity = row[11]
            order_item.currency_code = row[12]
            order_item.price = row[13]

            order_item.variation = row[14]
            order_item.variation_01_name = row[15]
            order_item.variation_01_value = row[16]
            order_item.variation_02_name = row[17]
            order_item.variation_02_value = row[18]
            order_item.variation_03_name = row[19]
            order_item.variation_03_value = row[20]
            order_item.variation_04_name = row[21]
            order_item.variation_04_value = row[22]
            order_item.variation_05_name = row[23]
            order_item.variation_05_value = row[24]

            order_item.input_personalisation = row[25]
            order_item.merge_personalisation = row[26]

            order_item.transaction_no = row[27]
            order_item.listing_id = row[28]

            order_item.mergeable_ind = row[29]
            order_item.dispatch_priority = row[30]

            order_item.process_category = row[31]
            order_item.process_status = row[32]

            order_items.append(order_item)

        cursor.close()
        return (order_items)
    else:
        cursor.close()
        return (None)


def get_distinct_material_product_types(conn, process_status: int):
    #   ************************************************************************************************************************************************************
    #   gets a count of all unprocessed order items x quantity for each product material and product type
    #   ************************************************************************************************************************************************************
    cursor = conn.cursor()
    sql = '''
        SELECT
                product_material_code || '-' || product_type_code || ': ' || (COUNT(*) * quantity)
	    FROM
		    order_items
        GROUP BY
                order_items.product_material_code
            ,   order_items.product_type_code
        HAVING
		    order_items.process_status = ?
        ORDER BY
                order_items.product_material_code
            ,   order_items.product_type_code
        '''
    cursor.execute(sql, (process_status,))
    rows = cursor.fetchall()
    list = []

    if rows is not None:
        for row in rows:
            list.append(row[0])
        cursor.close()
        return (list)
    else:
        cursor.close()
        return (None)


def summarise_distinct_material_product_types(conn, process_status: int):
    #   ************************************************************************************************************************************************************
    #   gets a count of all unprocessed order items x quantity for each product material and product type
    #   ************************************************************************************************************************************************************
    cursor = conn.cursor()
    sql = '''
        SELECT
                product_material_code || '-' || product_type_code || ': ' || (COUNT(*) * quantity)
	    FROM
		    order_items
        GROUP BY
                order_items.product_material_code
            ,   order_items.product_type_code
        HAVING
		    order_items.process_status = ?
        ORDER BY
                order_items.product_material_code
            ,   order_items.product_type_code
        '''
    cursor.execute(sql, (process_status,))
    rows = cursor.fetchall()
    list = []

    if rows is not None:
        for row in rows:
            list.append(row[0])
        cursor.close()
        return (list)
    else:
        cursor.close()
        return (None)


def get_material_product_types(conn, process_status: int, process_category: int) -> list[str]:
    #   ************************************************************************************************************************************************************
    #   gets a count of all unprocessed order items x quantity for each product material and product type
    #   ************************************************************************************************************************************************************
    cursor = conn.cursor()
    sql = '''
        SELECT DISTINCT
                product_material_code|| '_' || product_type_code
	    FROM
		    order_items
        WHERE
		    order_items.process_status   = ? AND
            order_items.process_category = ?
        ORDER BY
                order_items.product_material_code
            ,   order_items.product_type_code
        '''
    cursor.execute(sql, (process_status, process_category,))
    rows = cursor.fetchall()
    list = []

    if rows is not None:
        for row in rows:
            list.append(row[0])
        cursor.close()
        return (list)
    else:
        cursor.close()
        return (None)


# ************************************************************************************************************************************************************
# FUNCTION: Return ISO formatted date from MM/DD/YY, MM/DD/YYYY, null or blank date field
# ************************************************************************************************************************************************************
def iso_YYYYMMDD(in_date):
    if in_date != None and in_date != '':
        try:
            o_date = datetime.strptime(in_date, '%m/%d/%y')
            r_date = o_date.isoformat()
        except ValueError as ve:
            o_date = datetime.strptime(in_date, '%m/%d/%Y')
            r_date = o_date.isoformat()
    else:
        r_date = None

    return r_date
