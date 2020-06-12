"""This is the external API, that other teams can call."""
from typing import Optional
from typing import Sequence

from help_project.src.disease_model import base_model
from help_project.src.disease_model import data
from help_project.src.disease_model.models import auquan_seir


class EnsembleModel(base_model.BaseDiseaseModel):
    """Class for Ensemble model."""

    def __init__(
            self,
            models: Optional[Sequence[base_model.BaseDiseaseModel]] = None):
        if not models:
            models = [auquan_seir.AuquanSEIR()]
        self.models = list(models)

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
        for model in self.models:
            model.fit(population_data, health_data, policy_data)

    def predict(self,
                past_health_data: data.HealthData,
                future_policy_data: data.PolicyData) -> data.HealthData:
        """Get predictions.

        Args:
            past_health_data: Time-series of confirmed infections and deaths.
            future_policy_data: Time-series of lockdown policy to predict for.

        Returns:
            Averaged predictions of time-series of health data matching the
            length of the given policy.
        """
        predictions = [model.predict(past_health_data, future_policy_data)
                       for model in self.models]
        return data.HealthData(
            confirmed_cases=(
                sum([p.confirmed_cases for p in predictions]) /
                len(predictions)),
            recovered=(
                sum([p.recovered for p in predictions]) /
                len(predictions)),
            deaths=(
                sum([p.deaths for p in predictions]) /
                len(predictions)),
        )
