""" Test for dummy lockdown vector """

from src.exit_strategies.ExitStrategies import ExitStrategies

def test_ld_vec():

    exit_strat = ExitStrategies()
    ld_vec = exit_strat.get_lockdown_vectors()

    assert ld_vec.shape == (2, 30, 90)
