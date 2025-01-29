import os

from src.logging import logging
from src.config.config import DataIngestionConfig
from langchain_community.document_loaders import WebBaseLoader

class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        self.data_ingestion_config = data_ingestion_config

    def fetch_data_from_wikipedia(self, url: list, filename: str):
        try:
            logging.info("Web data ingestion started.")
            logging.info(f" url: {url}")

            all_text = ""

            # Load documents from URLs
            
            loader = WebBaseLoader(url)
            docs = loader.load()
            logging.info('Data Loded Successfully')

            if docs:
                    all_text += f"=== {url} ===\n{docs[0].page_content}\n\n"

            # Create directory if not exists
            dir_path = os.path.dirname(filename)
            os.makedirs(dir_path, exist_ok=True)

            # Save the fetched content
            with open(filename, "w", encoding="utf-8") as f:
                f.write(all_text)
            logging.info(f"Data save {filename} successfully.")
        except Exception as e:
            raise e

    def initiate_data_ingestion(self):
        try:
            data_store_path = self.data_ingestion_config.data_ingestion_ingest_data
            url_titles = self.data_ingestion_config.data_ingestion_url_name

            self.fetch_data_from_wikipedia(
                url=url_titles,
                filename=data_store_path
            )
            print('Data Ingestion completed')
            return data_store_path
        except Exception as e:
            raise e
