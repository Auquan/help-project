"""
Module for Infections Models
"""

from scipy import optimize
from scipy.integrate import odeint
import numpy as np
import pandas as pd

from src.disease_model.models.base_model import BaseDiseaseModel


def sier_deriv(
        initial_y,
        intial_t,
        population,
        beta1,
        beta2,
        alpha,
        delta,
        zeta,
        ccfr):
    """
    function to define the differential euqations for the model
    """
    incubation_period = 5
    eta = 1 / 14
    epsilon = (1 / incubation_period) - alpha
    susceptible, exposed, infected_unreported, \
        infected_reported, deaths, cured, cured_unreported = initial_y
    ds_dt = (-beta1 * susceptible * infected_unreported / population) - \
        (beta2 * susceptible * infected_reported / population)
    de_dt = (beta1 * susceptible * infected_unreported / population) + \
            (beta2 * susceptible * infected_reported / population) - \
        alpha * exposed - epsilon * exposed
    diu_dt = epsilon * exposed - eta * infected_unreported
    dcu_dt = eta * infected_unreported
    dir_dt = alpha * exposed - delta * \
        (ccfr) * infected_reported - zeta * (1 - ccfr) * infected_reported
    dd_dt = delta * (ccfr) * infected_reported
    dc_dt = zeta * (1 - ccfr) * infected_reported
    return ds_dt, de_dt, diu_dt, dir_dt, dd_dt, dc_dt, dcu_dt


def setup_seir(
        beta1,
        beta2,
        alpha,
        delta,
        zeta,
        ccfr,
        exposed0,
        cured_unreported0,
        susceptible0,
        infected_unreported0,
        population,
        df_conf,
        df_reco,
        df_death,
        initial_time,
        forward,
        generating_curve=False):
    """
    This function is for the setup of the model,
    given parameters this tries to integrate the curves
    """
    if generating_curve:
        deaths0 = df_death.iloc[-1]
        try:
            cured0 = max(df_reco.iloc[-1], .15 * (df_conf.iloc[-14] - deaths0))
        except BaseException:
            cured0 = df_reco.iloc[-1]
        infected_reported0 = df_conf.iloc[-1] - cured0 - deaths0
        # susceptible0 = population - exposed0- infected_unreported0- \
        # infected_reported0- deaths0- cured0 - cured_unreported0
        # Initial conditions vector
        initial_y = int(susceptible0), int(exposed0), int(infected_unreported0), int(
            infected_reported0), int(deaths0), int(cured0), int(cured_unreported0)
        print(
            "(susceptible0, exposed0, infected_unreported0, \
            infected_reported0, deaths0, cured0, cured_unreported0), population")
        print(initial_y, sum(initial_y))
    else:
        deaths0 = df_death.iloc[0]
        cured0 = max(df_reco.iloc[0], .10 * df_conf.iloc[0])
        infected_reported0 = df_conf.iloc[0] - cured0 - deaths0
        # susceptible0 = population - exposed0- infected_unreported0-\
        # infected_reported0- deaths0- cured0 - cured_unreported0
        # Initial conditions vector
        initial_y = int(susceptible0), int(exposed0), int(infected_unreported0), int(
            infected_reported0), int(deaths0), int(cured0), int(cured_unreported0)

    forward_period = len(df_death) + forward
    # A grid of time points (in days)
    timegrid = np.linspace(0, forward_period, forward_period)

    # Integrate the SIR equations over the time grid, t.
    ret = odeint(
        sier_deriv,
        initial_y,
        timegrid,
        args=(
            population,
            beta1,
            beta2,
            alpha,
            delta,
            zeta,
            ccfr))
    susceptible, exposed, infected_unreported, \
        infected_reported, deaths, cured, cured_unreported0 = ret.T
    return susceptible, exposed, infected_unreported, \
        infected_reported, deaths, cured, cured_unreported0, forward_period


def resid_seir(
        params,
        population,
        df_conf,
        df_reco,
        df_death,
        initial_time,
        ccfr):
    """
    This function is used to fit the observed data with
    the curves generated so as to estimate the parameters
    """
    susceptible, exposed, infected_unreported, \
        infected_reported, deaths, cured, cured_unreported0, _ = \
        setup_seir(params[0], params[1], params[2], params[3], params[4],
                   # params[9],
                   params[5], params[6], .1 * \
                   params[8], params[7], params[8],
                   population, df_conf, df_reco, df_death, initial_time, ccfr, 0)
    true_infected_reported = df_conf - df_reco - df_death
    true_deaths = df_death
    fit_days = len(true_deaths)
    return np.nan_to_num(np.array((
        .3 * np.abs(((infected_reported + deaths + cured)[:len(true_infected_reported)] -
                     df_conf)) + np.abs((deaths[len(true_deaths) - fit_days:len(true_deaths)] -
                                         true_deaths.iloc[-fit_days:])) + 0)).astype(float))


def resid_seir_global(params, *args):
    """
    residue function for global optimization
    """
    population, df_conf, df_reco, df_death, initial_time, ccfr = args
    susceptible, exposed, infected_unreported, \
        infected_reported, deaths, cured, cured_unreported0, _ = \
        setup_seir(params[0], params[1], params[2], params[3], params[4],
                   params[5], params[6], .1 *
                   params[8], params[7], params[8],
                   population, df_conf, df_reco, df_death, initial_time, ccfr, 0)
    true_infected_reported = df_conf - df_reco - df_death
    true_deaths = df_death
    true_cured = df_reco
    fit_days = len(true_deaths)
    return np.sum(np.nan_to_num(np.array((
        # np.abs(((infected_reported)[:len(true_infected_reported)] -
        # true_infected_reported)) + \
        ((np.median(true_deaths) / (10 * np.median(infected_reported + deaths + cured))) \
         * np.abs(((infected_reported + deaths + cured)[:len(true_infected_reported)] \
                   - df_conf))) + np.abs((deaths[len(true_deaths) - fit_days:len(true_deaths)] - \
                                          true_deaths.iloc[-fit_days:])) + 0)).astype(float)))


class AuquanSEIR(BaseDiseaseModel):
    """
    class for Auquan's Infection Model
    """

    def __init__(
            self,
            country=None,
            fit_on_days=14,
            fit_from_last_death=False):
        self.country = country
        self.fit_on_days = fit_on_days
        self.fit_from_last_death = fit_from_last_death

    def fit(self, country_parameters):
        """
        fits the model
        """
        population = country_parameters.get_population(self.country)
        population = int(population)
        self.population = population
        df_conf, df_reco, df_death = country_parameters.get_historical_infections(
            self.country)

        if self.fit_from_last_death:
            fit_on_days = len(df_death[df_death > 0])
        else:
            fit_on_days = self.fit_on_days

        initial_time = df_death.index[-1 * fit_on_days]

        df_conf = df_conf.loc[df_conf.index >= initial_time]
        df_reco = df_reco.loc[df_reco.index >= initial_time]
        df_death = df_death.loc[df_death.index >= initial_time]

        self.df_conf = df_conf
        self.df_reco = df_reco
        self.df_death = df_death

        exposed_up = max(
            20 * df_conf.iloc[0] + (population / 10), population / 3)
        infected_unreported_up = max(
            df_conf.iloc[0] + (population / 10), 2 * population / 3)

        exposed_dn = 20 * df_conf.iloc[0]
        infected_unreported_dn = df_conf.iloc[0]
        s_up = population - exposed_dn - 1.1 * \
            infected_unreported_dn - df_conf.iloc[0]
        s_dn = max(
            0,
            (population -
             exposed_up -
             1.1 *
             infected_unreported_up -
             df_conf.iloc[0]) /
            2)
        ccfr = 0.04
        res = optimize.differential_evolution(
            resid_seir_global,
            bounds=[
                (0.05,
                 0.25),
                (0.01,
                 0.2),
                (0.0001,
                 0.2),
                ((1 / 21),
                 (1 / 10)),
                ((1 / 25),
                 (1 / 14)),
                (0.03,
                 0.15),
                (exposed_dn,
                 exposed_up),
                (s_dn,
                 s_up),
                (infected_unreported_dn,
                 infected_unreported_up)],
            args=(
                population,
                df_conf,
                df_reco,
                df_death,
                initial_time,
                0),
            workers=-1)  # In[238]:

        susceptible, exposed, infected_unreported, \
            infected_reported, deaths, cured, cured_unreported, _ = \
            setup_seir(res['x'][0], res['x'][1], res['x'][2],
                       res['x'][3], res['x'][4],
                       res['x'][5], res['x'][6], .1 * res['x'][8],
                       res['x'][7], res['x'][8],
                       population, df_conf, df_reco, df_death, initial_time, 0)

        self.set_params({
            "res": res['x'],
            "startE": exposed[-1],
            "startS": susceptible[-1],
            "startIu": infected_unreported[-1],
            "startCu": cured_unreported[-1],
            "initial_time": initial_time
        })

    def predict(self):
        """
        predict future infections using pre learned
        parameters
        """
        s_long, e_long, iu_long, ir_long, \
            d_long, c_long, cu_long, _ = \
            setup_seir(self.params['res'][0], self.params['res'][1],
                       self.params['res'][2], self.params['res'][3],
                       self.params['res'][4], self.params['res'][5],
                       self.params['startE'], .1 * self.params['startIu'],
                       self.params['startS'], self.params['startIu'], self.population,
                       self.df_conf, self.df_reco, self.df_death, self.params['initial_time'], 150,
                       generating_curve=True)

        dates = pd.date_range(
            start=self.df_death.index[-1], periods=len(ir_long))
        final_df = pd.DataFrame()
        final_df['DATE'] = dates
        final_df['Deaths'] = pd.Series(d_long)
        final_df['Confirmed Infections'] = pd.Series(ir_long + c_long + d_long)
        final_df['Active Infections'] = pd.Series(ir_long)
        return final_df

    def set_params(self, params):
        """
        parameter setter
        """
        self.params = params
