"""
Test for ensemble model/ if it works everything works
"""

from help_project.src.disease_model.ensemble_model.ensemble_model import EnsembleModel


def test_ensemble_model():
    """
    end to end test for disease model
    """
    test = False
    model = EnsembleModel(country="India")
    health_vector = model.get_health_status()
    if len(health_vector) > 0:
        test = True

    assert test
