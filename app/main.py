from fastapi import FastAPI
from models import *
import pymongo
app = FastAPI()

client = pymongo.MongoClient("mongodb://localhost:27017/")

DB_NAME = "PIAD"

mydb = client["PIAD"]

@app.post('/piad_model_2')
def fetch_piad_model_2(data: Input_piad_model_2):
    try:
        response = mydb['piad_model_2'].find(dict(data))[0]
        del response['_id']
        return response
    except IndexError:
        return {"error" : "No data."}


@app.post('/piad_model_1')
def fetch_piad_model_1(data: Input_piad_model_1):
    try:
        response = mydb['piad_model_1'].find(dict(data))[0]
        del response['_id']
        return response
    except IndexError:
        return {"error" : "No data."}