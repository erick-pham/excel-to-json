import os
import pandas as pd
import numpy as np
import pydash
import json
from src.models.Mapper import Mapper, Field


def parse_to_int(x):
    if(x == None):
        return None
    x = str(x)
    x = x.strip('\xa0')

    if(x == 'nan'):
        return None
    return int(float(x))


def parse_to_str(x):
    if(x == None):
        return None
    x = str(x)
    x = x.strip('\xa0')
    if(x == 'nan'):
        return None
    return x


def parse_to_dict(x):
    if(x == None):
        return None
    x = str(x)
    x = x.strip('\xa0')
    if(x == 'nan'):
        return None
    return json.loads(x)


def parse_to_bool(x):
    if(x == None):
        return None

    if isinstance(x, bool):
        return x
    x = str(x)
    x = str.lower(x.strip('\xa0'))

    yes_options = ['true', '1', 'yes', 'y']
    no_options = ['false', '0', 'no', 'n']

    if x in yes_options:
        return True

    if x in no_options:
        return False
    return x


class MainClass:
    path_input_file_data: str = ''
    path_input_file_mapper: str = ''
    sheet_names: list = []
    sheet_data_names: list = []
    sheets_data: dict = {}
    dict_model_mapper: dict = {}
    list_of_mapper = []
    dict_data = {}

    def __init__(self, path_input_file_data, path_input_file_mapper=None):
        self.path_input_file_data = path_input_file_data
        self.path_input_file_mapper = path_input_file_mapper

    def read_excel_file(self):
        current_directory = os.getcwd()
        input_path = os.path.join(
            current_directory, "storages/.tmp", self.path_input_file_data)
        excel_data_fragment = pd.read_excel(input_path, None)
        self.sheet_names = list(excel_data_fragment.keys())
        self.sheet_data_names = self.sheet_names
        del self.sheet_data_names[0]

        self.list_of_mapper = excel_data_fragment['ModelMapper'].replace(
            {np.nan: None}).to_dict(
            orient='records')
        self.dict_model_mapper = pydash.group_by(self.list_of_mapper, 'model')

        # current_sheet_name = 'General'
        # current_model_name = 'CMS'
        # current_sheet_name = 'Properties'
        # current_model_name = 'Property'
        current_sheet_name = 'Additional Properties'
        current_model_name = 'AdditionalProperty'

        current_dataframe = excel_data_fragment[current_sheet_name]

        columns = {}

        # parse datatype
        for attr in self.dict_model_mapper[current_model_name]:
            if attr['type'] == 'Integer':
                current_dataframe.loc[:, attr['headerColumn']
                                      ] = current_dataframe.loc[:, attr['headerColumn']].apply(parse_to_int)
            if attr['type'] == 'String':
                current_dataframe.loc[:, attr['headerColumn']
                                      ] = current_dataframe.loc[:, attr['headerColumn']].apply(parse_to_str)
            if attr['type'] == 'Json':
                current_dataframe.loc[:, attr['headerColumn']
                                      ] = current_dataframe.loc[:, attr['headerColumn']].apply(parse_to_dict)
            if attr['type'] == 'Boolean':
                current_dataframe.loc[:, attr['headerColumn']
                                      ] = current_dataframe.loc[:, attr['headerColumn']].apply(parse_to_bool)

        # build dict column to rename old column(header name) to field name following mapper
        for attr in self.dict_model_mapper[current_model_name]:
            columns[attr['headerColumn']] = attr['field']

        current_dataframe.rename(columns=columns, inplace=True)

        # replace value np.nan to None
        current_dataframe = current_dataframe.replace({np.nan: None})
        current_dataframe = current_dataframe.replace({np.NAN: None})

        self.dict_data[current_model_name] = current_dataframe.to_dict(
            orient='records')
