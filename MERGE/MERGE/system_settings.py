# ****************************************************************************************************************
# CLASS: SystemSettings
# ****************************************************************************************************************
import datetime
import logging


class SystemSettings:
    """Etch & Cut SystemSettings Class"""

    __dictionary__ =    {
                            "process year"                  : "2025"
                        ,   "process month"                 : "01"
                        ,   "process day"                   : "25"
                        ,   "logging level"                 : logging.INFO # DEBUG | INFO | WARNING | ERROR | CRITICAL
                        ,   "logging file path"             : "C:/Users/Adam/iCloudDrive/Work/Etch & Cut LTD/Test Program/MERGE/TEST/DATA/LOGS"
                        ,   "database suffix"               : "DEV"
                        ,   "run country code"              : "GB" # "GB" "US"
                        ,   "absolute home path"            : "C:/Users/Adam/iCloudDrive/Work/Etch & Cut LTD/Test Program/MERGE/TEST"
#                        ,   "absolute home path"           :  "S:"
                        ,   "database path"                 : "C:/Users/Adam/iCloudDrive/Work/Etch & Cut LTD/Test Program/MERGE/TEST/DATABASE/EtchCut_DB_DEV"
                        ,   "indesign merge path"           : "MERGE\INDESIGN\PRODUCTION"
#                        ,   "design component path"         : "S:\MERGE\IMAGES"
                        ,   "design component path"         : "C:/Users/Adam/iCloudDrive/Work/Etch & Cut LTD/Test Program/MERGE/TEST/IMAGES"
                        ,   "etsy source data path"         : "C:/Users/Adam/iCloudDrive/Work/Etch & Cut LTD/Test Program/MERGE/TEST/DATA/ETSY/LIVE"
                        ,   "etsy source invoice path"      : "C:/Users/Adam/iCloudDrive/Work/Etch & Cut LTD/Test Program/MERGE/TEST/DATA"
                        ,   "etsy target invoice path"      : "C:/Users/Adam/iCloudDrive/Work/Etch & Cut LTD/Test Program/MERGE/TEST/DATA/INVOICES"
                        ,   "sorted invoice path"           : "C:/Users/Adam/iCloudDrive/Work/Etch & Cut LTD/Test Program/MERGE/TEST/DATA/INVOICES_FOR_PRINTING"
                        ,   "etsy target gift receipt path" : "C:/Users/Adam/iCloudDrive/Work/Etch & Cut LTD/Test Program/MERGE/TEST/DATA/GIFT_RECEIPTS"
                        ,   "etsy output barcode path"      : "C:/Users/Adam/iCloudDrive/Work/Etch & Cut LTD/Test Program/MERGE/TEST/DATA/BARCODES"
                        ,   "merge input path"              : r"MERGE\INPUT"
                        ,   "merge output path"             : r"MERGE\OUTPUT"
                        ,   "US post spreadsheet path"      : "C:/Users/Adam/iCloudDrive/Work/Etch & Cut LTD/Test Program/MERGE/TEST/DATA"
                        ,   "personalise list"              : 
                            [
                                'SXXXX'
#                            ,   'S0151', 'CWS_RMH_S0151'
#                            ,   'S0154', 'CWS_RMH_S0154', 'CWS_HMH_S0154
#                            ,   'S0155', 'CWS_RMH_S0155'
#                            ,   'S0157', 'CWS_RMH_S0157', 'CWS_HMH_S0157'
#                            ,   'S0159', 'CWS_RMH_S0159'
#                            ,   'S0165', 'CWS_RMH_S0165'
#                            ,   'S0166', 'CWS_RMH_S0166'
#                            ,   'S0169', 'CWS_RMH_S0169'
#                            ,   'S0170', 'CWS_RMH_S0170'
#                            ,   'S0173', 'CWS_RMH_S0173'
#                            ,   'S0178', 'CWS_RMH_S0178'
#                            ,   'S0181', 'CWS_RMH_S0181', 'CWS_HMH_S0181'
#                            ,   'S0184', 'CWS_RMH_S0184', 'CWS_HMH_S0184'
#                            ,   'S0187', 'CWS_RMH_S0187', 'CWS_HMH_S0187'
#                            ,   'S0188', 'CWS_RMH_S0188', 'CWS_HMH_S0188'
#                            ,   'S0191', 'CWS_RMH_S0191'
#                            ,   'S0192', 'CWS_RMH_S0192', 'CWS_HMH_S0192'
#                            ,   'S0193', 'CWS_RMH_S0193', 'CWS_HMH_S0193'
#                            ,   'S0194', 'CWS_RMH_S0194', 'CWS_HMH_S0194'
#                            ,   'S0195', 'CWS_RMH_S0195'
#                            ,   'S0196', 'CWS_RMH_S0196', 'CWS_HMH_S0196'
#                            ,   'S0197', 'CWS_RMH_S0197', 'CWS_HMH_S0197'
#                            ,   'S0198', 'CWS_RMH_S0198', 'CWS_HMH_S0198'
#                            ,   'S0199', 'CWS_RMH_S0199'
#                            ,   'S0201', 'CWS_RMH_S0201', 'CWS_HMH_S0201'
#                            ,   'S0202', 'CWS_RMH_S0202', 'CWS_HMH_S0202'
#                            ,   'S0208', 'CWS_RMH_S0208'
#                            ,   'S0209', 'CWS_RMH_S0209'
#                            ,   'S0210', 'CWS_RMH_S0210'
#                            ,   'S0267', 'CWS_RMH_S0267'
#                            ,   'S0268', 'CWS_RMH_S0268', 'CWS_HMH_S0268'
#                            ,   'S0269', 'CWS_RMH_S0269'
#                            ,   'S0290', 'CWS_RMH_S0290', 'CWS_HMH_S0290'
#                            ,   'S0313', 'CWS_RMH_S0313'

#                            ,   'S0001', 'CWS_CSL_S0001', 'CWS_MGL_S0001', 'CWS_MCL_S0001'
#                            ,   'S0002', 'CWS_CSL_S0002', 'CWS_MGL_S0002', 'CWS_MCL_S0002'
#                            ,   'S0007', 'CWS_CSL_S0007', 'CWS_MGL_S0007', 'CWS_MCL_S0007'
#                            ,   'S0008', 'CWS_CSL_S0008', 'CWS_MGL_S0008', 'CWS_MCL_S0008'
#                            ,   'S0011', 'CWS_CSL_S0011', 'CWS_MGL_S0011', 'CWS_MCL_S0011'
#                            ,   'S0017', 'CWS_CSL_S0017', 'CWS_MGL_S0017', 'CWS_MCL_S0017'
#                            ,   'S0024', 'CWS_CSL_S0024', 'CWS_MGL_S0024', 'CWS_MCL_S0024'
#                            ,   'S0025', 'CWS_CSL_S0025', 'CWS_MGL_S0025', 'CWS_MCL_S0025'
#                            ,   'S0026', 'CWS_CSL_S0026', 'CWS_MGL_S0026', 'CWS_MCL_S0026'
#                            ,   'S0027', 'CWS_CSL_S0027', 'CWS_MGL_S0027', 'CWS_MCL_S0027'
#                            ,   'S0028', 'CWS_CSL_S0028', 'CWS_MGL_S0028', 'CWS_MCL_S0028'
#                            ,   'S0029', 'CWS_CSL_S0029', 'CWS_MGL_S0029', 'CWS_MCL_S0029'
#                            ,   'S0031', 'CWS_CSL_S0031', 'CWS_MGL_S0031', 'CWS_MCL_S0031'
#                            ,   'S0034', 'CWS_CSL_S0034', 'CWS_MGL_S0034', 'CWS_MCL_S0034'
#                            ,   'S0036', 'CWS_CSL_S0036', 'CWS_MGL_S0036', 'CWS_MCL_S0036'
#                            ,   'S0037', 'CWS_CSL_S0037', 'CWS_MGL_S0037', 'CWS_MCL_S0037'
#                            ,   'S0060', 'CWS_CSL_S0060', 'CWS_MGL_S0060', 'CWS_MCL_S0060'
#                            ,   'S0064', 'CWS_CSL_S0064', 'CWS_MGL_S0064', 'CWS_MCL_S0064'
#                            ,   'S0066', 'CWS_CSL_S0066', 'CWS_MGL_S0066', 'CWS_MCL_S0066'
#                            ,   'S0070', 'CWS_CSL_S0070', 'CWS_MGL_S0070', 'CWS_MCL_S0070'
#                            ,   'S0072', 'CWS_CSL_S0072', 'CWS_MGL_S0072', 'CWS_MCL_S0072'
#                            ,   'S0097', 'CWS_CSL_S0097', 'CWS_MGL_S0097', 'CWS_MCL_S0097'
#                            ,   'S0114', 'CWS_CSL_S0114', 'CWS_MGL_S0114', 'CWS_MCL_S0114'
#                            ,   'S0115', 'CWS_CSL_S0115', 'CWS_MGL_S0115', 'CWS_MCL_S0115'
#                            ,   'S0118', 'CWS_CSL_S0118', 'CWS_MGL_S0118', 'CWS_MCL_S0118'
#                            ,   'S0121', 'CWS_CSL_S0121', 'CWS_MGL_S0121', 'CWS_MCL_S0121'
#                            ,   'S0123', 'CWS_CSL_S0123', 'CWS_MGL_S0123', 'CWS_MCL_S0123'
#                            ,   'S0125', 'CWS_CSL_S0125', 'CWS_MGL_S0125', 'CWS_MCL_S0125'
#                            ,   'S0135', 'CWS_CSL_S0135', 'CWS_MGL_S0135', 'CWS_MCL_S0135'
#                            ,   'S0217', 'CWS_CSL_S0217', 'CWS_MGL_S0217', 'CWS_MCL_S0217'
                            ,   'FD100'
                            ,   'FD101'
                            ,   'FD102'
                            ,   'FD103'
                            ,   'FD104'
                            ,   'FD105'
                            ,   'MD001'
                            ,   'MD002'
                            ,   'MD010'
                            ,   'MG003'
                            ,   'S0001'
                            ,   'S0002'
                            ,   'S0007'
                            ,   'S0008'
                            ,   'S0011'
                            ,   'S0024'
                            ,   'S0025'
                            ,   'S0026'
                            ,   'S0027'
                            ,   'S0028'
                            ,   'S0029'
                            ,   'S0031'
                            ,   'S0034'
                            ,   'S0036'
                            ,   'S0037'
                            ,   'S0045'
                            ,   'S0051'
                            ,   'S0055'
                            ,   'S0060'
                            ,   'S0064'
                            ,   'S0066'
                            ,   'S0067'
                            ,   'S0070'
                            ,   'S0072'
                            ,   'S0076'
                            ,   'S0097'
                            ,   'S0100'
                            ,   'S0114'
                            ,   'S0115'
                            ,   'S0118'
                            ,   'S0119'
                            ,   'S0120'
                            ,   'S0121'
                            ,   'S0122'
                            ,   'S0123'
                            ,   'S0124'
                            ,   'S0125'
                            ,   'S0134'
                            ,   'S0135'
                            ,   'S0136'
                            ,   'S0137'
                            ,   'S0138'
                            ,   'S0145'
                            ,   'S0146'
                            ,   'S0147'
                            ,   'S0151'
                            ,   'S0154'
                            ,   'S0155'
                            ,   'S0157'
                            ,   'S0159'
                            ,   'S0165'
                            ,   'S0166'
                            ,   'S0169'
                            ,   'S0170'
                            ,   'S0173'
                            ,   'S0178'
                            ,   'S0181'
                            ,   'S0184'
                            ,   'S0187'
                            ,   'S0188'
                            ,   'S0191'
                            ,   'S0192'
                            ,   'S0193'
                            ,   'S0194'
                            ,   'S0195'
                            ,   'S0196'
                            ,   'S0197'
                            ,   'S0198'
                            ,   'S0199'
                            ,   'S0200'
                            ,   'S0201'
                            ,   'S0202'
                            ,   'S0203'
                            ,   'S0204'
                            ,   'S0206'
                            ,   'S0208'
                            ,   'S0209'
                            ,   'S0210'
                            ,   'S0217'
                            ,   'S0265'
                            ,   'S0268'
                            ,   'S0269'
                            ,   'S0270'
                            ,   'S0276'
                            ,   'S0280'
                            ,   'S0284'
                            ,   'S0290'
                            ,   'S0313'
#                            ,   'P0001'
#                            ,   'P0010'
#                            ,   'P0011'
#                            ,   'P0012'
#                            ,   'P0014'
#                            ,   'P0015'
#                            ,   'P0016'
#                            ,   'P0017'
#                            ,   'P0018'
#                            ,   'P0073'
#                            ,   'P0179'
#                            ,   'P0206'
#                            ,   'P0214'
#                            ,   'P0768'
                            ,   'EG105'
                            ,   'EG106'
                            ,   'EG108'
                            ,   'WG109'
                            ,   'WG110'
                            ,   'WG111'
                            ,   'WG112'
                            ,   'WG116'
                            ,   'WS136'
                            ,   'WS102'
                            ,   'WS103'
                            ,   'WS104'
                            ,   'WS105'
                            ,   'WS106'
                            ,   'WS107'
                            ,   'WS108'
                            ,   'WS109'
                            ,   'WS119'
                            ,   'WS120'
                            ,   'WS121'
                            ,   'WS122'
                            ,   'WS123'
                            ,   'WS124'
                            ,   'WS126'
                            ,   'WS128'
                            ,   'WS129'
                            ,   'WS130'
                            ,   'WS135'
                            ,   'WS137'
                            ,   'WS139'
                            ,   'WS141'
                            ,   'WS142'
                            ,   'XM001'
                            ,   'XM002'
                            ,   'XM003'
                            ,   'XM004'
                            ,   'XM006'
                            ,   'XM007'
                            ,   'XM008'
                            ,   'XM009'
                            ,   'XM010'
                            ,   'XM011'
                            ,   'XM013'
                            ,   'XM014'
                            ,   'XM015'
                            ,   'XM016'
                            ,   'XMM02'
                            ,   'P0006'
                            ,   'P0051'
                            ,   'P0418'
                            ,   'P0420'
                            ,   'P0436'
                            ,   'P0446'
                            ,   'P0448'
                            ,   'P0468'
                            ,   'P0524'
                            ,   'P0528'
                            ,   'P0592'
                            ,   'P0327'
                            ,   'P0640'
                            ,   'P0955'
                            ,   'P0347'
                            ,   'P0438'
                            ,   'P0474'
                            ,   'P0484'
                            ,   'P0486'
                            ,   'P0488'
                            ,   'P0504'
                            ,   'P0506'
                            ,   'P0532'
                            ,   'XMH02'
                            ,   'FD018'
                            ,   'FD019'
                            ,   'CG002'
                            ,   'VD001'
                            ,   'VD002'
                            ,   'VD003'
                            ,   'EG101'
                            ,   'WG101'
                            ,   'WG102'
                            ,   'WG105'
                            ,   'WG107'
                            ,   'CG004'
                            ,   'BV004'
                            ,   'WD015'
                            ,   'AN004'
                            ,   'HM004'
                            ,   'HM002'
                            ,   'HM003'
                            ,   'BD006'
                            ,   'FD020'
                            ,   'FG001'
                            ,   'CS001'
                            ,   'WS138'
                            ,   'BB500'
                            ,   'BD004'
                            ,   'P0687'
                            ,   'P0708'
                            ,   'ID001'
                            ,   'WD011'
                            ,   'FD014'
                            ,   'P0322'
                            ,   'P0318'
#                            ,   'P0552' # P0326 - DESIGN B
#                            ,   'P0553' # P0326 - DESIGN C
#                            ,   'P0364' # P0326 - DESIGN D
                            ,   'P0320'
                            ,   'P0326' # P0326 - DESIGN A
                            ,   'P0360' # P0360 - DESIGN A
#                            ,   'P0361' # P0360 - DESIGN B
                            ,   'P0287'
                            ,   'P0307'
                            ,   'P0309'
                            ,   'P0328'
                            ,   'P0366'
                            ,   'P0345'
                            ,   'P0305'
                            ,   'P0339'
                            ,   'P0288'
                            ,   'P0945'
                            ,   'CG005'
                            ,   'GR001'
                            ,   'GR004'
                            ,   'GR005'
                            ,   'GR007'
                            ,   'WD001'
                            ,   'WD002'
                            ,   'WD003'
                            ,   'WD004'
                            ,   'WD005'
                            ,   'WD006'
                            ,   'WD012'
                            ,   'WD013'
                            ,   'WD014'
                            ,   'WD016'
                            ,   'WD017'
                            ,   'WD018'
                            ,   'WD023'
                            ,   'WD024'
                            ,   'WD025'
                            ,   'AN001'
                            ,   'AN002'
                            ,   'AN003'
                            ,   'AN006'
                            ,   'BD007'
                            ,   'HY001'
                            ,   'HY002'
                            ,   'BD008'
                            ,   'BV005'
                            ,   'BV006'
                            ,   'CG003'
                            ,   'CG006'
                            ,   'DG001'
                            ,   'DG002'
                            ,   'DG003'
                            ,   'FD008'
                            ,   'FD009'
                            ,   'FD010'
                            ,   'FD011'
                            ,   'FD012'
                            ,   'FD013'
                            ,   'FD016'
                            ,   'FD017'
                            ,   'FD021'
                            ,   'FM001'
                            ,   'FM002'
                            ,   'FM011'
                            ,   'FM005'
                            ,   'SC001'
                            ,   'FM009'
                            ,   'WD019'
                            ,   'WD018'
                            ,   'XMB01'
                            ,   'XMB02'
                            ,   'XMB03'
                            ,   'XMB04'
                            ,   'XMB05'
                            ,   'XMB06'
                            ,   'P0054'
                            ,   'P0018'
                            ,   'WS111'
                            ,   'WS115'
                            ,   'WS101'
                            ,   'XM101'
                            ,   'P0220'
                            ,   'P0055'
                            ,   'P0768'
                            ,   'P0888'
                            ,   'P0641'
                            ,   'P0096'
                            ,   'P0546'
                            ,   'P0547'
                            ,   'P0300'
                            ,   'P0608'
                            ,   'WS152'
                            ,   'P0203'
                            ,   'P0754'
                            ,   'P0623'
                            ,   'P0626'
                            ,   'XM117'
                            ,   'FD004'
                            ,   'BB501'
                            ]
                        }


    def __init__(
        self
    ):
        str_CurrentYear  = SystemSettings.__dictionary__.get("process year")
        str_CurrentMonth = SystemSettings.__dictionary__.get("process month")
        str_CurrentDay   = SystemSettings.__dictionary__.get("process day")
        str_CurrentDate  = f'''{str_CurrentYear}{str_CurrentMonth}{str_CurrentDay}'''

        try:
            self.logging_level                  = SystemSettings.__dictionary__.get("logging level")
            self.logging_file_path              = SystemSettings.__dictionary__.get("logging file path")
            self.database_suffix                = SystemSettings.__dictionary__.get("database suffix")
            self.run_country_code               = SystemSettings.__dictionary__.get("run country code")
            self.absolute_home_path             = SystemSettings.__dictionary__.get("absolute home path")
            self.database_path                  = SystemSettings.__dictionary__.get("database path")
            self.indesign_merge_path            = SystemSettings.__dictionary__.get("indesign merge path")
            self.design_component_path          = SystemSettings.__dictionary__.get("design component path")
            self.etsy_source_data_path          = SystemSettings.__dictionary__.get("etsy source data path")
            self.etsy_source_invoice_path       = SystemSettings.__dictionary__.get("etsy source invoice path")
            self.etsy_target_invoice_path       = SystemSettings.__dictionary__.get("etsy target invoice path")
            self.sorted_invoice_path            = SystemSettings.__dictionary__.get("sorted invoice path")
            self.etsy_target_gift_receipt_path  = SystemSettings.__dictionary__.get("etsy target gift receipt path")
            self.etsy_output_barcode_path       = SystemSettings.__dictionary__.get("etsy output barcode path")
            self.merge_input_path               = SystemSettings.__dictionary__.get("merge input path")
            self.merge_output_path              = SystemSettings.__dictionary__.get("merge output path")
            self.us_post_spreadsheet_path       = SystemSettings.__dictionary__.get("US post spreadsheet path")
            self.personalise_list               = SystemSettings.__dictionary__.get("personalise list")
            self.process_date                   = str_CurrentDate
            self.debug                          = SystemSettings.__dictionary__.get("debug")
        except:
            self.logging_level                  = logging.DEBUG
            self.logging_file_path              = None
            self.database_suffix                = None
            self.run_country_code               = None
            self.absolute_home_path             = None
            self.database_path                  = None
            self.indesign_merge_path            = None
            self.design_component_path          = None
            self.etsy_source_data_path          = None
            self.etsy_source_invoice_path       = None
            self.etsy_target_invoice_path       = None
            self.sorted_invoice_path            = None
            self.etsy_target_gift_receipt_path  = None
            self.merge_input_path               = None
            self.merge_output_path              = None
            self.us_post_spreadsheet_path       = None
            self.personalise_list               = None
            self.process_date                   = None
            self.debug                          = False


    def __repr__(self):
        p_string ='''
            database_suffix:% s run_country_code:% s database_path:% s design_component_path:% s etsy_source_data_path:% s etsy_source_invoice_path:% spersonalise_list:% s
        '''
        return  p_string % (
            self.database_suffix, self.run_country_code, self.database_path, self.design_component_path, self.etsy_source_data_path, self.etsy_source_invoice_path, self.personalise_list
        )

    def __str__(self):
        p_string =f'''System Settings: 
            database suffix:{self.database_suffix}, run country code:{self.run_country_code}, database_path:{self.database_path}, design_component_path:{self.design_component_path}, etsy_source_data_path:{self.etsy_source_data_path}, etsy_source_invoice_path:{self.etsy_source_invpoice_path}, personalise_list:{self.personalise_list}'''
        return p_string