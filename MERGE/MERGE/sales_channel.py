# ****************************************************************************************************************
# CLASS: SalesChannel
# ****************************************************************************************************************
class SalesChannel:
    """Etch & Cut SalesChannel Class"""

    __dictionary__ = {
        "EtsyTM"                : {"id": 1,        "name": "Two Moons on Etsy"             , "user_id": "", "password": ""}
    ,   "EtsyHW"                : {"id": 2,        "name": "Honey and Wild on Etsy"        , "user_id": "", "password": ""}
    ,   "EtsySJ"                : {"id": 3,        "name": "SubliJubbly on Etsy"           , "user_id": "", "password": ""}
    ,   "EtsyFS"                : {"id": 4,        "name": "Frame Store on Etsy"           , "user_id": "", "password": ""}
    ,   "EtsyLL"                : {"id": 5,        "name": "Live Laugh Love Craft on Etsy" , "user_id": "", "password": ""}
    ,   "EtsyFL"                : {"id": 6,        "name": "Forever Lily on Etsy"          , "user_id": "", "password": ""}
    ,   "EBAY"                  : {"id": 7,        "name": "EBAY"                          , "user_id": "", "password": ""}
    ,   "AMAZON"                : {"id": 8,        "name": "AMAZON"                        , "user_id": "", "password": ""}
    ,   "HoneyAndWildCo"        : {"id": "EtsyHW", "name": "Honey and Wild on Etsy"        , "user_id": "", "password": ""}
    ,   "TwoMoonsGiftCo"        : {"id": "EtsyTM", "name": "Two Moons on Etsy"             , "user_id": "", "password": ""}
    ,   "SubliJubbly"           : {"id": "EtsySJ", "name": "SubliJubbly on Etsy"           , "user_id": "", "password": ""}
    ,   "theframestoreuk"       : {"id": "EtsyFS", "name": "Frame Store on Etsy"           , "user_id": "", "password": ""}
    ,   "livecraftlovedesign"   : {"id": "EtsyLL", "name": "Live Laugh Love Craft on Etsy" , "user_id": "", "password": ""}
    ,   "ForeverLilyCo"         : {"id": "EtsyFL", "name": "Forever Lily on Etsy"          , "user_id": "", "password": ""}
    }


    def __init__(
        self
    
    ,   p_code
    ):
        try:
            SalesChannel.__dictionary__.get(p_code)

            self.code     = p_code
            self.id       = SalesChannel.__dictionary__.get(p_code)["id"]
            self.name     = SalesChannel.__dictionary__.get(p_code)["name"]
            self.user_id  = SalesChannel.__dictionary__.get(p_code)["user_id"]
            self.password = SalesChannel.__dictionary__.get(p_code)["password"]
        except:
            self.code     = None
            self.id       = None
            self.name     = None
            self.user_id  = None
            self.password = None


    def __repr__(self):
        p_string ='''
            code:% s id:% s name:% s user_id:% s password:% s 
        '''
        return  p_string % (
            self.code, self.id, self.name, self.user_id, self.password
        )

    def __str__(self):
        p_string =rf'SALES CHANNEL - code:{self.code}, id:{self.id}, name:{self.name}, user_id:{self.user_id}, password:{self.password}'
        return p_string