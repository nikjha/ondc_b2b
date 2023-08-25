from pymongo import MongoClient

conn = MongoClient("mongodb://localhost:27017/")
database = conn["ondc_b2b_mock"]
