from fastapi import FastAPI
from models import *
import pymongo
app = FastAPI()

client = pymongo.MongoClient("mongodb://localhost:27017/")

DB_NAME = "PIAD"

mydb = client["PIAD"]

