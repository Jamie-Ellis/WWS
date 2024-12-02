from data_generator import generate_test_observations
from main import create_wws_data, process_wws_data
from pprint import pprint
import pandas as pd

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.float_format', lambda x: '%.2f' % x)

def export_to_excel(df):
    # Create Excel writer object
    excel_filename = 'wws_detailed_results.xlsx'
    with pd.ExcelWriter(excel_filename, engine='openpyxl') as writer:
        # Write main results
        df.to_excel(writer, sheet_name='Detailed Results', index=False)
        
        # Create summary sheet
        summary = df.groupby('Category').agg({
            'WWS Min': ['count', 'mean', 'min', 'max'],
            'WWS Max': ['mean', 'min', 'max'],
            'Size (m²)': 'mean'
        }).round(2)
        summary.to_excel(writer, sheet_name='Summary')

def test_wws_model():
    print("Starting WWS calculations with synthetic data...\n")
    
    # Generate 50 test observations
    test_data = generate_test_observations(50)
    results_list = []
    
    # Process each observation
    for i, observation in enumerate(test_data, 1):
        try:
            observation.update({
                'construction_year': 2000,
                'woz_value': 350000,
                'woz_date': 2023,
                'municipality_code': "GM0451",
            })
            
            data = create_wws_data(observation, sparse=True)
            results = process_wws_data(data)
            
            results['aggregate_results'].update({
                'property_type': observation['property_type'],
                'property_cat': observation['property_cat'],
                'living_space': observation['living_space']
            })
            
            results_list.append(results['aggregate_results'])
            
        except Exception as e:
            print(f"Error processing observation {i}: {e}\n")
    
    # Create and process DataFrame
    df = pd.DataFrame(results_list)
    df = df.sort_values('wws_max', ascending=False)
    
    df = df.rename(columns={
        'wws_min': 'WWS Min',
        'wws_max': 'WWS Max',
        'living_space_points': 'Living Space Points',
        'bathroom_points_min': 'Bathroom Min',
        'bathroom_points_max': 'Bathroom Max',
        'woz_points': 'WOZ Points',
        'property_type': 'Property Type',
        'property_cat': 'Category',
        'living_space': 'Size (m²)'
    })
    
    # Export to Excel
    export_to_excel(df)
    print(f"\nExcel file saved as: wws_detailed_results.xlsx")

if __name__ == "__main__":
    test_wws_model()