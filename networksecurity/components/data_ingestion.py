from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig
from sklearn.model_selection import train_test_split
from networksecurity.entity.artifact_entity import DataIngestionArtifact
import pandas as pd
import os
import sys
import pymongo
import numpy as np
from typing import List

from dotenv import load_dotenv
load_dotenv()


MONGO_DB_URL=os.getenv("MONGO_DB_URL")


class DataIngestion:

    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    # Reading data from the mongodb
    def export_collection_as_dataframe(self):
        try:
            '''
            getting DATABASE NAME and COLLECTION NAME from the config_entity.py
            & config_entity file is fetching it from constant/training_pipeline/__init__.py file 
            '''
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name

            # Making connection with database 
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            # Selecting database and collection inside the database
            collection= self.mongo_client[database_name][collection_name]
            
            # Fetches all the documents of the collection and convert them into the list then convert list of dict into dataframe
            df=pd.DataFrame(list(collection.find()))

            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"],axis=1)
            
            df.replace({"na":np.nan},inplace=True)
            return df
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    # Func to save rawData.csv into feature store artifact
    def export_data_to_feature_store(self,dataframe: pd.DataFrame):
        try:

            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            #Creating Folder
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            return dataframe
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    # Splitting data into train and test splits 
    def split_data_as_train_test(self,dataframe: pd.DataFrame):
        try:
            train_set, test_set, = train_test_split(
                dataframe,test_size=self.data_ingestion_config.train_test_split_ratio
            )
            logging.info("Performed Train & Test split on the dataframe")

            logging.info("Exited split_data_as_train_test method of Data_Ingestion class")

            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path,exist_ok=True)

            logging.info(f"Exporting train and test file path.")

            train_set.to_csv(
                self.data_ingestion_config.training_file_path, index=False, header=True
            )

            test_set.to_csv(
                self.data_ingestion_config.testing_file_path, index=False, header=True
            )

            logging.info(f"Exported train and test file path.")
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    # Func to initiate data ingestion 
    def initiate_data_ingestion(self):
        try:
            #Read data from mongodb 
            dataframe = self.export_collection_as_dataframe()
            # Save raw data.csv into feature store 
            dataframe = self.export_data_to_feature_store(dataframe)
            # Split data into test and train
            self.split_data_as_train_test(dataframe)
            
            # This is our final out from Data_ingestion component 
            dataIngestionArtifacts=DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path
            )

            return dataIngestionArtifacts

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        



