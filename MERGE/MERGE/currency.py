
# ****************************************************************************************************************
# CLASS: Currency
# ****************************************************************************************************************
class Currency:
    """Etch & Cut Currency Class"""

    __dictionary__ = {
        "GBP": {"name": "Pound Sterling", "symbol": "£", "code": "GBP"}
    ,   "USD": {"name": "US Dollar"     , "symbol": "$", "code": "USD"}
    ,   "£":   {"name": "Pound Sterling", "symbol": "£", "code": "GBP"}
    ,   "$":   {"name": "US Dollar"     , "symbol": "$", "code": "USD"}
    }


    def __init__(
        self
    ,   p_code
    ):
        try:
            Currency.__dictionary__.get(p_code, p_code)

            self.name   = Currency.__dictionary__.get(p_code)['name']
            self.symbol = Currency.__dictionary__.get(p_code)['symbol']
            self.code   = Currency.__dictionary__.get(p_code)['code']

        except:
            self.name   = None
            self.symbol = None
            self.code   = None


    def __repr__(self):
        p_string ='''
            name:% s symbol:% s code:% s
        '''
        return  p_string % (
            self.name, self.symbol, self.code
        )

    def __str__(self):
        p_string =f'''Currency: name:{self.name}, symbol:{self.symbol}, name:{self.name}'''
        return p_string