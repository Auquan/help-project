"""
Module for Infections Models
"""

from src.disease_model.models.base_model import BaseDiseaseModel


class AuquanSEIR(BaseDiseaseModel):
    """
    class for Auquan's Infection Model
    """

    def __init__(self):
        pass

    def fit(self):
        """
        fits the model
        """

    def set_params(self, params):
        """
        parameter setter
        """
