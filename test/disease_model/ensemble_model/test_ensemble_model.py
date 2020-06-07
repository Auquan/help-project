"""
Test for ensemble model/ if it works everything works
"""

from src.disease_model.ensemble_model.ensemble_model import EnsembleModel


def test_ensemble_model():
    """
    end to end test for disease model
    """
    try:
        model = EnsembleModel(country="India")
        health_vector = model.get_health_status()
        if len(health_vector) > 0:
            test = True
    except Exception as excep:
        print("disease model not working:\n", excep)
        test = False
    assert test
