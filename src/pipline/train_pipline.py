from src.logging import logging
from src.model.data_ingestion import DataIngestion
from src.config.config import DataIngestionConfig
import os

class TrainPipline:
    def __init__(self):
        pass

    def start_data_ingestion(self):
        try:
            logging.info(f'<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Data Ingestion Started >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
            start_data_ingestion_config=DataIngestionConfig()
            data_ingestion=DataIngestion(data_ingestion_config=start_data_ingestion_config)
            data_ingestion.initiate_data_ingestion()
        except Exception as e:
            print(e)

    def run(self):
        try:
            logging.info('************************************ Traning Pipline Started ************************************')
            data_ingestion_artifacts=self.start_data_ingestion()
            

            logging.info('************************************ Traning Pipline Completed ************************************')
         

        except Exception as e:
            logging.info(f'Error in training pipeline {str(e)}')
            print(e)
if __name__=="__main__":
    obj=TrainPipline()
    obj.run()