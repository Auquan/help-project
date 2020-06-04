"""
Class for ELT of lockdown policy data
"""

import numpy as np
import pandas

class DataExtract():
    focus_areas = ["agriculture", "chemical", "commerce", "construction", "education", "fin_prof_services", "food_consumables", "healthcare", "hospitality_tourism", "manufacturing", "mining", "engineering", "media", "energy", "telecom", "public_admin", "supply_chain_ship", "forest_husb_fish", "textiles", "transportation", "utilities", "gathering_size", "open_border", "air_travel", "roal_rail_travel", "public_transport", "curfew", "ecommerce", "contact_tracing", "covid_testing"]

    def __init__(self):
        pass

    def load_files(self):
        # Reading data files with lockdown policies
        pass

    def extract_metadata(self):
        # Extract strategy id, date, country
        pass

    def transform_data(self):
        # Create 3D vector here from 2D lockdown policies
        pass

        # Define dummy vector
        strat_count = 2
        focus_area_count = 30
        days_count = 90
        vec_shape = (strat_count, focus_area_count, days_count)
        ld_vec = np.ones(vec_shape)

        return ld_vec
