"""
Test for ensemble model/ if it works everything works
"""

from src.disease_model.ensemble_model.ensemble_model import EnsembleModel


def test_ensemble_model():
    vec_created = False

    try:
        model = EnsembleModel(country="India")
        health_vector = model.get_health_status()
        if len(health_vector)>0:
            test = True
    except Exception as inst:
        # TODO: change to logging
        print("exitstrategies test failed with exception:\n", inst)

    assert test