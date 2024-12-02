import logging
import sys
import pandas as pd
import numpy as np
import random
import datetime
from typing import Optional
from pprint import pprint

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
    electrical_outlet_min_p = 0.25
    electrical_outlet_max_p = 0.25
    single_lever_mixer_p = 0.25
    thermo_mixer_p = 0.5
    inbuilt_washbasin_p = 1

    # Calculate base points
    base_points = {
        'toilet': toilet_p if (toilet or separate_toilet) else 0,
        'hanging_toilet': hanging_toilet_p if hanging_toilet else 0,
        'sink': sink_p if sink else 0,
        'double_sink': double_sink_p if double_sink else 0,
        'shower': shower_p if shower else 0,
        'bathtub': bathtub_p if (shower and bathtub) else 0,
        'bathtub_shower_combo': bathtub_shower_combo_p if (not shower and bathtub) else 0
    }

    # Calculate additional points
    additional_points = {
        'bubble_function': bubble_function_p if bubble_function else 0,
        'shower_enclosure': mounted_shower_enclosure_p if shower_enclosure else 0,
        'built_in_cabinet': built_in_cabinet_p if built_in_cabinet else 0,
        'cabinet_extra_storage': cabinet_extra_storage_p if cabinet_extra_storage else 0,
        'bathroom_faucet': single_lever_mixer_p if bound == 'min' else thermo_mixer_p,
        'electrical_outlet': electrical_outlet_min_p if bound == 'min' else electrical_outlet_max_p,
        'towel_radiator': towel_radiator_p if bound == 'max' else 0,
        'inbuilt_washbasin': inbuilt_washbasin_p if bound == 'max' else 0
    }

    base_wws_points = sum(base_points.values())
    additional_wws_points = sum(additional_points.values())
    
    # Total points with limitation on additional points
    wws_points = base_wws_points + min(base_wws_points, additional_wws_points)

    data['bathroom'][bound] = wws_points

    return data

def create_wws_data(input: dict, sparse: bool) -> dict:
    """Create WWS data object from input dictionary."""
    data = {
        'bathroom': {'min': 0, 'max': 0},
        'kitchen': {'min': 0, 'max': 0},
        'living_space': {'min': 0, 'max': 0},
        'outside_space': {'min': 0, 'max': 0},
        'parking_space': {'min': 0, 'max': 0},
        'woz': {'min': 0, 'max': 0},
        'energy_performance': {'min': 0, 'max': 0},
        'heating': {'min': 0, 'max': 0},
        'summary': {'min': 0, 'max': 0}
    }

    # Process living space points
    for bound in ['min', 'max']:
        data = calculate_living_space_points(
            data=data,
            bound=bound,
            living_space=input['living_space'],
            storage_space=input.get('storage_area', None)
        )

    # Process bathroom points
    for bound in ['min', 'max']:
        data = calculate_bathroom_points(
            data=data,
            bound=bound,
            toilet=input.get('toilet', False),
            hanging_toilet=input.get('hanging_toilet', False),
            separate_toilet=input.get('separate_toilet', False),
            sink=input.get('sink', False),
            double_sink=input.get('double_sink', False),
            shower=input.get('shower', False),
            shower_enclosure=input.get('shower_enclosure', False),
            bathtub=input.get('bathtub', False),
            bubble_function=input.get('bubble_function', False),
            built_in_cabinet=input.get('built_in_cabinet', False),
            cabinet_extra_storage=input.get('cabinet_extra_storage', False)
        )

    # Process WOZ points
    data = calculate_woz_points(
        data=data,
        woz=input['woz_value'],
        woz_date=input['woz_date'],
        living_space=input['living_space'],
        construction_year=input['construction_year'],
        municipality_code=input['municipality_code']
    )

    # Calculate total points
    data['summary']['min'] = sum(v['min'] for v in data.values() if isinstance(v, dict) and 'min' in v)
    data['summary']['max'] = sum(v['max'] for v in data.values() if isinstance(v, dict) and 'max' in v)

    return data

def calculate_living_space_points(data: dict, bound: str, living_space: float, storage_space: Optional[float] = None) -> dict:
    """Calculate points for living space."""
    points = living_space
    if storage_space:
        points += storage_space * 0.75
    
    data['living_space'][bound] = points
    return data

def calculate_woz_points(data: dict, woz: int, woz_date: int, living_space: float, 
                        construction_year: int, municipality_code: str) -> dict:
    """Calculate points for WOZ value."""
    woz_divisor = 14543 if woz_date == 2023 else 14146
    points = woz / woz_divisor
    
    data['woz']['min'] = points
    data['woz']['max'] = points
    return data

def process_wws_data(data: dict) -> dict:
    """Process WWS data and return results."""
    results = {
        'aggregate_results': {
            'wws_min': data['summary']['min'],
            'wws_max': data['summary']['max'],
            'living_space_points': data['living_space']['min'],  # Same for min/max
            'bathroom_points_min': data['bathroom']['min'],
            'bathroom_points_max': data['bathroom']['max'],
            'woz_points': data['woz']['min']  # Same for min/max
        }
    }
    return results

# Add other functions and main logic here as needed

if __name__ == '__main__':
    # Example usage
    logging.disable(logging.CRITICAL)
    sys.stdout = sys.__stdout__
    # Add your main logic here