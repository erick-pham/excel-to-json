from dataclasses import field
import os
from fastapi import FastAPI, Request, Depends, HTTPException, Header
from fastapi.responses import FileResponse

import pandas as pd
import uuid
import numpy as np
import traceback
import json
from itertools import groupby
from operator import itemgetter
import pydash
from src.logger.app_logger import logger, screen_handler
from src.models.Mapper import Mapper, Field
from src.models.MainClass import MainClass


api = FastAPI()


@api.middleware('http')
async def add_request_id_header(request: Request, call_next):
    uuid_str = str(uuid.uuid4())
    id_header = 'trace_id'.encode(), uuid_str.encode()
    request.headers.__dict__['_list'].append(id_header)
    response = await call_next(request)
    response.headers['trace_id'] = uuid_str
    return response


@api.get('/', summary='Check health', tags=['Common'])
async def on_get():
    return 'ok'


@ api.get('/log', summary='Get log file')
async def on_get():
    return FileResponse('./logs/app.log')


def get_model_mapper(mapperConfigs):
    print(mapperConfigs)
    result = []
    new_list = pydash.group_by(mapperConfigs, 'model')
    for item in new_list:
        parentModel = None
        list_of_field = []
        for kwargs in new_list[item]:
            if kwargs['parentModel']:
                parentModel = kwargs['parentModel']
            list_of_field.append((Field(**kwargs)))

        result.append(Mapper(model=new_list[item][0]['model'],
                             fields=list_of_field,
                             sheet=new_list[item][0]['sheet'],
                             parentModel=parentModel
                             ))
    return result


def get_model_value(mapperModel, data):
    result = []
    data = data.replace({np.nan: None})
    records = data.to_dict(orient='records')
    for r in records:
        tmp = {}
        for field in mapperModel.fields:
            if field.type == 'Json':
                tmp[field.field] = json.loads(r[field.headerColumn])
            elif field.type == 'Integer':
                tmp[field.field] = int(r[field.headerColumn])
            elif field.type == 'Double':
                tmp[field.field] = float(r[field.headerColumn])
            else:
                tmp[field.field] = r[field.headerColumn]
        result.append(tmp)

    return result


def set_model_relationship(mapperModel, data):
    result = []
    return data


@ api.post('/parse-xlsx-to-json', summary='Parse records from *.xlsx to json')
async def on_post(filename: str = "CAITAWCP 20PAYLIFE - 20PLAND - 20220802.xlsx"):
    try:
        main_class = MainClass(path_input_file_data=filename)
        main_class.read_excel_file()
        # main_class.build()
        return main_class.dict_data

        # current_directory = os.getcwd()
        # input_path = os.path.join(
        #     current_directory, "storages/.tmp", filename)

        # excel_data_fragment = pd.read_excel(input_path, None)

        # result = {}
        # list_of_mapper = get_model_mapper(
        #     excel_data_fragment['ModelMapper'].replace({np.nan: None}).to_dict(orient='records'))
        # for mapperItem in list_of_mapper:
        #     result[mapperItem.model] = get_model_value(
        #         mapperItem, excel_data_fragment[mapperItem.sheet])
        # result = set_model_relationship(list_of_mapper, result)
        # return result

    except Exception as e:
        exc_string = traceback.format_exc()
        logger.error(exc_string)
        raise e


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(api, host='127.0.0.1', port=5000, log_level='info')
