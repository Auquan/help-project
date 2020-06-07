'''
This is the external API, that other teams can call
'''
import pandas as pd


class EnsembleModel():
    def __init__(self, country = None, lockdown_strategy = None):
        self.models = self.pickModels(lockdown_strategy)
        self.country = country

    def pickModels(self,lockdown_strategy):
        """
        Function to pick what models to use for a particular lockdown strategy
        """

    def get_health_status(self):
        """ output health_status of a country """
        cases_df = pd.read_csv('data/full_data.csv')
        cases_df = cases_df[cases_df['location'] == self.country]
        return cases_df[['date', 'location', 'total_cases']]
