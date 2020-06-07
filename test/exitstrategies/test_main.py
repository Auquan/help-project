"""
Test for dummy lockdown vector
"""

from help_project.src.exitstrategies.interface import ExitStrategies


def test_ld_vec():
    vec_created = False

    try:
        exit_strat = ExitStrategies()
        ld_vec = exit_strat.get_lockdown_vectors()
        cls_len = len(exit_strat.get_focus_areas())
        df_len = len(ld_vec["category"].tolist())
        if df_len == cls_len:
            vec_created = True
    except Exception as inst:
        # TODO: change to logging
        print("exitstrategies test failed with exception:\n", inst)

    assert vec_created
