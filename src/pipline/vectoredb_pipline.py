from src.logging import logging
from src.knowledge_base.data_ingestion import DataIngestion
from src.knowledge_base.chunking import DataChunking
from src.knowledge_base.embedding_vector_store import VectorDatabase
from src.config.config import TraningPiplineConfig,DataIngestionConfig,DataChunkingConfig
from src.config.artifacts_entity import DataIngestionArtifacts,DataChunkingArtifacts
from src.cloud.s3_storege import S3Storage
import os

class TrainPipline:
    def __init__(self):
        self.traing_pipeline_config=TraningPiplineConfig()
        self.s3_storege=S3Storage()


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
            data_chuinking_artifacts=data_chuinking.initiate_data_chunking()
            logging.info(f'<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Data Chunking completed >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
            return data_chuinking_artifacts
        except Exception as e:
            print(e)
    def start_vectordb_data_store(self,data_chunking_artifacts:DataChunkingArtifacts):
        try:
            logging.info(f'<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Data Vectore completed >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
           
            data_chunking=VectorDatabase(
                data_chunking_artifacts=data_chunking_artifacts
            )
            vectoredb=data_chunking.initate_vector_store()

            logging.info(f'<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Data vectore completed >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
            return vectoredb

        except Exception as e:
            print(e)

    def run(self):
        try:
            logging.info('************************************ Traning Pipline Started ************************************')
            data_ingestion_artifacts=self.start_data_ingestion()
            data_chunking_artifacts=self.start_data_chuinking(data_ingestion_artifact=data_ingestion_artifacts)
            # self.s3_storege.upload_folder(
            #     folder_path=self.traing_pipeline_config.artifacts_path,
            #     s3_folder='Artifacts'
            # )
            db=self.start_vectordb_data_store(data_chunking_artifacts=data_chunking_artifacts)
            # self.s3_storege.upload_folder(
            #     folder_path=self.traing_pipeline_config.vector_database,
            #     s3_folder='Vector_db'
            # )
            

            logging.info('************************************ Traning Pipline Completed ************************************')
            return db

        except Exception as e:
            logging.info(f'Error in training pipeline {str(e)}')
            print(e)
if __name__=="__main__":
    obj=TrainPipline()
    obj.run()