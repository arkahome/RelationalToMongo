import pandas as pd
import pymongo
import re
from pathlib import Path


def replace_start_str_to_end_str(start_str, end_str, given_str):
    start_str_idx = given_str.find(start_str)
    end_str_iter = re.finditer(end_str, given_str)
    end_str_indices = [m.end(0) for m in end_str_iter]
    end_str_dict = {(i-start_str_idx):i for i in end_str_indices if (i-start_str_idx)>0}
    if len(end_str_dict.keys())>0:
        end_str_idx = end_str_dict.get(min(end_str_dict.keys()))
    if start_str_idx ==-1:
        return given_str
    given_str = given_str.replace(given_str[start_str_idx:end_str_idx], '')
    return given_str

# Create RestAPI
def create_rest_api_script(CONTAINER_NAME, KEY_COLS):
    p = Path('../app')
    p.mkdir(parents=True, exist_ok=True)

    fn_models = 'models.py'
    fn_main = 'main.py'

    filepath_models = p / fn_models
    filepath_main = p / fn_main



    with filepath_models.open("r", encoding ="utf-8") as f:
        pydantic_class_str = f.read()
    with filepath_main.open("r", encoding ="utf-8") as f:
        fastapi_main = f.read()


    fastapi_main = replace_start_str_to_end_str(start_str= f'''@app.post('/{CONTAINER_NAME}')''', end_str = 'return {"error" : "No data."}', given_str=fastapi_main)
    pydantic_class_str = replace_start_str_to_end_str(start_str = f'class Input_{CONTAINER_NAME}(BaseModel):', end_str='str\n\n', given_str=pydantic_class_str)

    pydantic_class_str = pydantic_class_str + '\n\n' if pydantic_class_str[-2:] != "\n\n" else pydantic_class_str

    pydantic_class_str = pydantic_class_str + f'''class Input_{CONTAINER_NAME}(BaseModel):'''

    for i in KEY_COLS.split(','): pydantic_class_str = pydantic_class_str + f'\n\t{i} : str'
    pydantic_class_str = pydantic_class_str + '\n\n'

    fastapi_main = fastapi_main + '\n\n' if fastapi_main[-2:] != "\n\n" else fastapi_main
    fastapi_main = fastapi_main + f'''@app.post('/{CONTAINER_NAME}')
def fetch_{CONTAINER_NAME}(data: Input_{CONTAINER_NAME}):
    try:
        response = mydb['{CONTAINER_NAME}'].find(dict(data))[0]
        del response['_id']
        return response
    except IndexError:
        return ''' + '{"error" : "No data."}'


    with filepath_models.open("w", encoding ="utf-8") as f:
        f.write(pydantic_class_str)

    with filepath_main.open("w", encoding ="utf-8") as f:
        f.write(fastapi_main)

def create_mongo_client(DB_URL, DB_NAME):
    client = pymongo.MongoClient(DB_URL)
    mydb = client[DB_NAME]
    print(client.list_database_names())
    print(client[DB_NAME].list_collection_names())
    return client, mydb

def push_data_to_mongo_and_create_index(df, KEY_COLS, CONTAINER_NAME, mydb):

    df[KEY_COLS.split(',')] = df[KEY_COLS.split(',')].astype(str)
    mydb[CONTAINER_NAME].drop()
    mydb[CONTAINER_NAME].insert_many(df.to_dict(orient = 'records'))


    index_list = [eval(f'''"{col}", pymongo.ASCENDING''')  for col in KEY_COLS.split(',')]
    index_name = '_'.join(KEY_COLS.split(','))
    mydb[CONTAINER_NAME].create_index(index_list, name = index_name, unique=True)


if __name__=="__main__":
    DB_URL = "mongodb://localhost:27017/"
    DB_NAME = "PIAD"
    CONTAINER_NAME = "piad_model_1"

    df = pd.read_html('https://gist.github.com/kevin336/acbb2271e66c10a5b73aacf82ca82784')[0].iloc[:,1:]

    KEY_COLS = 'EMPLOYEE_ID,FIRST_NAME'
    VALUE_COLS = 'LAST_NAME,EMAIL,PHONE_NUMBER,HIRE_DATE,JOB_ID,SALARY,COMMISSION_PCT,MANAGER_ID,DEPARTMENT_ID'


    client, mydb = create_mongo_client(DB_URL, DB_NAME)

    push_data_to_mongo_and_create_index(df, KEY_COLS, CONTAINER_NAME, mydb)
    create_rest_api_script(CONTAINER_NAME, KEY_COLS)
