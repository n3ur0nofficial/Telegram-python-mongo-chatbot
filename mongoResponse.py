import pymongo
from pymongo import *
import pprint
import json
import pandas as pd
from bson import ObjectId


class mongoResponse:

    def mongoResponse(stud_name, db_name, coll_name, db_url='localhost', db_port=27017):
        client = MongoClient(db_url, db_port)
        db = client[db_name]
        coll = db[coll_name]
        respo = coll.find_one({"first_name": stud_name})
        #print(respo)
        #respo = coll.find_one({"Let's start with your* first name.*": stud_name})
        df = pd.DataFrame(list(respo.items()), columns=["c1", "c2"])
        # , "c3", "c4", "c5", "c6", "c7", "c8", "c9"])
        return df


pass