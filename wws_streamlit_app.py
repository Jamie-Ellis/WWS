import streamlit as st
import pandas as pd
from main import create_wws_data, process_wws_data

# Constants from original script
COROP_CODES = [
    'GM0358', 'GM0362', 'GM0363', 'GM0384', 'GM0385', 'GM0394', 'GM0415', 'GM0431',
    'GM0437', 'GM0439', 'GM0451', 'GM0852', 'GM0307', 'GM0308', 'GM0310', 'GM0312',
    'GM0313', 'GM0317', 'GM0321', 'GM0353', 'GM0327', 'GM0331', 'GM0335', 'GM0356',
    'GM0589', 'GM0339', 'GM0340', 'GM0736', 'GM0342', 'GM1904', 'GM0344', 'GM1581',
    'GM0345', 'GM1961', 'GM0352', 'GM0632', 'GM0351', 'GM0355'
]

ENERGY_CLASSES = ["G", "F", "E", "D", "C", "B", "A", "A+", "A++", "A+++", "A++++", "A+++++"]

def run_single_wws_calculation(property_params):
    """Run WWS calculation for a single property with given parameters"""
    try:
        data = create_wws_data(property_params, sparse=True)
        results = process_wws_data(data)
        return results['aggregate_results']
    except Exception as e:
        st.error(f"Error processing property: {e}")
        return None

def display_detailed_results(results, property_params):
    """Display detailed breakdown of WWS calculations"""
    st.header("Results")
    
    # Basic WWS Points
    col1, col2 = st.columns(2)
    with col1:
        st.metric("WWS Points (Min)", f"{results['wws_min']:.2f}")
    with col2:
        st.metric("WWS Points (Max)", f"{results['wws_max']:.2f}")
    
    # Component Breakdowns
    st.subheader("Points Breakdown")
    
    # Living Space Calculation
    st.markdown("#### Living Space Points")
    living_space_df = pd.DataFrame({
        'Component': ['Main Living Space', 'Storage Space', 'Other Area'],
        'Area (m²)': [
            property_params['living_space'],
            property_params.get('storage_area', 0),
            property_params.get('other_area', 0)
        ],
        'Multiplier': ['1.0', '0.75', '0.25'],
        'Points': [
            property_params['living_space'] * 1.0,
            property_params.get('storage_area', 0) * 0.75,
            property_params.get('other_area', 0) * 0.25
        ]
    })
    st.dataframe(living_space_df.astype(str))
    
    # Kitchen Features
    st.markdown("#### Kitchen Features")
    kitchen_features = {
        'Countertop Length': ('Base points per meter', property_params.get('kitchen_countertop', 0) * 0.5),
        'Kitchen Fan': ('Ventilation', 0.5 if property_params.get('kitchen_fan') else 0),
        'Inbuilt Kitchen': ('Premium feature', 0.75 if property_params.get('inbuilt') else 0),
        'Cook Top': ('Type', {
            'none': 0,
            'gas': 0.5,
            'ceramic': 0.75,
            'induction': 1.0
        }.get(property_params.get('cook_top', 'none'), 0)),
        'Dishwasher': ('Appliance', 0.5 if property_params.get('dishwasher') else 0),
        'Freezer': ('Appliance', 0.5 if property_params.get('freezer') else 0)
    }
    kitchen_df = pd.DataFrame([
        {
            'Feature': feature,
            'Description': desc,
            'Points': points,
            'Present': 'Yes' if points > 0 else 'No'
        }
        for feature, (desc, points) in kitchen_features.items()
    ])
    st.dataframe(kitchen_df.astype(str))
    
    # Bathroom Features
    st.markdown("#### Bathroom Points")
    bathroom_features = {
        'Toilet': ('Base toilet', 2),
        'Hanging Toilet': ('Premium toilet', 2.75),
        'Separate Toilet': ('Additional points', 1),
        'Sink': ('Basic sink', 1),
        'Double Sink': ('Premium feature', 1.5),
        'Shower': ('Basic shower', 4),
        'Shower Enclosure': ('Premium feature', 1.25),
        'Bathtub': ('Basic bathtub', 6),
        'Bubble Function': ('Premium feature', 1.5),
        'Built-in Cabinet': ('Storage', 1),
        'Extra Storage Cabinet': ('Additional storage', 0.75)
    }
    bathroom_df = pd.DataFrame([
        {
            'Feature': feature,
            'Description': desc,
            'Points': points,
            'Present': 'Yes' if property_params.get(feature.lower().replace(' ', '_'), False) else 'No',
            'Points Earned': points if property_params.get(feature.lower().replace(' ', '_'), False) else 0
        }
        for feature, (desc, points) in bathroom_features.items()
    ])
    st.dataframe(bathroom_df.astype(str))
    
    # Outside Space
    st.markdown("#### Outside Space")
    outside_features = {
        'Total Outside Space': ('Base area', property_params.get('outside_space', 0) * 0.75),
        'Private Balcony/Terrace': ('Premium space', property_params.get('balcony_or_other_private_outside_space', 0) * 1.0),
        'Shared Outside Space': ('Communal area', 2 if property_params.get('shared_outside_space') else 0),
        'Parking Facilities': ('Basic parking', 2 if property_params.get('parking_facilities') else 0),
        'Garage': ('Type', {
            'none': 0,
            'private': 6,
            'shared': 3,
            'carport': 4
        }.get(property_params.get('garage', 'none'), 0))
    }
    outside_df = pd.DataFrame([
        {
            'Feature': feature,
            'Description': desc,
            'Area/Type': (
                f"{property_params.get(feature.lower().replace(' ', '_'), 0)} m²" 
                if 'Space' in feature 
                else property_params.get('garage', 'none') 
                if feature == 'Garage' 
                else 'Yes' if points > 0 else 'No'
            ),
            'Points': points
        }
        for feature, (desc, points) in outside_features.items()
    ])
    st.dataframe(outside_df.astype(str))
    
    # WOZ Value
    st.markdown("#### WOZ Points")
    woz_df = pd.DataFrame({
        'Component': ['WOZ Value', 'WOZ Divisor (2023)', 'Base WOZ Points'],
        'Value': [
            f"€{property_params['woz_value']:,.2f}",
            '14,543',
            f"{property_params['woz_value'] / 14543:.2f}"
        ]
    })
    st.dataframe(woz_df.astype(str))

    # Additional Information
    st.markdown("#### Important Notes")
    st.info("""
    - Living space points are calculated directly from the area
    - Storage space is weighted at 75% of main living space
    - Other areas are weighted at 25% of main living space
    - Kitchen points are cumulative based on features
    - Bathroom points have minimum requirements
    - Outside space points depend on type and accessibility
    - WOZ points use the 2023 divisor of 14,543
    """)

def main():
    st.title("WWS Points Calculator - Single Property Tester")
    
    # Basic Property Information
    st.header("Basic Property Information")
    col1, col2 = st.columns(2)
    with col1:
        living_space = st.number_input("Living Space (m²)", 20, 500, 100)
        property_type = st.selectbox(
            "Property Type",
            ["galerijwoning", "rijwoning hoek", "benedenwoning", "bovenwoning", "rijwoning tussen"]
        )
        property_cat = st.selectbox("Property Category", ["apartment", "house"])
        construction_year = st.number_input("Construction Year", 1900, 2023, 2000)
    with col2:
        woz_value = st.number_input("WOZ Value", 100000, 1000000, 350000, step=10000)
        woz_date = st.number_input("WOZ Date", 2000, 2023, 2023)
        municipality_code = st.selectbox("Municipality Code", COROP_CODES)
        storage_area = st.number_input("Storage Area (m²)", 0, 100, 5)

    # Energy Information
    st.header("Energy Information")
    col1, col2 = st.columns(2)
    with col1:
        energy_class = st.selectbox("Energy Label", ENERGY_CLASSES)
        energy_label_date = st.number_input("Energy Label Date", 2000, 2023, 2021)
    with col2:
        ventilation = st.selectbox("Ventilation", ["none", "mechanical", "airconditioning"])
        n_heated_rooms = st.number_input("Number of Heated Rooms", 0, 20, 3)

    # Kitchen Features
    st.header("Kitchen Features")
    col1, col2, col3 = st.columns(3)
    with col1:
        kitchen_countertop = st.number_input("Kitchen Countertop (meters)", 0, 10, 3)
        kitchen_fan = st.checkbox("Kitchen Fan", True)
    with col2:
        cook_top = st.selectbox("Cook Top", ["none", "gas", "ceramic", "induction"])
        inbuilt = st.checkbox("Inbuilt Kitchen", True)
    with col3:
        dishwasher = st.checkbox("Dishwasher", True)
        freezer = st.checkbox("Freezer", True)

    # Bathroom Features
    st.header("Bathroom Features")
    col1, col2, col3 = st.columns(3)
    with col1:
        toilet = st.checkbox("Toilet", True)
        hanging_toilet = st.checkbox("Hanging Toilet", False)
        separate_toilet = st.checkbox("Separate Toilet", False)
        sink = st.checkbox("Sink", True)
    with col2:
        double_sink = st.checkbox("Double Sink", False)
        shower = st.checkbox("Shower", True)
        shower_enclosure = st.checkbox("Shower Enclosure", False)
    with col3:
        bathtub = st.checkbox("Bathtub", False)
        bubble_function = st.checkbox("Bubble Function", False)
        built_in_cabinet = st.checkbox("Built-in Cabinet", False)
        cabinet_extra_storage = st.checkbox("Extra Storage Cabinet", False)

    # Outside Space
    st.header("Outside Space and Parking")
    col1, col2 = st.columns(2)
    with col1:
        outside_space = st.number_input("Total Outside Space (m²)", 0, 500, 50)
        balcony_space = st.number_input("Balcony/Private Space (m²)", 0, 100, 8)
        shared_outside_space = st.checkbox("Shared Outside Space", False)
    with col2:
        parking_facilities = st.checkbox("Parking Facilities", True)
        garage_type = st.selectbox("Garage Type", ["none", "private", "shared", "carport"])

    # Calculate button
    if st.button("Calculate WWS Points"):
        property_params = {
            'living_space': living_space,
            'property_type': property_type,
            'property_cat': property_cat,
            'construction_year': construction_year,
            'woz_value': woz_value,
            'woz_date': woz_date,
            'municipality_code': municipality_code,
            'storage_area': storage_area,
            'energy_class': energy_class,
            'energy_label_date': energy_label_date,
            'ventilation': ventilation,
            'n_heated_rooms': n_heated_rooms,
            'kitchen_countertop': kitchen_countertop,
            'kitchen_fan': kitchen_fan,
            'cook_top': cook_top,
            'inbuilt': inbuilt,
            'dishwasher': dishwasher,
            'freezer': freezer,
            'toilet': toilet,
            'hanging_toilet': hanging_toilet,
            'separate_toilet': separate_toilet,
            'sink': sink,
            'double_sink': double_sink,
            'shower': shower,
            'shower_enclosure': shower_enclosure,
            'bathtub': bathtub,
            'bubble_function': bubble_function,
            'built_in_cabinet': built_in_cabinet,
            'cabinet_extra_storage': cabinet_extra_storage,
            'outside_space': outside_space,
            'balcony_or_other_private_outside_space': balcony_space,
            'shared_outside_space': shared_outside_space,
            'parking_facilities': parking_facilities,
            'garage': garage_type
        }
        
        results = run_single_wws_calculation(property_params)
        
        if results:
            display_detailed_results(results, property_params)

if __name__ == "__main__":
    main() 