"""
Module for defining country parameters
"""
import pandas as pd


def clean_df(df):
    """
    cleaning dataframe
    """
    df = df.sum(axis=0)
    df = df[[d for d in df.index if d.find('/') > 0]].T
    df.index = pd.to_datetime(df.index)
    return df


def get_dfs():
    """
    Read number of deaths and infections from JHU data
    """

    data_dir = '../data/COVID-19/csse_covid_19_data/csse_covid_19_time_series/'
    rename = {'Country/Region': 'zone',
              'Province/State': 'sub_zone'}
    df_recovery = pd.read_csv(
        data_dir +
        'time_series_covid19_recovered_global.csv').rename(columns=rename)
    df_death = pd.read_csv(
        data_dir +
        'time_series_covid19_deaths_global.csv').rename(columns=rename)
    df_confirmed = pd.read_csv(
        data_dir +
        'time_series_covid19_confirmed_global.csv').rename(columns=rename)
    return df_recovery, df_death, df_confirmed


def get_population():
    """
    Read population from population csv
    """
    population = pd.read_csv(
        "../data/population-figures-by-country-csv_csv.csv")
    population = population.set_index("Country")
    return population


class CountryParameters():
    """
    Class for country parameters, given a country this gets information like number of cases,
    population etc
    """

    def __init__(self):
        self.recovered_cases, self.deaths, self.confirmed_cases = get_dfs()
        self.population = get_population()

    def get_population(self, country=None):
        """
        Population, Age_demographics
        """
        return self.population.loc[country]

    def get_historical_infections(self, country=None):
        """
        historical infections numbers
        """
        conf = clean_df(self.confirmed_cases[(
            self.confirmed_cases['zone'] == country)])
        reco = clean_df(self.recovered_cases[(
            self.recovered_cases['zone'] == country)])
        death = clean_df(self.recovered_cases[(
            self.recovered_cases['zone'] == country)])
        return {"confirmed": conf, "recovered": reco, "deaths": death}
