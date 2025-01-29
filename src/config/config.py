from src.logging import logging
from src.constants import traning_pipline
from datetime import datetime
import os

class TraningPiplineConfig:
    def __init__(self):
        self.timestamp=datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
        self.artifacts_path=os.path.join(traning_pipline.ARTIFACTS_PATH,self.timestamp) # Artifacts path

class DataIngestionConfig:
    def __init__(self,traning_pipline_config:TraningPiplineConfig)->None:
        # data ingestion dir inside artifacts
        self.data_ingestion_dir=os.path.join(
            traning_pipline_config.artifacts_path,traning_pipline.DATA_INGESTION_DIR_NAME
        )
        # data path to store data
        self.data_ingestion_ingest_data=os.path.join(
            self.data_ingestion_dir,traning_pipline.DATA_INGESTION_INGEST_FILE
        )
        # url
        self.data_ingestion_url_name= traning_pipline.DATA_INGESTION_DATA_URL

class DataChunkingConfig:
    def __init__(self,traning_pipline_config:TraningPiplineConfig):
        # data chunking path
        self.data_chunking__dir= os.path.join(
            traning_pipline_config.artifacts_path, traning_pipline.DATA_CHUNKING_DIR
        )
        # save chuninking
        self.data_chunking_data_path=os.path.join(
            self.data_chunking__dir,traning_pipline.DATA_CHUNKING_FILE
        )
        # chuinking size
        self.chuninking_size=traning_pipline.CHUINK_SIZE
        # chunink overlap
        self.chuninking_overlap=traning_pipline.CHUINK_OVERLAP
