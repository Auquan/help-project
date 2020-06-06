"""
Interface class to be used by other modules
"""

from help_project.src.exitstrategies.elt.dataextractor import DataExtractor


class ExitStrategies():
    focus_areas = ["agriculture", "chemical", "commerce", "construction", "education", "fin_prof_services",
                   "food_consumables", "healthcare", "hospitality_tourism", "manufacturing", "mining", "engineering",
                   "media", "energy", "telecom", "public_admin", "supply_chain_ship", "forest_husb_fish", "textiles",
                   "transportation", "utilities", "gathering_size", "open_border", "air_travel", "roal_rail_travel",
                   "public_transport", "curfew", "ecommerce", "contact_tracing", "covid_testing"]

    def __init__(self):
        pass

    def get_lockdown_vectors(self):
        # Fetch list of lockdown vectors
        data_extractor = DataExtractor()
        lockdown_vector = data_extractor.transform_data()

        return lockdown_vector

    def get_focus_areas(self):
        return self.focus_areas
