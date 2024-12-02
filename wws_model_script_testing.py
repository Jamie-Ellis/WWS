### Dependencies ###
import logging
import sys
import pandas as pd
import numpy as np
import random
import datetime
from typing import Optional
from pprint import pprint

# Changes
# New OLS and Mean statistics
# New handling of no n_livable_rooms
# New handling of standard garden size




### Reference ###
# region (Fixed Variables)


wws_table_point_to_rent = {40: 235.96, 41: 241.87, 42: 247.74, 43: 253.65, 44: 259.54, 45: 265.42, 46: 271.34, 47: 277.23, 48: 283.14, 49: 289.03, 50: 294.93, 51: 300.8, 52: 306.72, 53: 312.6, 54: 318.51, 55: 324.4, 56: 330.34, 57: 336.17, 58: 342.07, 59: 348.01, 60: 353.89, 61: 359.76, 62: 365.68, 63: 371.56, 64: 377.46, 65: 383.36, 66: 389.27, 67: 395.17, 68: 401.04, 69: 406.92, 70: 412.81, 71: 418.73, 72: 424.64, 73: 430.5, 74: 436.43, 75: 442.3, 76: 448.22, 77: 454.1, 78: 460.03, 79: 465.89, 80: 471.81, 81: 478.25, 82: 484.72, 83: 491.21, 84: 497.67, 85: 504.17, 86: 510.64, 87: 517.09, 88: 523.58, 89: 530.03, 90: 536.54, 91: 542.99, 92: 549.44, 93: 555.94, 94: 562.39, 95: 568.87, 96: 575.35, 97: 581.85, 98: 588.31, 99: 594.8, 100: 601.26, 101: 607.73, 102: 614.17, 103: 620.66, 104: 627.14, 105: 633.58, 106: 640.09, 107: 646.55, 108: 653.02, 109: 659.51, 110: 665.99, 111: 672.47, 112: 678.93, 113: 685.39, 114: 691.89, 115: 698.36, 116: 704.82, 117: 711.29, 118: 717.74, 119: 724.22, 120: 730.69, 121: 737.2, 122: 743.67, 123: 750.13, 124: 756.62, 125: 763.09, 126: 769.54, 127: 776.02, 128: 782.55, 129: 788.96, 130: 795.45, 131: 801.93, 132: 808.38, 133: 814.89, 134: 821.32, 135: 827.84, 136: 834.27, 137: 840.76, 138: 847.25, 139: 853.69, 140: 860.17, 141: 866.66, 142: 873.11, 143: 879.66, 144: 886.07, 145: 892.56, 146: 899.01, 147: 905.5, 148: 911.96, 149: 918.44, 150: 924.9, 151: 931.38, 152: 937.84, 153: 944.32, 154: 950.78, 155: 957.26, 156: 963.71, 157: 970.25, 158: 976.67, 159: 983.2, 160: 989.65, 161: 996.1, 162: 1002.61, 163: 1009.04, 164: 1015.51, 165: 1022.0, 166: 1028.49, 167: 1034.94, 168: 1041.4, 169: 1047.93, 170: 1054.38, 171: 1060.84, 172: 1067.31, 173: 1073.82, 174: 1080.27, 175: 1086.74, 176: 1093.2, 177: 1099.68, 178: 1106.16, 179: 1112.63, 180: 1119.07, 181: 1125.6, 182: 1132.06, 183: 1138.52, 184: 1144.97, 185: 1151.48, 186: 1157.95, 187: 1164.41, 188: 1170.91, 189: 1177.36, 190: 1183.84, 191: 1190.32, 192: 1196.78, 193: 1203.26, 194: 1209.75, 195: 1216.21, 196: 1222.66, 197: 1229.14, 198: 1235.64, 199: 1242.07, 200: 1248.58, 201: 1255.03, 202: 1261.5, 203: 1267.97, 204: 1274.46, 205: 1280.94, 206: 1287.39, 207: 1293.89, 208: 1300.35, 209: 1306.82, 210: 1313.32, 211: 1319.78, 212: 1326.25, 213: 1332.73, 214: 1339.19, 215: 1345.67, 216: 1352.12, 217: 1358.6, 218: 1365.06, 219: 1371.55, 220: 1378.05, 221: 1384.48, 222: 1390.97, 223: 1397.44, 224: 1403.93, 225: 1410.37, 226: 1416.87, 227: 1423.34, 228: 1429.82, 229: 1436.3, 230: 1442.75, 231: 1449.22, 232: 1455.7, 233: 1462.17, 234: 1468.63, 235: 1475.13, 236: 1481.59, 237: 1488.06, 238: 1494.51, 239: 1501.02, 240: 1507.48, 241: 1513.96, 242: 1520.45, 243: 1526.9, 244: 1533.39, 245: 1539.86, 246: 1546.33, 247: 1552.76, 248: 1559.28, 249: 1565.73, 250: 1572.2}

RENAME_PROPERTY_TYPE_MAP = {
    "Flatwoning (overig)": "flat_dwelling_other",
    "Appartement": "apartment",
    "Galerijwoning": "gallery_access_apartment",
    "Galerijflat": "gallery_access_apartment",  
    "Portiekwoning": "portico_access_apartment",
    "Portiekflat": "portico_access_apartment", 
    "Bovenwoning": "upper_floor_apartment",
    "Benedenwoning": "ground_floor_apartment",
    "BenedenPlusBovenwoning": "ground_floor_plus_upper_apartment",
    "Tussenverdieping": "intermediate_floor_apartment",
    "DubbelBenedenhuis": "double_ground_floor_apartment",
    "Maisonnette": "maisonette",
    "Penthouse": "penthouse",
    "Kamer": "invalid",
    "Studentenkamer": "invalid", 
    "Logieswoning": "boarding_house",
    "Woongebouw met niet-zelfstandige woonruimte": "invalid",
    "Huis": "house",
    "Rijwoning tussen": "mid_terrace_house",
    "Tussenwoning": "mid_terrace_house", 
    "Rijwoning hoek": "end_terrace_house",
    "Hoekwoning": "end_terrace_house",  
    "Eindwoning": "end_terrace_house",  
    "Twee-onder-één-kap": "semi_detached_house",
    "TweeOnderEenKapwoning": "semi_detached_house", 
    "Twee-onder-een-kap / rijwoning hoek": "semi_detached_end_terrace_house",
    "GeschakeldeTweeOnderEenKapwoning": "linked_semi_detached_house",
    "Vrijstaande woning": "detached_house",
    "Vrijstaandewoning": "detached_house",  
    "Halfvrijstaandewoning": "semi_detached_house", 
    "Geschakeldewoning": "terraced_house",
    "Verspringend": "staggered_row_houses",
    "Woonboot bestaande ligplaats": "invalid",
    "Woonboot nieuwe ligplaats": "invalid",

    # Cat -> Type
    "apartment": "apartment",
    "house": "house"
}

RENAME_PROPERTY_CAT_MAP = {
    "Flatwoning (overig)": "apartment", 
    "Appartement": "apartment",  
    "Galerijwoning": "apartment",  
    "Galerijflat": "apartment",  
    "Portiekwoning": "apartment",  
    "Portiekflat": "apartment",  
    "Bovenwoning": "apartment",  
    "Benedenwoning": "apartment", 
    "BenedenPlusBovenwoning": "apartment", 
    "Tussenverdieping": "apartment",  
    "DubbelBenedenhuis": "apartment", 
    "Maisonnette": "apartment",  
    "Penthouse": "apartment",  
    "Kamer": "apartment",  
    "Studentenkamer": "apartment",  
    "Logieswoning": "apartment", 
    "Woongebouw met niet-zelfstandige woonruimte": "apartment",  
    "Huis": "house",  
    "Rijwoning tussen": "house", 
    "Tussenwoning": "house",  
    "Rijwoning hoek": "house", 
    "Hoekwoning": "house", 
    "Eindwoning": "house",  
    "Twee-onder-één-kap": "house", 
    "TweeOnderEenKapwoning": "house", 
    "Twee-onder-een-kap / rijwoning hoek": "house", 
    "GeschakeldeTweeOnderEenKapwoning": "house", 
    "Vrijstaande woning": "house",  
    "Vrijstaandewoning": "house",  
    "Halfvrijstaandewoning": "house", 
    "Geschakeldewoning": "house", 
    "Verspringend": "house", 
    "Woonboot bestaande ligplaats": "house", 
    "Woonboot nieuwe ligplaats": "house",  

    # Cat -> Cat
    "apartment": "apartment", 
    "house": "house"  
}

RENAME_PROPERTY_TYPE_MAP = {k.lower(): v.lower() for k, v in RENAME_PROPERTY_TYPE_MAP.items()}
RENAME_PROPERTY_CAT_MAP = {k.lower(): v.lower() for k, v in RENAME_PROPERTY_CAT_MAP.items()}
VALID_PROPERTY_TYPES_DUTCH = [k for k in RENAME_PROPERTY_TYPE_MAP.keys()]
VALID_PROPERTY_TYPES_ENGLISH = list(set(RENAME_PROPERTY_TYPE_MAP.values()))

DISCLAIMER_MONUMENTS = (
    "The WWS calculation provided does not account for exemptions or special rules "
    "applicable to properties classified as national, provincial, or municipal monuments. Specific adjustments, "
    "such as exemptions from negative energy performance points, must be verified with relevant authorities."
)

DISCLAIMER_SHARED = (
    "Shared housing arrangements may fall under distinct conditions that affect their eligibility as self-contained dwellings. "
    "The WWS calculation provided here does not reflect these conditions. Users are strongly encouraged to review applicable laws "
    "and seek professional advice where necessary."
)

ENERGY_SCORE_MAP = {
        np.nan: None,
        "G": 10,
        "F": 9,
        "E": 8,
        "D": 7,
        "C": 6,
        "B": 5,
        "A": 4,
        "A+": 3,
        "A++": 2,
        "A+++": 1,
        "A++++": 0,
        "A+++++": 0
    }

COROP_CODES = [
    'GM0358', 'GM0362', 'GM0363', 'GM0384', 'GM0385', 'GM0394', 'GM0415', 'GM0431',
    'GM0437', 'GM0439', 'GM0451', 'GM0852', 'GM0307', 'GM0308', 'GM0310', 'GM0312',
    'GM0313', 'GM0317', 'GM0321', 'GM0353', 'GM0327', 'GM0331', 'GM0335', 'GM0356',
    'GM0589', 'GM0339', 'GM0340', 'GM0736', 'GM0342', 'GM1904', 'GM0344', 'GM1581',
    'GM0345', 'GM1961', 'GM0352', 'GM0632', 'GM0351', 'GM0355'
]

CAP_THRESHOLD = 186
CAP_MIN_TOTAL_POINTS = 186
EXCEPTION_RULE_YEAR_RANGE = (2018, 2022)
EXCEPTION_RULE_AREA_LIMIT = 40
EXCEPTION_RULE_ADDITIONAL_YEAR_RANGE = (2015, 2019)
EXCEPTION_RULE_MIN_WWS_MIN = 110
EXCEPTION_RULE_MIN_WOZ_POINTS = 40


# endregion

# region (Statistics & Estimation Functions)

def static_estimate_n_livable_rooms(living_space, base_room_size=25):
    estimated_rooms = living_space / base_room_size
    return max(1, int(round(estimated_rooms)))

garden_space_apartment_mean = 46
garden_space_house_mean = 77

def bedroom_to_rooms_ols(living_space, n_bedrooms, constr_year):
    const = 0.925777
    living_space_c = 0.004861
    living_space_sqrd_c = -0.000003
    n_bedrooms_c = 0.956303
    construction_year_c = -0.000093
    n_livable_rooms = (const + 
                       living_space * living_space_c + 
                       (living_space ** 2) * living_space_sqrd_c + 
                       n_bedrooms * n_bedrooms_c + 
                       constr_year * construction_year_c)
    return n_livable_rooms


# endregion

# region (Rich Base Models)


# Apartment Model
apartment_model = {
    # Kitchen
    "gas_oven": (False, False),                    # Property has a gas oven
    "electric_oven": (False, False),               # Property has an electric oven
    "ceramic_cooktop": (False, False),             # Property has a ceramic cooktop
    "induction_cooktop": (False, False),           # Property has an induction cooktop
    "exhaust_system": (False, False),              # Property has an exhaust system
    "freezer": (False, False),                     # Property has a freezer
    "refrigerator": (False, False),                # Property has a refrigerator
    "microwave": (False, False),                   # Property has a microwave
    "dishwasher": (False, False),                  # Property has a dishwasher

    # Bathroom
    "toilet": (False, False),                      # Property has a toilet
    "separate_toilet": (False, False),             # Property has a separate toilet room
    "sink": (False, False),                         # Property has a sink
    "double_sink": (False, False),                 # Property has double sinks
    "shower": (False, False),                       # Property has a shower
    "shower_enclosure": (False, False),            # Property has a shower enclosure
    "bathtub": (False, False),                     # Property has a bathtub
    "bubble_function": (False, False),            # Property has a bathtub with a bubble function
    "towel_radiator": (False, False),              # Property has a towel radiator
    "thermo_faucet": (False, False),               # Property has a thermostatic faucet
    "built_in_cabinet": (False, False),            # Property has a built-in cabinet
    "cabinet_extra_storage": (False, False),       # Property has extra storage cabinets
    "hanging_toilet": (False, False),              # Property has a wall-mounted toilet

    # Outside
    'private_outside_space': (False, False),      # Property has private outdoor space
    'shared_outside_space': (False, False),       # Property has shared outdoor space
    'outside_space': 0,                           # Amount of outdoor space available
    'pct_private_to_shared': (0, 0),              # Percentage of private to shared outdoor space
    'n_sharing_outside_space': (0, 0),         # Number of units sharing outdoor space

    # Parking
    "private_garage": (False, False),             # Property has a private garage
    "shared_garage": (False, False),              # Property has a shared garage
    "other_shared_parking": (False, False),       # Property has other types of shared parking
    "n_sharing_shared_parking": (0, 0)            # Number of units sharing parking
}

# House Model
house_model = {
    # Kitchen
    "gas_oven": (False, False),                    # Property has a gas oven
    "electric_oven": (False, False),               # Property has an electric oven
    "ceramic_cooktop": (False, False),             # Property has a ceramic cooktop
    "induction_cooktop": (False, False),           # Property has an induction cooktop
    "exhaust_system": (False, False),              # Property has an exhaust system
    "freezer": (False, False),                     # Property has a freezer
    "refrigerator": (False, False),                # Property has a refrigerator
    "microwave": (False, False),                   # Property has a microwave
    "dishwasher": (False, False),                  # Property has a dishwasher

    # Bathroom
    "toilet": (False, False),                      # Property has a toilet
    "separate_toilet": (False, False),             # Property has a separate toilet room
    "sink": (False, False),                         # Property has a sink
    "double_sink": (False, False),                 # Property has double sinks
    "shower": (False, False),                       # Property has a shower
    "shower_enclosure": (False, False),            # Property has a shower enclosure
    "bathtub": (False, False),                     # Property has a bathtub
    "bubble_function": (False, False),            # Property has a bathtub with a bubble function
    "towel_radiator": (False, False),              # Property has a towel radiator
    "thermo_faucet": (False, False),               # Property has a thermostatic faucet
    "built_in_cabinet": (False, False),            # Property has a built-in cabinet
    "cabinet_extra_storage": (False, False),       # Property has extra storage cabinets
    "hanging_toilet": (False, False),              # Property has a wall-mounted toilet

    # Outside
    'private_outside_space': (False, False),      # Property has private outdoor space
    'shared_outside_space': (False, False),       # Property has shared outdoor space
    'outside_space': 0,                           # Amount of outdoor space available
    'pct_private_to_shared': (0, 0),              # Percentage of private to shared outdoor space
    'n_sharing_outside_space': (0, 0),            # Number of units sharing outdoor space

    # Parking
    "private_garage": (False, False),             # Property has a private garage
    "shared_garage": (False, False),              # Property has a shared garage
    "other_shared_parking": (False, False),       # Property has other types of shared parking
    "n_sharing_shared_parking": (0, 0)            # Number of units sharing parking
}


# endregion

# region (Sparse Base Models)


low_apartment = {
    # Kitchen
    'kitchen_countertop_point': (7, 7),
    "gas_oven": (True, True),                     # Property has a gas oven
    "electric_oven": (False, False),              # Property has an electric oven
    "gas_cooktop": (True, False),                  # Property has a gas cooktop
    "ceramic_cooktop": (False, True),              # Property has a ceramic cooktop
    "induction_cooktop": (False, False),          # Property has an induction cooktop
    "exhaust_system": (False, False),             # Property has an exhaust system
    "freezer": (False, False),                    # Property has a freezer
    "refrigerator": (False, False),               # Property has a refrigerator
    "microwave": (False, False),                  # Property has a microwave
    "dishwasher": (False, False),                 # Property has a dishwasher

    # Bathroom
    "toilet": (True, True),                       # Property has a toilet
    "separate_toilet": (False, False),            # Property has a separate toilet room
    "sink": (True, True),                         # Property has a sink
    "double_sink": (False, False),                # Property has double sinks
    "shower": (True, True),                       # Property has a shower
    "shower_enclosure": (False, False),           # Property has a shower enclosure
    "bathtub": (False, False),                    # Property has a bathtub
    "bubble_function": (False, False),            # Property has a bathtub with a bubble function
    "towel_radiator": (False, False),             # Property has a towel radiator
    "thermo_faucet": (False, False),              # Property has a thermostatic faucet
    "built_in_cabinet": (False, False),           # Property has a built-in cabinet
    "cabinet_extra_storage": (False, False),      # Property has extra storage cabinets
    "hanging_toilet": (False, False),             # Property has a wall-mounted toilet

    # Outside
    "private_outside_space": (False, False),      # Property has private outdoor space
    "shared_outside_space": (False, False),       # Property has shared outdoor space
    "outside_space": (None, None),                # Amount of outdoor space available
    "pct_private_to_shared": (0, 0),              # Percentage of private to shared outdoor space
    "n_sharing_outside_space": (None, None),      # Number of units sharing outdoor space

    # Parking
    "private_garage": (False, False),             # Property has a private garage
    "shared_garage": (False, False),              # Property has a shared garage
    "other_shared_parking": (False, False),       # Property has other types of shared parking
    "n_sharing_shared_parking": (None, None)      # Number of units sharing parking
}

# Mid-range Apartment Model
mid_apartment = {
    # Kitchen
    'kitchen_countertop_point': (7, 7),
    "gas_oven": (False, False),                   # Property has a gas oven
    "electric_oven": (True, True),                # Property has an electric oven
    "ceramic_cooktop": (False, False),            # Property has a ceramic cooktop
    "gas_cooktop": (False, False), 
    "induction_cooktop": (True, True),            # Property has an induction cooktop
    "exhaust_system": (True, True),               # Property has an exhaust system
    "freezer": (True, True),                      # Property has a freezer
    "refrigerator": (True, True),                 # Property has a refrigerator
    "microwave": (False, False),                  # Property has a microwave
    "dishwasher": (True, True),                   # Property has a dishwasher

    # Bathroom
    "toilet": (True, True),                       # Property has a toilet
    "separate_toilet": (False, False),            # Property has a separate toilet room
    "sink": (True, True),                         # Property has a sink
    "double_sink": (False, False),                # Property has double sinks
    "shower": (True, True),                       # Property has a shower
    "shower_enclosure": (True, True),             # Property has a shower enclosure
    "bathtub": (False, False),                    # Property has a bathtub
    "bubble_function": (False, False),            # Property has a bathtub with a bubble function
    "towel_radiator": (False, False),             # Property has a towel radiator
    "thermo_faucet": (False, False),              # Property has a thermostatic faucet
    "built_in_cabinet": (True, True),             # Property has a built-in cabinet
    "cabinet_extra_storage": (False, False),      # Property has extra storage cabinets
    "hanging_toilet": (False, False),             # Property has a wall-mounted toilet

    # Outside
    "private_outside_space": (False, False),      # Property has private outdoor space
    "shared_outside_space": (True, True),       # Property has shared outdoor space
    "outside_space": (0, garden_space_apartment_mean * 0.75),                # Amount of outdoor space available
    "pct_private_to_shared": (0, 0),              # Percentage of private to shared outdoor space
    "n_sharing_outside_space": (25, 5),      # Number of units sharing outdoor space

    # Parking
    "private_garage": (False, False),             # Property has a private garage
    "shared_garage": (False, False),              # Property has a shared garage
    "other_shared_parking": (True, True),         # Property has other types of shared parking
    "n_sharing_shared_parking": (1, 1)            # Number of units sharing parking
}

# High-end Apartment Model
high_apartment = {
    # Kitchen
    'kitchen_countertop_point': (7, 7),
    "gas_oven": (False, False),                   # Property has a gas oven
    "electric_oven": (True, True),                # Property has an electric oven
    "ceramic_cooktop": (False, False),            # Property has a ceramic cooktop
    "gas_cooktop": (False, False), 
    "induction_cooktop": (True, True),            # Property has an induction cooktop
    "exhaust_system": (True, True),               # Property has an exhaust system
    "freezer": (True, True),                      # Property has a freezer
    "refrigerator": (True, True),                 # Property has a refrigerator
    "microwave": (True, True),                    # Property has a microwave
    "dishwasher": (True, True),                   # Property has a dishwasher

    # Bathroom
    "toilet": (True, True),                       # Property has a toilet
    "separate_toilet": (True, True),              # Property has a separate toilet room
    "sink": (True, True),                         # Property has a sink
    "double_sink": (True, True),                  # Property has double sinks
    "shower": (True, True),                       # Property has a shower
    "shower_enclosure": (True, True),             # Property has a shower enclosure
    "bathtub": (False, True),                      # Property has a bathtub
    "bubble_function": (False, True),              # Property has a bathtub with a bubble function
    "towel_radiator": (True, True),               # Property has a towel radiator
    "thermo_faucet": (True, True),                # Property has a thermostatic faucet
    "built_in_cabinet": (True, True),             # Property has a built-in cabinet
    "cabinet_extra_storage": (True, True),        # Property has extra storage cabinets
    "hanging_toilet": (True, True),             # Property has a wall-mounted toilet

    # Outside
    "private_outside_space": (False, True),      # Property has private outdoor space
    "shared_outside_space": (True, False),         # Property has shared outdoor space
    "outside_space": (garden_space_apartment_mean - 10, garden_space_apartment_mean + 10),                    # Amount of outdoor space available
    "pct_private_to_shared": (0, 1),              # Percentage of private to shared outdoor space
    "n_sharing_outside_space": (5, 1),          # Number of units sharing outdoor space

    # Parking
    "private_garage": (False, True),             # Property has a private garage
    "shared_garage": (True, False),                # Property has a shared garage
    "other_shared_parking": (False, False),       # Property has other types of shared parking
    "n_sharing_shared_parking": (1, 1)            # Number of units sharing parking
}

# Low-end House
low_house = {
    # Kitchen
    'kitchen_countertop_point': (7, 7),
    "gas_oven": (True, True),                     # Property has a gas oven
    "electric_oven": (False, False),              # Property has an electric oven
    "ceramic_cooktop": (True, True),              # Property has a ceramic cooktop
    "gas_cooktop": (False, False), 
    "induction_cooktop": (False, False),          # Property has an induction cooktop
    "exhaust_system": (False, False),             # Property has an exhaust system
    "freezer": (False, False),                    # Property has a freezer
    "refrigerator": (False, False),               # Property has a refrigerator
    "microwave": (False, False),                  # Property has a microwave
    "dishwasher": (False, False),                 # Property has a dishwasher

    # Bathroom
    "toilet": (True, False),                       # Property has a toilet
    "separate_toilet": (False, True),            # Property has a separate toilet room
    "sink": (True, True),                         # Property has a sink
    "double_sink": (False, False),                # Property has double sinks
    "shower": (True, True),                       # Property has a shower
    "shower_enclosure": (False, False),           # Property has a shower enclosure
    "bathtub": (False, False),                    # Property has a bathtub
    "bubble_function": (False, False),            # Property has a bathtub with a bubble function
    "towel_radiator": (False, False),             # Property has a towel radiator
    "thermo_faucet": (False, False),              # Property has a thermostatic faucet
    "built_in_cabinet": (False, False),           # Property has a built-in cabinet
    "cabinet_extra_storage": (False, False),      # Property has extra storage cabinets
    "hanging_toilet": (False, False),             # Property has a wall-mounted toilet

    # Outside
    "private_outside_space": (False, False),      # Property has private outdoor space
    "shared_outside_space": (True, True),         # Property has shared outdoor space
    "outside_space": (garden_space_house_mean - 10, garden_space_house_mean + 10),                    # Amount of outdoor space available
    "pct_private_to_shared": (0, 0),              # Percentage of private to shared outdoor space
    "n_sharing_outside_space": (3, 3),            # Number of units sharing outdoor space

    # Parking
    "private_garage": (False, False),             # Property has a private garage
    "shared_garage": (False, False),              # Property has a shared garage
    "other_shared_parking": (True, True),         # Property has other types of shared parking
    "n_sharing_shared_parking": (1, 1)            # Number of units sharing parking
}

# Mid-high House
mid_high_house = {
    # Kitchen
    'kitchen_countertop_point': (7, 7),
    "gas_oven": (False, False),                   # Property has a gas oven
    "electric_oven": (True, True),                # Property has an electric oven
    "ceramic_cooktop": (False, False),            # Property has a ceramic cooktop
    "gas_cooktop": (False, False), 
    "induction_cooktop": (True, True),            # Property has an induction cooktop
    "exhaust_system": (True, True),               # Property has an exhaust system
    "freezer": (True, True),                      # Property has a freezer
    "refrigerator": (True, True),                 # Property has a refrigerator
    "microwave": (True, True),                    # Property has a microwave
    "dishwasher": (True, True),                   # Property has a dishwasher

    # Bathroom
    "toilet": (True, True),                       # Property has a toilet
    "separate_toilet": (True, True),              # Property has a separate toilet room
    "sink": (True, True),                         # Property has a sink
    "double_sink": (True, True),                  # Property has double sinks
    "shower": (True, True),                       # Property has a shower
    "shower_enclosure": (True, True),             # Property has a shower enclosure
    "bathtub": (True, True),                      # Property has a bathtub
    "bubble_function": (False, False),            # Property has a bathtub with a bubble function
    "towel_radiator": (True, True),               # Property has a towel radiator
    "thermo_faucet": (True, True),                # Property has a thermostatic faucet
    "built_in_cabinet": (True, True),             # Property has a built-in cabinet
    "cabinet_extra_storage": (True, True),        # Property has extra storage cabinets
    "hanging_toilet": (True, True),               # Property has a wall-mounted toilet

    # Outside
    "private_outside_space": (True, True),        # Property has private outdoor space
    "shared_outside_space": (False, False),       # Property has shared outdoor space
    "outside_space": (garden_space_house_mean, garden_space_house_mean * 1.5),                    # Amount of outdoor space available
    "pct_private_to_shared": (1, 1),              # Percentage of private to shared outdoor space
    "n_sharing_outside_space": (None, None),      # Number of units sharing outdoor space

    # Parking
    "private_garage": (True, True),               # Property has a private garage
    "shared_garage": (False, False),              # Property has a shared garage
    "other_shared_parking": (False, False),       # Property has other types of shared parking
    "n_sharing_shared_parking": (None, None)      # Number of units sharing parking
}


# endregion

# region (Help Functions)


# Initialize Logger
def init_logger(log_level=logging.INFO):
    logger = logging.getLogger('wws_logger')
    logger.setLevel(log_level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    if not logger.handlers:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    log_file = 'wws.log'
    file_handler = logging.FileHandler(log_file, mode='w')
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

# Custom Class to Store Logs per Category
class CategoryAdapter(logging.LoggerAdapter):
    def __init__(self, logger, extra):
        super().__init__(logger, extra)
        if not hasattr(self, '_log_storage'):
            self._log_storage = {"warnings": [], "info": []}

    def process(self, msg, kwargs):
        return f"[{self.extra['category']}] {msg}", kwargs

    def warning(self, msg, *args, **kwargs):
        self._log_storage["warnings"].append(msg)  # Store warning
        super().warning(msg, *args, **kwargs)  # Log the message normally

    def info(self, msg, *args, **kwargs):
        self._log_storage["info"].append(msg)  # Store info
        super().info(msg, *args, **kwargs)  # Log the message normally

    def get_logs(self):
        """Retrieve the stored logs."""
        return self._log_storage

# Extract Logs from Logger
def extract_logger_info(data):
    logger_summary = {}
    for category, details in data.items():
        if 'log' in details:
            logger = details['log']
            if hasattr(logger, "get_logs"):
                logs = logger.get_logs()
                logger_summary[category] = {
                    "warnings": logs["warnings"],
                    "information": logs["info"]
                }

    return logger_summary

# Input validation - Catch Edge Cases
def validate_restrictions(data: dict, surface_area: float, constr_year: int, property_type: Optional[str] = None) -> None:
    if surface_area < 10:
        raise ValueError("Invalid property\nReason: Too small surface area to accurately calculate WWS points")
    
    if property_type not in (VALID_PROPERTY_TYPES_DUTCH + VALID_PROPERTY_TYPES_ENGLISH):
        raise ValueError("Invalid property\nReason: Property type not recognized")

    if property_type == "houseboat":
        raise ValueError("Invalid property\nReason: WWS calculation for mobile homes is not supported")

    if property_type in ["room", "boarding_house"]:
        data['summary']['log'].warning(DISCLAIMER_SHARED)

# Calculate Aggregate WWS Points
def sum_aggregate_wws_points(data: dict) -> tuple:
    aggregate_wws_points_min = sum(v['min'] for k, v in data.items() if k != 'summary')
    aggregate_wws_points_max = sum(v['max'] for k, v in data.items() if k != 'summary')

    return aggregate_wws_points_min, aggregate_wws_points_max


# endregion

# region (Base Model Selection Functions)


# Select Base Model - Sparse
def select_base_model_sparse(property_type: str, living_space: float, energy_score: Optional[int] = None):
        # Handle the fact that we use energy score as optional
        if not energy_score:
            energy_score = 7

        match property_type:

            # Low-end apartments
            case "flat_dwelling_other" | "gallery_access_apartment" | "portico_access_apartment" | "room" | \
                    "residential_building_with_non_self_contained_living_spaces" | "boarding_house":
                if living_space < 50 or energy_score >= 8:
                    return "low_apartment"
                else:
                    return "mid_apartment"

            # Mid-range apartments
            case "apartment" | "maisonette" | "upper_floor_apartment" | "ground_floor_apartment" | \
                    "ground_floor_plus_upper_apartment" | "intermediate_floor_apartment" | \
                    "double_ground_floor_apartment":
                if living_space >= 50 and energy_score <= 7:
                    return "mid_apartment"
                else:
                    return "low_apartment"

            # High-end apartments
            case "penthouse":
                return "high_apartment"

            # Terrace houses (mid or low)
            case "mid_terrace_house" | "end_terrace_house" | "terraced_house" | "staggered_row_houses":
                if living_space >= 100 and energy_score <= 7:
                    return "mid_high_house"
                else:
                    return "low_house"

            # Semi-detached houses (mid-high or low)
            case "semi_detached_house" | "semi_detached_end_terrace_house" | "linked_semi_detached_house" | "house":
                if living_space >= 90 and energy_score <= 7:
                    return "mid_high_house"
                else:
                    return "low_house"

            # Detached houses (typically mid-high)
            case "detached_house":
                if living_space >= 120 or energy_score <= 6:
                    return "mid_high_house"
                else:
                    return "low_house"

            # Houseboats (generally low but can vary)
            case "houseboat":
                if living_space >= 60 and energy_score <= 7:
                    return "mid_apartment"
                else:
                    return "low_apartment"

            # Default case for unknown property types
            case _:
                raise ValueError("Invalid property type in base model estimation")

# Estimate Base Model - Rich             
def select_base_model_rich(obs, property_cat):
    match property_cat:
        case "house":
            obs.update(house_model)
        case "apartment":
            obs.update(apartment_model)
        case _:
            raise ValueError("Invalid property category in base model estimation")
    return obs

def update_w_base_model(obs, base_model):
    match base_model:
        case "low_apartment":
            additions_dict = low_apartment
        case "mid_apartment":
            additions_dict = mid_apartment
        case "high_apartment":
            additions_dict = high_apartment
        case "low_house":
            additions_dict = low_house
        case "mid_high_house":
            additions_dict = mid_high_house
        case _:
            raise ValueError("Invalid base model")
    
    obs.update(additions_dict)

    return obs


# endregion

# region (HYPER PARAMETERS)


# Parking
N_PEOPLE_SHARING_NON_GARAGE_APARTMENT_PARKING_FACILITIES_MIN = 1
N_PEOPLE_SHARING_NON_GARAGE_APARTMENT_PARKING_FACILITIES_MAX = 5
N_PEOPLE_SHARING_GARAGE_APARTMENT_MIN = 1
N_PEOPLE_SHARING_GARAGE_APARTMENT_MAX = 3
N_PEOPLE_SHARING_NON_GARAGE_HOUSE_PARKING_FACILITIES_MIN = 1
N_PEOPLE_SHARING_NON_GARAGE_HOUSE_PARKING_FACILITIES_MAX = 3

# Outside Space
N_PEOPLE_SHARING_SHARED_OUTSIDE_SPACE_APARTMENT_MIN = 10
N_PEOPLE_SHARING_SHARED_OUTSIDE_SPACE_APARTMENT_MAX = 50
N_PEOPLE_SHARING_SHARED_OUTSIDE_SPACE_HOUSE_MIN = 1
N_PEOPLE_SHARING_SHARED_OUTSIDE_SPACE_HOUSE_MAX = 2

# Outside Space - Sparse
PROPORTION_GARDEN_LIVING_SPACE_HOUSE_MIN = 0.25
PROPORTION_GARDEN_LIVING_SPACE_HOUSE_MAX = 1
PROPORTION_GARDEN_LIVING_SPACE_APARTMENT_MIN = 0.5 # For apartment this might differ if we think that garden might be large roof terrace or communal garden (larger)
PROPORTION_GARDEN_LIVING_SPACE_APARTMENT_MAX = 2

PROPORTION_BALCONY_LIVING_SPACE_MIN = 0.05
PROPORTION_BALCONY_LIVING_SPACE_MAX = 0.15
PROPORTION_ROOF_TERRACE_LIVING_SPACE_MIN = 0.5 # For apartment this might differ if we think that garden might be large roof terrace or communal garden (larger)
PROPORTION_ROOF_TERRACE_LIVING_SPACE_MAX = 2

# Storage Space - Sparse
PROPORTION_STORAGE_LIVING_SPACE_MIN = 0.05
PROPORTION_STORAGE_LIVING_SPACE_MAX = 0.15

PRIVATE_GARAGE_SIZE_MIN = 20
PRIVATE_GARAGE_SIZE_MAX = 50

# endregion

### Main Functions ###
# region (Observation Initialization Function) 


def obs_obj_init(data: dict, sparse: bool,
                # Required Features
                living_space: int, # Living area in square meters 
                constr_year: int, # Construction year of the property
                woz_value: int,  # WOZ value of the property
                woz_date: int, # Year the WOZ value was issued
                municipality_code: str, # Municipality code of the property

                # At least one is required, including both guarantee best accuracy
                n_livable_rooms: Optional[str] = None,   # Total number of livable rooms.
                property_cat: Optional[str] = None, # Category of property "apartment" or "house" 
                property_type: Optional[str] = None, # Property building type in dutch, must adhere to our register

                # Optional Other Features
                n_heated_rooms: Optional[int] = None, # Number of heated rooms.
                n_other_rooms: Optional[int] = None,  # Total number of non-livable rooms.
                storage_space: Optional[int] = None,  # Storage area in square meters.
                other_space: Optional[int] = None,  # Area of other rooms in square meters.
                energy_class: Optional[str] = None,  # Energy class, from A++++ to G.
                energy_label_date: Optional[int] = None,  # Year the energy label was issued.

                # HPD Overwrite Features
                n_bedrooms: Optional[int] = None,  # Number of bedrooms.
                parking_space_bool: Optional[bool] = None,
                garage_space_bool: Optional[bool] = None,
                garden_bool: Optional[bool] = None,
                storage_space_bool: Optional[bool] = None,
                balcony_bool: Optional[bool] = None,
                roof_terrace_bool: Optional[bool] = None,

                # Pararius Overwrite Features
                kitchen_countertop: Optional[int] = None,  # Length of the kitchen countertop in meters.
                kitchen_fan: Optional[bool] = None,  # Whether the kitchen has a ventilation fan.
                cook_top: Optional[str] = None,  # Type of cooktop: "induction", "ceramic", or "gas".
                inbuilt: Optional[bool] = None,  # Whether the kitchen is built-in.
                freezer: Optional[bool] = None,  # Whether there is a built-in freezer.
                fridge: Optional[bool] = None,  # Whether there is a built-in fridge.
                oven: Optional[bool] = None,  # Whether there is a built-in oven.
                microwave: Optional[bool] = None,  # Whether there is a built-in microwave.
                dishwasher: Optional[bool] = None,  # Whether there is a built-in dishwasher.
                bath: Optional[bool] = None,  # Whether the bathroom has a bathtub.
                double_sink: Optional[bool] = None,  # Whether the bathroom has a double sink.
                jacuzzi: Optional[bool] = None,  # Whether the bathroom has a jacuzzi.
                separate_shower: Optional[bool] = None,  # Whether there is a separate shower.
                walk_in_shower: Optional[bool] = None,  # Whether there is a walk-in shower.
                sink_cabinet: Optional[bool] = None,  # Whether there is a sink cabinet.
                whirlpool: Optional[bool] = None,  # Whether there is a whirlpool.
                outside_space: Optional[bool] = None,  # Whether there is a garden.
                balcony_or_other_private_outside_space: Optional[float] = None,  # Area of the balcony in square meters or False.
                shared_outside_space: Optional[bool] = None,  # Whether there is a shared garden.
                parking_facilities: Optional[bool] = None,  # Whether there are parking facilities.
                garage: Optional[str] = None,  # Type of garage, e.g., "carport".
                ventilation: Optional[str] = None  # Ventilation system type, e.g., "airconditioning".
                ) -> dict:
    
    # Mode
    if sparse:
        data['summary']['log'].info("---Sparse Feature Mode---")
    else:
        data['summary']['log'].info("---Rich Feature Mode---")

    # Input Validation
    if property_type and property_cat:
        property_type = RENAME_PROPERTY_TYPE_MAP.get(property_type.lower())
        property_cat = RENAME_PROPERTY_CAT_MAP.get(property_cat.lower())

    elif property_type and not property_cat:
        property_cat = RENAME_PROPERTY_CAT_MAP.get(property_type.lower())
        property_type = RENAME_PROPERTY_TYPE_MAP.get(property_type.lower())

    elif not property_type and property_cat:
        property_cat = property_cat.lower()
        property_type = RENAME_PROPERTY_TYPE_MAP.get(property_cat)
        data['summary']['log'].warning(f"Possible accuracy decrease due to no property_type provided") #?#

    else:
        property_type = 'apartment'
        property_cat = 'apartment'
        data['summary']['log'].warning(f"!!! WARNING - NEITHER PROPERTY TYPE OR CATEGORY PROVIDED -> ASSUMING APARTMENT FOR BOTH !!!") #?#

    if not n_livable_rooms:
        n_livable_rooms = bedroom_to_rooms_ols(living_space=living_space, n_bedrooms=n_bedrooms, constr_year=constr_year)
        data['summary']['log'].warning(f"Assumption: Number of livable rooms (important feature) estimated to {n_livable_rooms} using linear regression, may not be accurate\nReason: Number of rooms not provided")

    validate_restrictions(data, property_type=property_type, surface_area=living_space, constr_year=constr_year)
    
    # Dictionary initialization
    obs = dict()

    obs['property_cat'] = property_cat
    
    if n_heated_rooms:
        obs['n_main_heated_rooms'] = n_heated_rooms
    else:
        obs['n_main_heated_rooms'] = n_livable_rooms
        data['main_heating']['log'].info('Assumption: All rooms are heated\nReason: Number of heated rooms not provided')
    
    obs['living_space'] = living_space
    obs['construction_year'] = constr_year
    obs['woz'] = woz_value
    obs['woz_date'] = woz_date
    obs['municipality_code'] = municipality_code

    if energy_class:
        obs['energy_score'] = ENERGY_SCORE_MAP.get(energy_class)
    else:
        obs['energy_score'] = None
        data['energy_performance']['log'].warning("Note: Energy label not provided will decrease preformance of the model")

    if energy_label_date:
        obs['energy_label_date'] = energy_label_date
    else:
        obs['energy_label_date'] = None

    if sparse: # If mode is Sparse then we make more assumptions to make up for lack of information
        if storage_space:
            obs['storage_space'] = (storage_space, storage_space)
        else:
            obs['storage_space'] = (0, 0.15 * living_space)
            data['storage_space']['log'].info(
                "Minimum Assumption: No storage space\n"
                "Maximum Assumption: Storage space is 15% of living space\n"
                "Reason: Storage area not provided"
            )
        
        if other_space:
            obs['other_space'] = (other_space, other_space)
        else:
            obs['other_space'] = (0, 0.05 * living_space)
            data['other_space']['log'].info(
                "Minimum Assumption: No other space\n"
                "Maximum Assumption: Other space is 5% of living space\n"
                "Reason: Other area not provided"
            )
        
        if n_other_rooms:
            obs['n_other_heated_rooms'] = (0, n_other_rooms)
            data['other_heating']['log'].info(
                "Minimum Assumption: No other heated rooms\n"
                "Maximum Assumption: All provided rooms are heated\n"
                "Reason: Room heating status not provided"
            )
        else:
            obs['n_other_heated_rooms'] = (0, 1)
            data['other_heating']['log'].info(
                "Minimum Assumption: No other heated rooms\n"
                "Maximum Assumption: One additional heated room\n"
                "Reason: Number of other rooms not provided"
            )


    else: # If mode is Rich then we make less assumptions to give more transparency and more accurate spread
        if storage_space:
            obs['storage_space'] = (storage_space, storage_space)
        else:
            obs['storage_space'] = (0, 0)
            data['storage_space']['log'].info(
                "Assumption: No storage space\n"
                "Reason: Storage area not provided"
            )

        if other_space:
            obs['other_space'] = (other_space, other_space)
        else:
            obs['other_space'] = (0, 0)
            data['other_space']['log'].info(
                "Assumption: No other space\n"
                "Reason: Other area not provided"
            )

        if n_other_rooms:
            obs['n_other_heated_rooms'] = n_other_rooms
        else:
            obs['n_other_heated_rooms'] = 0
            data['other_heating']['log'].info(
                "Assumption: No other heated rooms\n"
                "Reason: Number of other rooms not provided"
            )


    # Blend with Base Model
    if sparse:
        base_model = select_base_model_sparse(property_type=property_type, living_space=living_space, energy_score=obs['energy_score'])
        obs = update_w_base_model(obs, base_model=base_model)
    else:
        obs = select_base_model_rich(obs, property_cat=property_cat)
    

    # Overwrite Features
    if sparse:
        # Parking
        if parking_space_bool and not garage_space_bool:
            if property_cat == 'apartment':
                obs['private_garage'] = (False, False)
                obs['shared_garage'] = (False, False)  # Shared garage space is also unlikely
                obs['other_shared_parking'] = (True, True)
                obs['n_sharing_shared_parking'] = (
                    N_PEOPLE_SHARING_NON_GARAGE_APARTMENT_PARKING_FACILITIES_MAX, # Mindboogle: In minimum scenario we have maximum number of people sharing
                    N_PEOPLE_SHARING_NON_GARAGE_APARTMENT_PARKING_FACILITIES_MIN
                    )
            else:
                obs['private_garage'] = (False, False)
                obs['shared_garage'] = (False, False)
                obs['other_shared_parking'] = (True, True)
                obs['n_sharing_shared_parking'] = (
                    N_PEOPLE_SHARING_NON_GARAGE_HOUSE_PARKING_FACILITIES_MAX, # Mindboogle: In minimum scenario we have maximum number of people sharing
                    N_PEOPLE_SHARING_NON_GARAGE_HOUSE_PARKING_FACILITIES_MIN
                    )
        elif garage_space_bool:
            if property_cat == 'apartment':
                obs['private_garage'] = (False, False)
                obs['shared_garage'] = (True, True)
                obs['other_shared_parking'] = (False, False)
                obs['n_sharing_shared_parking'] = (
                    N_PEOPLE_SHARING_GARAGE_APARTMENT_MAX, 
                    N_PEOPLE_SHARING_GARAGE_APARTMENT_MIN, 
                    )
            elif property_cat == 'house':
                obs['private_garage'] = (True, True)
                obs['shared_garage'] = (False, False)
                obs['other_shared_parking'] = (False, False)
                obs['n_sharing_shared_parking'] = (1, 1)
            else:
                raise ValueError("Invalid property category")
        else:
            obs['private_garage'] = (False, False)
            obs['shared_garage'] = (False, False)
            obs['other_shared_parking'] = (False, False)
            obs['n_sharing_shared_parking'] = (0, 0)

        # Outside Space
        if garden_bool and property_cat == 'house':
            obs['private_outside_space'] = (True, True)
            obs['shared_outside_space'] = (False, False)
            obs['outside_space'] = (PROPORTION_GARDEN_LIVING_SPACE_HOUSE_MIN * living_space, 
                             PROPORTION_GARDEN_LIVING_SPACE_HOUSE_MAX * living_space)
            obs['n_sharing_outside_space'] = (1, 1)

        elif garden_bool and property_cat == 'apartment':
            obs['private_outside_space'] = (False, True)
            obs['shared_outside_space'] = (True, False)
            obs['outside_space'] = (PROPORTION_GARDEN_LIVING_SPACE_APARTMENT_MIN * living_space, 
                             PROPORTION_GARDEN_LIVING_SPACE_APARTMENT_MAX * living_space)
            obs['n_sharing_outside_space'] = (30, 1)
        
        else:
            obs['private_outside_space'] = (False, False)
            obs['shared_outside_space'] = (False, False)
            obs['outside_space'] = (0, 0)
            obs['n_sharing_outside_space'] = (0, 0)

        if balcony_bool:
            obs['pct_private_to_shared'] = (PROPORTION_BALCONY_LIVING_SPACE_MIN, PROPORTION_BALCONY_LIVING_SPACE_MAX),
            obs['outside_space'][0] += PROPORTION_BALCONY_LIVING_SPACE_MIN * living_space
            obs['outside_space'][1] += PROPORTION_BALCONY_LIVING_SPACE_MAX * living_space

        if roof_terrace_bool:
            obs['outside_space'][0] += PROPORTION_ROOF_TERRACE_LIVING_SPACE_MIN * living_space
            obs['outside_space'][1] += PROPORTION_ROOF_TERRACE_LIVING_SPACE_MAX * living_space

        if storage_space_bool and not storage_space:
            obs['storage_space'] = (living_space * PROPORTION_STORAGE_LIVING_SPACE_MIN, 
                             living_space * PROPORTION_STORAGE_LIVING_SPACE_MAX)

        obs['cooling_function_dummy'] = (0, 1)


    else: # Rich Mode
        # For rich data we use the provided data almost exclusively

        # Kitchen Overwrite
        if kitchen_countertop:
            if not isinstance(kitchen_countertop, (int, float)):
                raise ValueError("Invalid kitchen_countertop type, have to be numeric and represent the length in meters")
            if kitchen_countertop >= 2:
                kcp = 7
            elif kitchen_countertop >= 1:
                kcp = 4
            else:
                kcp = 0
                data['kitchen']['log'].warning("Kitchen countertop length < 1 meter and this will set kithen wws points to 0") #?#
        else:
            kcp = 7
            data['kitchen']['log'].info("Assumption: Kitchen countertop length is 2 meters\nReason: No kitchen countertop length provided and cannot calculate kitchen points properly without a specified length") #?#
        obs['kitchen_countertop_point'] = (kcp, kcp)

        if cook_top == 'ceramic':
            obs['ceramic_cooktop'] = (True, True)
            obs['induction_cooktop'] = (False, False)
            obs['gas_cooktop'] = (False, False)
        elif cook_top == 'induction':
            obs['ceramic_cooktop'] = (False, False)
            obs['induction_cooktop'] = (True, True)
            obs['gas_cooktop'] = (False, False)
        elif cook_top == 'gas':
            obs['ceramic_cooktop'] = (False, False)
            obs['induction_cooktop'] = (False, False)
            obs['gas_cooktop'] = (True, True)
        
        if kitchen_fan:
            obs['exhaust_system'] = (True, True)
        elif kitchen_fan == False:
            obs['exhaust_system'] = (False, False)
            data['kitchen']['log'].info("Assumption: No kitchen exhaust system\nReason: No kitchen fan provided") #?#
        
        if oven:
            if inbuilt:
                obs['electric_oven'] = (True, True)
                obs['gas_oven'] = (False, False)
            elif inbuilt == False:
                obs['electric_oven'] = (False, False)
                obs['gas_oven'] = (False, False)
                data['kitchen']['log'].info(
                "Assumption: No inbuilt oven\n"
                "Reason: No oven provided"
            ) #?#
            else:
                obs['electric_oven'] = (True, True)
                obs['gas_oven'] = (True, True)
                data['kitchen']['log'].info(
                "Minimum Assumption: Inbuilt gas oven\n"
                "Maximum Assumption: Inbuilt electric oven\n"
                "Reason: Oven but not inbuilt boolean provided"
            ) #?#
                
        if oven == False:
            obs['electric_oven'] = (False, False)
            obs['gas_oven'] = (False, False)
            data['kitchen']['log'].info("Assumption: No inbuilt oven\nReason: No inbuilt oven provided") #?#
            
        if inbuilt:
            data['kitchen']['log'].info("Assumption: All kitchen appliances are built-in\nReason: built-in boolean provided and True") #?#
            
            if freezer:
                obs['freezer'] = (True, True)
            elif freezer == False:
                obs['freezer'] = (False, False)
                data['kitchen']['log'].info("Assumption: No inbuilt freezer\nReason: No inbuilt freezer provided") #?#
            
            if fridge:
                obs['refrigerator'] = (True, True)
            elif fridge == False:
                obs['refrigerator'] = (False, False)
                data['kitchen']['log'].info("Assumption: No inbuilt refrigerator\nReason: No inbuilt refrigerator provided") #?#
            
            if microwave:
                obs['microwave'] = (True, True)
            elif microwave == False:
                obs['microwave'] = (False, False)
                data['kitchen']['log'].info("Assumption: No inbuilt microwave\nReason: No inbuilt microwave provided") #?#
            
            if dishwasher:
                obs['dishwasher'] = (True, True)
            elif dishwasher == False:
                obs['dishwasher'] = (False, False)
                data['kitchen']['log'].info("Assumption: No inbuilt dishwasher\nReason: No inbuilt dishwasher provided") #?#

        else:
            data['kitchen']['log'].info("Assumption: No built-in kitchen appliances\nReason: inbuilt not provided")

        data['kitchen']['log'].info(
                "Spread Information\n"
                "Minimum Assumption: Single lever mixer tap\n"
                "Maximum Assumption: Thermostatic mixer tap\n"
                "Reason: No information, but required for calculation"
            )#? Spread #

        # Bathroom Overwrite
        if bath:
            obs['bathtub'] = (True, True)
        else:
            obs['bathtub'] = (False, False)
        
        if double_sink:
            obs['double_sink'] = (True, True)
        else:
            obs['double_sink'] = (False, False)
        
        if jacuzzi or whirlpool:
            obs['bubble_function'] = (True, True)
        else:
            obs['bubble_function'] = (False, False)
        
        if walk_in_shower:
            obs['shower'] = (True, True)
            obs['shower_enclosure'] = (True, True)
            data['bathroom']['log'].info("Assumption: Mounted shower partition\nReason: Walk-in shower provided") #?#
        elif separate_shower:
            obs['shower'] = (True, True)
            obs['shower_enclosure'] = (False, True)
            data['bathroom']['log'].info("Minimum Assumption: No mounted shower partition\n"
                                         "Maximum Assumption: Mounted shower partition\n"
                                         "Reason: Separate shower provided and not walk in shower") #?#
        else:
            obs['shower'] = (False, False)
            obs['shower_enclosure'] = (False, False)
            data['bathroom']['log'].info("Assumption: No separate shower, if bathtub is provided a combination is assumed\nReason: Shower not provided") #?#

        if sink_cabinet:
            obs['built_in_cabinet'] = (False, True)
            obs['cabinet_extra_storage'] = (False, True)
            data['bathroom']['log'].info(
                "Minimum Assumption: Non built-in cabinet\n"
                "Maximum Assumption: Built-in cabinet\n"
                "Reason: Sink cabinet provided but built-in unknown"
            ) #?#

            data['bathroom']['log'].info(
                "Minimum Assumption: No extra storage cabinet\n"
                "Maximum Assumption: Extra storage cabinet\n"
                "Reason: Sink cabinet provided but extra storage unknown"
            ) #?#
        else:
            obs['built_in_cabinet'] = (False, False)
            obs['cabinet_extra_storage'] = (False, False)
            data['bathroom']['log'].info("Assumption: No built in cabinet\nReason: No sink cabinet provided") #?#
        
        data['bathroom']['log'].info(
                "Spread Information\n"
                "Minimum Assumption: Single lever mixer faucet\n"
                "Maximum Assumption: Thermostatic faucet, electrical outlets, towel radiator and inbuilt washbasin\n"
                "Reason: No information, but required for calculation"
            )#? Spread #
        
        # Outside Overwrite - No assumptions about number sharing
        if outside_space:
            obs['outside_space'] = outside_space

            if shared_outside_space:
                obs['shared_outside_space'] = (True, True)
                obs['private_outside_space'] = (False, False)

                if property_cat == 'apartment':
                    obs['n_sharing_outside_space'] = (N_PEOPLE_SHARING_SHARED_OUTSIDE_SPACE_APARTMENT_MAX, # Mindboogle: In minimum scenario we have maximum number of people sharing
                                                      N_PEOPLE_SHARING_SHARED_OUTSIDE_SPACE_APARTMENT_MIN)
                else:
                    obs['n_sharing_outside_space'] = (N_PEOPLE_SHARING_SHARED_OUTSIDE_SPACE_HOUSE_MAX, # Mindboogle: In minimum scenario we have maximum number of people sharing
                                                      N_PEOPLE_SHARING_SHARED_OUTSIDE_SPACE_HOUSE_MIN)

                if balcony_or_other_private_outside_space:
                    if not isinstance(balcony_or_other_private_outside_space, (int, float)):
                        raise ValueError("Invalid balcony or other private outside space area, have to be numeric")
                    
                    obs['private_outside_space'] = (True, True) # Sets both private and shared outside space bools to True in both maximum and minimum scenarios (to be treated as special case)
                    obs['pct_private_to_shared'] = (
                        balcony_or_other_private_outside_space / outside_space,
                        balcony_or_other_private_outside_space / outside_space
                    )
                    data['outside_space']['log'].info(
                        "Assumption: Shared and private outside space\n"
                        "Reason: Balcony or other private outside space area provided along with shared outside space"
                    ) #?#
                else:
                    data['outside_space']['log'].info(
                        "Assumption: Shared outside space exclusively\n"
                        "Reason: Shared outside space provided and no balcony or other private outside space provided"
                    ) #?#
            else:
                obs['n_sharing_outside_space'] = (1, 1)
                obs['shared_outside_space'] = (False, False)
                obs['private_outside_space'] = (True, True)
                data['outside_space']['log'].info(
                    "Assumption: All outside space is private\n"
                    "Reason: No shared outside space provided"
                ) #?#
        else:
            obs['n_sharing_outside_space'] = (0, 0)
            obs['shared_outside_space'] = (False, False)
            obs['private_outside_space'] = (False, False)
            obs['outside_space'] = 0
            data['outside_space']['log'].info(
                "Assumption: No outside space\n"
                "Reason: No outside space provided"
            ) #?#
        
        # Parking Overwrite - Assumptions about number sharing
        if parking_facilities or garage:
            if property_cat == 'apartment':
                if garage:
                    obs['shared_garage'] = (True, True)
                    obs['private_garage'] = (False, False)
                    obs['other_shared_parking'] = (False, False)
                    obs['n_sharing_shared_parking'] = (
                        N_PEOPLE_SHARING_GARAGE_APARTMENT_MAX, # Mindboogle: In minimum scenario we have maximum number of people sharing
                        N_PEOPLE_SHARING_GARAGE_APARTMENT_MIN
                        ) #HP
                    data['parking_space']['log'].info(
                        "Assumption: Shared garage available\n"
                        "Reason: Garage provided for property type apartment"
                    ) #?#
                else:
                    obs['shared_garage'] = (False, False)
                    obs['private_garage'] = (False, False)
                    obs['other_shared_parking'] = (True, True)
                    obs['n_sharing_shared_parking'] = (
                        N_PEOPLE_SHARING_NON_GARAGE_APARTMENT_PARKING_FACILITIES_MAX, # Mindboogle: In minimum scenario we have maximum number of people sharing
                        N_PEOPLE_SHARING_NON_GARAGE_APARTMENT_PARKING_FACILITIES_MIN
                        ) #HP
                    data['parking_space']['log'].info(
                        "Assumption: Other shared parking space than garage provided\n"
                        "Reason: Parking facilities but no garage provided for property type apartment"
                    ) #?#

            elif property_cat == 'house':
                if garage:
                    obs['shared_garage'] = (False, False)
                    obs['private_garage'] = (True, True)
                    obs['other_shared_parking'] = (False, False)
                    obs['n_sharing_shared_parking'] = (1, 1)
                    data['parking_space']['log'].info(
                        "Minimum Assumption: Private garage available\n"
                        "Reason: Garage provided for property type house"
                    ) #?#
                else:
                    obs['private_garage'] = (False, False)
                    obs['shared_garage'] = (False, False)
                    obs['other_shared_parking'] = (True, True)
                    obs['n_sharing_shared_parking'] = (
                        N_PEOPLE_SHARING_NON_GARAGE_HOUSE_PARKING_FACILITIES_MAX, # Mindboogle: In minimum scenario we have maximum number of people sharing
                        N_PEOPLE_SHARING_NON_GARAGE_HOUSE_PARKING_FACILITIES_MIN
                        )
                    data['parking_space']['log'].info(
                        "Assumption: Other parking facilities than garage\n"
                        "Reason: Parking but no garage provided for house"
                    ) #?#
            
            else:
                raise ValueError("Invalid property category identified in overwrite section")
        else:
            obs['shared_garage'] = (False, False)
            obs['private_garage'] = (False, False)
            obs['other_shared_parking'] = (False, False)
            data['parking_space']['log'].info(
                        "Assumption: No parking space\n"
                        "Reason: No parking space provided"
                    ) #?#
            
        # Ventilation Overwrite
        if ventilation:
            if not isinstance(ventilation, str):
                raise ValueError("Invalid ventilation type, have to be string")
            
            if ventilation.lower() == "airconditioning":
                obs['cooling_function_dummy'] = (1, 1)
                data['cooling']['log'].info(
                    "Minimum Assumption: 1 room has a cooling function\n"
                    "Maximum Assumption: All livable rooms have a cooling function\n"
                    "Reason: Airconditioning function provided"
                ) #?#
            else:
                obs['cooling_function_dummy'] = (0, 0)
                data['cooling']['log'].info(
                    "Assumption: No cooling function\n"
                    "Reason: Airconditioning function not provided in ventilation feature"
                ) #?#
        else:
            obs['cooling_function_dummy'] = (0, 0)
            data['cooling']['log'].info(
                "Assumption: No cooling function\n"
                "Reason: Ventilation feature not provided"
            ) #?#

    if obs['private_garage'][0] == True: # According to staatsblad private garages (non-communal) are counted as other space rather than giving parking type 1, 2, 3 points
        obs['other_space'][0] += PRIVATE_GARAGE_SIZE_MIN
    if obs['private_garage'][1] == True:
        obs['other_space'][1] += PRIVATE_GARAGE_SIZE_MAX
    
    # Output
    return obs


# endregion

# region (Space Function)


def calculate_living_space_points(data: dict, bound: str, living_space: float, storage_space: Optional[float]=None, other_space: Optional[float]=None) -> dict:
    if bound not in ['min', 'max']:
        raise ValueError("Bound must be either 'min' or 'max'")
    if not living_space:
        raise ValueError('Missing required variable: n_main_heated_rooms')
    
    living_space_p = 1
    other_space_p = 0.75

    wws_points = {
        'living_space': living_space * living_space_p,
        'storage_space': storage_space * other_space_p if storage_space else 0,
        'other_space': other_space * other_space_p if other_space else 0
    }

    data['living_space'][bound] = wws_points['living_space']
    data['storage_space'][bound] = wws_points['storage_space']
    data['other_space'][bound] = wws_points['other_space']

    return data


# endregion

# region (Heating & Cooling Function)


def calculate_heating_points(data: dict, bound: str, n_main_heated_rooms: int, n_other_heated_rooms: Optional[int]=None, cooling_function_dummy: Optional[int]=None) -> dict:
    if bound not in ['min', 'max']:
        raise ValueError("Bound must be either 'min' or 'max'")
    if not n_main_heated_rooms:
        raise ValueError('Missing required variable: n_main_heated_rooms')
    
    main_heated_room_p = 2 
    other_heated_room_p = 1 
    other_heated_room_p_limit = 4
    cooling_min_point = 1 # 1 room with cooling & heating combination
    cooling_max_point = 2 # 1+ room with cooling & heating combination

    wws_points = {
        'main_heating': n_main_heated_rooms * main_heated_room_p,
        'other_heating': min(n_other_heated_rooms * other_heated_room_p, other_heated_room_p_limit) if n_other_heated_rooms else 0,
        'cooling': cooling_function_dummy * cooling_min_point if bound == 'min' else cooling_function_dummy * cooling_max_point
    }

    data['main_heating'][bound] = wws_points['main_heating']
    data['cooling'][bound] = wws_points['cooling']

    if n_other_heated_rooms:
        data['other_heating'][bound] = wws_points['other_heating']

    return data


# endregion

# region (Energy Function - Update point sequences according to new edition of staatsblad)


def energy_year_bin(construction_year: int) -> int:
    if 0 <= construction_year < 1977:
        return 0
    
    elif 1977 <= construction_year < 1979:
        return 1
    
    elif 1979 <= construction_year < 1984:
        return 2
    
    elif 1984 <= construction_year < 1992:
        return 3
    
    elif 1992 <= construction_year < 2000:
        return 4
    
    elif 2000 <= construction_year < 2002:
        return 5
    
    elif 2002 <= construction_year < np.inf:
        return 6
    
    else:
        return 0

def energy_year_point_sequence(property_cat: str):

    house_points = [41, 34, 22, 14, -5, -9, -15]
    apartment_points = [37, 30, 15, 11, -5, -9, -15]

    return house_points if property_cat == "house" else apartment_points

def energy_label_point_sequence(property_cat: str, living_space: float):

    if living_space < 25:
        house_points = [62, 62, 60, 55, 48, 40, 36, 32, 13, -5, -10]
        apartment_points = [62, 62, 56, 51, 44, 36, 32, 28, 9, -5, -10]

    elif 25 <= living_space < 40:
        house_points = [62, 57, 52, 47, 40, 32, 22, 14, -1, -5, -10]
        apartment_points = [62, 53, 48, 43, 36, 28, 15, 11, -1, -5, -10]

    else:
        house_points = [62, 57, 52, 47, 40, 32, 22, 14, -1, -5, -10]
        apartment_points = [58, 53, 48, 43, 36, 28, 15, 11, -1, -5, -10]

    return house_points if property_cat == "house" else apartment_points

def calculate_energy_points(data: dict, bound: str, construction_year: int, living_space: float, property_cat: str, energy_score: Optional[int]=None, energy_label_date: Optional[int]=None) -> dict:
    if bound not in ['min', 'max']:
        raise ValueError("Bound must be either 'min' or 'max'")
    if not all([living_space, construction_year, property_cat]):
        raise ValueError('Missing any of required variables: living_space, construction_year, property_cat')

    if energy_label_date: # If energy label date is provided we can validate if it is outdated
        if not isinstance(energy_label_date, int):
            raise ValueError("Invalid energy_label_date, have to be integer")
        
        VALID_ENERGY_LABEL = (energy_label_date >= int(datetime.datetime.now().year - 10))

        if not VALID_ENERGY_LABEL:
            data['energy_performance']['log'].warning("Energy label outdated (< 10 years) and construction year used instead")

    else: # If energy label date is not provided we assume it is not outdated
        VALID_ENERGY_LABEL = True
        data['energy_performance']['log'].warning("Assumption: Energy label is not outdated (< 10 years)\nReason: energy_label_date not provided")

    if VALID_ENERGY_LABEL and energy_score:
        point_seq = energy_label_point_sequence(property_cat, living_space)
        energy_points = point_seq[energy_score] # Energy score is used as index to get the points, A+++... will select first number in the list
    else:
        year_index = energy_year_bin(construction_year) # Construction year is converted to index
        point_seq = energy_year_point_sequence(property_cat) # Property category defines the list
        energy_points = point_seq[year_index] # Index retrieves the points from the list

    wws_points = { # Coherence...
        'energy_performance': energy_points
    }

    data['energy_performance'][bound] = wws_points['energy_performance']

    return data


# endregion

# region (Kitchen Function )


def calculate_kitchen_points(data: dict, bound: str, kitchen_counter_point: int, gas_oven: bool, electric_oven: bool, ceramic_cooktop: bool, induction_cooktop: bool, gas_cooktop: bool, exhaust_system: bool, freezer: bool, refrigerator: bool, microwave: bool, dishwasher: bool) -> dict:
    if bound not in ['min', 'max']:
        raise ValueError("Bound must be either 'min' or 'max'")

    gas_oven_p = 0.5
    electric_oven_p = 1
    ceramic_cooktop_p = 1
    gas_cooktop_p = 0.5
    induction_cooktop_p = 1.75
    exhaust_system_p = 0.75
    freezer_p = 0.75
    refrigerator_p = 1
    microwave_p = 1
    dishwasher_p = 1.5
    single_lever_tap_p = 0.25
    thermo_mixer_tap_p = 0.5

    additional_wws_points = {
        'gas_oven': gas_oven_p if gas_oven else 0,
        'electric_oven': electric_oven_p if electric_oven else 0,
        'ceramic_cooktop': ceramic_cooktop_p if ceramic_cooktop else 0,
        'induction_cooktop': induction_cooktop_p if induction_cooktop else 0,
        'gas_cooktop': gas_cooktop_p if gas_cooktop else 0,
        'exhaust_system': exhaust_system_p if exhaust_system else 0,
        'freezer': freezer_p if freezer else 0,
        'refrigerator': refrigerator_p if refrigerator else 0,
        'microwave': microwave_p if microwave else 0,
        'dishwasher': dishwasher_p if dishwasher else 0,
        'mixer_tap': single_lever_tap_p if bound == 'min' else thermo_mixer_tap_p
    }

    additional_wws_points = sum(additional_wws_points.values())
    wws_points = kitchen_counter_point + min(kitchen_counter_point, additional_wws_points) # Limits the additional points to the kitchen counter points (usually max 7 points)

    data['kitchen'][bound] = wws_points

    return data


# endregion

# region (Bathroom Function) 


def calculate_bathroom_points(data: dict, bound: str, toilet: bool, hanging_toilet: bool, separate_toilet: bool, sink: bool, double_sink: bool, shower: bool, shower_enclosure: bool, bathtub: bool, bubble_function: bool, built_in_cabinet: bool, cabinet_extra_storage: bool) -> dict:
    if bound not in ['min', 'max']:
        raise ValueError("Bound must be either 'min' or 'max'")

    # Points allocation based on bathroom features
    toilet_p = 3 if separate_toilet else 2
    hanging_toilet_p = 3.75 if separate_toilet else 2.75
    sink_p = 1
    double_sink_p = 1.5
    shower_p = 4
    bathtub_p = 6
    bathtub_shower_combo_p = 7
    bubble_function_p = 1.5
    mounted_shower_enclosure_p = 1.25
    towel_radiator_p = 0.75
    built_in_cabinet_p = 1
    cabinet_extra_storage_p = 0.75
    electrical_outlet_min_p = 0.25  # assuming max points if outlets are present
    electrical_outlet_max_p = 0.25  # assuming max points if outlets are present
    single_lever_mixer_p = 0.25
    thermo_mixer_p = 0.5
    inbuilt_washbasin_p = 1

    wws_points = {
        'toilet': toilet_p if (toilet or separate_toilet)else 0,
        'hanging_toilet': hanging_toilet_p if hanging_toilet else 0,
        'sink': sink_p if sink else 0,
        'double_sink': double_sink_p if double_sink else 0,
        'shower': shower_p if shower else 0,
        'bathtub': bathtub_p if (shower and bathtub) else 0, # Otherwise combination of shower and bathtub is assumed
        'bathtub_shower_combo': bathtub_shower_combo_p if (not shower and bathtub) else 0, # If only bathtub and not shower is registered we assume that this bathtub is a shower-bathtub combo
        'bubble_function': bubble_function_p if bubble_function else 0,
        'shower_enclosure': mounted_shower_enclosure_p if shower_enclosure else 0,
        'built_in_cabinet': built_in_cabinet_p if built_in_cabinet else 0,
        'cabinet_extra_storage': cabinet_extra_storage_p if cabinet_extra_storage else 0,
        'bathroom_faucet': single_lever_mixer_p if bound == 'min' else thermo_mixer_p,
        'electrical_outlet': electrical_outlet_min_p if bound == 'min' else electrical_outlet_max_p,
        'towel_radiator': towel_radiator_p if bound == 'max' else 0,
        'inbuilt_washbasin': inbuilt_washbasin_p if bound == 'max' else 0,
    }

    base_wws_points = sum(wws_points['toilet',
                                     'hanging_toilet',
                                     'sink',
                                     'double_sink',
                                     'shower',
                                     'bathtub',
                                     'bathtub_shower_combo'].values())
    additional_wws_points = sum(wws_points['bubble_function',
                                     'shower_enclosure',
                                     'built_in_cabinet',
                                     'cabinet_extra_storage',
                                     'bathroom_faucet',
                                     'electrical_outlet',
                                     'towel_radiator',
                                     'inbuilt_washbasin'].values())
    wws_points = base_wws_points + min(base_wws_points, additional_wws_points)  # Limits the additional points to the base points

    data['bathroom'][bound] = wws_points

    return data


# endregion

# region (Outside Area Function )


def calculate_outside_space_points(data: dict, bound: str, private_outside_space: bool, shared_outside_space: bool, outside_space: Optional[float] = None, pct_private_to_shared: Optional[float] = None, n_sharing_outside_space: Optional[int] = None) -> dict:
    if bound not in ['min', 'max']:
        raise ValueError("Bound must be either 'min' or 'max'")

    private_fixed_p = 2
    private_coefficient_p = 0.35
    shared_coefficient_p = 0.75

    if outside_space:

        if private_outside_space:

            if shared_outside_space:  # Both imply that the property have shared outside space combined with a balcony or other private outside space addition
                private_space = outside_space * pct_private_to_shared
                shared_space = outside_space - private_space
                wws_points = (private_fixed_p + private_coefficient_p * private_space + 
                              shared_coefficient_p * shared_space / n_sharing_outside_space)

            else:  # Exclusively private
                wws_points = private_fixed_p + private_coefficient_p * outside_space

        elif shared_outside_space:  # Exclusively shared
            wws_points = shared_coefficient_p * outside_space / n_sharing_outside_space

    else:  # No outside space
        wws_points = -5

    data['outside_space'][bound] += wws_points

    return data


# endregion

# region (Parking Function )


def calculate_parking_points(data: dict, bound: str, shared_garage: bool, other_shared_parking: bool, n_sharing_shared_parking: Optional[int] = None) -> dict:
    if bound not in ['min', 'max']:
        raise ValueError("Bound must be either 'min' or 'max'")

    type_1_point = 9
    type_2_point = 6
    type_3_point = 4
    charging_point = 2

    if shared_garage:
        if not n_sharing_shared_parking: # Avoid division by 0
            raise ValueError("No number of people sharing parking set while shared garage is present")
            
        wws_points = type_1_point / n_sharing_shared_parking
        wws_points += charging_point if bound == 'max' else 0

    elif other_shared_parking:
        if not n_sharing_shared_parking: # Avoid division by 0
            raise ValueError("No number of people sharing parking set while shared garage is present")

        wws_points = (type_2_point / n_sharing_shared_parking) if bound == 'max' else (type_3_point / n_sharing_shared_parking)
        wws_points += charging_point if bound == 'max' else 0

    else: # Either no garage or private garage - in the staatsblad it explicitly says that the type 1, 2, 3 points are only for communal parking facilities
        wws_points = 0

    return data


# endregion

# region (WOZ Function)


def calculate_woz_points(data: dict, woz: int, woz_date: int, living_space: float, construction_year: int, municipality_code: str, storage_area: Optional[float] = None, outside_space: Optional[float] = None) -> dict:

    if not storage_area:
        storage_area = 0

    woz_points = 0
    
    woz_divisor_1 = 14543 if woz_date == 2023 else 14146

    woz_points += woz / woz_divisor_1

    effective_area = living_space
    if storage_area:
        effective_area += storage_area
    if outside_space:
        effective_area += outside_space

    meets_condition = (
        (2018 <= construction_year <= 2022) and
        (living_space < 40) and
        (municipality_code in COROP_CODES)
    )

    if meets_condition:
        if woz_date == 2023:
            woz_divisor_2 = 97
        else:
            woz_divisor_2 = 94
    else:
        if woz_date == 2023:
            woz_divisor_2 = 229
        else:
            woz_divisor_2 = 222

    woz_points += (woz / effective_area) / woz_divisor_2

    wws_pre_woz_min_points, _ = sum_aggregate_wws_points(data)
    total_points_without_cap_min = wws_pre_woz_min_points + woz_points

    is_new_construction = EXCEPTION_RULE_YEAR_RANGE[0] <= construction_year <= EXCEPTION_RULE_YEAR_RANGE[1]
    is_small_area = (effective_area) < EXCEPTION_RULE_AREA_LIMIT  # Effective area = living area + outside area + parking area + storage area 
    is_in_corop_area = municipality_code in COROP_CODES
    meets_exception_condition = is_new_construction and is_small_area and is_in_corop_area

    # No exception rule applied and capped
    if total_points_without_cap_min > CAP_THRESHOLD and not meets_exception_condition:
        max_woz_points = (0.33 * wws_pre_woz_min_points) / 0.67
        woz_points_capped = min(woz_points, max_woz_points)
        total_points_with_cap = wws_pre_woz_min_points + woz_points_capped
        if total_points_with_cap < CAP_MIN_TOTAL_POINTS + 1:
            total_points_with_cap = CAP_MIN_TOTAL_POINTS
            woz_points_capped = total_points_with_cap - wws_pre_woz_min_points

    # No cap threshold reached or meets exception rule
    else:
        woz_points_capped = woz_points
    
    # Apply Exception Rule 11.2
    is_in_exception_range = EXCEPTION_RULE_ADDITIONAL_YEAR_RANGE[0] <= construction_year <= EXCEPTION_RULE_ADDITIONAL_YEAR_RANGE[1]

    # If exception woz points capped get substituted for exception points
    if is_in_exception_range and wws_pre_woz_min_points >= EXCEPTION_RULE_MIN_WWS_MIN and woz_points_capped < EXCEPTION_RULE_MIN_WOZ_POINTS:
        woz_points_capped = EXCEPTION_RULE_MIN_WOZ_POINTS
    
    data['woz']['min'] = round(woz_points_capped, 2)
    data['woz']['max'] = round(woz_points_capped, 2)

    return data


# endregion

# region (Create WWS Data Object)


def create_wws_data(input: dict, sparse: bool) -> dict:
    logger = init_logger()

    data = {
    'summary': {'min': 0, 'max': 0, 'log': CategoryAdapter(logger, {"category": "general"})},
    'living_space': {'min': 0, 'max': 0, 'log': CategoryAdapter(logger, {"category": "living_space"})},
    'storage_space': {'min': 0, 'max': 0, 'log': CategoryAdapter(logger, {"category": "other_space"})},
    'other_space': {'min': 0, 'max': 0, 'log': CategoryAdapter(logger, {"category": "external_space"})},
    'main_heating': {'min': 0, 'max': 0, 'log': CategoryAdapter(logger, {"category": "main_heating"})},
    'other_heating': {'min': 0, 'max': 0, 'log': CategoryAdapter(logger, {"category": "other_heating"})},
    'cooling': {'min': 0, 'max': 0, 'log': CategoryAdapter(logger, {"category": "cooling"})},
    'energy_performance': {'min': 0, 'max': 0, 'log': CategoryAdapter(logger, {"category": "energy_performance"})},
    'kitchen': {'min': 0, 'max': 0, 'log': CategoryAdapter(logger, {"category": "kitchen"})},
    'bathroom': {'min': 0, 'max': 0, 'log': CategoryAdapter(logger, {"category": "bathroom"})},
    'outside_space': {'min': 0, 'max': 0, 'log': CategoryAdapter(logger, {"category": "outside_space"})},
    'parking_space': {'min': 0, 'max': 0, 'log': CategoryAdapter(logger, {"category": "parking_space"})},
    'woz': {'min': 0, 'max': 0, 'log': CategoryAdapter(logger, {"category": "woz_value"})}
    }

    try:
        obs = obs_obj_init(
            data=data,
            sparse=sparse,
            
            # Required Features
            living_space=input['living_space'],
            constr_year=input['construction_year'],
            woz_value=input['woz_value'],
            woz_date=input['woz_date'],
            municipality_code=input['municipality_code'],

            # At least one required
            property_cat=input.get('property_cat'),
            property_type=input.get('property_type'),

            # Prefably required
            n_livable_rooms=input.get('n_livable_rooms'),
            
            # Optional Other Features
            n_heated_rooms=input.get('n_heated_rooms'),
            n_other_rooms=input.get('n_other_rooms'),
            storage_space=input.get('storage_space'),
            other_space=input.get('other_space'),
            energy_class=input.get('energy_class'),
            energy_label_date=input.get('energy_label_date'),

            # HPD Overwrite Features
            n_bedrooms=input.get('n_bedrooms'),
            parking_space_bool=input.get('parking_space_bool'),
            garage_space_bool=input.get('garage_space_bool'),
            garden_bool=input.get('garden_bool'),
            storage_space_bool=input.get('storage_space_bool'),
            balcony_bool=input.get('balcony_bool'),
            roof_terrace_bool=input.get('roof_terrace_bool'),

            # Pararius Overwrite Features
            kitchen_countertop=input.get('kitchen_countertop'),
            kitchen_fan=input.get('kitchen_fan'),
            cook_top=input.get('cook_top'),
            inbuilt=input.get('inbuilt'),
            freezer=input.get('freezer'),
            fridge=input.get('fridge'),
            oven=input.get('oven'),
            microwave=input.get('microwave'),
            dishwasher=input.get('dishwasher'),
            bath=input.get('bath'),
            double_sink=input.get('double_sink'),
            jacuzzi=input.get('jacuzzi'),
            separate_shower=input.get('separate_shower'),
            walk_in_shower=input.get('walk_in_shower'),
            sink_cabinet=input.get('sink_cabinet'),
            whirlpool=input.get('whirlpool'),
            outside_space=input.get('outside_space'),
            balcony_or_other_private_outside_space=input.get('balcony_or_other_private_outside_space'),
            shared_outside_space=input.get('shared_outside_space'),
            parking_facilities=input.get('parking_facilities'),
            garage=input.get('garage'),
            ventilation=input.get('ventilation'),
        )

    except KeyError as ke:
        print(f'key error {ke}')
        sys.exit(1)
    except Exception as e:
        print(f'exception {e}')
        sys.exit(1)

    try:
        for i, bound in enumerate(['min', 'max']):
            data = calculate_living_space_points(
                data,
                bound=bound,
                living_space=obs['living_space'],
                storage_space=obs['storage_space'][i]
    )
            
    except Exception as e:
        print(f'ls exception {e}')
        sys.exit()
    
    try:
        for i, bound in enumerate(['min', 'max']):
            data = calculate_heating_points(
                data,
                bound=bound,
                n_main_heated_rooms=obs['n_main_heated_rooms'],
                n_other_heated_rooms=obs['n_other_heated_rooms'][i],
                cooling_function_dummy=obs['cooling_function_dummy'][i]
            )
    except Exception as e:
        print(f'hp exception {e}')
        sys.exit()

    try:
        for i, bound in enumerate(['min', 'max']):
            data = calculate_energy_points(
                data,
                bound=bound,
                construction_year=obs['construction_year'],
                living_space=obs['living_space'],
                property_cat=obs['property_cat'],
                energy_score=obs['energy_score'],
                energy_label_date=obs['energy_label_date']
            )
    except Exception as e:
        print(f'ep exception energy {e}')
        sys.exit()

    try:
        for i, bound in enumerate(['min', 'max']):
            data = calculate_kitchen_points(
                data,
                bound=bound,
                kitchen_counter_point=obs['kitchen_countertop_point'][i],
                gas_oven=obs['gas_oven'][i],
                electric_oven=obs['electric_oven'][i],
                gas_cooktop=obs['gas_cooktop'][i],
                ceramic_cooktop=obs['ceramic_cooktop'][i],
                induction_cooktop=obs['induction_cooktop'][i],
                exhaust_system=obs['exhaust_system'][i],
                freezer=obs['freezer'][i],
                refrigerator=obs['refrigerator'][i],
                microwave=obs['microwave'][i],
                dishwasher=obs['dishwasher'][i],
            )
    except Exception as e:
        print(f'kp exception {e}')
        sys.exit()
    
    try:
        for i, bound in enumerate(['min', 'max']):
            data = calculate_bathroom_points(
                data,
                bound=bound,
                toilet=obs['toilet'][i],
                hanging_toilet=obs['hanging_toilet'][i],
                separate_toilet=obs['separate_toilet'][i],
                sink=obs['sink'][i],
                double_sink=obs['double_sink'][i],
                shower=obs['shower'][i],
                shower_enclosure=obs['shower_enclosure'][i],
                bathtub=obs['bathtub'][i],
                bubble_function=obs['bubble_function'][i],
                built_in_cabinet=obs['built_in_cabinet'][i],
                cabinet_extra_storage=obs['cabinet_extra_storage'][i]
            )
    except Exception as e:
        print(f'bp exception {e}')
        sys.exit()

    try:
        for i, bound in enumerate(['min', 'max']):
            data = calculate_outside_space_points(
                data,
                bound=bound,
                private_outside_space=obs['private_outside_space'][i],
                shared_outside_space=obs['shared_outside_space'][i],
                outside_space=obs['outside_space'],
                pct_private_to_shared=obs['pct_private_to_shared'][i],
                n_sharing_outside_space=obs['n_sharing_outside_space'][i]
            )
    except Exception as e:
        print(f'op exception {e}')
        sys.exit()
    
    try:
        for i, bound in enumerate(['min', 'max']):
            data = calculate_parking_points(
                data,
                bound=bound,
                shared_garage=obs['shared_garage'][i],
                other_shared_parking=obs['other_shared_parking'][i],
                n_sharing_shared_parking=obs['n_sharing_shared_parking'][i]
            )
    except Exception as e:
        print(f'pp exception {e}')
        sys.exit()

    try:
        for i, bound in enumerate(['min', 'max']):
            data = calculate_woz_points(data,
                                    woz=obs['woz'],
                                    woz_date=obs['woz_date'],
                                    living_space=obs['living_space'],
                                    construction_year=obs['construction_year'],
                                    municipality_code=obs['municipality_code'],
                                    storage_area=obs['storage_space'][i],
                                    outside_space=obs['outside_space'][i])
    except Exception as e:
        print(f'woz exception {e}')
        sys.exit()
    
    try:
        wws_min, wws_max = sum_aggregate_wws_points(data)
        data['summary']['min'] = round(wws_min)
        data['summary']['max'] = round(wws_max)

        
    except Exception as e:
        print(f'exception {e}')
        sys.exit()
    
    return data


# endregion

# region (Format Results)


def process_wws_data(data: dict) -> dict:
    aggregate_results = {
        'wws_max': data['summary']['max'],
        'wws_min': data['summary']['min'],
        'max_rent': wws_table_point_to_rent.get(data['summary']['max']),
        'min_rent': wws_table_point_to_rent.get(data['summary']['min'])
    }

    logger_summary = extract_logger_info(data)

    # Combine max, min, information, and warnings for each category
    category_summary = {
        k: {
            **({'information': logger_summary.get(k, {}).get('information')} if logger_summary.get(k, {}).get('information') else {}),
            **({'warnings': logger_summary.get(k, {}).get('warnings')} if logger_summary.get(k, {}).get('warnings') else {}),
            'max': v.get('max', None),
            'min': v.get('min', None)
        }
        for k, v in data.items() if k != 'summary'
    }

    results = {
        'aggregate_results': aggregate_results,
        'category_summary': category_summary
    }
    return results


# endregion

import random
from faker import Faker

def generate_test_observations(n=10):
    fake = Faker()  # Initialize faker instance
    observations = []
    for _ in range(n):
            test_observation = {
                "living_space": random.randint(50, 200),  # in square meters
                "n_livable_rooms": random.randint(1, 10),
                "property_cat": random.choice(["house", "apartment"]),
                "construction_year": random.randint(1900, 2023),
                "woz_value": random.randint(50000, 1000000),  # Property value in Euros
                "woz_date": random.randint(2000, 2023),
                "municipality_code": f"GM{random.randint(1000, 9999)}",
                "property_type": random.choice(VALID_PROPERTY_TYPES_DUTCH),

                # Optional fields
                "ventilation": random.choice(["airconditioning", "mechanical", "natural"]),
                "n_heated_rooms": random.randint(1, 10),
                "storage_area": random.randint(5, 30),  # in square meters
                "other_area": random.randint(0, 20),  # in square meters
                "total_other_rooms": random.randint(0, 5),
                "energy_class": random.choice(["A++", "A+", "A", "B", "C", "D"]),
                "energy_label_date": random.randint(2000, 2023),
                "kitchen_countertop": random.randint(1, 5),  # e.g., 1-5 rating
                "kitchen_fan": fake.boolean(),
                "cook_top": random.choice(["induction", "ceramic"]),
                "inbuilt": fake.boolean(),
                "freezer": fake.boolean(),
                "fridge": random.choice([True, False, None]),
                "oven": random.choice([True, False, None]),
                "microwave": random.choice([True, False, None]),
                "dishwasher": fake.boolean(),
                "bath": fake.boolean(),
                "double_sink": fake.boolean(),
                "jacuzzi": fake.boolean(),
                "separate_shower": fake.boolean(),
                "walk_in_shower": fake.boolean(),
                "sink_cabinet": fake.boolean(),
                "whirlpool": random.choice([True, False, None]),
                "outside_space": random.randint(0, 100),  # in square meters
                "balcony_or_other_private_outside_space": round(random.uniform(0, 20), 2),  # in square meters
                "shared_outside_space": fake.boolean(),
                "parking_facilities": fake.boolean(),
                "garage": fake.boolean(),
            }

            observations.append(test_observation)

    return observations

### Test Data ###
test_observation = {
    "living_space": 120,
    "n_livable_rooms": 4,
    "property_cat": "house",
    "construction_year": 1990,
    "woz_value": 350000,
    "woz_date": 2023,
    "municipality_code": "GM0451",
    "property_type": "Bovenwoning",

    # Optional fields
    "ventilation": "airconditioning",
    "n_heated_rooms": 3,
    "storage_area": 15,
    "other_area": 10,
    "total_other_rooms": 2,
    "energy_class": "A++",
    "energy_label_date": 2021,
    "kitchen_countertop": 3,
    "kitchen_fan": True,
    "cook_top": "induction",
    "inbuilt": True,
    "freezer": True,
    "fridge": None,
    "oven": None,
    "microwave": None,
    "dishwasher": True,
    "bath": True,
    "double_sink": False,
    "jacuzzi": False,
    "separate_shower": True,
    "walk_in_shower": True,
    "sink_cabinet": True,
    "whirlpool": None,
    "outside_space": 50,
    "balcony_or_other_private_outside_space": 8.5,
    "shared_outside_space": False,
    "parking_facilities": True,
    "garage": "carport",
    "ventilation": "airconditioning"
}

INPUT = test_observation
SPARSE = True

# Replace the direct file read and processing (lines 2061-2077) with a function
def load_sample_data():
    sample = pd.read_csv('wws_test_sample.csv')
    sample = sample.where(pd.notna(sample), None)
    sample['living_space'] = sample['Oppervlakte (m2)'].astype(float)
    sample['property_cat'] = sample['property_cat']
    sample['property_type'] = sample['woning_type']
    sample['construction_year'] = sample['pand_bouwjaar'].astype(float)
    sample['woz_value'] = sample['woz'].astype(float)
    sample['woz_date'] = 2023
    sample['municipality_code'] = sample['gemeentecode']
    sample['energy_class'] = sample['Energielabel']
    sample['n_livable_rooms'] = round(sample['living_space'] / 25)
    return sample

# Move the sample processing into the main block
if __name__ == '__main__':
    logging.disable(logging.CRITICAL)
    sys.stdout = sys.__stdout__
    sample = load_sample_data()  # Only load data when running as main script
    test_observations = generate_test_observations(n=10)
    for _, row in sample.iterrows():
        try:
            data = create_wws_data(input=row, sparse=SPARSE)
            results = process_wws_data(data)
            print(row['Straat'])
            pprint(results['aggregate_results']['wws_max'])
            pprint(results['aggregate_results']['wws_min'])

        except Exception as e:
            print(row['property_cat'])
            print(row['property_type'])
            print(f'exception {e}')

