'''
Base Class for all models
'''


class BaseDiseaseModel():

    """
    Base Disease Model Class
    """

    def __init__(self, country=None):
        self.country = country
        self.params = {}

    def fit(self, country_parameters):
        """
        function to fit to a Country
        """

    def set_params(self, params):
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
