import csv, sys, sqlite3, os
from datetime import datetime
from dataclasses import dataclass


# ************************************************************************************************************************************************************
# CLASS: Order
# ************************************************************************************************************************************************************
@dataclass
class NewOrder():
    """Etch & Cut Order Class"""

    order_id: int = None

    sales_channel_id: str = None
    order_no: str = None
    order_type: str = None
    dispatch_priority: int = None

    sale_date: datetime = None
    scheduled_dispatch_date: datetime = None
    invoice_date: datetime = None
    merge_date: datetime = None
    production_date: datetime = None
    packing_date: datetime = None
    dispatched_date: datetime = None

    number_of_items: int = None
    number_of_production_items: int = None
    currency_code: str = None
    order_amt: float = None
    delivery_amt: float = None
    sales_tax_amt: float = None
    delivery_discount_amt: float = None
    order_subtotal_amt: float = None
    order_refunded_amt: float = None
    discount_amt: float = None
    order_total_amt: float = None

    buyer_user_id: str = None
    buyer_first_name: str = None
    buyer_last_name: str = None
    buyer_full_name: str = None
    buyer_repeat_ind: str = None

    delivery_recipient: str = None
    delivery_street_01: str = None
    delivery_street_02: str = None
    delivery_city: str = None
    delivery_state: str = None
    delivery_zipcode: str = None
    delivery_country_code: str = None

    delivery_carrier: str = None
    delivery_carrier_order_ref: str = None
    delivery_method: str = None
    delivery_tracking_id: str = None

    delivery_address_01: str = None
    delivery_address_02: str = None
    delivery_address_03: str = None
    delivery_address_04: str = None
    delivery_address_05: str = None

    marked_as_gift: str = None
    gift_message_included: str = None

    payment_method: str = None
    payment_type: str = None

    private_notes: str = None
    buyer_note: str = None
    gift_message: str = None

    card_processing_fee_amt: float = None
    order_net_amt: float = None
    adjusted_order_total_amt: float = None
    adjusted_card_process_fee_amt: float = None
    adjusted_net_order_amt: float = None

    multi_item_ind: str = 'N'
    mergeable_ind: str = 'N'

    process_category: int = None  # 0 = UNALLOCATED, 1 = NEXT DAY, 2 = USA, 3 = MULTI ITEM (DIFFERENT PRODUCT ITEMS), 4 = SINGLE (OR MULTI WITH SAME PRODUCT ITEMS)
    process_status: int = 0  # 0 = unprocessed, 1 = pre-merge, 3 = merged, 4 = plated, 5 = processed, 6 = packed, 7 = dispatched, 99 = ERROR

    def save(self, conn):
        #   *** ************************************************************************************************************************************************************
        #   *** insert order database table record
        #   *** ************************************************************************************************************************************************************
        cursor = conn.cursor()
        sql = '''
            INSERT INTO orders(
                order_id
            ,   sales_channel_id, order_no, order_type, dispatch_priority
            ,   sale_date, scheduled_dispatch_date, invoice_date, merge_date, production_date, packing_date, dispatched_date
            ,   number_of_items, number_of_production_items, currency_code, order_amt, delivery_amt, sales_tax_amt, delivery_discount_amt, order_subtotal_amt, order_refunded_amt, discount_amt, order_total_amt
            ,   buyer_user_id, buyer_first_name, buyer_last_name, buyer_full_name, buyer_repeat_ind
            ,   delivery_recipient, delivery_street_01, delivery_street_02, delivery_city, delivery_state, delivery_zipcode, delivery_country_code
            ,   delivery_carrier, delivery_carrier_order_ref, delivery_method, delivery_tracking_id
            ,   delivery_address_01, delivery_address_02, delivery_address_03, delivery_address_04, delivery_address_05
            ,   marked_as_gift, gift_message_included
            ,   payment_method, payment_type
            ,   private_notes, buyer_note, gift_message
            ,   card_processing_fee_amt, order_net_amt, adjusted_order_total_amt, adjusted_card_process_fee_amt, adjusted_net_order_amt
            ,   multi_item_ind, mergeable_ind
            ,   process_category, process_status
            )
            VALUES(
                NULL
            ,   ?, ?, ?, ?
            ,   ?, ?, ?, ?, ?, ?, ?
            ,   ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            ,   ?, ?, ?, ?, ?
            ,   ?, ?, ?, ?, ?, ?, ?
            ,   ?, ?, ?, ?
            ,   ?, ?, ?, ?, ?             
            ,   ?, ?
            ,   ?, ?
            ,   ?, ?, ?
            ,   ?, ?, ?, ?, ?
            ,   ?, ?
            ,   ?, ?
            )
            '''
        cursor.execute(
            sql,
            (
                self.sales_channel_id, self.order_no, self.order_type, self.dispatch_priority
                , self.sale_date, self.scheduled_dispatch_date, self.invoice_date, self.merge_date,
                self.production_date, self.packing_date, self.dispatched_date
                , self.number_of_items, self.number_of_production_items, self.currency_code, self.order_amt,
                self.delivery_amt, self.sales_tax_amt, self.delivery_discount_amt, self.order_subtotal_amt,
                self.order_refunded_amt, self.discount_amt, self.order_total_amt
                , self.buyer_user_id, self.buyer_first_name, self.buyer_last_name, self.buyer_full_name,
                self.buyer_repeat_ind
                , self.delivery_recipient, self.delivery_street_01, self.delivery_street_02, self.delivery_city,
                self.delivery_state, self.delivery_zipcode, self.delivery_country_code
                , self.delivery_carrier, self.delivery_carrier_order_ref, self.delivery_method,
                self.delivery_tracking_id
                , self.delivery_address_01, self.delivery_address_02, self.delivery_address_03,
                self.delivery_address_04, self.delivery_address_05
                , self.marked_as_gift, self.gift_message_included
                , self.payment_method, self.payment_type
                , self.private_notes, self.buyer_note, self.gift_message
                , self.card_processing_fee_amt, self.order_net_amt, self.adjusted_order_total_amt,
                self.adjusted_card_process_fee_amt, self.adjusted_net_order_amt
                , self.multi_item_ind, self.mergeable_ind
                , self.process_category, self.process_status)
        )
        if cursor:
            conn.commit()
            cursor.close()
        else:
            print("orders table insert failed!")
            cursor.close()

    def update(self, conn):
        #   *** ************************************************************************************************************************************************************
        #   *** update order database table
        #   *** ************************************************************************************************************************************************************
        cursor = conn.cursor()
        sql = '''
            UPDATE 
                orders 
            SET
                sales_channel_id =?, order_no =?, order_type =?, dispatch_priority =?
            ,   sale_date =?, scheduled_dispatch_date =?, invoice_date =?, merge_date =?, production_date =?, packing_date =?, dispatched_date =?
            ,   number_of_items =?, number_of_production_items =?, currency_code =?, order_amt =?, delivery_amt =?, sales_tax_amt =?, delivery_discount_amt =?, order_subtotal_amt =?, order_refunded_amt =?, discount_amt =?, order_total_amt =?
            ,   buyer_user_id =?, buyer_first_name =?, buyer_last_name =?, buyer_full_name =?, buyer_repeat_ind =?
            ,   delivery_recipient =?, delivery_street_01 =?, delivery_street_02 =?, delivery_city =?, delivery_state =?, delivery_zipcode =?, delivery_country_code =?
            ,   delivery_carrier =?, delivery_carrier_order_ref =?, delivery_method =?, delivery_tracking_id =?
            ,   delivery_address_01 =?, delivery_address_02 =?, delivery_address_03 =?, delivery_address_04 =?, delivery_address_05 =?
            ,   marked_as_gift =?, gift_message_included =?
            ,   payment_method =?, payment_type =?
            ,   private_notes =?, buyer_note =?, gift_message =?
            ,   card_processing_fee_amt =?, order_net_amt =?, adjusted_order_total_amt =?, adjusted_card_process_fee_amt =?, adjusted_net_order_amt =?
            ,   multi_item_ind =?, mergeable_ind =?
            ,   process_category =?, process_status =?
            WHERE 
                orders.sales_channel_id =? AND
                orders.order_no         =?
            '''
        cursor.execute(
            sql,
            (
                self.sales_channel_id, self.order_no, self.order_type, self.dispatch_priority
                , self.sale_date, self.scheduled_dispatch_date, self.invoice_date, self.merge_date,
                self.production_date, self.packing_date, self.dispatched_date
                , self.number_of_items, self.number_of_production_items, self.currency_code, self.order_amt,
                self.delivery_amt, self.sales_tax_amt, self.delivery_discount_amt, self.order_subtotal_amt,
                self.order_refunded_amt, self.discount_amt, self.order_total_amt
                , self.buyer_user_id, self.buyer_first_name, self.buyer_last_name, self.buyer_full_name,
                self.buyer_repeat_ind
                , self.delivery_recipient, self.delivery_street_01, self.delivery_street_02, self.delivery_city,
                self.delivery_state, self.delivery_zipcode, self.delivery_country_code
                , self.delivery_carrier, self.delivery_carrier_order_ref, self.delivery_method,
                self.delivery_tracking_id
                , self.delivery_address_01, self.delivery_address_02, self.delivery_address_03,
                self.delivery_address_04, self.delivery_address_05
                , self.marked_as_gift, self.gift_message_included
                , self.payment_method, self.payment_type
                , self.private_notes, self.buyer_note, self.gift_message
                , self.card_processing_fee_amt, self.order_net_amt, self.adjusted_order_total_amt,
                self.adjusted_card_process_fee_amt, self.adjusted_net_order_amt
                , self.multi_item_ind, self.mergeable_ind
                , self.process_category, self.process_status
                ,
                self.sales_channel_id, self.order_no,)
        )
        if cursor:
            conn.commit()
            cursor.close()
        else:
            print("orders database table update failed!")
            cursor.close()


#   ************************************************************************************************************************************************************
#
#   ************************************************************************************************************************************************************
def existing_order(conn, sales_channel_id, order_no):
    cursor = conn.cursor()
    sql = '''
        SELECT
            orders.order_id
        FROM
            orders
        WHERE 
            orders.sales_channel_id =? AND
            orders.order_no         =?
        LIMIT 
            1
        '''
    cursor.execute(sql, (sales_channel_id, order_no,))
    row = cursor.fetchone()

    if row is not None:
        return (True)
    else:
        return (False)


def get_order(conn, sales_channel_id: str, order_no: str) -> NewOrder:
    #   ************************************************************************************************************************************************************
    #
    #   ************************************************************************************************************************************************************
    cursor = conn.cursor()
    sql = '''
        SELECT 
                order_id
            ,   sales_channel_id, order_no, order_type, dispatch_priority
            ,   sale_date, scheduled_dispatch_date, invoice_date, merge_date, production_date, packing_date, dispatched_date
            ,   number_of_items, number_of_production_items, currency_code, order_amt, delivery_amt, sales_tax_amt, delivery_discount_amt, order_subtotal_amt, order_refunded_amt, discount_amt, order_total_amt
            ,   buyer_user_id, buyer_first_name, buyer_last_name, buyer_full_name, buyer_repeat_ind
            ,   delivery_recipient, delivery_street_01, delivery_street_02, delivery_city, delivery_state, delivery_zipcode, delivery_country_code
            ,   delivery_carrier, delivery_carrier_order_ref, delivery_method, delivery_tracking_id
            ,   delivery_address_01, delivery_address_02, delivery_address_03, delivery_address_04, delivery_address_05
            ,   marked_as_gift, gift_message_included
            ,   payment_method, payment_type
            ,   private_notes, buyer_note, gift_message
            ,   card_processing_fee_amt, order_net_amt, adjusted_order_total_amt, adjusted_card_process_fee_amt, adjusted_net_order_amt
            ,   multi_item_ind, mergeable_ind
            ,   process_category, process_status
        FROM
            orders
        WHERE
            orders.sales_channel_id =? AND
            orders.order_no         =?
        LIMIT 
            1
        '''
    cursor.execute(sql, (sales_channel_id, order_no,))
    row = cursor.fetchone()

    if row is not None:
        db_order: NewOrder = NewOrder()

        db_order.order_id = row[0]
        db_order.sales_channel_id = row[1]
        db_order.order_no = row[2]
        db_order.order_type = row[3]
        db_order.dispatch_priority = row[4]

        db_order.sale_date = row[5]
        db_order.scheduled_dispatch_date = row[6]
        db_order.invoice_date = row[7]
        db_order.merge_date = row[8]
        db_order.production_date = row[9]
        db_order.packing_date = row[10]
        db_order.dispatched_date = row[11]

        db_order.number_of_items = row[12]
        db_order.number_of_production_items = row[13]
        db_order.currency_code = row[14]
        db_order.order_amt = row[15]
        db_order.delivery_amt = row[16]
        db_order.sales_tax_amt = row[17]
        db_order.delivery_discount_amt = row[18]
        db_order.order_subtotal_amt = row[19]
        db_order.order_refunded_amt = row[20]
        db_order.discount_amt = row[21]
        db_order.order_total_amt = row[22]

        db_order.buyer_user_id = row[23]
        db_order.buyer_first_name = row[24]
        db_order.buyer_last_name = row[25]
        db_order.buyer_full_name = row[26]
        db_order.buyer_repeat_ind = row[27]

        db_order.delivery_recipient = row[28]
        db_order.delivery_street_01 = row[29]
        db_order.delivery_street_02 = row[30]
        db_order.delivery_city = row[31]
        db_order.delivery_state = row[32]
        db_order.delivery_zipcode = row[33]
        db_order.delivery_country_code = row[34]

        db_order.delivery_carrier = row[35]
        db_order.delivery_carrier_order_ref = row[36]
        db_order.delivery_method = row[37]
        db_order.delivery_tracking_id = row[38]

        db_order.delivery_address_01 = row[39]
        db_order.delivery_address_02 = row[40]
        db_order.delivery_address_03 = row[41]
        db_order.delivery_address_04 = row[42]
        db_order.delivery_address_05 = row[43]

        db_order.marked_as_gift = row[44]
        db_order.gift_message_included = row[45]

        db_order.payment_method = row[46]
        db_order.payment_type = row[6]

        db_order.private_notes = row[48]
        db_order.buyer_note = row[49]
        db_order.gift_message = row[50]

        db_order.card_processing_fee_amt = row[51]
        db_order.order_net_amt = row[52]
        db_order.adjusted_order_total_amt = row[53]
        db_order.adjusted_card_process_fee_amt = row[54]
        db_order.adjusted_net_order_amt = row[55]

        db_order.multi_item_ind = row[56]
        db_order.mergeable_ind = row[57]

        db_order.process_category = row[58]
        db_order.process_status = row[59]

        cursor.close()
        return (db_order)
    else:
        cursor.close()
        return (None)


def get_orders(conn) -> list[NewOrder]:
    #   ************************************************************************************************************************************************************
    #
    #   ************************************************************************************************************************************************************
    cursor = conn.cursor()
    sql = '''
        SELECT
                order_id
            ,   sales_channel_id, order_no, order_type, dispatch_priority
            ,   sale_date, scheduled_dispatch_date, invoice_date, merge_date, production_date, packing_date, dispatched_date
            ,   number_of_items number_of_production_items, currency_code, order_amt, delivery_amt, sales_tax_amt, delivery_discount_amt, order_subtotal_amt, order_refunded_amt, discount_amt, order_total_amt
            ,   buyer_user_id, buyer_first_name, buyer_last_name, buyer_full_name, buyer_repeat_ind
            ,   delivery_recipient, delivery_street_01, delivery_street_02, delivery_city, delivery_state, delivery_zipcode, delivery_country_code
            ,   delivery_carrier, delivery_carrier_order_ref, delivery_method, delivery_tracking_id, delivery_carrier_barcode
            ,   delivery_address_01, delivery_address_02, delivery_address_03, delivery_address_04, delivery_address_05
            ,   marked_as_gift, gift_message_included
            ,   payment_method, payment_type
            ,   private_notes, buyer_note, gift_message
            ,   card_processing_fee_amt, order_net_amt, adjusted_order_total_amt, adjusted_card_process_fee_amt, adjusted_net_order_amt
            ,   multi_item_ind, mergeable_ind
            ,   process_category, process_status
        FROM
            orders
        '''
    cursor.execute(sql, )
    rows = cursor.fetchall()
    db_orders: list[NewOrder] = []

    if rows is not None:
        for row in rows:
            db_order: NewOrder = NewOrder()

            db_order.order_id = row[0]
            db_order.sales_channel_id = row[1]
            db_order.order_no = row[2]
            db_order.order_type = row[3]
            db_order.dispatch_priority = row[4]

            db_order.sale_date = row[5]
            db_order.scheduled_dispatch_date = row[6]
            db_order.invoice_date = row[7]
            db_order.merge_date = row[8]
            db_order.production_date = row[9]
            db_order.packing_date = row[10]
            db_order.dispatched_date = row[11]

            db_order.number_of_items = row[12]
            db_order.number_of_production_items = row[13]
            db_order.currency_code = row[14]
            db_order.order_amt = row[15]
            db_order.delivery_amt = row[16]
            db_order.sales_tax_amt = row[17]
            db_order.delivery_discount_amt = row[18]
            db_order.order_subtotal_amt = row[19]
            db_order.order_refunded_amt = row[20]
            db_order.discount_amt = row[21]
            db_order.order_total_amt = row[22]

            db_order.buyer_user_id = row[23]
            db_order.buyer_first_name = row[24]
            db_order.buyer_last_name = row[25]
            db_order.buyer_full_name = row[26]
            db_order.buyer_repeat_ind = row[27]

            db_order.delivery_recipient = row[28]
            db_order.delivery_street_01 = row[29]
            db_order.delivery_street_02 = row[30]
            db_order.delivery_city = row[31]
            db_order.delivery_state = row[32]
            db_order.delivery_zipcode = row[33]
            db_order.delivery_country_code = row[34]

            db_order.delivery_carrier = row[35]
            db_order.delivery_carrier_order_ref = row[36]
            db_order.delivery_method = row[37]
            db_order.delivery_tracking_id = row[38]

            db_order.delivery_address_01 = row[39]
            db_order.delivery_address_02 = row[40]
            db_order.delivery_address_03 = row[41]
            db_order.delivery_address_04 = row[42]
            db_order.delivery_address_05 = row[43]

            db_order.marked_as_gift = row[44]
            db_order.gift_message_included = row[45]

            db_order.payment_method = row[46]
            db_order.payment_type = row[6]

            db_order.private_notes = row[48]
            db_order.buyer_note = row[49]
            db_order.gift_message = row[50]

            db_order.card_processing_fee_amt = row[51]
            db_order.order_net_amt = row[52]
            db_order.adjusted_order_total_amt = row[53]
            db_order.adjusted_card_process_fee_amt = row[54]
            db_order.adjusted_net_order_amt = row[55]

            db_order.multi_item_ind = row[56]
            db_order.mergeable_ind = row[57]

            db_order.process_category = row[58]
            db_order.process_status = row[59]

            db_orders.append(db_order)
        cursor.close()
        return (db_orders)
    else:
        cursor.close()
        return (None)


def get_orders_by_status(conn, process_status: int) -> list[NewOrder]:
    #   ************************************************************************************************************************************************************
    #
    #   ************************************************************************************************************************************************************
    cursor = conn.cursor()
    sql = '''
        SELECT
                order_id
            ,   sales_channel_id, order_no, order_type, dispatch_priority
            ,   sale_date, scheduled_dispatch_date, invoice_date, merge_date, production_date, packing_date, dispatched_date
            ,   number_of_items, number_of_production_items, currency_code, order_amt, delivery_amt, sales_tax_amt, delivery_discount_amt, order_subtotal_amt, order_refunded_amt, discount_amt, order_total_amt
            ,   buyer_user_id, buyer_first_name, buyer_last_name, buyer_full_name, buyer_repeat_ind
            ,   delivery_recipient, delivery_street_01, delivery_street_02, delivery_city, delivery_state, delivery_zipcode, delivery_country_code
            ,   delivery_carrier, delivery_carrier_order_ref, delivery_method, delivery_tracking_id
            ,   delivery_address_01, delivery_address_02, delivery_address_03, delivery_address_04, delivery_address_05
            ,   marked_as_gift, gift_message_included
            ,   payment_method, payment_type
            ,   private_notes, buyer_note, gift_message
            ,   card_processing_fee_amt, order_net_amt, adjusted_order_total_amt, adjusted_card_process_fee_amt, adjusted_net_order_amt
            ,   multi_item_ind, mergeable_ind
            ,   process_category, process_status
        FROM
            orders
        WHERE
            orders.process_status = ?
        '''
    cursor.execute(sql, (process_status,))
    rows = cursor.fetchall()
    db_orders: list[NewOrder] = []

    if rows is not None:
        for row in rows:
            db_order: NewOrder = NewOrder()

            db_order.order_id = row[0]
            db_order.sales_channel_id = row[1]
            db_order.order_no = row[2]
            db_order.order_type = row[3]
            db_order.dispatch_priority = row[4]

            db_order.sale_date = row[5]
            db_order.scheduled_dispatch_date = row[6]
            db_order.invoice_date = row[7]
            db_order.merge_date = row[8]
            db_order.production_date = row[9]
            db_order.packing_date = row[10]
            db_order.dispatched_date = row[11]

            db_order.number_of_items = row[12]
            db_order.number_of_production_items = row[13]
            db_order.currency_code = row[14]
            db_order.order_amt = row[15]
            db_order.delivery_amt = row[16]
            db_order.sales_tax_amt = row[17]
            db_order.delivery_discount_amt = row[18]
            db_order.order_subtotal_amt = row[19]
            db_order.order_refunded_amt = row[20]
            db_order.discount_amt = row[21]
            db_order.order_total_amt = row[22]

            db_order.buyer_user_id = row[23]
            db_order.buyer_first_name = row[24]
            db_order.buyer_last_name = row[25]
            db_order.buyer_full_name = row[26]
            db_order.buyer_repeat_ind = row[27]

            db_order.delivery_recipient = row[28]
            db_order.delivery_street_01 = row[29]
            db_order.delivery_street_02 = row[30]
            db_order.delivery_city = row[31]
            db_order.delivery_state = row[32]
            db_order.delivery_zipcode = row[33]
            db_order.delivery_country_code = row[34]

            db_order.delivery_carrier = row[35]
            db_order.delivery_carrier_order_ref = row[36]
            db_order.delivery_method = row[37]
            db_order.delivery_tracking_id = row[38]

            db_order.delivery_address_01 = row[39]
            db_order.delivery_address_02 = row[40]
            db_order.delivery_address_03 = row[41]
            db_order.delivery_address_04 = row[42]
            db_order.delivery_address_05 = row[43]

            db_order.marked_as_gift = row[44]
            db_order.gift_message_included = row[45]

            db_order.payment_method = row[46]
            db_order.payment_type = row[6]

            db_order.private_notes = row[48]
            db_order.buyer_note = row[49]
            db_order.gift_message = row[50]

            db_order.card_processing_fee_amt = row[51]
            db_order.order_net_amt = row[52]
            db_order.adjusted_order_total_amt = row[53]
            db_order.adjusted_card_process_fee_amt = row[54]
            db_order.adjusted_net_order_amt = row[55]

            db_order.multi_item_ind = row[56]
            db_order.mergeable_ind = row[57]

            db_order.process_category = row[58]
            db_order.process_status = row[59]

            db_orders.append(db_order)
        cursor.close()
        return (db_orders)
    else:
        cursor.close()
        return (None)


def get_orders_by_status_category(conn, process_status: int, process_category: int) -> list[NewOrder]:
    #   ************************************************************************************************************************************************************
    #
    #   ************************************************************************************************************************************************************
    cursor = conn.cursor()
    sql = '''
        SELECT
                order_id
            ,   sales_channel_id, order_no, order_type, dispatch_priority
            ,   sale_date, scheduled_dispatch_date, invoice_date, merge_date, production_date, packing_date, dispatched_date
            ,   number_of_items, number_of_production_items, currency_code, order_amt, delivery_amt, sales_tax_amt, delivery_discount_amt, order_subtotal_amt, order_refunded_amt, discount_amt, order_total_amt
            ,   buyer_user_id, buyer_first_name, buyer_last_name, buyer_full_name, buyer_repeat_ind
            ,   delivery_recipient, delivery_street_01, delivery_street_02, delivery_city, delivery_state, delivery_zipcode, delivery_country_code
            ,   delivery_carrier, delivery_carrier_order_ref, delivery_method, delivery_tracking_id
            ,   delivery_address_01, delivery_address_02, delivery_address_03, delivery_address_04, delivery_address_05
            ,   marked_as_gift, gift_message_included
            ,   payment_method, payment_type
            ,   private_notes, buyer_note, gift_message
            ,   card_processing_fee_amt, order_net_amt, adjusted_order_total_amt, adjusted_card_process_fee_amt, adjusted_net_order_amt
            ,   multi_item_ind, mergeable_ind
            ,   process_category, process_status
        FROM
            orders
        WHERE
            orders.process_status   = ? AND
            orders.process_category = ?
        '''
    cursor.execute(sql, (process_status, process_category))
    rows = cursor.fetchall()
    db_orders: list[NewOrder] = []

    if rows is not None:
        for row in rows:
            db_order: NewOrder = NewOrder()

            db_order.order_id = row[0]
            db_order.sales_channel_id = row[1]
            db_order.order_no = row[2]
            db_order.order_type = row[3]
            db_order.dispatch_priority = row[4]

            db_order.sale_date = row[5]
            db_order.scheduled_dispatch_date = row[6]
            db_order.invoice_date = row[7]
            db_order.merge_date = row[8]
            db_order.production_date = row[9]
            db_order.packing_date = row[10]
            db_order.dispatched_date = row[11]

            db_order.number_of_items = row[12]
            db_order.number_of_production_items = row[13]
            db_order.currency_code = row[14]
            db_order.order_amt = row[15]
            db_order.delivery_amt = row[16]
            db_order.sales_tax_amt = row[17]
            db_order.delivery_discount_amt = row[18]
            db_order.order_subtotal_amt = row[19]
            db_order.order_refunded_amt = row[20]
            db_order.discount_amt = row[21]
            db_order.order_total_amt = row[22]

            db_order.buyer_user_id = row[23]
            db_order.buyer_first_name = row[24]
            db_order.buyer_last_name = row[25]
            db_order.buyer_full_name = row[26]
            db_order.buyer_repeat_ind = row[27]

            db_order.delivery_recipient = row[28]
            db_order.delivery_street_01 = row[29]
            db_order.delivery_street_02 = row[30]
            db_order.delivery_city = row[31]
            db_order.delivery_state = row[32]
            db_order.delivery_zipcode = row[33]
            db_order.delivery_country_code = row[34]

            db_order.delivery_carrier = row[35]
            db_order.delivery_carrier_order_ref = row[36]
            db_order.delivery_method = row[37]
            db_order.delivery_tracking_id = row[38]

            db_order.delivery_address_01 = row[39]
            db_order.delivery_address_02 = row[40]
            db_order.delivery_address_03 = row[41]
            db_order.delivery_address_04 = row[42]
            db_order.delivery_address_05 = row[43]

            db_order.marked_as_gift = row[44]
            db_order.gift_message_included = row[45]

            db_order.payment_method = row[46]
            db_order.payment_type = row[6]

            db_order.private_notes = row[48]
            db_order.buyer_note = row[49]
            db_order.gift_message = row[50]

            db_order.card_processing_fee_amt = row[51]
            db_order.order_net_amt = row[52]
            db_order.adjusted_order_total_amt = row[53]
            db_order.adjusted_card_process_fee_amt = row[54]
            db_order.adjusted_net_order_amt = row[55]

            db_order.multi_item_ind = row[56]
            db_order.mergeable_ind = row[57]

            db_order.process_category = row[58]
            db_order.process_status = row[59]

            db_orders.append(db_order)
        cursor.close()
        return (db_orders)
    else:
        cursor.close()
        return (None)


def iso_YYYYMMDD(in_date):
    # ************************************************************************************************************************************************************
    # FUNCTION: Return ISO formatted date from MM/DD/YY, MM/DD/YYYY, null or blank date field
    # ************************************************************************************************************************************************************
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
