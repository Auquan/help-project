"""
Class for ELT of data files
"""

from os import listdir
from os.path import dirname, join
import pandas as pd
import numpy as np


class DataExtractor():

    def __init__(self):
        pass

    def load_files(self):
        # Reading data files with lockdown policies
        ld_df = None
        df_created = False
        project_root = dirname(dirname(__file__))
        data_folder = join(project_root, "data")
        file_list = listdir(data_folder)

        for file_name in file_list:
            file_path = join(data_folder, file_name)
            file_df = pd.read_csv(file_path, encoding="utf-8")
            if not df_created:
                ld_df = file_df
                df_created = True
            else:
                ld_df.append(file_df)

        return ld_df

    def extract_metadata(self):
        # Extract strategy id, date, country
        pass

    def transform_data(self):
        # Define
        ld_df = self.load_files()

        return ld_df

    def dummy_np_array(self):
        # Create dummy 3D numpy array
        strat_count = 2
        focus_area_count = 30
        days_count = 90
        vec_shape = (strat_count, focus_area_count, days_count)
        ld_vec = np.ones(vec_shape)

        return ld_vec
