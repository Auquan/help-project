"""Base class for all models."""
import copy
from typing import Dict

from help_project.src.disease_model import data


class BaseDiseaseModel:
    """Base Disease Model for other models to inherit from."""

    def __init__(self):
        """Initialize the model."""
        self.params = {}

    def fit(self,
            population_data: data.PopulationData,
            health_data: data.HealthData,
            policy_data: data.PolicyData):
        """Fit the model to the given data.

        Args:
            population_data: Relevant data for the population of interest.
            health_data: Time-series of confirmed infections and deaths.
            policy_data: Time-series of lockdown policy applied.
        """
        raise NotImplementedError()

    def set_params(self, params: Dict):
        """Setter for params."""
        self.params = copy.deepcopy(params)

    def get_params(self) -> Dict:
        """Getter for params."""
        return copy.deepcopy(self.params)

    def predict(self,
                past_health_data: data.HealthData,
                future_policy_data: data.PolicyData) -> data.HealthData:
        """Get predictions.

        Args:
            past_health_data: Time-series of confirmed infections and deaths.
            future_policy_data: Time-series of lockdown policy to predict for.

        Returns:
            Predicted time-series of health data matching the length of the
            given policy.
        """
        raise NotImplementedError()
