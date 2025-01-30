from dataclasses import dataclass

@dataclass
class DataIngestionArtifacts:
    ingested_data:str

@dataclass
class DataChunkingArtifacts:
    chunking_data_path:str

@dataclass
class VectorDataBaseArtifacts:
    vector_database_path:object
   