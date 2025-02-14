import os
import shutil
import re
import sys
import requests
import json
import logging

import sqlite3

from pathlib import Path

from system_settings import *
from custom_logger import *
from sales_channel import *
from country import *
from country_code import *
from currency import *
from new_order import *
from new_order_item import *
from sku_substitution import *
from product_design_listing import *
from US_post_spreadsheet import *
from US_post import *

from datetime import datetime
from datetime import date
import time
import dateutil.parser

from pypdf import PdfReader, PdfWriter

import pdfreader
import pdfreader

from pdfreader import PDFDocument, SimplePDFViewer

from reportlab.pdfgen import canvas
from reportlab.lib.colors import red, black, blue, green, yellow, purple, pink, brown, orange, magenta, cyan, white
from reportlab.graphics.barcode import eanbc, qr, usps
from reportlab.graphics.shapes import Drawing
from reportlab.lib.pagesizes import A4
from reportlab.graphics import renderPDF
from reportlab.graphics.barcode import code128
from reportlab.lib.units import cm, mm, inch

import copy
import math

import subprocess
import os

MERGE_DIR = os.path.dirname(__file__)


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


def get_date(p_Date, p_CountryCode='GB'):
    #   ** **********************************************************************************************************************************************************
    #   ** Extract Date
    #   ** **********************************************************************************************************************************************************
    dte_Date = None
    str_Date = None

    if p_CountryCode == 'US':
        try:
            dte_Date = dateutil.parser.parse(p_Date, fuzzy=True, dayfirst=False)

            if dte_Date is None:
                dte_Date = dateutil.parser.parse(p_Date, fuzzy=True, dayfirst=True)
            else:
                pass
        except ValueError:
            try:
                dte_Date = dateutil.parser.parse(p_Date[4:8] + p_Date[0:2] + p_Date[2:4])
            except ValueError:
                try:
                    dte_Date = dateutil.parser.parse(p_Date[4:8] + p_Date[2:4] + p_Date[0:2])
                except ValueError:
                    pass
    else:
        try:
            dte_Date = dateutil.parser.parse(p_Date, fuzzy=True, dayfirst=True)
        except ValueError:
            try:
                dte_Date = dateutil.parser.parse(p_Date[4:8] + p_Date[2:4] + p_Date[0:2])
            except ValueError:
                try:
                    dte_Date = dateutil.parser.parse(p_Date[4:8] + p_Date[2:4] + p_Date[0:2])
                except ValueError:
                    pass

    return (dte_Date)


def get_carrier_order_ref(p_OrderNo):
    # ---------------------------------------------------------------------------------------------------------------------------------------------------------
    # Use Click and Drop API to obtain Royal Mail order reference
    #
    #    url = "https://api.parcel.royalmail.com/api/v1/orders/%222801081486%22/"
    url = f'''https://api.parcel.royalmail.com/api/v1/orders/%22{p_OrderNo}%22/'''

    payload = ""
    headers = {
        "Authorization": "85561871-28bc-4947-98ac-ca5f3ad92f22",
        "Content-Type": "application/json"
    }

    response = requests.request("GET", url, data=payload, headers=headers)

    if response.ok:
        response_dict = json.loads(response.text)
        return response_dict[0]["orderIdentifier"]
    else:
        return ("ERROR")


def add_invoice_annotations(p_invoice_path_in, p_message_path_in, p_combined_path_out, p_annotation_colour):
    #   ** ************************************************************************************************************************************************************
    #   **
    #   ** ************************************************************************************************************************************************************
    invoice_file_name: str = os.path.join(p_invoice_path_in, rf'{db_order.sales_channel_id}_{db_order.order_no}.pdf')
    message_file_name: str = os.path.join(p_message_path_in, rf'{db_order.sales_channel_id}_{db_order.order_no}.pdf')
    combined_file_name: str = os.path.join(p_combined_path_out, rf'{db_order.sales_channel_id}_{db_order.order_no}.pdf')

    os.mkdir(p_combined_path_out) if not os.path.exists(p_combined_path_out) else None

    #   612 x 792 Postscript Points - 8.5 x 11 inches - 850 * 1100 aspect ratio

    annotation_file_name: str = os.path.join(p_invoice_path_in,
                                             rf'{db_order.sales_channel_id}_{db_order.order_no}_TMP.pdf''')
    working_canvas: canvas.Canvas = canvas.Canvas(annotation_file_name, pagesize=A4)

    #    if db_order.delivery_country_code == 'US':
    #        int_BarHeight = 1.3*cm
    #        int_BarWidth  = .025*cm #.025 - .1
    #        int_XPosition = 442
    #        int_YPosition = 716

    #        barcode = code128.Code128(db_order.delivery_carrier_order_ref, barHeight=int_BarHeight, barWidth=int_BarWidth)
    #        barcode.drawOn(working_canvas, int_XPosition, int_YPosition)
    #    else:
    #        int_BarHeight = 1.3*cm
    #        int_BarWidth  = .05*cm #.025 - .1
    ##        int_XPosition = 462
    #        int_XPosition = 442
    #        int_YPosition = 716

    #        barcode = code128.Code128(db_order.delivery_carrier_order_ref, barHeight=int_BarHeight, barWidth=int_BarWidth)
    #        barcode.drawOn(working_canvas, int_XPosition, int_YPosition)

    int_BarHeight = 1.3 * cm
    int_BarWidth = .05 * cm  # .025 - .1
    int_XPosition = 442
    int_YPosition = 716

    barcode = code128.Code128(db_order.delivery_carrier_order_ref, barHeight=int_BarHeight, barWidth=int_BarWidth)
    barcode.drawOn(working_canvas, int_XPosition, int_YPosition)

    str_MultiItemOrder = 'M' if db_order.multi_item_ind == 'Y' else ''

    working_canvas.setFillColor(p_annotation_colour)
    working_canvas.setFont('Helvetica-Bold', 52)
    #    obj_Canvas.drawCentredString((612 / 2) + 45, 716, f'''{p_Order.delivery_country_code} x{p_Order.number_of_items} {str_MultiItemOrder}''')
    working_canvas.drawCentredString((612 / 2) + 15, 716,
                                     rf'{db_order.delivery_country_code} x{db_order.number_of_items} {str_MultiItemOrder}')

    working_canvas.save()

    with open(invoice_file_name, "rb") as invoice_file, open(annotation_file_name, "rb") as annotation_file:
        invoice_reader = PdfReader(invoice_file)
        annotation_reader = PdfReader(annotation_file)

        background = invoice_reader.pages[0]
        foreground = annotation_reader.pages[0]

        background.merge_page(foreground)

        combined_writer: PdfWriter = PdfWriter()

        for new_page in invoice_reader.pages:
            combined_writer.add_page(new_page)

        if db_order.marked_as_gift == 'Y':  # and p_Order.gift_message_included == 'Y':
            message_reader = PdfReader(message_file_name)
            combined_writer.add_page(message_reader.pages[0])

        with open(combined_file_name, "wb") as combined_file:
            combined_writer.write(combined_file)

    invoice_file.close()
    annotation_file.close()
    combined_file.close()

    os.remove(annotation_file_name)

    if db_order.marked_as_gift == 'Y':  # and p_Order.gift_message_included == 'Y':
        os.remove(message_file_name)
    else:
        pass

    return (True)


def get_order_no() -> bool:
    #   ** **********************************************************************************************************************************************************
    #   **
    #   ** **********************************************************************************************************************************************************
    try:
        pattern: str = rf'^Order #(.+)$'
        pattern_match = re.search(pattern, invoice_lines[0], flags=re.I)

        db_order.order_no = pattern_match.group(1).strip() if pattern_match else None
        invoice_lines.pop(0)

        logger.debug(rf'ORDER NO: {db_order.order_no}')

        return (True)

    except:
        logger.error(rf'ORDER NO PARSE ERROR: {sys.exc_info()[0]}')
        return (False)


def get_buyer_details():
    #   ** **********************************************************************************************************************************************************
    #   **
    #   ** **********************************************************************************************************************************************************
    try:
        pattern = rf'^(.+)[\s](.?)[\(](.+)[\)][\s]?(★)?$'
        pattern_match = re.search(pattern, invoice_lines[0], flags=re.I)

        invoice_lines.pop(0)

        db_order.buyer_first_name = pattern_match.group(1).strip() if pattern_match.group(1) else ''
        db_order.buyer_last_name = pattern_match.group(2).strip() if pattern_match.group(2) else ''
        db_order.buyer_user_id = pattern_match.group(3).strip() if pattern_match.group(3) else ''
        db_order.buyer_repeat_ind = 'Y' if pattern_match.group(4) else 'N'

        db_order.buyer_full_name = rf'{db_order.buyer_first_name} {db_order.buyer_last_name}' if db_order.buyer_last_name != '' else db_order.buyer_first_name

        logger.debug(
            rf'BUYER DETAILS: {db_order.buyer_first_name} {db_order.buyer_last_name} ({db_order.buyer_user_id}) REPEAT BUYER: {db_order.buyer_repeat_ind}')

    except:
        logger.error(rf'BUYER DETAILS PARSE ERROR: {sys.exc_info()[0]}')


def get_marked_as_gift():
    #   ** **********************************************************************************************************************************************************
    #   **
    #   ** **********************************************************************************************************************************************************
    try:
        pattern: str = rf'^(MARKED AS GIFT)$'
        pattern_match = re.search(pattern, invoice_lines[0], flags=re.I)

        if pattern_match:
            invoice_lines.pop(0)
            db_order.marked_as_gift = 'Y'
        else:
            db_order.marked_as_gift = 'N'

        logger.debug(rf'MARKED AS GIFT: {db_order.marked_as_gift}')

    except:
        logger.error(rf'MARKED AS GIFT PARSE ERROR: {sys.exc_info()[0]}')


def get_gift_message_included():
    #   ** **********************************************************************************************************************************************************
    #   **
    #   ** **********************************************************************************************************************************************************
    try:
        pattern: str = rf'^(GIFT MESSAGE INCLUDED)$'
        pattern_match = re.search(pattern, invoice_lines[0], flags=re.I)

        if pattern_match:
            invoice_lines.pop(0)
            db_order.gift_message_included = 'Y'
        else:
            db_order.gift_message_included = 'N'

        logger.debug(rf'GIFT MESSAGE INCLUDED: {db_order.gift_message_included}')

    except:
        logger.error(rf'GIFT MESSAGE INCLUDED PARSE ERROR: {sys.exc_info()[0]}')


def get_delivery_recipient():
    #   ** **********************************************************************************************************************************************************
    #   ** extract delivery_recipient from pdf
    #   ** **********************************************************************************************************************************************************
    try:
        pattern: str = rf'^(DELIVER TO|SHIP TO)$'
        pattern_match = re.search(pattern, invoice_lines[0], flags=re.I)

        if pattern_match:
            invoice_lines.pop(0)

            pattern: str = rf'^(.+)$'
            pattern_match = re.search(pattern, invoice_lines[0], flags=re.I)

            if pattern_match:
                invoice_lines.pop(0)
                db_order.delivery_recipient = pattern_match.group(1).strip()

                if len(db_order.delivery_recipient) == 20:
                    pattern: str = r'^([\D]+)$'
                    pattern_match = re.search(pattern, invoice_lines[0], flags=re.I)

                    if pattern_match:
                        db_order.delivery_recipient = rf'{db_order.delivery_recipient} {pattern_match.group(1).strip()}'''
                        invoice_lines.pop(0)
                    else:
                        pass
                else:
                    pass
            else:
                pass
        else:
            pass

        logger.debug(rf'DELIVERY RECIPIENT: {db_order.delivery_recipient}')

    except:
        logger.error(rf'DELIVERY RECIPIENT PARSE ERROR: {sys.exc_info()[0]}')


def get_delivery_address():
    #   ** **********************************************************************************************************************************************************
    #   ** extract delivery_recipient from pdf
    #   ** **********************************************************************************************************************************************************
    try:
        countries: list = ['Ireland', 'United Kingdom', 'United States']
        country: Country = None

        delivery_address: str = None
        delivery_address_line: list = []

        while re.search(rf'^(Scheduled to dispatch by|Scheduled to ship by)$', invoice_lines[0]) is None and re.search(
                rf'^Shop$', invoice_lines[0], flags=re.I) is None:

            pattern: str = r'^(.+)$'
            pattern_match = re.search(pattern, invoice_lines[0], flags=re.I)

            if pattern_match:
                delivery_address_line.append(pattern_match.group(1).strip())
                invoice_lines.pop(0)
            else:
                break

        tmp_address_line: str = None
        for tmp_address_line in delivery_address_line:
            if tmp_address_line.find(countries[2]) >= 0:
                country = Country(countries[2])
                break
            elif tmp_address_line.find(countries[1]) >= 0:
                country = Country(countries[1])
                break
            else:
                pass

        if country:
            db_order.delivery_country_code = country.alpha_2_code
        else:
            country = Country(countries[1])
            db_order.delivery_country_code = country.alpha_2_code

        #        if db_order.delivery_country_code is None:
        #            i = len(delivery_address_line) - 1
        #            country = Country (delivery_address_line[i])
        #            db_order.delivery_country_code = country.alpha_2_code

        i = 0
        while i < len(delivery_address_line):
            match i:
                case 0:
                    db_order.delivery_address_01 = delivery_address_line[i]
                case 1:
                    db_order.delivery_address_02 = delivery_address_line[i]
                case 2:
                    db_order.delivery_address_03 = delivery_address_line[i]
                case 3:
                    db_order.delivery_address_04 = delivery_address_line[i]
                case 4:
                    db_order.delivery_address_05 = delivery_address_line[i]
                case other:
                    pass

            i += 1

        delivery_address = ' '.join(delivery_address_line)

        if db_order.delivery_country_code == 'US':
            ptn_state_name_list = [
                '('
                ,
                'Armed Forces|Alabama|Alaska|Arizona|Arkansas|California|Colorado|Connecticut|Delaware|Florida|Georgia|Hawaii|'
                , 'Idaho|Illinois|Indiana|Iowa|Kansas|Kentucky|Louisiana|Maine|Maryland|Massachusetts|Michigan|'
                , 'Minnesota|Mississippi|Missouri|Montana|Nebraska|Nevada|New[ ]Hampshire|New[ ]Jersey|New[ ]Mexico|'
                , 'New[ ]York|North[ ]Carolina|North[ ]Dakota|Ohio|Oklahoma|Oregon|Pennsylvania|Rhode[ ]Island|'
                , 'South[ ]Carolina|South[ ]Dakota|Tennessee|Texas|Utah|Vermont|Virginia|Washington|West[ ]Virginia|'
                , 'Wisconsin|Wyoming'
                , ')'
            ]
            ptn_state_name = ''.join(ptn_state_name_list)

            ptn_state_abbrev_list = [
                '('
                , 'AE|AL|AK|AS|AZ|AR|CA|CO|CT|DE|DC|FM|FL|GA|GU|HI|ID|IL|IN|IA|KS|KY|LA|ME|MH|MD|MA|MI|MN|MS|MO|MT|'
                , 'NE|NV|NH|NJ|NM|NY|NC|ND|MP|OH|OK|OR|PW|PA|PR|RI|SC|SD|TN|TX|UT|VT|VI|VA|WA|WV|WI|WY'
                , ')'
            ]
            ptn_state_abbrev = ''.join(ptn_state_abbrev_list)

            ptn_country_name = rf'({country.short_name})'
            ptn_city = rf'([A-Z\s]+)'
            ptn_zip_code: str = rf'([\d{5}]+)[\-]?([\d{4}]*)'
            ptn_city_state_zip_code = rf'{ptn_city}\s?\,[ ]{ptn_state_abbrev}[\s]+{ptn_zip_code}'
            ptn_city_state = rf'{ptn_city}\s?\,[ ]{ptn_state_abbrev}'
            ptn_state_zip_code = rf'{ptn_state_abbrev}[ ]{ptn_zip_code}'
            ptn_address = rf'{ptn_city}\s?\,[ ]{ptn_state_abbrev}[\s]+{ptn_zip_code}*{ptn_country_name}'
            ptn_street = rf'\d+[ ](?:[A-Za-z0-9.-]+[ ]?)+(?:Avenue|Lane|Road|Boulevard|Drive|Street|Ave|Dr|Rd|Blvd|Ln|St)\.?'

            if db_order.delivery_address_05:
                pattern_match = re.search(ptn_country_name, db_order.delivery_address_05)

                if pattern_match:
                    if db_order.delivery_address_04:
                        pattern_match = re.search(ptn_city_state_zip_code, db_order.delivery_address_04)

                        if pattern_match:
                            db_order.delivery_city = rf'{pattern_match.group(1).strip().upper()}'
                            db_order.delivery_state = rf'{pattern_match.group(2).strip().upper()}'''

                            if pattern_match.group(3) and pattern_match.group(4):
                                db_order.delivery_zipcode = rf'{pattern_match.group(3).strip()}-{pattern_match.group(4).strip()}'
                            else:
                                db_order.delivery_zipcode = rf'{pattern_match.group(3).strip()}'''

                                db_order.delivery_street_01 = rf'{db_order.delivery_address_01.upper()}'
                                db_order.delivery_street_02 = rf'{db_order.delivery_address_02.upper()}, {db_order.delivery_address_03.upper()}'
                        else:
                            pattern_match = re.search(ptn_zip_code, db_order.delivery_address_04)

                            if pattern_match:
                                if pattern_match.group(1) and pattern_match.group(2):
                                    db_order.delivery_zipcode = rf'{pattern_match.group(1).strip()}-{pattern_match.group(2).strip()}'
                                else:
                                    db_order.delivery_zipcode = rf'{pattern_match.group(1).strip()}'

                                if db_order.delivery_address_03:
                                    pattern_match = re.search(ptn_city_state, db_order.delivery_address_03)

                                    if pattern_match:
                                        db_order.delivery_city = rf'{pattern_match.group(1).strip().upper()}'
                                        db_order.delivery_state = rf'{pattern_match.group(2).strip().upper()}'
                                    else:
                                        pass

                                    db_order.delivery_street_01 = rf'{db_order.delivery_address_01.upper()}'
                                    db_order.delivery_street_02 = rf'{db_order.delivery_address_02.upper()}'''
                                else:
                                    pass
                            else:
                                pass

                    else:
                        pass
                else:
                    pass

            elif db_order.delivery_address_04:
                pattern_match = re.search(ptn_country_name, db_order.delivery_address_04)

                if pattern_match:
                    if db_order.delivery_address_03:
                        pattern_match = re.search(ptn_city_state_zip_code, db_order.delivery_address_03)

                        if pattern_match:
                            db_order.delivery_city = rf'{pattern_match.group(1).strip().upper()}'
                            db_order.delivery_state = rf'{pattern_match.group(2).strip().upper()}'

                            if pattern_match.group(3) and pattern_match.group(4):
                                db_order.delivery_zipcode = rf'{pattern_match.group(3).strip()}-{pattern_match.group(4).strip()}'
                            else:
                                db_order.delivery_zipcode = rf'{pattern_match.group(3).strip()}'

                            db_order.delivery_street_01 = rf'{db_order.delivery_address_01.upper()}'
                            db_order.delivery_street_02 = rf'{db_order.delivery_address_02.upper()}'
                        else:
                            pattern_match = re.search(ptn_state_zip_code, db_order.delivery_address_03)

                            if pattern_match:
                                db_order.delivery_state = rf'{pattern_match.group(1).strip()}'

                                if pattern_match.group(2) and pattern_match.group(3):
                                    db_order.delivery_zipcode = rf'{pattern_match.group(2).strip()}-{pattern_match.group(3).strip()}'
                                else:
                                    db_order.delivery_zipcode = rf'{pattern_match.group(2).strip()}'

                                if db_order.delivery_address_02:
                                    ptn_City = ptn_City + rf'[\,]?'
                                    pattern_match = re.search(ptn_City, db_order.delivery_address_02)

                                    if pattern_match:
                                        db_order.delivery_city = rf'{pattern_match.group(1).strip().upper()}'
                                    else:
                                        pass
                                else:
                                    pass

                                db_order.delivery_street_01 = rf'{db_order.delivery_address_01.upper()}'
                                db_order.delivery_street_02 = ""
                            else:
                                pattern_match = re.search(ptn_zip_code, db_order.delivery_address_03)

                                if pattern_match:
                                    if pattern_match.group(1) and pattern_match.group(2):
                                        db_order.delivery_zipcode = rf'{pattern_match.group(1).strip()}-{pattern_match.group(2).strip()}'
                                    else:
                                        db_order.delivery_zipcode = rf'{pattern_match.group(1).strip()}'

                                    if db_order.delivery_address_02:
                                        pattern_match = re.search(ptn_city_state, db_order.delivery_address_02)

                                        if pattern_match:
                                            db_order.delivery_city = rf'{pattern_match.group(1).strip().upper()}'
                                            db_order.delivery_state = rf'{pattern_match.group(2).strip().upper()}'
                                        else:
                                            pass
                                    else:
                                        pass
                                else:
                                    pass

                            db_order.delivery_street_01 = rf'{db_order.delivery_address_01.upper()}'
                            db_order.delivery_street_02 = ""
                    else:
                        pass
                else:
                    pass
            else:
                pattern_match = re.search(ptn_country_name, db_order.delivery_address_03)

                if pattern_match:
                    if db_order.delivery_address_02:
                        pattern: str = rf'{ptn_city}\s?\,[ ]{ptn_state_abbrev}[\s]+{ptn_zip_code}'

                        pattern_match = re.search(pattern, db_order.delivery_address_02)

                        if pattern_match:
                            db_order.delivery_city = rf'{pattern_match.group(1).strip()}'
                            db_order.delivery_state = rf'{pattern_match.group(2).strip()}'

                            if pattern_match.group(3) and pattern_match.group(4):
                                db_order.delivery_zipcode = rf'{pattern_match.group(3).zfill(5)}-{pattern_match.group(4).zfill(4)}'
                            else:
                                db_order.delivery_zipcode = rf'{pattern_match.group(3).zfill(5)}'

                            db_order.delivery_street_01 = rf'{db_order.delivery_address_01.upper()}'
                            db_order.delivery_street_02 = ''
                        else:
                            pass
                    else:
                        pass
                else:
                    pass
        else:
            pass

        logger.debug(
            rf'DELIVERY ADDRESS: {db_order.delivery_street_01}, {db_order.delivery_street_02}, {db_order.delivery_city}, {db_order.delivery_state}, {db_order.delivery_zipcode}, {db_order.delivery_country_code}')
        logger.debug(
            rf'DELIVERY ADDRESS: {db_order.delivery_address_01}, {db_order.delivery_address_02}, {db_order.delivery_address_03}, {db_order.delivery_address_04}, {db_order.delivery_address_05}')

    except:
        logger.error(rf'DELIVERY ADDRESS PARSE ERROR: {sys.exc_info()[0]}')


def get_scheduled_dispatch_date():
    #   ** **********************************************************************************************************************************************************
    #   **
    #   ** **********************************************************************************************************************************************************
    try:
        if re.search(rf'^Scheduled to dispatch by|Scheduled to ship by$', invoice_lines[0], flags=re.I):
            invoice_lines.pop(0)

            db_order.scheduled_dispatch_date = get_date(invoice_lines[0], db_order.delivery_country_code)

            if db_order.scheduled_dispatch_date:
                invoice_lines.pop(0)
            else:
                db_order.scheduled_dispatch_date = date.today()
        else:
            db_order.scheduled_dispatch_date = date.today()

        logger.debug(rf'DISPATCH DATE: {db_order.scheduled_dispatch_date}')

    except:
        logger.error(rf'DISPATCH DATE PARSE ERROR: {sys.exc_info()[0]}')


def get_sales_channel_id():
    #   ** **********************************************************************************************************************************************************
    #   **
    #   ** **********************************************************************************************************************************************************
    try:
        if re.search(rf'^Shop$', invoice_lines[0], flags=re.I):
            invoice_lines.pop(0)

            pattern = rf'(.+)'
            pattern_match = re.search(pattern, invoice_lines[0], flags=re.I)

            if pattern_match:
                shop_name: str = pattern_match.group(1).strip()
                sales_channel: SalesChannel = SalesChannel(shop_name)
                db_order.sales_channel_id = sales_channel.id
                invoice_lines.pop(0)
            else:
                pass
        else:
            pass

        logger.debug(rf'SALES CHANNEL ID: {db_order.sales_channel_id}')

    except:
        logger.error(rf'SALES CHANNEL ID PARSE ERROR: {sys.exc_info()[0]}')


def get_order_date():
    #   ** **********************************************************************************************************************************************************
    #   **
    #   ** **********************************************************************************************************************************************************
    try:
        if re.search(rf'^Order date$', invoice_lines[0], flags=re.I):
            invoice_lines.pop(0)

            db_order.sale_date = get_date(invoice_lines[0], db_order.delivery_country_code)

            if db_order.sale_date:
                invoice_lines.pop(0)
            else:
                db_order.sale_date = datetime.date.today()
        else:
            pass

        logger.debug(rf'ORDER DATE: {db_order.sale_date}')

    except:
        logger.error(rf'ORDER DATE PARSE ERROR: {sys.exc_info()[0]}')


def get_payment_method():
    #   ** **********************************************************************************************************************************************************
    #   **
    #   ** **********************************************************************************************************************************************************
    try:
        if re.search(r'^Payment method$', invoice_lines[0], flags=re.I):
            invoice_lines.pop(0)

            pattern = rf'^(.+)$'
            pattern_match = re.search(pattern, invoice_lines[0], flags=re.I)
            if pattern_match:
                db_order.payment_method = pattern_match.group(1).strip()
                invoice_lines.pop(0)
            else:
                pass
        else:
            pass

        logger.debug(rf'PAYMENT METHOD: {db_order.payment_method}')

    except:
        logger.error(rf'PAYMENT METHOD PARSE ERROR: {sys.exc_info()[0]}')


def get_delivery_details_domestic():
    #   ** **********************************************************************************************************************************************************
    #   ** Extract delivery method, tracking, carrier (in any order) from PDF
    #   ** **********************************************************************************************************************************************************
    try:
        db_order.dispatch_priority = 0

        while re.search(rf'^([\d]+) (Item[s]?)$', invoice_lines[0], flags=re.I) is None:

            if re.search(r'^Delivery method$', invoice_lines[0], flags=re.I):
                invoice_lines.pop(0)

                pattern: str = rf'^(.+)$'
                pattern_match = re.search(pattern, invoice_lines[0], flags=re.I)

                if pattern_match:
                    db_order.delivery_method = pattern_match.group(1).strip()

                    match db_order.delivery_method:
                        case "Next Day Delivery" | "Royal Mail Next Day by 1pm" | "Royal Mail Next Day by 1PM":
                            db_order.dispatch_priority = 10
                        case "Royal Mail 1st Class" | "First Class" | "FIRST CLASS":
                            db_order.dispatch_priority = 0
                        case other:
                            db_order.dispatch_priority = 0
                    invoice_lines.pop(0)
            else:
                pass

            if re.search(rf'^Tracking$', invoice_lines[0], flags=re.I):
                invoice_lines.pop(0)

                pattern: str = rf'^(.+)$'
                pattern_match = re.search(pattern, invoice_lines[0], flags=re.I)

                if pattern_match:
                    db_order.delivery_tracking_id = pattern_match.group(1).strip()
                    invoice_lines.pop(0)

                pattern: str = rf'^(via )(.+)$'
                pattern_match = re.search(pattern, invoice_lines[0], flags=re.I)

                if pattern_match:
                    db_order.delivery_carrier = pattern_match.group(2).strip()
                    invoice_lines.pop(0)

                #               This catches error where tracking number is attached twice to order
                pattern: str = rf'^(via )(.+)$'
                pattern_match = re.search(pattern, invoice_lines[1], flags=re.I)

                if pattern_match:
                    invoice_lines.pop(0)
                    invoice_lines.pop(0)
            else:
                pass

        logger.debug(
            rf'DOMESTIC DELIVERY METHOD: {db_order.delivery_method}, PRIORITY: {db_order.dispatch_priority}, TRACKING: {db_order.delivery_tracking_id}, CARRIER: {db_order.delivery_carrier}')

    except:
        logger.error(rf'DOMESTIC DELIVERY METHOD PARSE ERROR: {sys.exc_info()[0]}')


def get_delivery_details_international():
    #   ** **********************************************************************************************************************************************************
    #   ** Extract delivery method, tracking, carrier (in any order) from PDF
    #   ** **********************************************************************************************************************************************************
    try:
        db_order.dispatch_priority = 5

        while re.search(r'^([\d]+) (Item[s]?)$', invoice_lines[0], flags=re.I) is None:

            if re.search(r'^Delivery method$', invoice_lines[0], flags=re.I):
                invoice_lines.pop(0)

                pattern: str = rf'^(.+)$'
                pattern_match = re.search(pattern, invoice_lines[0], flags=re.I)

                if pattern_match:
                    db_order.delivery_method = pattern_match.group(1).strip()
                    invoice_lines.pop(0)
                else:
                    pass

            elif re.search(rf'^Tracking$', invoice_lines[0], flags=re.I):
                invoice_lines.pop(0)

                pattern: str = rf'^(.+)$'
                pattern_match = re.search(pattern, invoice_lines[0], flags=re.I)

                if pattern_match:
                    db_order.delivery_tracking_id = pattern_match.group(1).strip()
                    invoice_lines.pop(0)
                else:
                    pass

            elif re.search(rf'^(via )(.+)$', invoice_lines[0], flags=re.I):
                pattern: str = rf'^(via )(.+)$'
                pattern_match = re.search(pattern, invoice_lines[0], flags=re.I)

                if pattern_match:
                    db_order.delivery_carrier = pattern_match.group(2).strip()
                    invoice_lines.pop(0)

                    #                       This catches error where tracking number is attached twice to order
                    pattern: str = rf'^(via )(.+)$'
                    pattern_match = re.search(pattern, invoice_lines[1], flags=re.I)

                    if pattern_match:
                        invoice_lines.pop(0)
                        invoice_lines.pop(0)
                    else:
                        pass
            else:
                pass

        logger.debug(
            rf'INTERNATIONAL DELIVERY METHOD: {db_order.delivery_method}, PRIORITY: {db_order.dispatch_priority}, TRACKING: {db_order.delivery_tracking_id}, CARRIER: {db_order.delivery_carrier}')

    except:
        logger.error(rf'INTERNATIONAL DELIVERY METHOD PARSE ERROR: {sys.exc_info()[0]}')


def get_number_of_items():
    #   ** **********************************************************************************************************************************************************
    #   **
    #   ** **********************************************************************************************************************************************************
    try:
        pattern: str = rf'^([\d]+) (Item[s]?)$'
        pattern_match = re.search(pattern, invoice_lines[0], flags=re.I)

        if pattern_match:
            db_order.number_of_items = int(pattern_match.group(1).strip())
            invoice_lines.pop(0)
        else:
            pass

        logger.debug(rf'ITEM_COUNT: {db_order.number_of_items}')

    except:
        logger.error(rf'ITEM COUNT PARSE ERROR: {sys.exc_info()[0]}')


def get_item_listing_title():
    #   ** **********************************************************************************************************************************************************
    #   **
    #   ** **********************************************************************************************************************************************************
    product_listing_title: list = []

    try:
        while invoice_lines and re.search(rf'^Item total$', invoice_lines[0]) is None and re.search(rf'^SKU:[\s]*',
                                                                                                    invoice_lines[
                                                                                                        0]) is None and re.search(
                rf'^([\d]+) x ([£]+)([\d.]+)$', invoice_lines[0]) is None:

            pattern: str = rf'^(.+)$'
            pattern_match = re.search(pattern, invoice_lines[0], flags=re.I)

            if pattern_match:
                product_listing_title.append(pattern_match.group(1).strip())
                invoice_lines.pop(0)
            else:
                break

        db_order_item.product_listing_title = " ".join(product_listing_title)

        logger.debug(rf'ITEM LISTING TITLE: {db_order_item.product_listing_title}')

    except:
        logger.error(rf'ITEM LISTING TITLE PARSE ERROR: {sys.exc_info()[0]}')


def get_item_sku():
    #   ** **********************************************************************************************************************************************************
    #   **
    #   ** **********************************************************************************************************************************************************
    try:
        pattern: str = rf'^SKU: (.+)$'
        pattern_match = re.search(pattern, invoice_lines[0], flags=re.I)

        if pattern_match and pattern_match.group(1).find('Postage') == -1:
            sku_substitution = SKUSubstitution(pattern_match.group(1).strip())

            if sku_substitution.key:
                db_order_item.sku = sku_substitution.new_sku
                db_order_item.product_material_code = sku_substitution.product_material_code
                db_order_item.product_type_code = sku_substitution.product_type_code
                db_order_item.product_design_code = sku_substitution.product_design_code
                db_order_item.product_listing_no = sku_substitution.product_listing_no
            else:
                db_order_item.sku = pattern_match.group(1).upper().strip()

                pattern: str = rf'([\w]+)_([\w]+)_([\w]+)_([\d]+)[\_]+([\w]*)$'
                pattern_match = re.search(pattern, db_order_item.sku, flags=re.I)

                if pattern_match:
                    db_order_item.product_material_code = pattern_match.group(1).upper().strip()

                    if pattern_match.group(5):
                        db_order_item.product_type_code = rf'{pattern_match.group(2).upper().strip()}{pattern_match.group(5).upper().strip()}'''
                        db_order_item.product_design_code = pattern_match.group(3).upper().strip()
                        db_order_item.product_listing_no = pattern_match.group(4).upper().strip()
                        db_order_item.sku = rf'{db_order_item.product_material_code}_{db_order_item.product_type_code}_{db_order_item.product_design_code}_{db_order_item.product_listing_no}'''
                    else:
                        db_order_item.product_type_code = pattern_match.group(2).upper().strip()
                        db_order_item.product_design_code = pattern_match.group(3).upper().strip()
                        db_order_item.product_listing_no = pattern_match.group(4).upper().strip()
                else:
                    pattern: str = rf'([\w]+)_([\w]+)_([\w]+)_([\w]+)$'
                    pattern_match = re.search(pattern, db_order_item.sku, flags=re.I)

                    if pattern_match:
                        db_order_item.product_material_code = pattern_match.group(1).upper().strip()
                        db_order_item.product_type_code = pattern_match.group(2).upper().strip()
                        db_order_item.product_design_code = pattern_match.group(3).upper().strip()
                        db_order_item.product_listing_no = pattern_match.group(4).upper().strip()
                    else:
                        pattern: str = rf'([\w]+)_([\w]+)_([\w]+)_([\w\+\-]+)$'
                        pattern_match = re.search(pattern, db_order_item.sku, flags=re.I)

                        if pattern_match:
                            db_order_item.product_material_code = pattern_match.group(1).upper().strip()
                            db_order_item.product_type_code = pattern_match.group(2).upper().strip()
                            db_order_item.product_design_code = pattern_match.group(3).upper().strip()
                            db_order_item.product_listing_no = pattern_match.group(4).upper().strip()
                        else:
                            pattern: str = rf'([\w]+)_([\w]+)_([\w]+)_([\d]+)[\_]+([\w]+)$'
                            pattern_match = re.search(pattern, db_order_item.sku, flags=re.I)

                            if pattern_match:
                                db_order_item.product_material_code = pattern_match.group(1).upper().strip()
                                db_order_item.product_type_code = pattern_match.group(2).upper().strip()
                                db_order_item.product_design_code = pattern_match.group(3).upper().strip()
                                db_order_item.product_listing_no = pattern_match.group(4).upper().strip()
                            else:
                                db_order_item.product_material_code = 'XXX'
                                db_order_item.product_type_code = 'XXX'
                                db_order_item.product_design_code = 'UNKNOWN'
                                db_order_item.product_listing_no = '00'
                                db_order_item.sku = rf'{db_order_item.product_material_code}_{db_order_item.product_type_code}_{db_order_item.product_design_code}_{db_order_item.product_listing_no}'''
                                logger.warning(
                                    rf'INVALID SKU FOR ORDER: {db_order.sales_channel_id}-{db_order.order_no}')

            db_order_item.mergeable_ind = 'Y' if db_order_item.product_design_code in sys_settings.personalise_list else 'N'
            invoice_lines.pop(0)
        else:
            db_order_item.product_material_code = 'XXX'
            db_order_item.product_type_code = 'XXX'
            db_order_item.product_design_code = 'UNKNOWN'
            db_order_item.product_listing_no = '00'
            db_order_item.sku = rf'{db_order_item.product_material_code}_{db_order_item.product_type_code}_{db_order_item.product_design_code}_{db_order_item.product_listing_no}'''
            logger.warning(rf'INVALID SKU FOR ORDER: {db_order.sales_channel_id}-{db_order.order_no}')

        logger.debug(rf'ITEM SKU TITLE: {db_order_item.sku}')

    except:
        logger.error(rf'ITEM SKU PARSE ERROR: {sys.exc_info()[0]}')


def get_item_variations():
    #   ** **********************************************************************************************************************************************************
    #   **
    #   ** **********************************************************************************************************************************************************
    try:
        variations: list[str] = []

        while invoice_lines and re.search(rf'^Item total$', invoice_lines[0]) is None and re.search(
                rf'^Personalisation:[\s]*', invoice_lines[0]) is None and re.search(rf'^([\d]+) x ([£]+)([\d\.]+)$',
                                                                                    invoice_lines[0]) is None:
            pattern: str = rf'^(.+)$'
            pattern_match = re.search(pattern, invoice_lines[0], flags=re.I)

            if pattern_match:
                variations.append(pattern_match.group(1).replace("&amp;", "&").strip())
                invoice_lines.pop(0)
            else:
                break

        for i in range(len(variations)):
            pattern: str = rf'([\w\s\&\.\?\/\(\)]+):\s*([\w\s\&\,\-\'\+\)\()]+)$'
            pattern_match = re.search(pattern, variations[i], flags=re.I)

            if pattern_match:
                match i:
                    case 0:
                        db_order_item.variation_01_name = pattern_match.group(1).strip()
                        db_order_item.variation_01_value = pattern_match.group(2).strip()
                    case 1:
                        db_order_item.variation_02_name = pattern_match.group(1).strip()
                        db_order_item.variation_02_value = pattern_match.group(2).strip()
                    case other:
                        pass

        if db_order_item.variation_01_name:
            db_order_item.variation = rf'{db_order_item.variation_01_name}: {db_order_item.variation_01_value}'

            if db_order_item.variation_02_name:
                db_order_item.variation = rf'{db_order_item.variation_01_name}: {db_order_item.variation_01_value},{db_order_item.variation_02_name}: {db_order_item.variation_02_value}'
            else:
                pass
        else:
            pass

        logger.debug(rf'ITEM VARIATION 01: {db_order_item.variation_01_name}: {db_order_item.variation_01_value}')
        logger.debug(rf'ITEM VARIATION 02: {db_order_item.variation_02_name}: {db_order_item.variation_02_value}')

    except:
        logger.error(rf'ITEM VARIATION PARSE ERROR: {sys.exc_info()[0]}')


def get_item_personalisation():
    #   ** **********************************************************************************************************************************************************
    #   **
    #   ** **********************************************************************************************************************************************************
    try:
        item_personalisations: list[str] = []

        if invoice_lines and (
                re.search(rf'^Personalisation: ', invoice_lines[0], flags=re.I) or re.search(rf'^Personalisation:',
                                                                                             invoice_lines[0])):
            if re.search(rf'^Personalisation: ', invoice_lines[0]):
                invoice_lines[0] = re.sub(rf'^Personalisation: ', "", invoice_lines[0], flags=re.I)
            else:
                invoice_lines[0] = re.sub(rf'^Personalisation:', "", invoice_lines[0], flags=re.I)

            while invoice_lines and re.search(rf'^Item total', invoice_lines[0]) is None and re.search(
                    rf'^([\d]+) x ([£]+)([\d\.]+)', invoice_lines[0]) is None:
                if invoice_lines[0] is not None and invoice_lines[0] != "" and invoice_lines[0] != " ":
                    s_pattern = rf"^(.+)"
                    s_pattern_match = re.search(s_pattern, invoice_lines[0], flags=re.I)

                    if s_pattern_match:

                        if (
                                db_order_item.product_material_code == 'CWT' and db_order_item.product_type_code == 'PLC') or (
                                db_order_item.product_design_code == 'WS152'):

                            if s_pattern_match.group(1).find(',') >= 0:
                                item_personalisations.append(s_pattern_match.group(1))
                            else:
                                item_personalisations.append(s_pattern_match.group(1) + ',')
                        else:
                            item_personalisations.append(s_pattern_match.group(1).strip())

                        invoice_lines.pop(0)
                    else:
                        break
                else:
                    invoice_lines.pop(0)

            if (db_order_item.product_material_code == 'CWT' and db_order_item.product_type_code == 'PLC') or (
                    db_order_item.product_design_code == 'WS152'):

                for i in range(len(item_personalisations)):
                    if i != 0 and item_personalisations[i][0].isupper() == True and (
                            item_personalisations[i - 1][-1].isupper() == False and item_personalisations[i - 1][
                        -1] != ','):
                        item_personalisations[i - 1] = rf'{item_personalisations[i - 1]} '
                    else:
                        pass

                item_personalisation: str = "".join(item_personalisations)

                db_order_item.input_personalisation = item_personalisation
                db_order_item.merge_personalisation = item_personalisation
            else:
                db_order_item.input_personalisation = ",".join(item_personalisations)
                db_order_item.merge_personalisation = "~".join(item_personalisations)
        else:
            pass

        logger.debug(rf'ITEM PERSONALISATION: {db_order_item.merge_personalisation}')

    except:
        logger.error(rf'ITEM PERSONALISATION PARSE ERROR: {sys.exc_info()[0]}')


def get_item_quantity_price():
    #   ** **********************************************************************************************************************************************************
    #   **
    #   ** **********************************************************************************************************************************************************
    try:
        if invoice_lines and re.search(rf'^([\d]+) x ([£$]?)([\d\.]+)$', invoice_lines[0]):

            pattern: str = rf'^([\d]+) x ([£$]?)([\d\.]+)$'
            pattern_match = re.search(pattern, invoice_lines[0], flags=re.I)

            if pattern_match:
                db_order_item.quantity = int(pattern_match.group(1).strip())
                currency: Currency = Currency(pattern_match.group(2).strip())
                db_order_item.currency_code = currency.code
                db_order_item.price = float(pattern_match.group(3).strip())
                invoice_lines.pop(0)
            else:
                print(rf'ERROR: Extracting Order Item Quantity: {invoice_lines[0]}')
                db_order_item.valid_ind = 'N'
                db_order_item.currency_code = 'XXX'
                db_order_item.quantity = 0
                db_order_item.price = 0
        else:
            print(f'''ERROR: Extracting Order Item Quantity:''')
            db_order_item.valid_ind = 'N'
            db_order_item.currency_code = 'XXX'
            db_order_item.quantity = 0
            db_order_item.price = 0

        logger.debug(
            rf'ITEM QUANTITY/PRICE: {db_order_item.quantity} x {db_order_item.price} {db_order_item.currency_code}')

        while invoice_lines and (invoice_lines[0] is None or invoice_lines[0] == "" or invoice_lines[0] == " "):
            invoice_lines.pop(0)
    except:
        logger.error(rf'ITEM QUANTITY/PRICE PARSE ERROR: {sys.exc_info()[0]}')


def get_item_total():
    #   ** **********************************************************************************************************************************************************
    #   **
    #   ** **********************************************************************************************************************************************************
    try:
        if invoice_lines and re.search(rf'^Item total$', invoice_lines[0], flags=re.I):
            invoice_lines.pop(0)

            pattern: str = rf'^([£]+)([\d\.]+)$'
            pattern_match = re.search(pattern, invoice_lines[0], flags=re.I)
            if pattern_match:
                currency: Currency = Currency(pattern_match.group(1).strip())
                db_order.currency_code = currency.code
                db_order.order_amt = float(pattern_match.group(2).strip())
                invoice_lines.pop(0)
            else:
                pass

        logger.debug(rf'ITEM TOTAL: {db_order.order_amt} {db_order.currency_code}')

    except:
        logger.error(rf'ITEM TOTAL PARSE ERROR: {sys.exc_info()[0]}')


def get_order_sub_totals():
    #   ** **********************************************************************************************************************************************************
    #   **
    #   ** **********************************************************************************************************************************************************
    try:
        while invoice_lines and re.search(rf'^Order total$', invoice_lines[0], flags=re.I) is None:

            match invoice_lines[0]:
                case 'Delivery total':
                    invoice_lines.pop(0)

                    pattern: str = rf'^([£]+)([\d\.]+)$'
                    pattern_match = re.search(pattern, invoice_lines[0], flags=re.I)

                    if pattern_match:
                        db_order.delivery_amt = float(pattern_match.group(2).strip())
                        invoice_lines.pop(0)
                    else:
                        pass

                    logger.debug(rf'DELIVERY TOTAL: {db_order.delivery_amt}')

                case 'Subtotal':
                    invoice_lines.pop(0)

                    pattern: str = rf'^([£]+)([\d\.]+)$'
                    pattern_match = re.search(pattern, invoice_lines[0], flags=re.I)

                    if pattern_match:
                        db_order.order_subtotal_amt = float(pattern_match.group(2).strip())
                        invoice_lines.pop(0)
                    else:
                        pass

                    logger.debug(rf'SUB-TOTAL: {db_order.order_subtotal_amt}')

                case 'Refunded cost':
                    invoice_lines.pop(0)

                    pattern: str = rf'^([£]+)([\d\.]+$)'
                    pattern_match = re.search(pattern, invoice_lines[0], flags=re.I)

                    if pattern_match:
                        db_order.order_refunded_amt = float(pattern_match.group(2).strip())
                        invoice_lines.pop(0)
                    else:
                        pass

                    logger.debug(rf'REFUNDED COST: {db_order.order_refunded_amt}')

                case 'Tax':
                    invoice_lines.pop(0)

                    pattern: str = rf'^([£]+)([\d\.]+)$'
                    pattern_match = re.search(pattern, invoice_lines[0], flags=re.I)

                    if pattern_match:
                        db_order.sales_tax_amt = float(pattern_match.group(2).strip())
                        invoice_lines.pop(0)
                    else:
                        pass

                    logger.debug(rf'TAX: {db_order.sales_tax_amt}')

                case 'Postage Discount':
                    invoice_lines.pop(0)

                    pattern: str = rf'^([\-]?[£]+)([\d\.]+)$'
                    pattern_match = re.search(pattern, invoice_lines[0], flags=re.I)

                    if pattern_match:
                        db_order.delivery_discount_amt = float(pattern_match.group(2).strip())
                        invoice_lines.pop(0)
                    else:
                        pass

                    logger.debug(rf'POSTAGE DISCOUNT: {db_order.delivery_discount_amt}')

                case 'Shop discount':
                    invoice_lines.pop(0)

                    pattern: str = rf'^([\-]+)$'
                    pattern_match = re.search(pattern, invoice_lines[0], flags=re.I)

                    if pattern_match:
                        invoice_lines.pop(0)

                        pattern: str = rf'^([\s£]+)([\d\.]+)$'
                        pattern_match = re.search(pattern, invoice_lines[0], flags=re.I)

                        if pattern_match:
                            db_order.discount_amt = pattern_match.group(2).strip()
                            invoice_lines.pop(0)
                        else:
                            pass
                    else:
                        pattern: str = rf'^([-\s£]+)([\d\.]+)$'
                        pattern_match = re.search(pattern, invoice_lines[0], flags=re.I)

                        if pattern_match:
                            db_order.discount_amt = pattern_match.group(2).strip()
                            invoice_lines.pop(0)
                        else:
                            pass

                    logger.debug(rf'SHOP DISCOUNT: {db_order.discount_amt}')

                case _:
                    logger.error(rf'UNKNOWN INVOICE ITEM: {invoice_lines[0]}')
                    invoice_lines.pop(0)



    except:
        logger.error(rf'ITEM SUB TOTALS PARSE ERROR: {sys.exc_info()[0]}')


def get_order_total():
    #   ** **********************************************************************************************************************************************************
    #   **
    #   ** **********************************************************************************************************************************************************
    try:
        if invoice_lines and re.search(rf'^Order total$', invoice_lines[0], flags=re.I):
            invoice_lines.pop(0)

            pattern: str = rf'^([£$]?)([\d\.]+)+$'
            pattern_match = re.search(pattern, invoice_lines[0], flags=re.I)

            if pattern_match:
                db_order.order_total_amt = pattern_match.group(2).strip()
                invoice_lines.pop(0)
            else:
                pass

            logger.debug(rf'ORDER TOTAL: {db_order.order_total_amt}')
        else:
            pass

    except:
        logger.error(rf'ORDER TOTAL PARSE ERROR: {sys.exc_info()[0]}')


def get_buyer_note():
    #   ** **********************************************************************************************************************************************************
    #   **
    #   ** **********************************************************************************************************************************************************
    try:
        if invoice_lines and re.search(rf'^Note from buyer$', invoice_lines[0]):
            invoice_lines.pop(0)

            buyer_notes: list[str] = []

            while invoice_lines and re.search(rf'^Gift message$', invoice_lines[0]) is None and re.search(
                    rf'^Private notes$', invoice_lines[0]) is None:
                pattern: str = rf'^(.+)$'
                pattern_match = re.search(pattern, invoice_lines[0], flags=re.I)

                if pattern_match:
                    buyer_notes.append(pattern_match.group(1).strip())
                    invoice_lines.pop(0)
                else:
                    invoice_lines.pop(0)

            db_order.buyer_note = " ".join(buyer_notes).replace(";", ":")
        else:
            pass

        logger.debug(rf'BUYER NOTE: {db_order.buyer_note}')

    except:
        logger.error(rf'BUYER NOTE PARSE ERROR: {sys.exc_info()[0]}')


def get_private_note():
    #   ** **********************************************************************************************************************************************************
    #   **
    #   ** **********************************************************************************************************************************************************
    try:
        if invoice_lines and re.search(rf'^Private notes$', invoice_lines[0]):
            invoice_lines.pop(0)

            private_notes: list[str] = []

            while invoice_lines and re.search(rf'^Gift message$', invoice_lines[0]) is None and re.search(
                    rf'^Note from buyer$', invoice_lines[0]) is None:
                pattern: str = rf'^(.+)$'
                pattern_match = re.search(pattern, invoice_lines[0], flags=re.I)

                if pattern_match:
                    private_notes.append(pattern_match.group(1).strip())
                    invoice_lines.pop(0)
                else:
                    invoice_lines.pop(0)

            db_order.private_notes = " ".join(private_notes).replace(";", ":")
        else:
            pass

        logger.debug(rf'PRIVATE NOTE: {db_order.private_notes}')

    except:
        logger.error(rf'PRIVATE NOTE PARSE ERROR: {sys.exc_info()[0]}')


def get_gift_message():
    #   ** **********************************************************************************************************************************************************
    #   **
    #   ** **********************************************************************************************************************************************************
    try:
        if invoice_lines and re.search(rf'^Gift message$', invoice_lines[0]):
            invoice_lines.pop(0)

            line_count: int = 0
            gift_message: list[str] = []

            while invoice_lines and re.search(rf'^Private notes$', invoice_lines[0]) is None and re.search(
                    rf'^Note from buyer$', invoice_lines[0]) is None:
                line_count += 1

                pattern: str = rf'^(.+)$'
                pattern_match = re.search(pattern, invoice_lines[0], flags=re.I)

                if pattern_match:
                    gift_message.append(pattern_match.group(1).strip())
                    invoice_lines.pop(0)
                else:
                    invoice_lines.pop(0)

            db_order.gift_message = " ".join(gift_message).replace(";", ":")
        else:
            pass

        logger.debug(rf'GIFT MESSAGE: {db_order.gift_message}')

    except:
        logger.error(rf'GIFT MESSAGE PARSE ERROR: {sys.exc_info()[0]}')


def load_invoice_lines(p_file_name: str) -> list[str]:
    #   ** **********************************************************************************************************************************************************
    #   **
    #   ** **********************************************************************************************************************************************************
    invoice_line: str = ""
    invoice_lines: list[str] = []

    page_count: int = 0
    line_count: int = 0

    try:
        invoice_file = open(p_file_name, "rb")
        invoice_viewer: SimplePDFViewer = SimplePDFViewer(invoice_file)

        for page in invoice_viewer:
            page_count = page_count + 1

            for invoice_line in page.strings:

                if re.search(rf'^Do the green thing$', invoice_line) or re.search(
                        rf'^Reuse this paper to make origami, confetti$', invoice_line) or re.search(
                        rf'^or your next to-do list.$', invoice_line):
                    pass
                else:
                    line_count = line_count + 1
                    invoice_lines.append(invoice_line)

                    logger.debug(rf'LINE-{line_count}:{invoice_line}')

        invoice_file.close()

        return (invoice_lines)
    except:
        logger.error(rf'LOAD INVOICE LINES ERROR: {sys.exc_info()[0]}')
        return (None)


if __name__ == '__main__':
    #   ** ************************************************************************************************************************************************************
    #   ** Mainline code
    #   ** ************************************************************************************************************************************************************

    #   Vertical Process Segration Constants
    UNPROCESSED: int = 0
    PRE_MERGE: int = 1
    POST_MERGE: int = 2

    #   ** Horizontal Process Segration Constants
    UNALLOCATED: int = 0
    NEXT_DAY: int = 1
    USA_MULTI: int = 2
    USA_NON_MULTI: int = 3
    GB_MULTI: int = 4
    GB_NON_MULTI: int = 5

    non_diacritics: str = rf'a-zA-Z'
    diacritics: str = rf'àèìòùÀÈÌÒÙáéíóúýÁÉÍÓÚÝâêîôûÂÊÎÔÛãñõÃÑÕäëïöüÿÄËÏÖÜŸåÅæÆœŒçÇðÐøØ¿¡ß'

    success: bool = False

    sys_settings: SystemSettings = SystemSettings()

    invoice_path_in: str = os.path.join(sys_settings.etsy_target_invoice_path, sys_settings.process_date)
    message_path_in: str = os.path.join(sys_settings.etsy_target_gift_receipt_path, sys_settings.process_date)
    combined_path_out: str = os.path.join(sys_settings.etsy_target_invoice_path, sys_settings.process_date)

    database: str = sys_settings.database_path

    invoice_file_name: str = None

    sales_channel_id: str = None
    order_no: str = None

    invoice_count: int = 0

    logger: logging.Logger = get_custom_logger('DATA EXTRACTION')

    usa_order_count: int = 0
    usa_post: USPost = USPost()

    conn = create_connection(database)

    with conn:
        cursor = conn.cursor()
        cursor.execute('''PRAGMA foreign_keys = ON''')
        cursor.close()

        db_order: NewOrder = NewOrder()
        db_orders: list[NewOrder] = get_orders_by_status(conn, UNPROCESSED)

        for db_order in db_orders:

            try:
                invoice_count += 1
                logger.info(
                    rf'{str(invoice_count).zfill(4)}, {db_order.sales_channel_id}-{db_order.order_no} - Extracting Order Details from PDF')

                full_file_name: str = os.path.join(invoice_path_in,
                                                   rf'{db_order.sales_channel_id}_{db_order.order_no}.pdf')
                invoice_line: str = ""
                invoice_lines: list[str] = load_invoice_lines(full_file_name)

                if len(invoice_lines) > 1:
                    #                   ## =================================================================================================================================================================
                    ## Trap potential error for invoices with missing dispatch date
                    ## =================================================================================================================================================================
                    success = get_order_no()

                    get_buyer_details() if success else None
                    get_marked_as_gift() if success else None
                    get_gift_message_included() if success else None
                    get_delivery_recipient() if success else None
                    get_delivery_address() if success else None

                    get_scheduled_dispatch_date() if success else None
                    get_sales_channel_id() if success else None
                    get_order_date() if success else None
                    get_payment_method() if success else None

                    if db_order.delivery_country_code == "GB":
                        get_delivery_details_domestic()
                        #                       db_order.delivery_carrier_order_ref = str(get_carrier_order_ref(db_order.order_no))
                        db_order.delivery_carrier_order_ref = db_order.order_no
                    #                       time.sleep(0.2)
                    else:
                        get_delivery_details_international()
                        db_order.delivery_carrier_order_ref = db_order.order_no
                    #                        db_order.delivery_carrier_order_ref = rf'{db_order.sales_channel_id}-{db_order.order_no}'
                    #                       o_Order.delivery_carrier_order_ref = rf'000{db_order.order_no}'

                    get_number_of_items() if success else None

                    db_order_items: list[NewOrderItem] = []
                    order_item_count: int = 0

                    while invoice_lines and re.search(rf'^Item total$', invoice_lines[
                        0]) is None and order_item_count < db_order.number_of_items:
                        db_order_item: NewOrderItem = NewOrderItem()
                        order_item_count = order_item_count + 1
                        db_order_item.order_item_no = order_item_count
                        db_order_item.order_no = db_order.order_no
                        db_order_item.sales_channel_id = db_order.sales_channel_id
                        db_order_item.date_sold = db_order.sale_date
                        db_order_item.dispatch_priority = db_order.dispatch_priority
                        db_order_item.process_status = PRE_MERGE

                        get_item_listing_title() if success else None
                        get_item_sku() if success else None
                        get_item_variations() if success else None
                        get_item_personalisation() if success else None
                        get_item_quantity_price() if success else None

                        db_order_items.append(db_order_item)

                    get_item_total() if success else None
                    get_order_sub_totals() if success else None
                    get_order_total() if success else None
                    get_buyer_note() if success else None
                    get_private_note() if success else None
                    get_gift_message() if success else None

                    saved_product_material_code: str = 'XXX'
                    saved_product_type_code: str = 'XXX'
                    saved_product_design_code: str = 'UNKNOWN'
                    product_material_type_count: int = 0

                    for db_order_item in db_order_items:
                        product_material_type_count += 1

                        if db_order.multi_item_ind == 'N':
                            if db_order_item.product_material_code != saved_product_material_code or db_order_item.product_type_code != saved_product_type_code or db_order_item.product_design_code != saved_product_design_code or db_order_item.product_type_code in [
                                'HTLA6', 'CRLA6']:
                                saved_product_material_code = db_order_item.product_material_code
                                saved_product_type_code = db_order_item.product_type_code
                                saved_product_design_code = db_order_item.product_design_code

                                db_order.multi_item_ind = 'Y' if product_material_type_count > 1 or db_order_item.product_type_code in [
                                    'HTLA6', 'CRLA6', 'BDLM', 'SSTK'] else 'N'
                            else:
                                pass
                        else:
                            pass

                        if db_order_item.mergeable_ind == 'Y' and db_order.mergeable_ind == 'N':
                            db_order.mergeable_ind = 'Y'
                        else:
                            pass
                    #                   end - db_order_item in order_items:

                    for db_order_item in db_order_items:

                        if db_order.dispatch_priority == 10 and db_order.delivery_country_code != "US":
                            db_order.process_category = NEXT_DAY
                            db_order_item.process_category = NEXT_DAY

                            combined_path_out = os.path.join(invoice_path_in, 'NEXT_DAY')
                            os.mkdir(combined_path_out) if not os.path.exists(combined_path_out) else None

                            combined_path_out = os.path.join(combined_path_out,
                                                             rf'{db_order_item.product_material_code}_{db_order_item.product_type_code}')

                        elif db_order.multi_item_ind == "Y":
                            if db_order.delivery_country_code != "US":
                                db_order.process_category = GB_MULTI
                                db_order_item.process_category = GB_MULTI

                                combined_path_out = os.path.join(invoice_path_in, 'GB_MULTI')
                                os.mkdir(combined_path_out) if not os.path.exists(combined_path_out) else None

                                combined_path_out = os.path.join(combined_path_out,
                                                                 rf'{db_order_item.product_material_code}_{db_order_item.product_type_code}')
                            else:
                                db_order.process_category = USA_MULTI
                                db_order_item.process_category = USA_MULTI

                                combined_path_out = os.path.join(invoice_path_in, 'USA_MULTI')
                                os.mkdir(combined_path_out) if not os.path.exists(combined_path_out) else None

                                combined_path_out = os.path.join(combined_path_out,
                                                                 rf'{db_order_item.product_material_code}_{db_order_item.product_type_code}')

                        elif db_order.delivery_country_code == "US":
                            db_order.process_category = USA_NON_MULTI
                            db_order_item.process_category = USA_NON_MULTI

                            combined_path_out = os.path.join(invoice_path_in, 'USA_NON_MULTI')
                            os.mkdir(combined_path_out) if not os.path.exists(combined_path_out) else None

                            combined_path_out = os.path.join(combined_path_out,
                                                             rf'{db_order_item.product_material_code}_{db_order_item.product_type_code}')

                        #                        elif saved_product_material_code != '' and saved_product_type_code != '' and saved_product_material_code != 'XXX' and saved_product_type_code != 'XXX':
                        elif saved_product_material_code != '' and saved_product_type_code != '':
                            db_order.process_category = GB_NON_MULTI
                            db_order_item.process_category = GB_NON_MULTI

                            combined_path_out = os.path.join(invoice_path_in, 'GB_NON_MULTI')
                            os.mkdir(combined_path_out) if not os.path.exists(combined_path_out) else None

                            combined_path_out = os.path.join(combined_path_out,
                                                             rf'{db_order_item.product_material_code}_{db_order_item.product_type_code}')

                        else:
                            combined_path_out = os.path.join(invoice_path_in, 'UNALLOCATED')
                            db_order.process_category = UNALLOCATED
                            db_order_item.process_category = UNALLOCATED

                        db_order_item.save(conn)
                        logger.debug(rf'{db_order_item}')
                    #                   end - db_order_item in order_items:

                    country_code: CountryCode = CountryCode(db_order.delivery_country_code)
                    if db_order.delivery_country_code == "US":
                        usa_order_count += 1
                        usa_post.add_order(
                            None
                            , db_order.delivery_recipient
                            , db_order.delivery_street_01
                            , db_order.delivery_street_02
                            , db_order.delivery_city
                            , db_order.delivery_state
                            , db_order.delivery_zipcode
                            , country_code.name
                            , rf'{db_order.sales_channel_id}-{db_order.order_no}')
                    else:
                        pass

                    if db_order.mergeable_ind == 'N':
                        success: bool = add_invoice_annotations(invoice_path_in, message_path_in, combined_path_out,
                                                                red)
                    else:
                        success: bool = add_invoice_annotations(invoice_path_in, message_path_in, combined_path_out,
                                                                green)

                    db_order.process_status = PRE_MERGE
                    logger.debug(rf'{db_order}')
                    db_order.update(conn)
                else:
                    logger.error(rf'{db_order.sales_channel_id}-{db_order.order_no}: Invoice Invalid')

            except:
                logger.error(rf'{db_order.sales_channel_id}-{db_order.order_no}: {sys.exc_info()[0]}')

            os.remove(full_file_name)
        #       end - db_order in db_orders:

        if usa_order_count > 0:
            usa_post.create_spreadsheet()
        else:
            pass

        # Ensure database tables are up to date before generating .txt files
        subprocess.run(["python", os.path.join(MERGE_DIR, "populate_merge_items.py")])
        subprocess.run(["python", os.path.join(MERGE_DIR, "populate_production_items.py")])
        subprocess.run(["python", os.path.join(MERGE_DIR, "populate_product_design_listings.py")])
        subprocess.run(["python", os.path.join(MERGE_DIR, "populate_pdl_material_variations.py")])
        subprocess.run(["python", os.path.join(MERGE_DIR, "generate_txt_files.py")])

        material_product_item_list: list[str] = summarise_distinct_material_product_types(conn, PRE_MERGE)
        material_product_item: str = None

        if len(material_product_item_list) > 0:
            logger.info(rf'========================================================================')
            logger.info(rf'Database Loaded Successfully - Order Item Count By Material-Product Type')
            logger.info(rf'========================================================================')

            for material_product_item in material_product_item_list:
                logger.info(rf'{material_product_item}')
        else:
            logger.warning(rf'No Orders To Load')
