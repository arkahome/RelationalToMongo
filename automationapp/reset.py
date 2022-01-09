from pathlib import Path
    

fastapi_main = '''from fastapi import FastAPI
from models import *
import pymongo
app = FastAPI()

client = pymongo.MongoClient("mongodb://localhost:27017/")

DB_NAME = "PIAD"

mydb = client["PIAD"]\n\n'''

pydantic_class_str = '''from pydantic import BaseModel\n\n'''

p = Path('../app')
p.mkdir(parents=True, exist_ok=True)

fn_models = 'models.py'
fn_main = 'main.py'

filepath_models = p / fn_models
filepath_main = p / fn_main

with filepath_models.open("w", encoding ="utf-8") as f:
    f.write(pydantic_class_str)

with filepath_main.open("w", encoding ="utf-8") as f:
    f.write(fastapi_main)