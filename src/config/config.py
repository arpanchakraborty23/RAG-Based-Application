from src.logging import logging
from src.constants import traning_pipline
import os

class DataIngestionConfig:
    def __init__(self):
        self.data_ingestion_ingest_data=os.path.join(
            traning_pipline.DATA_INGESTION_INGEST_DIR,traning_pipline.DATA_INGESTION_INGEST_FILE # Data folder
        )
        self.data_ingestion_url_name= traning_pipline.DATA_INGESTION_DATA_URL

