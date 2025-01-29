from src.logging import logging
from src.model.data_ingestion import DataIngestion
from src.model.chunking import DataChunking
from src.config.config import TraningPiplineConfig,DataIngestionConfig,DataChunkingConfig
from src.config.artifacts_entity import DataIngestionArtifacts
import os

class TrainPipline:
    def __init__(self):
        self.traing_pipeline_config=TraningPiplineConfig()

    def start_data_ingestion(self):
        try:
            logging.info(f'<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Data Ingestion Started >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
            start_data_ingestion_config=DataIngestionConfig(self.traing_pipeline_config)
            data_ingestion=DataIngestion(data_ingestion_config=start_data_ingestion_config)
            data_ingestion_artifact=data_ingestion.initiate_data_ingestion()
            
            logging.info(f'<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Data Ingestion Completed >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
            return data_ingestion_artifact
        except Exception as e:
            print(e)

    def start_data_chuinking(self,data_ingestion_artifact:DataIngestionArtifacts):
        try:
            logging.info(f'<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Data Chunking Started >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
            data_chuinking_config=DataChunkingConfig(traning_pipline_config=self.traing_pipeline_config)
            data_chuinking=DataChunking(
                data_ingestion_artifact=data_ingestion_artifact,
                chunking_config=data_chuinking_config                        
                )
            data_chuinking.initiate_data_chunking()
        except Exception as e:
            print(e)

    def run(self):
        try:
            logging.info('************************************ Traning Pipline Started ************************************')
            data_ingestion_artifacts=self.start_data_ingestion()
            data_chunking_artifacts=self.start_data_chuinking(data_ingestion_artifact=data_ingestion_artifacts)
            

            logging.info('************************************ Traning Pipline Completed ************************************')
         

        except Exception as e:
            logging.info(f'Error in training pipeline {str(e)}')
            print(e)
if __name__=="__main__":
    obj=TrainPipline()
    obj.run()