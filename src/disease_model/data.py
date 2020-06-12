"""Module for objects holding data for the models."""
import attr


@attr.s
class PopulationData:  # pylint: disable=too-few-public-methods
    """Struct for holding population data."""
    population_size = attr.ib()
    demographics = attr.ib()


@attr.s
class HealthData:  # pylint: disable=too-few-public-methods
    """Struct for holding a time-series of health data."""
    confirmed_cases = attr.ib()
    recovered = attr.ib()
    deaths = attr.ib()


@attr.s
class PolicyData:  # pylint: disable=too-few-public-methods
    """Struct for holding a time-series of policy data."""
    lockdown = attr.ib()
