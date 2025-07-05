from flask_pymongo import PyMongo
from flask_cors import CORS

# Setup MongoDB here
# mongo = PyMongo(uri="mongodb://localhost:27017/database")
mongo = PyMongo()
cors = CORS()
