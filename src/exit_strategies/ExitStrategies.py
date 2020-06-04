"""
Class for ELT of lockdown policy data
"""

import numpy as np
from src.exit_strategies.elt.DataExtract import DataExtract

class ExitStrategies():
    def __init__(self):
        pass

    def get_lockdown_vectors(self):
        # Fetch list of lockdown vectors
        exit_strat = DataExtract()
        lockdown_vector = exit_strat.transform_data()
        return lockdown_vector
