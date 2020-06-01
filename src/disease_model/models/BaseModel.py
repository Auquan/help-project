'''
Base Class for all models
'''

import pandas as pd


class BaseDiseaseModel(object):
    def __init__(self, country=None):
        self.country = country
        self.params = {}


    def fit(self, CountryParameters):
        """
        function to fit to a Country
        """

    def set_params(self,params):
        """
        Setter for params
        """

    def get_params(self):
        """
        getter for params
        """

    def make_predictions(self):
        """
        predictions
        """