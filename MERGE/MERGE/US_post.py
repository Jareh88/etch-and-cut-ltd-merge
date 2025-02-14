import os
import time

import pandas as pd
import openpyxl

from collections        import OrderedDict
from operator           import getitem

from system_settings    import *


class USPost:
    """
    A class for creating a spreadsheet for US orders from Etsy Data
    """

    def __init__(self) -> None:
        """
        Initialisation Function to set up variables used throughout the class.
        """
        o_SystemSettings = SystemSettings()

        self.spreadsheet_path = o_SystemSettings.us_post_spreadsheet_path
        self.file_name        = "Etail_US_Orders"
        self.path_file_name   = os.path.join (self.spreadsheet_path, f'''{self.file_name}.xlsx''').replace("\\","/")

        self.column_names = [
                'Weight'
            ,   'Delivery Name'
            ,   'Delivery Address1'
            ,   'Delivery Address2'
            ,   'Delivery City'
            ,   'Delivery State'
            ,   'Delivery Zipcode'
            ,   'Delivery Country'
            ,   'Order ID'
        ]

        self.weight            = []
        self.delivery_name     = []
        self.delivery_address1 = []
        self.delivery_address2 = []
        self.delivery_city     = []
        self.delivery_state    = []
        self.delivery_zipcode  = []
        self.delivery_country  = []
        self.order_id          = []


        try:
            df_ExistingData   = pd.read_excel(self.path_file_name)
            dict_ExistingData = df_ExistingData.to_dict(orient='list')

            df_ExistingData = pd.DataFrame (
                data        = dict_ExistingData
            ,   columns     = self.column_names
            )

            self.weight            = df_ExistingData['Weight'].values.tolist()
            self.delivery_name     = df_ExistingData['Delivery Name'].values.tolist()
            self.delivery_address1 = df_ExistingData['Delivery Address1'].values.tolist()
            self.delivery_address2 = df_ExistingData['Delivery Address2'].values.tolist()
            self.delivery_city     = df_ExistingData['Delivery City'].values.tolist()
            self.delivery_state    = df_ExistingData['Delivery State'].values.tolist()
            self.delivery_zipcode  = df_ExistingData['Delivery Zipcode'].values.tolist()
            self.delivery_country  = df_ExistingData['Delivery Country'].values.tolist()
            self.order_id          = df_ExistingData['Order ID'].values.tolist()

            print(f'''Existing spreadsheet loaded: {self.order_id}''')
        except:
            pass


    def add_order(self, p_Weight, p_DeliveryRecipient, p_DeliveryStreet01, p_DeliveryStreet02, p_DeliveryCity, p_DeliveryState, p_DeliveryZipcode, p_DeliveryCountryCode, p_OrderNo):
        """
        A method to add an order to the list object
        """
        if p_OrderNo in self.order_id:
            pass
        else:
            self.weight.append(p_Weight)
            self.delivery_name.append(p_DeliveryRecipient.title())
            self.delivery_address1.append(p_DeliveryStreet01)
            self.delivery_address2.append(p_DeliveryStreet02)
            self.delivery_city.append(p_DeliveryCity)
            self.delivery_state.append(p_DeliveryState)
            self.delivery_zipcode.append(p_DeliveryZipcode)
            self.delivery_country.append(p_DeliveryCountryCode)
            self.order_id.append(p_OrderNo)


    def create_spreadsheet(self):
        """
        A method to create the final spreadsheet
        """
        dict_NewData = {
            'Weight'           : self.weight
        ,   'Delivery Name'    : self.delivery_name
        ,   'Delivery Address1': self.delivery_address1
        ,   'Delivery Address2': self.delivery_address2
        ,   'Delivery City'    : self.delivery_city
        ,   'Delivery State'   : self.delivery_state
        ,   'Delivery Zipcode' : self.delivery_zipcode
        ,   'Delivery Country' : self.delivery_country
        ,   'Order ID'         : self.order_id
        }

        df_NewData = pd.DataFrame (
            data    = dict_NewData
        ,   index   = self.delivery_name
        ,   columns = self.column_names
        )

        o_SortedDateFrame = df_NewData.sort_values(by=['Delivery Name'])
        o_SortedDateFrame.to_excel(self.path_file_name, index=False, header=True)

        print(self.spreadsheet_path)