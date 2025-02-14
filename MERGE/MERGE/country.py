
# ****************************************************************************************************************
# CLASS: Country
# ****************************************************************************************************************
class Country:
    """Etch & Cut Country Class"""

    __dictionary__ = {
        "Ireland"       : {"full_name": "Ireland",                                                       "alpha_2_code": "IE", "alpha_3_code": "IRL", "numeric_code": 372}
    ,   "United Kingdom": {"full_name": "United Kingdom of Great Britain and Northern Ireland (the)",    "alpha_2_code": "GB", "alpha_3_code": "GBR", "numeric_code": 826}
    ,   "United States" : {"full_name": "United States of America (the)",                                "alpha_2_code": "US", "alpha_3_code": "USA", "numeric_code": 840}
    }

    def __init__(
        self
    ,   p_name
    ):
        try:
            Country.__dictionary__.get(p_name, p_name)

            self.short_name   = p_name
            self.full_name    = Country.__dictionary__.get(p_name)['full_name']
            self.alpha_2_code = Country.__dictionary__.get(p_name)['alpha_2_code']
            self.alpha_3_code = Country.__dictionary__.get(p_name)['alpha_3_code']
            self.numeric_code = Country.__dictionary__.get(p_name)['numeric_code']
        except:
            self.short_name   = None
            self.full_name    = None
            self.alpha_2_code = None
            self.alpha_3_code = None
            self.numeric_code = None

