from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
accidents_and_injuries_db =client["accidents_and_injuries_db"]


accidents = accidents_and_injuries_db['accidents']
injuries = accidents_and_injuries_db['injuries']
