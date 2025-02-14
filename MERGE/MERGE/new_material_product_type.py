import csv, sys, sqlite3, os
from datetime import datetime
from dataclasses import dataclass

from system_settings import *


class NewMaterialProductType:
    """MaterialProductType Class"""


#   ** ***************************************************************************************************************************************************************************************************************
#   ** CLASS: NewMaterialProductType
#   ** ***************************************************************************************************************************************************************************************************************
@dataclass
class NewMaterialProductType:
    """NewMaterialProductType Class"""

    material_code: str = None
    material_desc: str = None

    product_type_code: str = None
    product_type_desc: str = None

    merge_priority: int = 0
    merge_material_consolidation: str = 'Y'

    merge_plate_size: int = 0
    merge_plate_date: datetime = None
    merge_plate_number: int = 0
    merge_plate_item_number: int = 0
    merge_plate_item_number_increment: int = 1
    merge_plate_order_consolidation: str = 'Y'

    merge_ind: str = 'N'

    def save(self, conn):
        #   ** *****************************************************************************************************************************************************
        #   ** Insert material_product_types database record
        #   ** *****************************************************************************************************************************************************
        cursor = conn.cursor()
        sql = '''
            INSERT
                INTO material_product_types
                (
                    material_product_type_id
                ,   material_code, material_desc
                ,   product_type_code, product_type_desc
                ,   merge_priority, merge_material_consolidation 
                ,   merge_plate_size, merge_plate_date, merge_plate_number, merge_plate_item_number, merge_plate_item_number_increment, merge_plate_order_consolidation
                ,   merge_ind
                )
            VALUES(
                NULL
            ,   ?, ?
            ,   ?, ?
            ,   ?, ?
            ,   ?, ?, ?, ?, ?, ?
            ,   ?
            )
            '''
        cursor.execute(
            sql,
            (
                self.material_code, self.material_desc
                , self.product_type_code, self.product_type_desc
                , self.merge_priority, self.merge_material_consolidation
                , self.merge_plate_size, self.merge_plate_date, self.merge_plate_number, self.merge_plate_item_number,
                self.merge_plate_item_number_increment, self.merge_plate_order_consolidation
                , self.merge_ind
            ))
        if cursor:
            conn.commit()
            cursor.close()
        else:
            print("material_product_types table insert failed!")
            cursor.close()

    def update(self, conn):
        #   ** *****************************************************************************************************************************************************
        #   ** update material_product_types database record
        #   ** *****************************************************************************************************************************************************
        cursor = conn.cursor()
        sql = '''
            UPDATE material_product_types 
                SET
                    material_code =?, material_desc =?
                ,   product_type_code =?, product_type_desc =?
                ,   merge_priority =?, merge_material_consolidation =?
                ,   merge_plate_size =?, merge_plate_date =?, merge_plate_number =?, merge_plate_item_number =?, merge_plate_item_number_increment =?, merge_plate_order_consolidation =?
                ,   merge_ind =?
                WHERE 
                    material_product_types.material_code     =? AND
                    material_product_types.product_type_code =?
            '''
        cursor.execute(
            sql,
            (
                self.material_code, self.material_desc
                , self.product_type_code, self.product_type_desc
                , self.merge_priority, self.merge_material_consolidation
                , self.merge_plate_size, self.merge_plate_date, self.merge_plate_number, self.merge_plate_item_number,
                self.merge_plate_item_number_increment, self.merge_plate_order_consolidation
                , self.merge_ind
                ,
                self.material_code, self.product_type_code,)
        )
        if cursor:
            conn.commit()
            cursor.close()
        else:
            print("material_product_types database table update failed!")
            cursor.close()


def get_MaterialProductType(conn, material_code: str, product_type_code: str) -> NewMaterialProductType:
    # ** ***********************************************************************************************************************************
    # ** Get material_product_type database record for a particular material_code and product_code combination
    # ** ***********************************************************************************************************************************
    cursor = conn.cursor()
    sql = '''
        SELECT
            material_code, material_desc
        ,   product_type_code, product_type_desc
        ,   merge_priority, merge_material_consolidation 
        ,   merge_plate_size, merge_plate_date, merge_plate_number, merge_plate_item_number, merge_plate_item_number_increment, merge_plate_order_consolidation
        ,   merge_ind
        FROM
            material_product_types
        WHERE 
            material_product_types.material_code     =? AND
            material_product_types.product_type_code =? 
        LIMIT 
            1
        '''
    cursor.execute(sql, (material_code, product_type_code,))
    row = cursor.fetchone()
    o_object = NewMaterialProductType()

    if row is not None:
        db_material_product_type: NewMaterialProductType = NewMaterialProductType()

        db_material_product_type.material_code = row[0]
        db_material_product_type.material_desc = row[1]

        db_material_product_type.product_type_code = row[2]
        db_material_product_type.product_type_desc = row[3]

        db_material_product_type.merge_priority = row[4]
        db_material_product_type.merge_material_consolidation = row[5]

        db_material_product_type.merge_plate_size = row[6]
        db_material_product_type.merge_plate_date = row[7]
        db_material_product_type.merge_plate_number = row[8]
        db_material_product_type.merge_plate_item_number = row[9]
        db_material_product_type.merge_plate_item_number_increment = row[10]
        db_material_product_type.merge_plate_order_consolidation = row[11]

        db_material_product_type.merge_ind = row[12]

        return (db_material_product_type)
    else:
        return (None)


def get_MaterialProductTypes(conn) -> list[NewMaterialProductType]:
    # ** ***********************************************************************************************************************************
    # **  Get material_product_type database records for a particular material_code
    # ** ***********************************************************************************************************************************
    cursor = conn.cursor()
    sql = '''
        SELECT
            material_code, material_desc
        ,   product_type_code, product_type_desc
        ,   merge_priority, merge_material_consolidation
        ,   merge_plate_size, merge_plate_date, merge_plate_number, merge_plate_item_number, merge_plate_item_number_increment, merge_plate_order_consolidation
        ,   merge_ind
        FROM
            material_product_types
        ORDER BY
            material_product_types.material_code, product_type_code
        '''
    cursor.execute(sql, ())
    rows = cursor.fetchall()
    db_material_product_types: list[NewMaterialProductType] = []

    if rows is not None:
        for row in rows:
            db_material_product_type: NewMaterialProductType = NewMaterialProductType()

            db_material_product_type.material_code = row[0]
            db_material_product_type.material_desc = row[1]

            db_material_product_type.product_type_code = row[2]
            db_material_product_type.product_type_desc = row[3]

            db_material_product_type.merge_priority = row[4]
            db_material_product_type.merge_material_consolidation = row[5]

            db_material_product_type.merge_plate_size = row[6]
            db_material_product_type.merge_plate_date = row[7]
            db_material_product_type.merge_plate_number = row[8]
            db_material_product_type.merge_plate_item_number = row[9]
            db_material_product_type.merge_plate_item_number_increment = row[10]
            db_material_product_type.merge_plate_order_consolidation = row[11]

            db_material_product_type.merge_ind = row[12]

            db_material_product_types.append(db_material_product_type)
        cursor.close()
        return (db_material_product_types)
    else:
        cursor.close()
        return (None)


def get_MaterialProductTypes(conn, material_code: str = "%", product_type_code: str = "%") -> list[
    NewMaterialProductType]:
    # ** ***********************************************************************************************************************************
    # ** Get material_product_type database records for a particular material_code
    # ** ***********************************************************************************************************************************
    cursor = conn.cursor()
    sql = '''
        SELECT
            material_code, material_desc
        ,   product_type_code, product_type_desc
        ,   merge_priority, merge_material_consolidation
        ,   merge_plate_size, merge_plate_date, merge_plate_number, merge_plate_item_number, merge_plate_item_number_increment, merge_plate_order_consolidation
        FROM
            material_product_types
        WHERE
            material_product_types.material_code      =? AND
            material_product_types.product_type_codes =?
        ORDER BY
            material_product_types.product_type_code
        '''
    cursor.execute(sql, (material_code, product_type_code))
    rows = cursor.fetchall()
    db_material_product_types: list[NewMaterialProductType] = []

    if rows is not None:
        for row in rows:
            db_material_product_type: NewMaterialProductType = NewMaterialProductType()

            db_material_product_type.material_code = row[0]
            db_material_product_type.material_desc = row[1]

            db_material_product_type.product_type_code = row[2]
            db_material_product_type.product_type_desc = row[3]

            db_material_product_type.merge_priority = row[4]
            db_material_product_type.merge_material_consolidation = row[5]

            db_material_product_type.merge_plate_size = row[6]
            db_material_product_type.merge_plate_date = row[7]
            db_material_product_type.merge_plate_number = row[8]
            db_material_product_type.merge_plate_item_number = row[9]
            db_material_product_type.merge_plate_item_number_increment = row[10]
            db_material_product_type.merge_plate_order_consolidation = row[11]

            db_material_product_type.merge_ind = row[12]

            db_material_product_types.append(db_material_product_type)
        cursor.close()
        return (db_material_product_types)
    else:
        cursor.close()
        return (None)


def create_DefaultMaterialProductTypes(conn):
    #   ** *********************************************************************************************************************************************
    #   ** Create initial defaul values for material product types
    #   ** *********************************************************************************************************************************************
    o_SystemSettings = SystemSettings()
    current_date = o_SystemSettings.process_date

    material_product_type: NewMaterialProductType = NewMaterialProductType()

    material_product_type.material_code = "CWS"
    material_product_type.material_desc = "Sublimated White Ceramic"
    material_product_type.product_type_code = "HHL"
    material_product_type.product_type_desc = "Single 72mm x 72mm Hanging Heart"
    material_product_type.merge_priority = 10
    material_product_type.merge_material_consolidation = 'N'
    material_product_type.merge_plate_size = 30
    material_product_type.merge_plate_date = current_date
    material_product_type.merge_plate_number = 1
    material_product_type.merge_plate_item_number = 1
    material_product_type.merge_plate_item_number_increment = 1
    material_product_type.merge_plate_order_consolidation = 'Y'
    material_product_type.merge_ind = 'Y'
    material_product_type.save(conn)

    material_product_type.product_type_code = "HCL"
    material_product_type.product_type_desc = "Single 72mm x 72mm Hanging Disc"
    material_product_type.merge_priority = 10
    material_product_type.merge_material_consolidation = 'N'
    material_product_type.merge_plate_size = 30
    material_product_type.merge_plate_date = current_date
    material_product_type.merge_plate_number = 1
    material_product_type.merge_plate_item_number = 1
    material_product_type.merge_plate_item_number_increment = 1
    material_product_type.merge_plate_order_consolidation = 'Y'
    material_product_type.merge_ind = 'Y'
    material_product_type.save(conn)

    material_product_type.product_type_code = "MGL"
    material_product_type.product_type_desc = "Single 11oz Mug"
    material_product_type.merge_priority = 10
    material_product_type.merge_material_consolidation = 'N'
    material_product_type.merge_plate_size = 16
    material_product_type.merge_plate_date = current_date
    material_product_type.merge_plate_number = 1
    material_product_type.merge_plate_item_number = 1
    material_product_type.merge_plate_item_number_increment = 1
    material_product_type.merge_plate_order_consolidation = 'Y'
    material_product_type.merge_ind = 'Y'
    material_product_type.save(conn)

    material_product_type.product_type_code = "CSL"
    material_product_type.product_type_desc = "Single 107mm x 107mm Coaster"
    material_product_type.merge_priority = 10
    material_product_type.merge_material_consolidation = 'N'
    material_product_type.merge_plate_size = 16
    material_product_type.merge_plate_date = current_date
    material_product_type.merge_plate_number = 1
    material_product_type.merge_plate_item_number = 1
    material_product_type.merge_plate_item_number_increment = 1
    material_product_type.merge_plate_order_consolidation = 'Y'
    material_product_type.merge_ind = 'Y'
    material_product_type.save(conn)

    material_product_type.product_type_code = "MCL"
    material_product_type.product_type_desc = "Single 11oz Mug and Single 107mm x 107mm Coaster Set"
    material_product_type.merge_priority = 10
    material_product_type.merge_material_consolidation = 'N'
    material_product_type.merge_plate_size = 16
    material_product_type.merge_plate_date = current_date
    material_product_type.merge_plate_number = 1
    material_product_type.merge_plate_item_number = 1
    material_product_type.merge_plate_item_number_increment = 1
    material_product_type.merge_plate_order_consolidation = 'Y'
    material_product_type.merge_ind = 'Y'
    material_product_type.save(conn)

    material_product_type.material_code = "MWS"
    material_product_type.material_desc = "Sublimated White Metal"
    material_product_type.product_type_code = "BMK"
    material_product_type.product_type_desc = "Single 150mm x 45mm Bookmark"
    material_product_type.merge_priority = 10
    material_product_type.merge_material_consolidation = 'N'
    material_product_type.merge_plate_size = 10
    material_product_type.merge_plate_date = current_date
    material_product_type.merge_plate_number = 1
    material_product_type.merge_plate_item_number = 1
    material_product_type.merge_plate_item_number_increment = 1
    material_product_type.merge_plate_order_consolidation = 'Y'
    material_product_type.merge_ind = 'Y'
    material_product_type.save(conn)

    material_product_type.material_code = "ACC"
    material_product_type.material_desc = "Clear Cast Acrylic"
    material_product_type.product_type_code = "BLK"
    material_product_type.product_type_desc = "Single 100mm x 100mm x 12mm Block"
    material_product_type.merge_priority = 10
    material_product_type.merge_material_consolidation = 'N'
    material_product_type.merge_plate_size = 15
    material_product_type.merge_plate_date = current_date
    material_product_type.merge_plate_number = 1
    material_product_type.merge_plate_item_number = 1
    material_product_type.merge_plate_item_number_increment = 1
    material_product_type.merge_plate_order_consolidation = 'Y'
    material_product_type.merge_ind = 'Y'
    material_product_type.save(conn)

    material_product_type.material_code = "FCS"
    material_product_type.material_desc = "Sublimated Canvas Fabric"
    material_product_type.product_type_code = "CSH"
    material_product_type.product_type_desc = "Single 400mm x 400mm Cushion"
    material_product_type.merge_priority = 10
    material_product_type.merge_material_consolidation = 'N'
    material_product_type.merge_plate_size = 4
    material_product_type.merge_plate_date = current_date
    material_product_type.merge_plate_number = 1
    material_product_type.merge_plate_item_number = 1
    material_product_type.merge_plate_item_number_increment = 1
    material_product_type.merge_plate_order_consolidation = 'Y'
    material_product_type.merge_ind = 'Y'
    material_product_type.save(conn)

    material_product_type.material_code = "FCS"
    material_product_type.material_desc = "Sublimated Canvas Fabric"
    material_product_type.product_type_code = "SKM"
    material_product_type.product_type_desc = "Single 480mm x 380mm Sack"
    material_product_type.merge_priority = 10
    material_product_type.merge_material_consolidation = 'N'
    material_product_type.merge_plate_size = 10
    material_product_type.merge_plate_date = current_date
    material_product_type.merge_plate_number = 1
    material_product_type.merge_plate_item_number = 1
    material_product_type.merge_plate_item_number_increment = 1
    material_product_type.merge_plate_order_consolidation = 'Y'
    material_product_type.merge_ind = 'Y'
    material_product_type.save(conn)

    material_product_type.material_code = "FCS"
    material_product_type.material_desc = "Sublimated Canvas Fabric"
    material_product_type.product_type_code = "STK"
    material_product_type.product_type_desc = "Single Stocking"
    material_product_type.merge_priority = 10
    material_product_type.merge_material_consolidation = 'N'
    material_product_type.merge_plate_size = 10
    material_product_type.merge_plate_date = current_date
    material_product_type.merge_plate_number = 1
    material_product_type.merge_plate_item_number = 1
    material_product_type.merge_plate_item_number_increment = 1
    material_product_type.merge_plate_order_consolidation = 'Y'
    material_product_type.merge_ind = 'Y'
    material_product_type.save(conn)

    material_product_type.material_code = "WFOV"
    material_product_type.material_desc = "Engraved French Oak Veneer Frame"
    material_product_type.product_type_code = "FRM"
    material_product_type.product_type_desc = "Single 7 x 5 or 6 x 4 Frame"
    material_product_type.merge_priority = 10
    material_product_type.merge_material_consolidation = 'N'
    material_product_type.merge_plate_size = 8
    material_product_type.merge_plate_date = current_date
    material_product_type.merge_plate_number = 1
    material_product_type.merge_plate_item_number = 1
    material_product_type.merge_plate_item_number_increment = 1
    material_product_type.merge_plate_order_consolidation = 'Y'
    material_product_type.merge_ind = 'Y'
    material_product_type.save(conn)

    material_product_type.material_code = "WFOV"
    material_product_type.material_desc = "Engraved French Oak Veneer Frame"
    material_product_type.product_type_code = "FRMMP"
    material_product_type.product_type_desc = "Single 7 x 5 Portrait Frame"
    material_product_type.merge_priority = 10
    material_product_type.merge_material_consolidation = 'N'
    material_product_type.merge_plate_size = 8
    material_product_type.merge_plate_date = current_date
    material_product_type.merge_plate_number = 1
    material_product_type.merge_plate_item_number = 1
    material_product_type.merge_plate_item_number_increment = 1
    material_product_type.merge_plate_order_consolidation = 'Y'
    material_product_type.merge_ind = 'Y'
    material_product_type.save(conn)

    material_product_type.material_code = "WFOV"
    material_product_type.material_desc = "Engraved French Oak Veneer Frame"
    material_product_type.product_type_code = "FRMML"
    material_product_type.product_type_desc = "Single 7 x 5 Landscape Frame"
    material_product_type.merge_priority = 10
    material_product_type.merge_material_consolidation = 'N'
    material_product_type.merge_plate_size = 8
    material_product_type.merge_plate_date = current_date
    material_product_type.merge_plate_number = 1
    material_product_type.merge_plate_item_number = 1
    material_product_type.merge_plate_item_number_increment = 1
    material_product_type.merge_plate_order_consolidation = 'Y'
    material_product_type.merge_ind = 'Y'
    material_product_type.save(conn)

    material_product_type.material_code = "WFOV"
    material_product_type.material_desc = "Engraved French Oak Veneer Frame"
    material_product_type.product_type_code = "FRMSP"
    material_product_type.product_type_desc = "Single 6 x 4 Portrait Frame"
    material_product_type.merge_priority = 10
    material_product_type.merge_material_consolidation = 'N'
    material_product_type.merge_plate_size = 8
    material_product_type.merge_plate_date = current_date
    material_product_type.merge_plate_number = 1
    material_product_type.merge_plate_item_number = 1
    material_product_type.merge_plate_item_number_increment = 1
    material_product_type.merge_plate_order_consolidation = 'Y'
    material_product_type.merge_ind = 'Y'
    material_product_type.save(conn)

    material_product_type.material_code = "WFOV"
    material_product_type.material_desc = "Engraved French Oak Veneer Frame"
    material_product_type.product_type_code = "FRMSL"
    material_product_type.product_type_desc = "Single 6 x 4 Landscape Frame"
    material_product_type.merge_priority = 10
    material_product_type.merge_material_consolidation = 'N'
    material_product_type.merge_plate_size = 8
    material_product_type.merge_plate_date = current_date
    material_product_type.merge_plate_number = 1
    material_product_type.merge_plate_item_number = 1
    material_product_type.merge_plate_item_number_increment = 1
    material_product_type.merge_plate_order_consolidation = 'Y'
    material_product_type.merge_ind = 'Y'
    material_product_type.save(conn)

    material_product_type.material_code = "WCHV"
    material_product_type.material_desc = "Engraved Cherrywood Veneer Hanging Paw Print Plaque"
    material_product_type.product_type_code = "HPPP"
    material_product_type.product_type_desc = "Single Plaque"
    material_product_type.merge_priority = 10
    material_product_type.merge_material_consolidation = 'N'
    material_product_type.merge_plate_size = 8
    material_product_type.merge_plate_date = current_date
    material_product_type.merge_plate_number = 1
    material_product_type.merge_plate_item_number = 1
    material_product_type.merge_plate_item_number_increment = 1
    material_product_type.merge_plate_order_consolidation = 'Y'
    material_product_type.merge_ind = 'Y'
    material_product_type.save(conn)

    material_product_type.material_code = "CWT"
    material_product_type.material_desc = "Printed Greetings Card"
    material_product_type.product_type_code = "6X6"
    material_product_type.product_type_desc = "Single 148 x 148 mm Card"
    material_product_type.merge_priority = 10
    material_product_type.merge_material_consolidation = 'N'
    material_product_type.merge_plate_size = 50
    material_product_type.merge_plate_date = current_date
    material_product_type.merge_plate_number = 1
    material_product_type.merge_plate_item_number = 1
    material_product_type.merge_plate_item_number_increment = 1
    material_product_type.merge_plate_order_consolidation = 'Y'
    material_product_type.merge_ind = 'Y'
    material_product_type.save(conn)

    material_product_type.material_code = "AFE"
    material_product_type.material_desc = "Frosted Acrylic (Extruded)"
    material_product_type.product_type_code = "RCL"
    material_product_type.product_type_desc = "Single 80 x 80 mm Hanging Disc"
    material_product_type.merge_priority = 10
    material_product_type.merge_material_consolidation = 'N'
    material_product_type.merge_plate_size = 28
    material_product_type.merge_plate_date = current_date
    material_product_type.merge_plate_number = 1
    material_product_type.merge_plate_item_number = 1
    material_product_type.merge_plate_item_number_increment = 1
    material_product_type.merge_plate_order_consolidation = 'Y'
    material_product_type.merge_ind = 'Y'
    material_product_type.save(conn)

    material_product_type.material_code = "CWT"
    material_product_type.material_desc = "White Thin Card"
    material_product_type.product_type_code = "PLC"
    material_product_type.product_type_desc = "Single 100 x 90 Place Setting Card"
    material_product_type.merge_priority = 10
    material_product_type.merge_material_consolidation = 'N'
    material_product_type.merge_plate_size = 600
    material_product_type.merge_plate_date = current_date
    material_product_type.merge_plate_number = 1
    material_product_type.merge_plate_item_number = 1
    material_product_type.merge_plate_item_number_increment = 1
    material_product_type.merge_plate_order_consolidation = 'N'
    material_product_type.merge_ind = 'Y'
    material_product_type.save(conn)

    material_product_type.material_code = "CWT"
    material_product_type.material_desc = "White Thin Card"
    material_product_type.product_type_code = "A6"
    material_product_type.product_type_desc = "Single 105 x 148 (A6) Save The Date Card/Envelope"
    material_product_type.merge_priority = 10
    material_product_type.merge_material_consolidation = 'N'
    material_product_type.merge_plate_size = 300
    material_product_type.merge_plate_date = current_date
    material_product_type.merge_plate_number = 1
    material_product_type.merge_plate_item_number = 1
    material_product_type.merge_plate_item_number_increment = 1
    material_product_type.merge_plate_order_consolidation = 'Y'
    material_product_type.merge_ind = 'Y'
    material_product_type.save(conn)

    material_product_type.material_code = "AFE"
    material_product_type.material_desc = "Frosted Acrylic"
    material_product_type.product_type_code = "CKT"
    material_product_type.product_type_desc = "Single 105 x 180 Wedding Cake Topper"
    material_product_type.merge_priority = 10
    material_product_type.merge_material_consolidation = 'N'
    material_product_type.merge_plate_size = 10
    material_product_type.merge_plate_date = current_date
    material_product_type.merge_plate_number = 1
    material_product_type.merge_plate_item_number = 1
    material_product_type.merge_plate_item_number_increment = 1
    material_product_type.merge_plate_order_consolidation = 'Y'
    material_product_type.merge_ind = 'Y'
    material_product_type.save(conn)

    material_product_type.material_code = "WOKV"
    material_product_type.material_desc = "Wooden Oak Veneer"
    material_product_type.product_type_code = "CRL"
    material_product_type.product_type_desc = "Single Save The Date Disc"
    material_product_type.merge_priority = 10
    material_product_type.merge_material_consolidation = 'Y'
    material_product_type.merge_plate_size = 300
    material_product_type.merge_plate_date = current_date
    material_product_type.merge_plate_number = 1
    material_product_type.merge_plate_item_number = 1
    material_product_type.merge_plate_item_number_increment = 1
    material_product_type.merge_plate_order_consolidation = 'Y'
    material_product_type.merge_ind = 'Y'
    material_product_type.save(conn)

    material_product_type.material_code = "WBEV"
    material_product_type.material_desc = "Wooden Beech Veneer"
    material_product_type.product_type_code = "CRL"
    material_product_type.product_type_desc = "Single Save The Date Disc"
    material_product_type.merge_priority = 10
    material_product_type.merge_material_consolidation = 'Y'
    material_product_type.merge_plate_size = 300
    material_product_type.merge_plate_date = current_date
    material_product_type.merge_plate_number = 1
    material_product_type.merge_plate_item_number = 1
    material_product_type.merge_plate_item_number_increment = 1
    material_product_type.merge_plate_order_consolidation = 'Y'
    material_product_type.merge_ind = 'Y'
    material_product_type.save(conn)

    material_product_type.material_code = "WOKV"
    material_product_type.material_desc = "Wooden Oak Veneer"
    material_product_type.product_type_code = "HTL"
    material_product_type.product_type_desc = "Single Save The Date Heart"
    material_product_type.merge_priority = 10
    material_product_type.merge_material_consolidation = 'Y'
    material_product_type.merge_plate_size = 300
    material_product_type.merge_plate_date = current_date
    material_product_type.merge_plate_number = 1
    material_product_type.merge_plate_item_number = 1
    material_product_type.merge_plate_item_number_increment = 1
    material_product_type.merge_plate_order_consolidation = 'Y'
    material_product_type.merge_ind = 'Y'
    material_product_type.save(conn)

    material_product_type.material_code = "WBEV"
    material_product_type.material_desc = "Wooden Beech Veneer"
    material_product_type.product_type_code = "HTL"
    material_product_type.product_type_desc = "Single Save The Date Heart"
    material_product_type.merge_priority = 10
    material_product_type.merge_material_consolidation = 'Y'
    material_product_type.merge_plate_size = 300
    material_product_type.merge_plate_date = current_date
    material_product_type.merge_plate_number = 1
    material_product_type.merge_plate_item_number = 1
    material_product_type.merge_plate_item_number_increment = 1
    material_product_type.merge_plate_order_consolidation = 'Y'
    material_product_type.merge_ind = 'Y'
    material_product_type.save(conn)

    material_product_type.material_code = "WBEV"
    material_product_type.material_desc = "Wooden Beech Veneer"
    material_product_type.product_type_code = "HSM"
    material_product_type.product_type_desc = "Hanging Star 80mm x 80mm"
    material_product_type.merge_priority = 10
    material_product_type.merge_material_consolidation = 'N'
    material_product_type.merge_plate_size = 77
    material_product_type.merge_plate_date = current_date
    material_product_type.merge_plate_number = 1
    material_product_type.merge_plate_item_number = 1
    material_product_type.merge_plate_item_number_increment = 1
    material_product_type.merge_plate_order_consolidation = 'Y'
    material_product_type.merge_ind = 'Y'
    material_product_type.save(conn)

    material_product_type.material_code = "AMSC"
    material_product_type.material_desc = "Acrylic Mirrored Silver Cast"
    material_product_type.product_type_code = "HSM"
    material_product_type.product_type_desc = "Hanging Star 80mm x 80mm"
    material_product_type.merge_priority = 10
    material_product_type.merge_material_consolidation = 'N'
    material_product_type.merge_plate_size = 77
    material_product_type.merge_plate_date = current_date
    material_product_type.merge_plate_number = 1
    material_product_type.merge_plate_item_number = 1
    material_product_type.merge_plate_item_number_increment = 1
    material_product_type.merge_plate_order_consolidation = 'Y'
    material_product_type.merge_ind = 'Y'
    material_product_type.save(conn)

    material_product_type.material_code = "ACC"
    material_product_type.material_desc = "Acrylic Clear Cast"
    material_product_type.product_type_code = "HSM"
    material_product_type.product_type_desc = "Hanging Star 80mm x 80mm"
    material_product_type.merge_priority = 10
    material_product_type.merge_material_consolidation = 'N'
    material_product_type.merge_plate_size = 77
    material_product_type.merge_plate_date = current_date
    material_product_type.merge_plate_number = 1
    material_product_type.merge_plate_item_number = 1
    material_product_type.merge_plate_item_number_increment = 1
    material_product_type.merge_plate_order_consolidation = 'Y'
    material_product_type.merge_ind = 'Y'
    material_product_type.save(conn)

    material_product_type.material_code = "WBEV"
    material_product_type.material_desc = "Wooden Beech Veneer"
    material_product_type.product_type_code = "HHM"
    material_product_type.product_type_desc = "Hanging Heart 87mm x 84mm"
    material_product_type.merge_priority = 10
    material_product_type.merge_material_consolidation = 'N'
    material_product_type.merge_plate_size = 77
    material_product_type.merge_plate_date = current_date
    material_product_type.merge_plate_number = 1
    material_product_type.merge_plate_item_number = 1
    material_product_type.merge_plate_item_number_increment = 1
    material_product_type.merge_plate_order_consolidation = 'Y'
    material_product_type.merge_ind = 'Y'
    material_product_type.save(conn)

    material_product_type.material_code = "AMSC"
    material_product_type.material_desc = "Acrylic Mirrored Silver Cast"
    material_product_type.product_type_code = "HHM"
    material_product_type.product_type_desc = "Hanging Heart 87mm x 84mm"
    material_product_type.merge_priority = 10
    material_product_type.merge_material_consolidation = 'N'
    material_product_type.merge_plate_size = 77
    material_product_type.merge_plate_date = current_date
    material_product_type.merge_plate_number = 1
    material_product_type.merge_plate_item_number = 1
    material_product_type.merge_plate_item_number_increment = 1
    material_product_type.merge_plate_order_consolidation = 'Y'
    material_product_type.merge_ind = 'Y'
    material_product_type.save(conn)

    material_product_type.material_code = "ACC"
    material_product_type.material_desc = "Acrylic Clear Cast"
    material_product_type.product_type_code = "HHM"
    material_product_type.product_type_desc = "Hanging Heart 87mm x 84mm"
    material_product_type.merge_priority = 10
    material_product_type.merge_material_consolidation = 'N'
    material_product_type.merge_plate_size = 77
    material_product_type.merge_plate_date = current_date
    material_product_type.merge_plate_number = 1
    material_product_type.merge_plate_item_number = 1
    material_product_type.merge_plate_item_number_increment = 1
    material_product_type.merge_plate_order_consolidation = 'Y'
    material_product_type.merge_ind = 'Y'
    material_product_type.save(conn)

    material_product_type.material_code = "WBEV"
    material_product_type.material_desc = "Wooden Beech Veneer"
    material_product_type.product_type_code = "HBM"
    material_product_type.product_type_desc = "Hanging Circular Bauble 73.5mm x 85mm"
    material_product_type.merge_priority = 10
    material_product_type.merge_material_consolidation = 'N'
    material_product_type.merge_plate_size = 72
    material_product_type.merge_plate_date = current_date
    material_product_type.merge_plate_number = 1
    material_product_type.merge_plate_item_number = 1
    material_product_type.merge_plate_item_number_increment = 1
    material_product_type.merge_plate_order_consolidation = 'Y'
    material_product_type.merge_ind = 'Y'
    material_product_type.save(conn)

    material_product_type.material_code = "AMSC"
    material_product_type.material_desc = "Acrylic Mirrored Silver Cast"
    material_product_type.product_type_code = "HBM"
    material_product_type.product_type_desc = "Hanging Circular Bauble 73.5mm x 85mm"
    material_product_type.merge_priority = 10
    material_product_type.merge_material_consolidation = 'N'
    material_product_type.merge_plate_size = 72
    material_product_type.merge_plate_date = current_date
    material_product_type.merge_plate_number = 1
    material_product_type.merge_plate_item_number = 1
    material_product_type.merge_plate_item_number_increment = 1
    material_product_type.merge_plate_order_consolidation = 'Y'
    material_product_type.merge_ind = 'Y'
    material_product_type.save(conn)

    material_product_type.material_code = "ACC"
    material_product_type.material_desc = "Acrylic Clear Cast"
    material_product_type.product_type_code = "HBM"
    material_product_type.product_type_desc = "Hanging Circular Bauble 73.5mm x 85mm"
    material_product_type.merge_priority = 10
    material_product_type.merge_material_consolidation = 'N'
    material_product_type.merge_plate_size = 72
    material_product_type.merge_plate_date = current_date
    material_product_type.merge_plate_number = 1
    material_product_type.merge_plate_item_number = 1
    material_product_type.merge_plate_item_number_increment = 1
    material_product_type.merge_plate_order_consolidation = 'Y'
    material_product_type.merge_ind = 'Y'
    material_product_type.save(conn)

    material_product_type.material_code = "PTRS"
    material_product_type.material_desc = "Plastic Silver Trolase"
    material_product_type.product_type_code = "WLT"
    material_product_type.product_type_desc = "Wallet Insert 81mm x 51mm"
    material_product_type.merge_priority = 10
    material_product_type.merge_material_consolidation = 'N'
    material_product_type.merge_plate_size = 90
    material_product_type.merge_plate_date = current_date
    material_product_type.merge_plate_number = 1
    material_product_type.merge_plate_item_number = 1
    material_product_type.merge_plate_item_number_increment = 1
    material_product_type.merge_plate_order_consolidation = 'Y'
    material_product_type.merge_ind = 'Y'
    material_product_type.save(conn)

    material_product_type.material_code = "PTRG"
    material_product_type.material_desc = "Plastic Gold Trolase"
    material_product_type.product_type_code = "WLT"
    material_product_type.product_type_desc = "Wallet Insert 81mm x 51mm"
    material_product_type.merge_priority = 10
    material_product_type.merge_material_consolidation = 'N'
    material_product_type.merge_plate_size = 90
    material_product_type.merge_plate_date = current_date
    material_product_type.merge_plate_number = 1
    material_product_type.merge_plate_item_number = 1
    material_product_type.merge_plate_item_number_increment = 1
    material_product_type.merge_plate_item_number_increment = 1
    material_product_type.merge_plate_order_consolidation = 'Y'
    material_product_type.merge_ind = 'Y'
    material_product_type.save(conn)

    material_product_type.material_code = "WBEV"
    material_product_type.material_desc = "Wood Beech Veneer"
    material_product_type.product_type_code = "BDL"
    material_product_type.product_type_desc = "Large Baby Disc - 145mm x 145mm"
    material_product_type.merge_priority = 10
    material_product_type.merge_material_consolidation = 'Y'
    material_product_type.merge_plate_size = 18
    material_product_type.merge_plate_date = current_date
    material_product_type.merge_plate_number = 1
    material_product_type.merge_plate_item_number = 1
    material_product_type.merge_plate_item_number_increment = 1
    material_product_type.merge_plate_order_consolidation = 'Y'
    material_product_type.merge_ind = 'Y'
    material_product_type.save(conn)

    material_product_type.material_code = "WBEV"
    material_product_type.material_desc = "Wood Beech Veneer"
    material_product_type.product_type_code = "BDM"
    material_product_type.product_type_desc = "Medium Baby Disc - 97mm x 97mm"
    material_product_type.merge_priority = 10
    material_product_type.merge_material_consolidation = 'Y'
    material_product_type.merge_plate_size = 45
    material_product_type.merge_plate_date = current_date
    material_product_type.merge_plate_number = 1
    material_product_type.merge_plate_item_number = 1
    material_product_type.merge_plate_item_number_increment = 1
    material_product_type.merge_plate_order_consolidation = 'Y'
    material_product_type.merge_ind = 'Y'
    material_product_type.save(conn)

    material_product_type.material_code = "WBIV"
    material_product_type.material_desc = "Wood Birch Veneer"
    material_product_type.product_type_code = "BDL"
    material_product_type.product_type_desc = "Large Baby Disc - 145mm x 145mm"
    material_product_type.merge_priority = 10
    material_product_type.merge_material_consolidation = 'Y'
    material_product_type.merge_plate_size = 18
    material_product_type.merge_plate_date = current_date
    material_product_type.merge_plate_number = 1
    material_product_type.merge_plate_item_number = 1
    material_product_type.merge_plate_item_number_increment = 1
    material_product_type.merge_plate_order_consolidation = 'Y'
    material_product_type.merge_ind = 'Y'
    material_product_type.save(conn)

    material_product_type.material_code = "WBIV"
    material_product_type.material_desc = "Wood Birch Veneer"
    material_product_type.product_type_code = "BDM"
    material_product_type.product_type_desc = "Medium Baby Disc - 97mm x 97mm"
    material_product_type.merge_priority = 10
    material_product_type.merge_material_consolidation = 'Y'
    material_product_type.merge_plate_size = 45
    material_product_type.merge_plate_date = current_date
    material_product_type.merge_plate_number = 1
    material_product_type.merge_plate_item_number = 1
    material_product_type.merge_plate_item_number_increment = 1
    material_product_type.merge_plate_order_consolidation = 'Y'
    material_product_type.merge_ind = 'Y'
    material_product_type.save(conn)

    material_product_type.material_code = "WCHV"
    material_product_type.material_desc = "Wood Cherry Veneer"
    material_product_type.product_type_code = "BDL"
    material_product_type.product_type_desc = "Large Baby Disc - 145mm x 145mm"
    material_product_type.merge_priority = 10
    material_product_type.merge_material_consolidation = 'Y'
    material_product_type.merge_plate_size = 18
    material_product_type.merge_plate_date = current_date
    material_product_type.merge_plate_number = 1
    material_product_type.merge_plate_item_number = 1
    material_product_type.merge_plate_item_number_increment = 1
    material_product_type.merge_plate_order_consolidation = 'Y'
    material_product_type.merge_ind = 'Y'
    material_product_type.save(conn)

    material_product_type.material_code = "WCHV"
    material_product_type.material_desc = "Wood Cherry Veneer"
    material_product_type.product_type_code = "BDM"
    material_product_type.product_type_desc = "Medium Baby Disc - 97mm x 97mm"
    material_product_type.merge_priority = 10
    material_product_type.merge_material_consolidation = 'Y'
    material_product_type.merge_plate_size = 45
    material_product_type.merge_plate_date = current_date
    material_product_type.merge_plate_number = 1
    material_product_type.merge_plate_item_number = 1
    material_product_type.merge_plate_item_number_increment = 1
    material_product_type.merge_plate_order_consolidation = 'Y'
    material_product_type.merge_ind = 'Y'
    material_product_type.save(conn)

    material_product_type.material_code = "WWHV"
    material_product_type.material_desc = "Wood White Veneer"
    material_product_type.product_type_code = "BDL"
    material_product_type.product_type_desc = "Large Baby Disc - 145mm x 145mm"
    material_product_type.merge_priority = 10
    material_product_type.merge_material_consolidation = 'Y'
    material_product_type.merge_plate_size = 18
    material_product_type.merge_plate_date = current_date
    material_product_type.merge_plate_number = 1
    material_product_type.merge_plate_item_number = 1
    material_product_type.merge_plate_item_number_increment = 1
    material_product_type.merge_plate_order_consolidation = 'Y'
    material_product_type.merge_ind = 'Y'
    material_product_type.save(conn)

    material_product_type.material_code = "WWHV"
    material_product_type.material_desc = "Wood White Veneer"
    material_product_type.product_type_code = "BDM"
    material_product_type.product_type_desc = "Medium Baby Disc - 97mm x 97mm"
    material_product_type.merge_priority = 10
    material_product_type.merge_material_consolidation = 'Y'
    material_product_type.merge_plate_size = 45
    material_product_type.merge_plate_date = current_date
    material_product_type.merge_plate_number = 1
    material_product_type.merge_plate_item_number = 1
    material_product_type.merge_plate_item_number_increment = 1
    material_product_type.merge_plate_order_consolidation = 'Y'
    material_product_type.merge_ind = 'Y'
    material_product_type.save(conn)

    material_product_type.material_code = "WBEV"
    material_product_type.material_desc = "Wood Beech Veneer"
    material_product_type.product_type_code = "CDRM"
    material_product_type.product_type_desc = "Medium Rectangular Countdown Plaque - 145mm x 92mm"
    material_product_type.merge_priority = 10
    material_product_type.merge_material_consolidation = 'N'
    material_product_type.merge_plate_size = 30
    material_product_type.merge_plate_date = current_date
    material_product_type.merge_plate_number = 1
    material_product_type.merge_plate_item_number = 1
    material_product_type.merge_plate_item_number_increment = 1
    material_product_type.merge_plate_order_consolidation = 'Y'
    material_product_type.merge_ind = 'Y'
    material_product_type.save(conn)

    material_product_type.material_code = "WBEV"
    material_product_type.material_desc = "Wood Beech Veneer"
    material_product_type.product_type_code = "HBTEM"
    material_product_type.product_type_desc = "Medium Hanging Basket Easter Egg Tag - 60mm x 80mm"
    material_product_type.merge_priority = 10
    material_product_type.merge_material_consolidation = 'N'
    material_product_type.merge_plate_size = 36
    material_product_type.merge_plate_date = current_date
    material_product_type.merge_plate_number = 1
    material_product_type.merge_plate_item_number = 1
    material_product_type.merge_plate_item_number_increment = 1
    material_product_type.merge_plate_order_consolidation = 'Y'
    material_product_type.merge_ind = 'Y'
    material_product_type.save(conn)

    material_product_type.material_code = "PTRS"
    material_product_type.material_desc = "Plastic TROLASE Silver"
    material_product_type.product_type_code = "BDGS"
    material_product_type.product_type_desc = "Standard Badge - 75mm x 20mm"
    material_product_type.merge_priority = 10
    material_product_type.merge_material_consolidation = 'N'
    material_product_type.merge_plate_size = 100
    material_product_type.merge_plate_date = current_date
    material_product_type.merge_plate_number = 1
    material_product_type.merge_plate_item_number = 1
    material_product_type.merge_plate_item_number_increment = 1
    material_product_type.merge_plate_order_consolidation = 'Y'
    material_product_type.merge_ind = 'Y'
    material_product_type.save(conn)

    material_product_type.material_code = "PTRG"
    material_product_type.material_desc = "Plastic TROLASE Gold"
    material_product_type.product_type_code = "BDGS"
    material_product_type.product_type_desc = "Standard Badge - 75mm x 20mm"
    material_product_type.merge_priority = 10
    material_product_type.merge_material_consolidation = 'N'
    material_product_type.merge_plate_size = 100
    material_product_type.merge_plate_date = current_date
    material_product_type.merge_plate_number = 1
    material_product_type.merge_plate_item_number = 1
    material_product_type.merge_plate_item_number_increment = 1
    material_product_type.merge_plate_order_consolidation = 'Y'
    material_product_type.merge_ind = 'Y'
    material_product_type.save(conn)

    material_product_type.material_code = "PTRS"
    material_product_type.material_desc = "Plastic TROLASE Silver"
    material_product_type.product_type_code = "BDGL"
    material_product_type.product_type_desc = "Large Badge - 82.5mm x 22mm"
    material_product_type.merge_priority = 10
    material_product_type.merge_material_consolidation = 'N'
    material_product_type.merge_plate_size = 100
    material_product_type.merge_plate_date = current_date
    material_product_type.merge_plate_number = 1
    material_product_type.merge_plate_item_number = 1
    material_product_type.merge_plate_item_number_increment = 1
    material_product_type.merge_plate_order_consolidation = 'Y'
    material_product_type.merge_ind = 'Y'
    material_product_type.save(conn)

    material_product_type.material_code = "PTRG"
    material_product_type.material_desc = "Plastic TROLASE Gold"
    material_product_type.product_type_code = "BDGL"
    material_product_type.product_type_desc = "Large Badge - 82.5mm x 22mm"
    material_product_type.merge_priority = 10
    material_product_type.merge_material_consolidation = 'N'
    material_product_type.merge_plate_size = 100
    material_product_type.merge_plate_date = current_date
    material_product_type.merge_plate_number = 1
    material_product_type.merge_plate_item_number = 1
    material_product_type.merge_plate_item_number_increment = 1
    material_product_type.merge_plate_order_consolidation = 'Y'
    material_product_type.merge_ind = 'Y'
    material_product_type.save(conn)

    material_product_type.material_code = "WBEV"
    material_product_type.material_desc = "Wood Beech Veneer"
    material_product_type.product_type_code = "KYL"
    material_product_type.product_type_desc = "Large Keyring - 90 mm x 24 mm"
    material_product_type.merge_priority = 10
    material_product_type.merge_material_consolidation = 'N'
    material_product_type.merge_plate_size = 100
    material_product_type.merge_plate_date = current_date
    material_product_type.merge_plate_number = 1
    material_product_type.merge_plate_item_number = 1
    material_product_type.merge_plate_item_number_increment = 1
    material_product_type.merge_plate_order_consolidation = 'Y'
    material_product_type.merge_ind = 'Y'
    material_product_type.save(conn)

    material_product_type.material_code = "WOKV"
    material_product_type.material_desc = "Wood Oak Veneer"
    material_product_type.product_type_code = "KYL"
    material_product_type.product_type_desc = "Large Keyring - 90 mm x 24 mm"
    material_product_type.merge_priority = 10
    material_product_type.merge_material_consolidation = 'N'
    material_product_type.merge_plate_size = 100
    material_product_type.merge_plate_date = current_date
    material_product_type.merge_plate_number = 1
    material_product_type.merge_plate_item_number = 1
    material_product_type.merge_plate_item_number_increment = 1
    material_product_type.merge_plate_order_consolidation = 'Y'
    material_product_type.merge_ind = 'Y'
    material_product_type.save(conn)

    material_product_type.material_code = "WBEV"
    material_product_type.material_desc = "Wood Beech Veneer"
    material_product_type.product_type_code = "PFM"
    material_product_type.product_type_desc = "Medium Pennant/Flag - 100 mm x 140 mm"
    material_product_type.merge_priority = 10
    material_product_type.merge_material_consolidation = 'N'
    material_product_type.merge_plate_size = 24
    material_product_type.merge_plate_date = current_date
    material_product_type.merge_plate_number = 1
    material_product_type.merge_plate_item_number = 1
    material_product_type.merge_plate_item_number_increment = 1
    material_product_type.merge_plate_order_consolidation = 'Y'
    material_product_type.merge_ind = 'Y'
    material_product_type.save(conn)

    material_product_type.material_code = "WBIV"
    material_product_type.material_desc = "Wood Birch Veneer"
    material_product_type.product_type_code = "PFM"
    material_product_type.product_type_desc = "Medium Pennant/Flag - 100 mm x 140 mm"
    material_product_type.merge_priority = 10
    material_product_type.merge_material_consolidation = 'N'
    material_product_type.merge_plate_size = 24
    material_product_type.merge_plate_date = current_date
    material_product_type.merge_plate_number = 1
    material_product_type.merge_plate_item_number = 1
    material_product_type.merge_plate_item_number_increment = 1
    material_product_type.merge_plate_order_consolidation = 'Y'
    material_product_type.merge_ind = 'Y'
    material_product_type.save(conn)

    material_product_type.material_code = "WWHV"
    material_product_type.material_desc = "Wood White Veneer"
    material_product_type.product_type_code = "PFM"
    material_product_type.product_type_desc = "Medium Pennant/Flag - 100 mm x 140 mm"
    material_product_type.merge_priority = 10
    material_product_type.merge_material_consolidation = 'N'
    material_product_type.merge_plate_size = 24
    material_product_type.merge_plate_date = current_date
    material_product_type.merge_plate_number = 1
    material_product_type.merge_plate_item_number = 1
    material_product_type.merge_plate_item_number_increment = 1
    material_product_type.merge_plate_order_consolidation = 'Y'
    material_product_type.merge_ind = 'Y'
    material_product_type.save(conn)

    material_product_type.material_code = "WCHV"
    material_product_type.material_desc = "Wood Cherry Veneer"
    material_product_type.product_type_code = "PFM"
    material_product_type.product_type_desc = "Medium Pennant/Flag - 100 mm x 140 mm"
    material_product_type.merge_priority = 10
    material_product_type.merge_material_consolidation = 'N'
    material_product_type.merge_plate_size = 24
    material_product_type.merge_plate_date = current_date
    material_product_type.merge_plate_number = 1
    material_product_type.merge_plate_item_number = 1
    material_product_type.merge_plate_item_number_increment = 1
    material_product_type.merge_plate_order_consolidation = 'Y'
    material_product_type.merge_ind = 'Y'
    material_product_type.save(conn)

    material_product_type.material_code = "WOKV"
    material_product_type.material_desc = "Wood Oak Veneer"
    material_product_type.product_type_code = "PFM"
    material_product_type.product_type_desc = "Medium Pennant/Flag - 100 mm x 140 mm"
    material_product_type.merge_priority = 10
    material_product_type.merge_material_consolidation = 'N'
    material_product_type.merge_plate_size = 24
    material_product_type.merge_plate_date = current_date
    material_product_type.merge_plate_number = 1
    material_product_type.merge_plate_item_number = 1
    material_product_type.merge_plate_item_number_increment = 1
    material_product_type.merge_plate_order_consolidation = 'Y'
    material_product_type.merge_ind = 'Y'
    material_product_type.save(conn)

    material_product_type.material_code = "WWS"
    material_product_type.material_desc = "Solid Wood White Painted"
    material_product_type.product_type_code = "HNGL"
    material_product_type.product_type_desc = "Single Large Adult Hanger"
    material_product_type.merge_priority = 10
    material_product_type.merge_material_consolidation = 'N'
    material_product_type.merge_plate_size = 300
    material_product_type.merge_plate_date = current_date
    material_product_type.merge_plate_number = 1
    material_product_type.merge_plate_item_number = 1
    material_product_type.merge_plate_item_number_increment = 1
    material_product_type.merge_plate_order_consolidation = 'Y'
    material_product_type.merge_ind = 'Y'
    material_product_type.save(conn)

    material_product_type.material_code = "WWS"
    material_product_type.material_desc = "Solid Wood White Painted"
    material_product_type.product_type_code = "HNGS"
    material_product_type.product_type_desc = "Single Small Child Hanger"
    material_product_type.merge_priority = 10
    material_product_type.merge_material_consolidation = 'N'
    material_product_type.merge_plate_size = 300
    material_product_type.merge_plate_date = current_date
    material_product_type.merge_plate_number = 1
    material_product_type.merge_plate_item_number = 1
    material_product_type.merge_plate_item_number_increment = 1
    material_product_type.merge_plate_order_consolidation = 'Y'
    material_product_type.merge_ind = 'Y'
    material_product_type.save(conn)

    material_product_type.material_code = "WBEV"
    material_product_type.material_desc = "Beech Veneer"
    material_product_type.product_type_code = "KRHSM"
    material_product_type.product_type_desc = "House Shape Keyring - 60mm x 60mm"
    material_product_type.merge_priority = 10
    material_product_type.merge_material_consolidation = 'Y'
    material_product_type.merge_plate_size = 99
    material_product_type.merge_plate_date = current_date
    material_product_type.merge_plate_number = 1
    material_product_type.merge_plate_item_number = 1
    material_product_type.merge_plate_item_number_increment = 1
    material_product_type.merge_plate_order_consolidation = 'Y'
    material_product_type.merge_ind = 'Y'
    material_product_type.save(conn)

    material_product_type.material_code = "WOKV"
    material_product_type.material_desc = "Oak Veneer"
    material_product_type.product_type_code = "KRHSM"
    material_product_type.product_type_desc = "House Shape Keyring - 60mm x 60mm"
    material_product_type.merge_priority = 10
    material_product_type.merge_material_consolidation = 'Y'
    material_product_type.merge_plate_size = 99
    material_product_type.merge_plate_date = current_date
    material_product_type.merge_plate_number = 1
    material_product_type.merge_plate_item_number = 1
    material_product_type.merge_plate_item_number_increment = 1
    material_product_type.merge_plate_order_consolidation = 'Y'
    material_product_type.merge_ind = 'Y'
    material_product_type.save(conn)

    material_product_type.material_code = "WXXX"
    material_product_type.material_desc = "Wood Test"
    material_product_type.product_type_code = "BDL"
    material_product_type.product_type_desc = "Large Baby Disc - 145mm x 145mm"
    material_product_type.merge_priority = 10
    material_product_type.merge_material_consolidation = 'Y'
    material_product_type.merge_plate_size = 18
    material_product_type.merge_plate_date = current_date
    material_product_type.merge_plate_number = 1
    material_product_type.merge_plate_item_number = 1
    material_product_type.merge_plate_item_number_increment = 1
    material_product_type.merge_plate_order_consolidation = 'Y'
    material_product_type.merge_ind = 'Y'
    material_product_type.save(conn)

    return (True)


def increment_plate_item_count(conn, material_product_type: NewMaterialProductType) -> bool:
    #   ** *********************************************************************************************************************************************
    #   ** Update material_product_types database record with incremented merge_plate_item_number
    #   ** *********************************************************************************************************************************************
    db_material_product_type = material_product_type

    if db_material_product_type.merge_plate_item_number == db_material_product_type.merge_plate_size:
        db_material_product_type.merge_plate_number += 1
        db_material_product_type.merge_plate_item_number = 1
    else:
        db_material_product_type.merge_plate_item_number += 1

    db_material_product_type.update_MaterialProductType(conn)

    return (True)