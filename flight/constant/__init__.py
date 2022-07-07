import os
from datetime import datetime

ROOT_DIR = os.getcwd()


CURRENT_TIME_STAMP = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

CONFIG_DIR = "config"
CONFIG_FILE_NAME = "config.yaml"
CONFIG_FILE_PATH = os.path.join(ROOT_DIR, CONFIG_DIR, CONFIG_FILE_NAME)

# Training pipeline related variables
TRAINING_PIPELINE_CONFIG_KEY = "training_pipeline_config"
TRAINING_PIPELINE_NAME_KEY = "pipeline_name"
TRAINING_PIPELINE_ARTIFACT_DIR_KEY = "artifact_dir"

# Data ingestion related variables
DATA_INGESTION_ARTIFACT_DIR = "data_ingestion"
DATA_INGESTION_CONFIG_KEY = "data_ingestion_config"
DATASET_DOWNLOAD_URL_KEY = "dataset_download_url"
RAW_DATA_DIR_KEY = "raw_data_dir"
ZIP_DOWNLOAD_DIR_KEY = "zip_download_dir"
INGESTED_DIR_KEY = "ingested_dir"
INGESTED_TRAIN_DIR_KEY = "ingested_train_dir"
INGESTED_TEST_DIR_KEY = "ingested_test_dir"


# Data Validation related variables
DATA_VALIDATION_CONFIG_KEY = "data_validation_config"
DATA_VALIDATION_SCHEMA_FILE_NAME_KEY = "schema_file_name"
DATA_VALIDATION_ARTIFACT_DIR = "data_validation"
DATA_VALIDATION_REPORT_FILE_NAME_KEY = "report_file_name"
DATA_VALIDATION_REPORT_PAGE_FILE_NAME_KEY = "report_page_file_name"
# print(CONFIG_FILE_PATH)
# print(PARENT_DIR_PATH, "hello")



# print("os.getcwd(): ", os.getcwd())

# print(CURRENT_TIME_STAMP, type(CURRENT_TIME_STAMP))