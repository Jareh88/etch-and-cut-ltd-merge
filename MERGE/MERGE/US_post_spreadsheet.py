import os
import time

import pandas as pd
from dotenv import load_dotenv
from styleframe import StyleFrame

from new_order import *
from system_settings import *


class EtsyUSSpreadsheet:
    """
    A class for creating a spreadsheet for US orders from Etsy Data

    **Initialise the class**\n
    `spreadsheet = EtsyUSSpreadsheet()`

    **Add an order**\n
    order1 = Order()\n
    # Add order details\n
    spreadsheet.add_order(order1)

    **Create a spreadsheet**\n
    `spreadsheet.create_spreadsheet()`

    **Create a spreadsheet with weights**\n
    weights = ["1", "2", "3"]\n
    spreadsheet.create_spreadsheet(weights)
    """

    def __init__(self) -> None:
        """
        Initialisation Function to set up variables used throughout the class.

        :return:
        """
        load_dotenv()
        o_SystemSettings = SystemSettings()
        self.custom_path = o_SystemSettings.us_post_spreadsheet_path

        # Define the column names as a set
        self.columns = ['Weight', 'Delivery Name', 'Delivery Address1', 'Delivery Address2', 'Delivery City',
                        'Delivery State', 'Delivery Zipcode', 'Delivery Country', 'Order ID']
        # Create an empty DataFrame with the defined columns
        df = pd.DataFrame(columns=self.columns)
        self.data_frame = df

    def add_order(self, p_Weight, p_DeliveryRecipient, p_DeliveryStreet01, p_DeliveryStreet02, p_DeliveryCity, p_DeliveryState, p_DeliveryZipcode, p_DeliveryCountryCode, p_OrderNo):
        """
        A method to add an order to the class' data frame.

        :param new_order: The order object to be added
        :return:
        """
        # Create a new row
        new_row = pd.Series({
            "Weight"            : p_Weight,
            "Delivery Name"     : p_DeliveryRecipient,
            "Delivery Address1" : p_DeliveryStreet01,
            "Delivery Address2" : p_DeliveryStreet02,
            "Delivery City"     : p_DeliveryCity,
            "Delivery State"    : p_DeliveryState,
            "Delivery Zipcode"  : p_DeliveryZipcode,
            "Delivery Country"  : p_DeliveryCountryCode,
            "Order ID"          : p_OrderNo
        })
        # Add the new row to the DataFrame
        self.data_frame = pd.concat([self.data_frame, new_row.to_frame().T], ignore_index=True)


    def create_spreadsheet(self, weights: list[str] = None) -> None:
        """
        A method to create the final spreadsheet and add any item weights that are passed to it.

        :param weights: An optional list of strings containing weights for the items in the order they have been added.
        :return:
        """
        # If there are weights to add
#        if weights:
            # Create a new data frame
#            new_data_frame = pd.DataFrame({"Weight": weights})
            # Update the class' data frame with the new weight information
#            self.data_frame.update(new_data_frame)
        # Set the index numbers as the Order ID column
        self.data_frame.set_index('Delivery Name')
#       self.data_frame = self.data_frame.set_index('Delivery Name')
        # Assign the column titles
        self.data_frame.set_axis(self.columns, axis="columns")
        # Sort by delivery name
        self.data_frame.sort_values(by=['Delivery Name'], ascending=True)
#        self.data_frame.sort_values(by=['Delivery Name'], axis=0, ascending=True, inplace=False, kind='quicksort', na_position='last', ignore_index=False, key=None)

        print(self.custom_path)

        # Create the file path + name
        str_FileName = time.strftime("%Y%m%d_US Orders")
        str_FullFileName = os.path.join (self.custom_path, f'''{str_FileName}.xlsx''').replace("\\","/")
        
        # Create the Excel writer
        excel_writer = StyleFrame.ExcelWriter(str_FullFileName)
        # Format and write the data to the Excel sheet
        sf = StyleFrame(self.data_frame)
        sf.to_excel(excel_writer=excel_writer, best_fit=self.columns)
        excel_writer.save()
