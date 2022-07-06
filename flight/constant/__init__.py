import os
from datetime import datetime

# for VSCODE use ROOT_DIR (because code execution starts from project main directory
ROOT_DIR = os.getcwd()

# for PYCHARM use PROJECT_DIR_PATH
# PROJECT_DIR = os.getcwd().split("/")[:-2]
# PROJECT_DIR_PATH = "/".join(PROJECT_DIR)

CURRENT_TIME_STAMP = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

# /home/mobo/Documents/Ineuron/Live_Class/ML/PracticeML/ml_practice

CONFIG_DIR = "config"
CONFIG_FILE_NAME = "config.yaml"
CONFIG_FILE_PATH = os.path.join(ROOT_DIR, CONFIG_DIR, CONFIG_FILE_NAME)

TRAINING_PIPELINE_CONFIG_KEY = "training_pipeline_config"
TRAINING_PIPELINE_NAME_KEY = "pipeline_name"
TRAINING_PIPELINE_ARTIFACT_DIR_KEY = "artifact_dir"

DATA_INGESTION_ARTIFACT_DIR = "data_ingestion"
DATA_INGESTION_CONFIG_KEY = "data_ingestion_config"
DATASET_DOWNLOAD_URL_KEY = "dataset_download_url"
RAW_DATA_DIR_KEY = "raw_data_dir"
ZIP_DOWNLOAD_DIR_KEY = "zip_download_dir"
INGESTED_DIR_KEY = "ingested_dir"
INGESTED_TRAIN_DIR_KEY = "ingested_train_dir"
INGESTED_TEST_DIR_KEY = "ingested_test_dir"

# print(CONFIG_FILE_PATH)
# print(PARENT_DIR_PATH, "hello")



# print("os.getcwd(): ", os.getcwd())

# print(CURRENT_TIME_STAMP, type(CURRENT_TIME_STAMP))