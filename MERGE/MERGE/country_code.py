
# ****************************************************************************************************************
# CLASS: CountryCode
# ****************************************************************************************************************
class CountryCode:
    """Etch & Cut Country Class"""

    __dictionary__ = {
        "AF": {"name": "Afghanistan"        , "alpha_3_code": "AFG", "numeric_code": 4}
    ,   "AL": {"name": "Albania"            , "alpha_3_code": "ALB", "numeric_code": 8}
    ,   "DZ": {"name": "Algeria"            , "alpha_3_code": "DZA", "numeric_code": 12}
    ,   "AS": {"name": "American Samoa"     , "alpha_3_code": "ASM", "numeric_code": 16}
    ,   "AD": {"name": "Andorra"            , "alpha_3_code": "AND", "numeric_code": 20}
    ,   "AO": {"name": "Angola"             , "alpha_3_code": "AGO", "numeric_code": 24}
    ,   "AI": {"name": "Anguilla"           , "alpha_3_code": "AIA", "numeric_code": 660}
    ,   "AQ": {"name": "Antarctica"         , "alpha_3_code": "ATA", "numeric_code": 10}
    ,   "AG": {"name": "Antigua and Barbuda", "alpha_3_code": "ATG", "numeric_code": 28}
    ,   "AR": {"name": "Argentina"          , "alpha_3_code": "ARG", "numeric_code": 32}
    ,   "AM": {"name": "Armenia"            , "alpha_3_code": "ARM", "numeric_code": 51}
    ,   "AW": {"name": "Aruba"              , "alpha_3_code": "ABW", "numeric_code": 533}
    ,   "AU": {"name": "Australia"          , "alpha_3_code": "AUS", "numeric_code": 36}
    ,   "AT": {"name": "Austria"            , "alpha_3_code": "AUT", "numeric_code": 40}
    ,   "AZ": {"name": "Azerbaijan"         , "alpha_3_code": "AZE", "numeric_code": 31}
    ,   "BS": {"name": "Bahamas (the)"      , "alpha_3_code": "BHS", "numeric_code": 44}
    ,   "BH": {"name": "Bahrain"            , "alpha_3_code": "BHR", "numeric_code": 48}
    ,   "BD": {"name": "Bangladesh"         , "alpha_3_code": "BGD", "numeric_code": 50}
    ,   "BB": {"name": "Barbados", "alpha_3_code": "BRB", "numeric_code": 52}
    ,   "BY": {"name": "Belarus", "alpha_3_code": "BLR", "numeric_code": 112}
    ,   "BE": {"name": "Belgium", "alpha_3_code": "BEL", "numeric_code": 56}
    ,   "BZ": {"name": "Belize", "alpha_3_code": "BLZ", "numeric_code": 84}
    ,   "BJ": {"name": "Benin", "alpha_3_code": "BEN", "numeric_code": 204}
    ,   "BM": {"name": "Bermuda", "alpha_3_code": "BMU", "numeric_code": 60}
    ,   "BT": {"name": "Bhutan", "alpha_3_code": "BTN", "numeric_code": 64}
    ,   "BO": {"name": "Bolivia (Plurinational State of)", "alpha_3_code": "BOL", "numeric_code": 68}
    ,   "BQ": {"name": "Bonaire, Sint Eustatius and Saba", "alpha_3_code": "BES", "numeric_code": 535}
    ,   "BA": {"name": "Bosnia and Herzegovina", "alpha_3_code": "BIH", "numeric_code": 70}
    ,   "BW": {"name": "Botswana", "alpha_3_code": "BWA", "numeric_code": 72}
    ,   "BV": {"name": "Bouvet Island", "alpha_3_code": "BVT", "numeric_code": 74}
    ,   "BR": {"name": "Brazil", "alpha_3_code": "BRA", "numeric_code": 76}
    ,   "IO": {"name": "British Indian Ocean Territory (the)", "alpha_3_code": "IOT", "numeric_code": 86}
    ,   "BN": {"name": "Brunei Darussalam", "alpha_3_code": "BRN", "numeric_code": 96}
    ,   "BG": {"name": "Bulgaria", "alpha_3_code": "BGR", "numeric_code": 100}
    ,   "BF": {"name": "Burkina Faso", "alpha_3_code": "BFA", "numeric_code": 854}
    ,   "BI": {"name": "Burundi", "alpha_3_code": "BDI", "numeric_code": 108}
    ,   "CV": {"name": "Cabo Verde", "alpha_3_code": "CPV", "numeric_code": 132}
    ,   "KH": {"name": "Cambodia", "alpha_3_code": "KHM", "numeric_code": 116}
    ,   "CM": {"name": "Cameroon", "alpha_3_code": "CMR", "numeric_code": 120}
    ,   "CA": {"name": "Canada", "alpha_3_code": "CAN", "numeric_code": 124}
    ,   "KY": {"name": "Cayman Islands (the)", "alpha_3_code": "CYM", "numeric_code": 136}
    ,   "CF": {"name": "Central African Republic (the)", "alpha_3_code": "CAF", "numeric_code": 140}
    ,   "TD": {"name": "Chad", "alpha_3_code": "TCD", "numeric_code": 148}
    ,   "CL": {"name": "Chile", "alpha_3_code": "CHL", "numeric_code": 152}
    ,   "CN": {"name": "China", "alpha_3_code": "CHN", "numeric_code": 156}
    ,   "CX": {"name": "Christmas Island", "alpha_3_code": "CXR", "numeric_code": 162}
    ,   "CC": {"name": "Cocos (Keeling) Islands (the)", "alpha_3_code": "CCK", "numeric_code": 166}
    ,   "CO": {"name": "Colombia", "alpha_3_code": "COL", "numeric_code": 170}
    ,   "KM": {"name": "Comoros (the)", "alpha_3_code": "COM", "numeric_code": 174}
    ,   "CD": {"name": "Congo (the Democratic Republic of the)", "alpha_3_code": "COD", "numeric_code": 180}
    ,   "CG": {"name": "Congo (the)", "alpha_3_code": "COG", "numeric_code": 178}
    ,   "CK": {"name": "Cook Islands (the)", "alpha_3_code": "COK", "numeric_code": 184}
    ,   "CR": {"name": "Costa Rica", "alpha_3_code": "CRI", "numeric_code": 188}
    ,   "HR": {"name": "Croatia", "alpha_3_code": "HRV", "numeric_code": 191}
    ,   "CU": {"name": "Cuba", "alpha_3_code": "CUB", "numeric_code": 192}
    ,   "CY": {"name": "Cyprus", "alpha_3_code": "CYP", "numeric_code": 196}
    ,   "CZ": {"name": "Czechia", "alpha_3_code": "CZE", "numeric_code": 203}
    ,   "DK": {"name": "Denmark", "alpha_3_code": "DNK", "numeric_code": 208}
    ,   "DJ": {"name": "Djibouti", "alpha_3_code": "DJI", "numeric_code": 262}
    ,   "DM": {"name": "Dominica", "alpha_3_code": "DMA", "numeric_code": 212}
    ,   "DO": {"name": "Dominican Republic (the)", "alpha_3_code": "DOM", "numeric_code": 214}
    ,   "EC": {"name": "Ecuador", "alpha_3_code": "ECU", "numeric_code": 218}
    ,   "EG": {"name": "Egypt", "alpha_3_code": "EGY", "numeric_code": 818}
    ,   "SV": {"name": "El Salvador", "alpha_3_code": "SLV", "numeric_code": 222}
    ,   "GQ": {"name": "Equatorial Guinea", "alpha_3_code": "GNQ", "numeric_code": 226}
    ,   "ER": {"name": "Eritrea", "alpha_3_code": "ERI", "numeric_code": 232}
    ,   "EE": {"name": "Estonia", "alpha_3_code": "EST", "numeric_code": 233}
    ,   "SZ": {"name": "Eswatini", "alpha_3_code": "SWZ", "numeric_code": 748}
    ,   "ET": {"name": "Ethiopia", "alpha_3_code": "ETH", "numeric_code": 231}
    ,   "FK": {"name": "Falkland Islands (the) [Malvinas]", "alpha_3_code": "FLK", "numeric_code": 238}
    ,   "FO": {"name": "Faroe Islands (the)", "alpha_3_code": "FRO", "numeric_code": 234}
    ,   "FJ": {"name": "Fiji", "alpha_3_code": "FJI", "numeric_code": 242}
    ,   "FI": {"name": "Finland", "alpha_3_code": "FIN", "numeric_code": 246}
    ,   "FR": {"name": "France", "alpha_3_code": "FRA", "numeric_code": 250}
    ,   "GF": {"name": "French Guiana", "alpha_3_code": "GUF", "numeric_code": 254}
    ,   "PF": {"name": "French Polynesia", "alpha_3_code": "PYF", "numeric_code": 258}
    ,   "TF": {"name": "French Southern Territories (the)", "alpha_3_code": "ATF", "numeric_code": 260}
    ,   "GA": {"name": "Gabon", "alpha_3_code": "GAB", "numeric_code": 266}
    ,   "GM": {"name": "Gambia (the)", "alpha_3_code": "GMB", "numeric_code": 270}
    ,   "GE": {"name": "Georgia", "alpha_3_code": "GEO", "numeric_code": 268}
    ,   "DE": {"name": "Germany", "alpha_3_code": "DEU", "numeric_code": 276}
    ,   "GH": {"name": "Ghana", "alpha_3_code": "GHA", "numeric_code": 288}
    ,   "GI": {"name": "Gibraltar", "alpha_3_code": "GIB", "numeric_code": 292}
    ,   "GR": {"name": "Greece", "alpha_3_code": "GRC", "numeric_code": 300}
    ,   "GL": {"name": "Greenland", "alpha_3_code": "GRL", "numeric_code": 304}
    ,   "GD": {"name": "Grenada", "alpha_3_code": "GRD", "numeric_code": 308}
    ,   "GP": {"name": "Guadeloupe", "alpha_3_code": "GLP", "numeric_code": 312}
    ,   "GU": {"name": "Guam", "alpha_3_code": "GUM", "numeric_code": 316}
    ,   "GT": {"name": "Guatemala", "alpha_3_code": "GTM", "numeric_code": 320}
    ,   "GG": {"name": "Guernsey", "alpha_3_code": "GGY", "numeric_code": 831}
    ,   "GN": {"name": "Guinea", "alpha_3_code": "GIN", "numeric_code": 324}
    ,   "GW": {"name": "Guinea-Bissau", "alpha_3_code": "GNB", "numeric_code": 624}
    ,   "GY": {"name": "Guyana", "alpha_3_code": "GUY", "numeric_code": 328}
    ,   "HT": {"name": "Haiti", "alpha_3_code": "HTI", "numeric_code": 332}
    ,   "HM": {"name": "Heard Island and McDonald Islands", "alpha_3_code": "HMD", "numeric_code": 334}
    ,   "VA": {"name": "Holy See (the)", "alpha_3_code": "VAT", "numeric_code": 336}
    ,   "HN": {"name": "Honduras", "alpha_3_code": "HND", "numeric_code": 340}
    ,   "HK": {"name": "Hong Kong", "alpha_3_code": "HKG", "numeric_code": 344}
    ,   "HU": {"name": "Hungary", "alpha_3_code": "HUN", "numeric_code": 348}
    ,   "IS": {"name": "Iceland", "alpha_3_code": "ISL", "numeric_code": 352}
    ,   "IN": {"name": "India", "alpha_3_code": "IND", "numeric_code": 356}
    ,   "ID": {"name": "Indonesia", "alpha_3_code": "IDN", "numeric_code": 360}
    ,   "IR": {"name": "Iran (Islamic Republic of)", "alpha_3_code": "IRN", "numeric_code": 364}
    ,   "IQ": {"name": "Iraq", "alpha_3_code": "IRQ", "numeric_code": 368}
    ,   "IE": {"name": "Ireland", "alpha_3_code": "IRL", "numeric_code": 372}
    ,   "IM": {"name": "Isle of Man", "alpha_3_code": "IMN", "numeric_code": 833}
    ,   "IL": {"name": "Israel", "alpha_3_code": "ISR", "numeric_code": 376}
    ,   "IT": {"name": "Italy", "alpha_3_code": "ITA", "numeric_code": 380}
    ,   "JM": {"name": "Jamaica", "alpha_3_code": "JAM", "numeric_code": 388}
    ,   "JP": {"name": "Japan", "alpha_3_code": "JPN", "numeric_code": 392}
    ,   "JE": {"name": "Jersey", "alpha_3_code": "JEY", "numeric_code": 832}
    ,   "JO": {"name": "Jordan", "alpha_3_code": "JOR", "numeric_code": 400}
    ,   "KZ": {"name": "Kazakhstan", "alpha_3_code": "KAZ", "numeric_code": 398}
    ,   "KE": {"name": "Kenya", "alpha_3_code": "KEN", "numeric_code": 404}
    ,   "KI": {"name": "Kiribati", "alpha_3_code": "KIR", "numeric_code": 296}
    ,   "KP": {"name": "Korea (the Democratic People's Republic of)", "alpha_3_code": "PRK", "numeric_code": 408}
    ,   "KR": {"name": "Korea (the Republic of)", "alpha_3_code": "KOR", "numeric_code": 410}
    ,   "KW": {"name": "Kuwait", "alpha_3_code": "KWT", "numeric_code": 414}
    ,   "KG": {"name": "Kyrgyzstan", "alpha_3_code": "KGZ", "numeric_code": 417}
    ,   "LA": {"name": "Lao People's Democratic Republic (the)", "alpha_3_code": "LAO", "numeric_code": 418}
    ,   "LV": {"name": "Latvia", "alpha_3_code": "LVA", "numeric_code": 428}
    ,   "LB": {"name": "Lebanon", "alpha_3_code": "LBN", "numeric_code": 422}
    ,   "LS": {"name": "Lesotho", "alpha_3_code": "LSO", "numeric_code": 426}
    ,   "LR": {"name": "Liberia", "alpha_3_code": "LBR", "numeric_code": 430}
    ,   "LY": {"name": "Libya", "alpha_3_code": "LBY", "numeric_code": 434}
    ,   "LI": {"name": "Liechtenstein", "alpha_3_code": "LIE", "numeric_code": 438}
    ,   "LT": {"name": "Lithuania", "alpha_3_code": "LTU", "numeric_code": 440}
    ,   "LU": {"name": "Luxembourg", "alpha_3_code": "LUX", "numeric_code": 442}
    ,   "MO": {"name": "Macao", "alpha_3_code": "MAC", "numeric_code": 446}
    ,   "MG": {"name": "Madagascar", "alpha_3_code": "MDG", "numeric_code": 450}
    ,   "MW": {"name": "Malawi", "alpha_3_code": "MWI", "numeric_code": 454}
    ,   "MY": {"name": "Malaysia", "alpha_3_code": "MYS", "numeric_code": 458}
    ,   "MV": {"name": "Maldives", "alpha_3_code": "MDV", "numeric_code": 462}
    ,   "ML": {"name": "Mali", "alpha_3_code": "MLI", "numeric_code": 466}
    ,   "MT": {"name": "Malta", "alpha_3_code": "MLT", "numeric_code": 470}
    ,   "MH": {"name": "Marshall Islands (the)", "alpha_3_code": "MHL", "numeric_code": 584}
    ,   "MQ": {"name": "Martinique", "alpha_3_code": "MTQ", "numeric_code": 474}
    ,   "MR": {"name": "Mauritania", "alpha_3_code": "MRT", "numeric_code": 478}
    ,   "MU": {"name": "Mauritius", "alpha_3_code": "MUS", "numeric_code": 480}
    ,   "YT": {"name": "Mayotte", "alpha_3_code": "MYT", "numeric_code": 175}
    ,   "MX": {"name": "Mexico", "alpha_3_code": "MEX", "numeric_code": 484}
    ,   "FM": {"name": "Micronesia (Federated States of)", "alpha_3_code": "FSM", "numeric_code": 583}
    ,   "MD": {"name": "Moldova (the Republic of)", "alpha_3_code": "MDA", "numeric_code": 498}
    ,   "MC": {"name": "Monaco", "alpha_3_code": "MCO", "numeric_code": 492}
    ,   "MN": {"name": "Mongolia", "alpha_3_code": "MNG", "numeric_code": 496}
    ,   "ME": {"name": "Montenegro", "alpha_3_code": "MNE", "numeric_code": 499}
    ,   "MS": {"name": "Montserrat", "alpha_3_code": "MSR", "numeric_code": 500}
    ,   "MA": {"name": "Morocco", "alpha_3_code": "MAR", "numeric_code": 504}
    ,   "MZ": {"name": "Mozambique", "alpha_3_code": "MOZ", "numeric_code": 508}
    ,   "MM": {"name": "Myanmar", "alpha_3_code": "MMR", "numeric_code": 104}
    ,   "NA": {"name": "Namibia", "alpha_3_code": "NAM", "numeric_code": 516}
    ,   "NR": {"name": "Nauru", "alpha_3_code": "NRU", "numeric_code": 520}
    ,   "NP": {"name": "Nepal", "alpha_3_code": "NPL", "numeric_code": 524}
    ,   "NL": {"name": "Netherlands (the)", "alpha_3_code": "NLD", "numeric_code": 528}
    ,   "NC": {"name": "New Caledonia", "alpha_3_code": "NCL", "numeric_code": 540}
    ,   "NZ": {"name": "New Zealand", "alpha_3_code": "NZL", "numeric_code": 554}
    ,   "NI": {"name": "Nicaragua", "alpha_3_code": "NIC", "numeric_code": 558}
    ,   "NE": {"name": "Niger (the)", "alpha_3_code": "NER", "numeric_code": 562}
    ,   "NG": {"name": "Nigeria", "alpha_3_code": "NGA", "numeric_code": 566}
    ,   "NU": {"name": "Niue", "alpha_3_code": "NIU", "numeric_code": 570}
    ,   "NF": {"name": "Norfolk Island", "alpha_3_code": "NFK", "numeric_code": 574}
    ,   "MK": {"name": "North Macedonia", "alpha_3_code": "MKD", "numeric_code": 807}
    ,   "MP": {"name": "Northern Mariana Islands (the)", "alpha_3_code": "MNP", "numeric_code": 580}
    ,   "NO": {"name": "Norway", "alpha_3_code": "NOR", "numeric_code": 578}
    ,   "OM": {"name": "Oman", "alpha_3_code": "OMN", "numeric_code": 512}
    ,   "PK": {"name": "Pakistan", "alpha_3_code": "PAK", "numeric_code": 586}
    ,   "PW": {"name": "Palau", "alpha_3_code": "PLW", "numeric_code": 585}
    ,   "PS": {"name": "Palestine, State of", "alpha_3_code": "PSE", "numeric_code": 275}
    ,   "PA": {"name": "Panama", "alpha_3_code": "PAN", "numeric_code": 591}
    ,   "PG": {"name": "Papua New Guinea", "alpha_3_code": "PNG", "numeric_code": 598}
    ,   "PY": {"name": "Paraguay", "alpha_3_code": "PRY", "numeric_code": 600}
    ,   "PE": {"name": "Peru", "alpha_3_code": "PER", "numeric_code": 604}
    ,   "PH": {"name": "Philippines (the)", "alpha_3_code": "PHL", "numeric_code": 608}
    ,   "PN": {"name": "Pitcairn", "alpha_3_code": "PCN", "numeric_code": 612}
    ,   "PL": {"name": "Poland", "alpha_3_code": "POL", "numeric_code": 616}
    ,   "PT": {"name": "Portugal", "alpha_3_code": "PRT", "numeric_code": 620}
    ,   "PR": {"name": "Puerto Rico", "alpha_3_code": "PRI", "numeric_code": 630}
    ,   "QA": {"name": "Qatar", "alpha_3_code": "QAT", "numeric_code": 634}
    ,   "RO": {"name": "Romania", "alpha_3_code": "ROU", "numeric_code": 642}
    ,   "RU": {"name": "Russian Federation (the)", "alpha_3_code": "RUS", "numeric_code": 643}
    ,   "RW": {"name": "Rwanda", "alpha_3_code": "RWA", "numeric_code": 646}
    ,   "SH": {"name": "Saint Helena, Ascension and Tristan da Cunha", "alpha_3_code": "SHN", "numeric_code": 654}
    ,   "KN": {"name": "Saint Kitts and Nevis", "alpha_3_code": "KNA", "numeric_code": 659}
    ,   "LC": {"name": "Saint Lucia", "alpha_3_code": "LCA", "numeric_code": 662}
    ,   "MF": {"name": "Saint Martin (French part)", "alpha_3_code": "MAF", "numeric_code": 663}
    ,   "PM": {"name": "Saint Pierre and Miquelon", "alpha_3_code": "SPM", "numeric_code": 666}
    ,   "VC": {"name": "Saint Vincent and the Grenadines", "alpha_3_code": "VCT", "numeric_code": 670}
    ,   "WS": {"name": "Samoa", "alpha_3_code": "WSM", "numeric_code": 882}
    ,   "SM": {"name": "San Marino", "alpha_3_code": "SMR", "numeric_code": 674}
    ,   "ST": {"name": "Sao Tome and Principe", "alpha_3_code": "STP", "numeric_code": 678}
    ,   "SA": {"name": "Saudi Arabia", "alpha_3_code": "SAU", "numeric_code": 682}
    ,   "SN": {"name": "Senegal", "alpha_3_code": "SEN", "numeric_code": 686}
    ,   "RS": {"name": "Serbia", "alpha_3_code": "SRB", "numeric_code": 688}
    ,   "SC": {"name": "Seychelles", "alpha_3_code": "SYC", "numeric_code": 690}
    ,   "SL": {"name": "Sierra Leone", "alpha_3_code": "SLE", "numeric_code": 694}
    ,   "SG": {"name": "Singapore", "alpha_3_code": "SGP", "numeric_code": 702}
    ,   "SX": {"name": "Sint Maarten (Dutch part)", "alpha_3_code": "SXM", "numeric_code": 534}
    ,   "SK": {"name": "Slovakia", "alpha_3_code": "SVK", "numeric_code": 703}
    ,   "SI": {"name": "Slovenia", "alpha_3_code": "SVN", "numeric_code": 705}
    ,   "SB": {"name": "Solomon Islands", "alpha_3_code": "SLB", "numeric_code": 90}
    ,   "SO": {"name": "Somalia", "alpha_3_code": "SOM", "numeric_code": 706}
    ,   "ZA": {"name": "South Africa", "alpha_3_code": "ZAF", "numeric_code": 710}
    ,   "GS": {"name": "South Georgia and the South Sandwich Islands", "alpha_3_code": "SGS", "numeric_code": 239}
    ,   "SS": {"name": "South Sudan", "alpha_3_code": "SSD", "numeric_code": 728}
    ,   "ES": {"name": "Spain", "alpha_3_code": "ESP", "numeric_code": 724}
    ,   "LK": {"name": "Sri Lanka", "alpha_3_code": "LKA", "numeric_code": 144}
    ,   "SD": {"name": "Sudan (the)", "alpha_3_code": "SDN", "numeric_code": 729}
    ,   "SR": {"name": "Suriname", "alpha_3_code": "SUR", "numeric_code": 740}
    ,   "SJ": {"name": "Svalbard and Jan Mayen", "alpha_3_code": "SJM", "numeric_code": 744}
    ,   "SE": {"name": "Sweden", "alpha_3_code": "SWE", "numeric_code": 752}
    ,   "CH": {"name": "Switzerland", "alpha_3_code": "CHE", "numeric_code": 756}
    ,   "SY": {"name": "Syrian Arab Republic (the)", "alpha_3_code": "SYR", "numeric_code": 760}
    ,   "TW": {"name": "Taiwan (Province of China)", "alpha_3_code": "TWN", "numeric_code": 158}
    ,   "TJ": {"name": "Tajikistan", "alpha_3_code": "TJK", "numeric_code": 762}
    ,   "TZ": {"name": "Tanzania, the United Republic of", "alpha_3_code": "TZA", "numeric_code": 834}
    ,   "TH": {"name": "Thailand", "alpha_3_code": "THA", "numeric_code": 764}
    ,   "TL": {"name": "Timor-Leste", "alpha_3_code": "TLS", "numeric_code": 626}
    ,   "TG": {"name": "Togo", "alpha_3_code": "TGO", "numeric_code": 768}
    ,   "TK": {"name": "Tokelau", "alpha_3_code": "TKL", "numeric_code": 772}
    ,   "TO": {"name": "Tonga", "alpha_3_code": "TON", "numeric_code": 776}
    ,   "TT": {"name": "Trinidad and Tobago", "alpha_3_code": "TTO", "numeric_code": 780}
    ,   "TN": {"name": "Tunisia", "alpha_3_code": "TUN", "numeric_code": 788}
    ,   "TR": {"name": "Turkey", "alpha_3_code": "TUR", "numeric_code": 792}
    ,   "TM": {"name": "Turkmenistan", "alpha_3_code": "TKM", "numeric_code": 795}
    ,   "TC": {"name": "Turks and Caicos Islands (the)", "alpha_3_code": "TCA", "numeric_code": 796}
    ,   "TV": {"name": "Tuvalu", "alpha_3_code": "TUV", "numeric_code": 798}
    ,   "UG": {"name": "Uganda", "alpha_3_code": "UGA", "numeric_code": 800}
    ,   "UA": {"name": "Ukraine", "alpha_3_code": "UKR", "numeric_code": 804}
    ,   "AE": {"name": "United Arab Emirates (the)", "alpha_3_code": "ARE", "numeric_code": 784}
    ,   "GB": {"name": "United Kingdom", "alpha_3_code": "GBR", "numeric_code": 826}
    ,   "UM": {"name": "United States Minor Outlying Islands (the)", "alpha_3_code": "UMI", "numeric_code": 581}
    ,   "US": {"name": "United States", "alpha_3_code": "USA", "numeric_code": 840}
    ,   "UY": {"name": "Uruguay", "alpha_3_code": "URY", "numeric_code": 858}
    ,   "UZ": {"name": "Uzbekistan", "alpha_3_code": "UZB", "numeric_code": 860}
    ,   "VU": {"name": "Vanuatu", "alpha_3_code": "VUT", "numeric_code": 548}
    ,   "VE": {"name": "Venezuela (Bolivarian Republic of)", "alpha_3_code": "VEN", "numeric_code": 862}
    ,   "VN": {"name": "Viet Nam", "alpha_3_code": "VNM", "numeric_code": 704}
    ,   "VG": {"name": "Virgin Islands (British)", "alpha_3_code": "VGB", "numeric_code": 92}
    ,   "VI": {"name": "Virgin Islands (U.S.)", "alpha_3_code": "VIR", "numeric_code": 850}
    ,   "WF": {"name": "Wallis and Futuna", "alpha_3_code": "WLF", "numeric_code": 876}
    ,   "YE": {"name": "Yemen", "alpha_3_code": "YEM", "numeric_code": 887}
    ,   "ZM": {"name": "Zambia", "alpha_3_code": "ZMB", "numeric_code": 894}
    ,   "ZW": {"name": "Zimbabwe", "alpha_3_code": "ZWE", "numeric_code": 716}
    ,   "XX": {"name": "Not Found", "alpha_3_code": "XXX", "numeric_code": 0}
    }

    def __init__(
        self
    ,   p_code
    ):
        try:
            CountryCode.__dictionary__.get(p_code, p_code)

            self.country_code = p_code
            self.name         = CountryCode.__dictionary__.get(p_code)['name']
            self.alpha_3_code = CountryCode.__dictionary__.get(p_code)['alpha_3_code']
            self.numeric_code = CountryCode.__dictionary__.get(p_code)['numeric_code']
        except:
            self.name         = None
            self.alpha_3_code = None
            self.numeric_code = None


    def __repr__(self):
        p_string ='''
            code:% s name:% s alpha_3_code:% s numeric_code:% s
        '''
        return  p_string % (
            self.code, self.name, self.alpha_3_code, self.numeric_code
        )

    def __str__(self):
        p_string =f'''Country: code:{self.country_code}, name:{self.name}, alpha_3_code:{self.alpha_3_code}, numeric_code:{self.numeric_code}'''
        return p_string
