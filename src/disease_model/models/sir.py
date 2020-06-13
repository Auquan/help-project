"""Simple SIR model."""
import numpy as np
from scipy import integrate
from typing import Tuple

from help_project.src.disease_model import base_model
from help_project.src.disease_model import data


class SIR(base_model.BaseDiseaseModel):
    """Base Disease Model for other models to inherit from."""

    @classmethod
    def differential_equations(
            cls, _,
            compartments: Tuple[float, float, float],
            beta: float,
            gamma: float):
        """Differential equations for this model.

        Args:
            _: Timestep, which is not used.
            compartments: Tuple of population in each compartment (S, I, R).
            beta: Infection rate.
            gamma: Recovery rate.

        Returns:
            Derivatives for each compartment.
        """
        # pylint: disable=invalid-name
        s, i, r = compartments
        ds = -beta * i / (s + i + r) * s
        di = beta * i / (s + i + r) * s - gamma * i
        dr = gamma * i
        return ds, di, dr

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
        #TODO (Consider input data)
        self.set_params({
            'beta': 0.5,
            'gamma': 0.1,
            'population': population_data.population_size,
        })

    def predict(self,
                past_health_data: data.PopulationData,
                future_policy_data: data.PolicyData) -> data.HealthData:
        """Get predictions.

        Args:
            population_data: Relevant data for the population of interest.
            past_health_data: Time-series of confirmed infections and deaths.
            future_policy_data: Time-series of lockdown policy to predict for.

        Returns:
            Predicted time-series of health data matching the length of the
            given policy.
        """
        if not self.params:
            raise (
                'Model params not set, call to fit function required.')

        initial_confirmed_cases = past_health_data.confirmed_cases[0]
        initial_recovered = past_health_data.recovered[0]
        initial_deaths = past_health_data.deaths[0]

        initial_population = self.params['population'] - initial_deaths
        initial_susceptible = initial_population - (initial_confirmed_cases +
                                                    initial_recovered)

        forecast_length = len(future_policy_data.lockdown)
        prediction = integrate.solve_ivp(
            SIR.differential_equations,
            t_span=(0, forecast_length),
            t_eval=np.arange(forecast_length),
            y0=(initial_susceptible,
                initial_confirmed_cases,
                initial_recovered),
            args=(self.params['beta'], self.params['gamma']))

        (_,
         predicted_infected,
         predicted_recovered) = prediction.y

        return data.HealthData(
            confirmed_cases=predicted_infected,
            recovered=predicted_recovered,
            deaths=np.ones(forecast_length) * initial_deaths)
