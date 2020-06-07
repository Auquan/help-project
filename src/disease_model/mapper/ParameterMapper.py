"""
Class for a mapper that maps the lockdown strategy for all the models
"""


class ParameterMapper():
    def __init__(self, to_model = None):
        self.to_model = to_model

    def fit(self):
        """
        fit the parameter mapper for a particular model
        """

