import os
import shutil
import re
import sys
import logging
import sqlite3

from pathlib import Path

from system_settings import *
from custom_logger import *
from sales_channel import *
from new_order import *

from datetime import datetime

from pypdf import PdfReader, PdfWriter

import copy
import math


def get_current_date() -> str:
    #   ** ************************************************************************************************************************************************************
    #   **
    #   ** ************************************************************************************************************************************************************
    current_date_YYYYMMDD: datetime = datetime.now()
    current_year: str = current_date_YYYYMMDD.strftime("%Y")
    current_month: str = current_date_YYYYMMDD.strftime("%m")
    current_day: str = current_date_YYYYMMDD.strftime("%d")
    current_date: str = rf'{current_year}{current_month}{current_day}'

    return (current_date)


def create_connection(db_file):
    # ************************************************************************************************************************************************************
    # create and return a database connection object
    # ************************************************************************************************************************************************************
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e_conn:
        logger.error(rf'DATABASE CONNECTION ERROR: {e_conn}, {sys.exc_info()[0]}')

    return conn


def prep_invoices(p_invoice_path_in: str, p_invoice_path_out: str, p_message_path_out: str) -> list[int]:
    #   ** ************************************************************************************************************************************************************
    #   **
    #   ** ************************************************************************************************************************************************************
    page_count: int = 0
    invoice_count: int = 0
    message_count: int = 0

    try:
        invoice_writer: PdfWriter = PdfWriter()
        message_writer: PdfWriter = PdfWriter()

        #
        #        Deletion of directories re-located to SYSTEM_RESET function
        #
        #        shutil.rmtree (p_invoice_path_out) if os.path.exists(p_invoice_path_out) else None
        #        shutil.rmtree (p_message_path_out) if os.path.exists(p_message_path_out) else None

        #        os.mkdir (p_invoice_path_out)
        #        os.mkdir (p_message_path_out)

        for file_name in os.listdir(p_invoice_path_in):

            if file_name.endswith(".pdf"):
                invoice_page: bool = False

                full_file_name: str = os.path.join(p_invoice_path_in, file_name)
                invoice_reader: PdfReader = PdfReader(full_file_name)

                for page in invoice_reader.pages:
                    page_count = page_count + 1

                    if page_count % 10 == 0:
                        logger.info(rf'FILE: {file_name}, PAGE: {page_count} LOADING...')
                    else:
                        pass

                    if page.extract_text().find("Your go-to for meaningful gifts") > 0:
                        message_count = message_count + 1
                        message_writer.add_page(page)
                    else:
                        if page.extract_text().find("Shop\n") > 0:
                            invoice_count = invoice_count + 1
                            invoice_page: bool = True
                            invoice_writer.add_page(page)
                        else:
                            if invoice_page == True:
                                invoice_writer.add_page(page)
                            else:
                                pass

                os.remove(full_file_name)
            else:
                pass

        #       end - for file_name in os.listdir(p_invoice_path_in)

        invoice_file_name: str = os.path.join(p_invoice_path_out, "INVOICES.pdf")
        message_file_name: str = os.path.join(p_message_path_out, "GIFT_MESSAGES.pdf")

        if invoice_count > 0:
            with open(invoice_file_name, "wb") as invoice_file:
                invoice_writer.write(invoice_file_name)
        else:
            pass

        if message_count > 0:
            with open(message_file_name, "wb") as message_file:
                message_writer.write(message_file_name)
        else:
            pass

        return (invoice_count, message_count)

    except:
        return (invoice_count, message_count)


def split_invoices(p_in_file_name: str, p_path_out: str) -> bool:
    #   ** ************************************************************************************************************************************************************
    #   **
    #   ** ************************************************************************************************************************************************************
    database: str = sys_settings.database_path

    conn = create_connection(database)

    cursor = conn.cursor()
    cursor.execute('''PRAGMA foreign_keys = ON''')
    cursor.close()

    invoice_reader: PdfReader = PdfReader(p_in_file_name)
    invoice_writer: PdfWriter = PdfWriter()

    out_file_name: str = None
    invoice_count: int = 0

    sales_channel: SalesChannel = None
    shop_name: str = None
    order_no: str = None

    for page in invoice_reader.pages:
        lines: list = page.extract_text().split('\n')

        pattern: str = rf'^Order #(.+)$'
        pattern_match = re.search(pattern, lines[0], flags=re.I)

        if pattern_match:
            order_no = pattern_match.group(1).strip()

            shop_name_index: int = [index for (index, item) in enumerate(lines) if item == "Shop"]
            shop_name = lines[shop_name_index[0] + 1]
            sales_channel = SalesChannel(shop_name)

            invoice_writer: PdfWriter = PdfWriter()

        pattern: str = rf'Order total(.+)'
        pattern_match = re.search(pattern, page.extract_text(), flags=re.I)

        if pattern_match:

            if existing_order(conn, sales_channel.id, order_no):
                out_file_name = os.path.join(p_path_out, rf'{sales_channel.id}_{order_no}.pdf')
                logger.warning(f'FILE: {out_file_name}, ORDER: {sales_channel.id}-{order_no} ALREADY SPLIT...')
            else:
                invoice_count = invoice_count + 1

                invoice_writer.add_page(page)
                out_file_name = os.path.join(p_path_out, rf'{sales_channel.id}_{order_no}.pdf')

                with open(out_file_name, "wb") as invoice_file:
                    invoice_writer.write(out_file_name)

                db_order: NewOrder = NewOrder()
                db_order.sales_channel_id = sales_channel.id
                db_order.order_no = order_no
                db_order.save(conn)

                logger.info(
                    f'{str(invoice_count).zfill(4)}, FILE: {out_file_name}, ORDER: {sales_channel.id}-{order_no} SAVING...')
        else:
            invoice_writer.add_page(page)

    #   end - with conn:

    return (True)


def alt_split_messages(p_in_file_name: str, p_path_out: str) -> bool:
    #   ** ************************************************************************************************************************************************************
    #   **
    #   ** ************************************************************************************************************************************************************
    message_reader: PdfReader = PdfReader(p_in_file_name)
    message_writer: PdfWriter = PdfWriter()

    out_file_name: str = None
    message_count: int = 0

    sales_channel_name: str = None
    order_no: str = None

    for page in message_reader.pages:
        pattern: str = rf'([\w]+)\n'
        pattern_match = re.search(pattern, page.extract_text(), flags=re.I)

        if pattern_match:
            sales_channel_name = pattern_match.group(1).strip()
            sales_channel = SalesChannel(sales_channel_name)

            pattern: str = rf'([0-9]{10})$'
            pattern_match = re.findall(pattern, page.extract_text())

            if pattern_match:
                name_count = 0

                obj_NewPage = copy.copy(page)
                obj_NewPage.mediabox = copy.copy(page.mediabox)

                #                           612 x 792 Postscript Points - 8.5 x 11 inches - 850 * 1100 aspect ratio
                x_LL, y_LL = 0, 0
                x_UR, y_UR = 612, 792

                #                            x_LL, y_LL = page.mediabox.lower_left
                #                            x_UR, y_UR = page.mediabox.upper_right

                x_LL = math.floor(x_LL)
                y_LL = math.floor(y_LL)
                x_UR = math.floor(x_UR)
                y_UR = math.floor(y_UR)

                y_MR = math.floor(y_UR / 2)

                #                            page.mediabox.upper_right = (x3, x4)
                #                            page.mediabox.lower_left = (x1, x6)

                #                            obj_NewPage.mediabox.upper_right = (x3, x6)
                #                            obj_NewPage.mediabox.lower_left = (x1, x2)

                for order_no in pattern_match:
                    logger.debug(rf'SPLITTING GIFT RECEIPT: Sales Channel: {sales_channel.id}, Order No: {order_no}')

                    name_count = name_count + 1
                    out_file_name: str = os.path.join(p_path_out, rf'{sales_channel.id}_{order_no}.pdf')
                    pdf_InvoiceWriter = PdfWriter()

                    if name_count == 1:
                        if len(pattern_match) > 1:
                            page.mediabox.upper_right = (x_UR, y_UR)
                            page.mediabox.lower_left = (x_LL, y_MR)
                            pdf_InvoiceWriter.add_page(page)
                        else:
                            page.mediabox.upper_right = (x_UR, y_UR)
                            page.mediabox.lower_left = (x_LL, y_LL)
                            pdf_InvoiceWriter.add_page(page)
                    else:
                        obj_NewPage.mediabox.upper_right = (x_UR, y_MR)
                        obj_NewPage.mediabox.lower_left = (x_LL, y_LL)
                        pdf_InvoiceWriter.add_page(obj_NewPage)

                    with open(out_file_name, "wb") as file_Invoice:
                        pdf_InvoiceWriter.write(file_Invoice)
                        int_InvoiceCount = int_InvoiceCount + 1

            # ==============================================================
            #                            if len(s_pattern_match) > 1:
            #                                obj_NewPage = copy.copy(page)
            #                                obj_NewPage.mediabox = copy.copy(page.mediabox)

            #                                x1, x2 = page.mediabox.lower_left
            #                                x3, x4 = page.mediabox.upper_right

            #                                x1, x2 = math.floor(x1), math.floor(x2)
            #                                x3, x4 = math.floor(x3), math.floor(x4)
            #                                x5, x6 = math.floor(x3/2), math.floor(x4/2)

            #                                page.mediabox.upper_right = (x3, x4)
            #                                page.mediabox.lower_left = (x1, x6)

            #                                obj_NewPage.mediabox.upper_right = (x3, x6)
            #                                obj_NewPage.mediabox.lower_left = (x1, x2)

            #                                for str_OrderNo in s_pattern_match:
            #                                    int_NameCount = int_NameCount + 1

            #                                    fname_GiftReceipt_OUT   = os.path.join(path_GiftReceipt_OUT, f'''{str_SalesChannel}_{str_OrderNo}.pdf''').replace("\\","/")
            #                                    print(f'''SPLITTING DOUBLE GIFT RECEIPT: Sales Channel: {str_SalesChannel}, Order No: {str_OrderNo}''')

            #                                    pdf_InvoiceWriter   = PdfWriter()
            #                                    if int_NameCount == 1:
            #                                        pdf_InvoiceWriter.add_page(page)
            #                                    else:
            #                                        pdf_InvoiceWriter.add_page(obj_NewPage)

            #                                    with open(fname_GiftReceipt_OUT, "wb") as file_Invoice:
            #                                        pdf_InvoiceWriter.write(file_Invoice)
            #                                        int_InvoiceCount = int_InvoiceCount + 1
            #                            else:
            #                                str_OrderNo             = s_pattern_match[0]
            #                                fname_GiftReceipt_OUT   = os.path.join(path_GiftReceipt_OUT, f'''{str_SalesChannel}_{str_OrderNo}.pdf''').replace("\\","/")
            #                                print(f'''SPLITTING SINGLE GIFT RECEIPT: Sales Channel: {str_SalesChannel}, Order No: {str_OrderNo}''')

            #                                pdf_InvoiceWriter = PdfWriter()

            #                                x1, x2 = page.mediabox.lower_left
            #                                x3, x4 = page.mediabox.upper_right

            #                                x1, x2 = math.floor(x1), math.floor(x2)
            #                                x3, x4 = math.floor(x3), math.floor(x4)
            #                                x5, x6 = math.floor(x3/2), math.floor(x4/2)

            #                                page.mediabox.upper_right = (x3, x4)
            #                                page.mediabox.lower_left = (x1, x2)

            #                                pdf_InvoiceWriter.add_page(page)

            #                                with open(fname_GiftReceipt_OUT, "wb") as file_Invoice:
            #                                    pdf_InvoiceWriter.write(file_Invoice)
            #                                    int_InvoiceCount = int_InvoiceCount + 1

            else:
                #                            print(f'''ERROR: Matching Gift Receipt Not Found - Sales Channel: {str_SalesChannel}, Order:: 'UNKNOWN''')
                pass
        else:
            pass

    #   end - for page in pdf_InputReader.pages:

    return (True)


def split_messages(p_in_file_name: str, p_path_out: str) -> bool:
    #   ** ************************************************************************************************************************************************************
    #   **
    #   ** ************************************************************************************************************************************************************
    message_reader: PdfReader = PdfReader(p_in_file_name)
    message_writer: PdfWriter = PdfWriter()

    out_file_name: str = None
    message_count: int = 0

    sales_channel_name: str = None
    order_no: str = None

    for page in message_reader.pages:
        pattern: str = rf'([\w]+)\n'
        pattern_match = re.search(pattern, page.extract_text(), flags=re.I)

        if pattern_match:
            sales_channel_name = pattern_match.group(1).strip()
            sales_channel = SalesChannel(sales_channel_name)

            pattern = r'([0-9]{10})\n'
            pattern_match = re.findall(pattern, page.extract_text())

            if pattern_match:
                order_count: int = 0

                new_page = copy.copy(page)
                new_page.mediabox = copy.copy(page.mediabox)

                #               612 x 792 Postscript Points - 8.5 x 11 inches - 850 * 1100 aspect ratio
                x_LL, y_LL = 0, 0
                x_UR, y_UR = 612, 792

                x_LL = math.floor(x_LL)
                y_LL = math.floor(y_LL)
                x_UR = math.floor(x_UR)
                y_UR = math.floor(y_UR)

                y_MR = math.floor(y_UR / 2)

                for order_no in pattern_match:
                    order_count = order_count + 1
                    out_file_name = os.path.join(p_path_out, rf'{sales_channel.id}_{order_no}.pdf')
                    message_writer: PdfWriter = PdfWriter()

                    if order_count == 1:
                        if len(pattern_match) > 1:
                            page.mediabox.upper_right = (x_UR, y_UR)
                            page.mediabox.lower_left = (x_LL, y_MR)
                            message_writer.add_page(page)
                        else:
                            page.mediabox.upper_right = (x_UR, y_UR)
                            page.mediabox.lower_left = (x_LL, y_LL)
                            message_writer.add_page(page)
                    else:
                        new_page.mediabox.upper_right = (x_UR, y_MR)
                        new_page.mediabox.lower_left = (x_LL, y_LL)
                        message_writer.add_page(new_page)

                    logger.debug(rf'FILE: {out_file_name}, MESSAGE: {sales_channel.id}-{order_no} SAVING...')

                    with open(out_file_name, "wb") as message_file:
                        message_writer.write(message_file)
                        message_count = message_count + 1
            else:
                pass
        else:
            pass

    #   end - for page in pdf_InputReader.pages:

    return (True)


if __name__ == '__main__':
    #   ** ************************************************************************************************************************************************************
    #   ** Mainline code
    #   ** ************************************************************************************************************************************************************
    success: bool = False
    invoice_message_count: list[int] = [0, 0]

    sys_settings: SystemSettings = SystemSettings()

    logger: logging.Logger = get_custom_logger('INVOICE SPLIT')

    invoice_path_in: str = rf'{sys_settings.etsy_source_invoice_path}'
    invoice_path_out: str = os.path.join(sys_settings.etsy_target_invoice_path, sys_settings.process_date)
    message_path_out: str = os.path.join(sys_settings.etsy_target_gift_receipt_path, sys_settings.process_date)

    invoice_message_count = prep_invoices(invoice_path_in, invoice_path_out, message_path_out)

    if invoice_message_count[0] > 0:
        invoice_file_name: str = os.path.join(sys_settings.etsy_target_invoice_path, sys_settings.process_date,
                                              "INVOICES.pdf")
        success = split_invoices(invoice_file_name, invoice_path_out) if os.path.isfile(invoice_file_name) else False

        if success == True:
            if invoice_message_count[0] > 1:
                logger.info(rf'{invoice_message_count[0]} Invoices Split')
            else:
                logger.info(rf'{invoice_message_count[0]} Invoice Split')

            os.remove(invoice_file_name)
        else:
            logger.error(rf'Invoice Split Failed')
    else:
        logger.warning(rf'No Invoices To Split')

    if invoice_message_count[1] > 0:
        message_file_name: str = os.path.join(sys_settings.etsy_target_gift_receipt_path, sys_settings.process_date,
                                              "GIFT_MESSAGES.pdf")
        success = split_messages(message_file_name, message_path_out) if os.path.isfile(message_file_name) else False

        if success == True:
            if invoice_message_count[1] > 1:
                logger.info(rf'{invoice_message_count[1]} Messages Split')
            else:
                logger.info(rf'{invoice_message_count[1]} Message Split')

            os.remove(message_file_name)
        else:
            logger.error(rf'Message Split Failed')
    else:
        logger.warning(rf'No Messages To Split')
