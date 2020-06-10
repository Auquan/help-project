"""
Module for defining country parameters
"""
from os import path
import pandas as pd
import git


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
    dir_path = path.dirname(path.realpath(__file__))
    data_dir = dir_path + '/../data/COVID-19/csse_covid_19_data/csse_covid_19_time_series/'
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
    dir_path = path.dirname(path.realpath(__file__))
    population = pd.read_csv(
        dir_path + "/../data/population-figures-by-country-csv_csv.csv")
    population = population.set_index("Country")
    return population


class CountryParameters():
    """
    Class for country parameters, given a country this gets information like number of cases,
    population etc
    """

    def __init__(self):
        dir_path = path.dirname(path.realpath(__file__))
        if not path.exists(dir_path + "/../data/COVID-19"):
            git.Git(
                dir_path + "/../data/").clone("https://github.com/CSSEGISandData/COVID-19.git")
        self.recovered_cases, self.deaths, self.confirmed_cases = get_dfs()
        self.population = get_population().Year_2016.to_dict()

    def get_population(self, country=None):
        """
        Population, Age_demographics
        """
        return self.population[country]

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
        return conf, reco, death
