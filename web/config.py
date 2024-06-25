from pymongo import MongoClient
from flask import Flask
from flask_restful import Api

client = MongoClient("mongodb://db:27017")
db = client.BankAPI
users = db["Users"]


app = Flask(__name__)
api = Api(app)


