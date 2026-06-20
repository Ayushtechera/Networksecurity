# testing if data ingestion is workin fine or not 
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.entity.config_entity import DataIngestionConfig,DataValidationConfig
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import TrainingPipelineConfig
import os

if __name__ == "__main__":
    try:
        trainingpipelineconfig=TrainingPipelineConfig()
        dataingestionconfig = DataIngestionConfig(trainingpipelineconfig)
        dataingestion = DataIngestion(dataingestionconfig)
        logging.info("Initiate the data ingestion")
        dataingestionartifact = dataingestion.initiate_data_ingestion()
        print(dataingestionartifact)
        logging.info("Data Initiation Completed")

        data_validation_config = DataValidationConfig(trainingpipelineconfig)
        data_validation = DataValidation(dataingestionartifact,data_validation_config)

        logging.info("Initiateed Data Validation")

        data_validation_artifact = data_validation.initiate_data_validation()
        logging.info("Data Validation Completed")
        
        print(data_validation_artifact)
        
    except Exception as e:
        raise NetworkSecurityException(e.sys)