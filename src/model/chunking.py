import os
import re
import json
from langchain.text_splitter import RecursiveCharacterTextSplitter
from src.config.artifacts_entity import DataIngestionArtifacts, DataChunkingArtifacts
from src.config.config import DataChunkingConfig
from src.logging import logging

class DataChunking:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifacts, chunking_config: DataChunkingConfig):
        self.data_ingestion_artifacts = data_ingestion_artifact
        self.chunking_config = chunking_config

    def preprocess_text(self, text):
        text = text.lower()  # Convert to lowercase
        text = re.sub(r"[^a-zA-Z0-9\n]", " ", text)  # Remove special characters
        text = re.sub(r"([a-z])([A-Z])", r"\1 \2", text)  # Add spaces between camelCase words
        text = re.sub(r"(\d+)", r" \1 ", text)  # Add spaces around numbers
        text = re.sub(r"\s+", " ", text).strip()  # Remove extra spaces
        return text

    def chunk_text(self, text):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunking_config.chuninking_size, 
            chunk_overlap=self.chunking_config.chuninking_overlap  
        )
        return text_splitter.split_text(text)

    def save_json(self, obj, filename):
        dir_path = os.path.dirname(filename)
        os.makedirs(dir_path, exist_ok=True)

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(obj, f, indent=4, ensure_ascii=False)

    def initiate_data_chunking(self):
        try:
            logging.info("Chunking and vector store started")

            # Read data from file
            data_path = self.data_ingestion_artifacts.ingested_data
            with open(data_path, "r", encoding="utf-8") as f:
                raw_data = f.read()

            # Save chunking data path 
            chunking_data_path = self.chunking_config.data_chunking_data_path

            # Data preprocessing
            cleaned_data = self.preprocess_text(raw_data)
            logging.info("Text preprocessing completed")

            # Chunking
            chunks = self.chunk_text(cleaned_data)
            logging.info(f"Chunking completed. Total Chunks: {len(chunks)}")
            print(len(chunks))

            # Save chunks
            self.save_json(chunks, chunking_data_path)
            logging.info(f"Chunking data saved at: {chunking_data_path}")

            return DataChunkingArtifacts(chunking_data_path=chunking_data_path)

        except Exception as e:
            logging.error(f"Error in data chunking: {str(e)}")
            raise e  