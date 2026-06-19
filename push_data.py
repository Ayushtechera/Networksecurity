# ----------------------------------------Here we will design our ETL pipeline--------------------
'''
Our Current basic ETL pipeline include:
CSV File
   ↓
Read using Pandas
   ↓
Convert to JSON Records
   ↓
Load into MongoDB Atlas


PRODUCTION LEVEL ETL INCLUDES : 
REST APIs
Databases
AWS S3
Kafka Streams
Logs
User Events
Sensors
Third Party Sources
   ↓
ETL Pipeline
   ↓
MongoDB / Data Lake / Data Warehouse

example: 
Amazon
↓
User orders API
Product API
Payment API
↓
ETL
↓
Store

OR 

Netflix
↓
Real-time user watch events
↓
Kafka
↓
ETL
↓
Database
↓
Recommendation Model

'''

import os
import sys
import json
import pandas as pd
import numpy as np
import pymongo 
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")
print(MONGO_DB_URL)

# Certifi is a package that provides set of root certificates , used by python libraries that need to make secured http connection
'''
Python
 ↓
Wants to connect to MongoDB Atlas
 ↓
MongoDB Atlas sends its SSL Certificate
 ↓
certifi verifies the certificate
 ↓
Is the certificate valid? ✅
 ↓
Connection established
'''
import certifi
ca=certifi.where()



class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    # Converting out csv file into json format 
    def csv_to_json_converter(self,file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True,inplace=True)
            # Converting dataframe into json form 
            records=list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    # Now inserting it into the mongodb
    def insert_data_mongodb(self,records,database,collection):

        try:
            self.database = database
            self.collection = collection
            self.records = records

            # Database connection
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)

            # assigning on this particular mongo_client like which database we are going to use 
            self.database = self.mongo_client[self.database]

            # Here we are assinging what collection are we using in database 
            self.collection = self.database[self.collection]
            
            # Inserting records into collection 
            self.collection.insert_many(self.records)
            return (len(self.records))
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

if __name__ == "__main__":
    FILE_PATH = "Network_Data\phisingData.csv"
    DATABASE = "AYUSHAI"
    Collection = "NetworkData"

    networkobj = NetworkDataExtract()
    records = networkobj.csv_to_json_converter(file_path=FILE_PATH)
    print(records)
    no_of_records = networkobj.insert_data_mongodb(records,DATABASE,Collection)

    print(no_of_records)


