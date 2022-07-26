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
INGESTED_VALIDATION_DIR_KEY = "ingested_validation_dir"
INGESTED_TEST_DIR_KEY = "ingested_test_dir"


# Data Validation related variables
DATA_VALIDATION_CONFIG_KEY = "data_validation_config"
DATA_VALIDATION_SCHEMA_FILE_NAME_KEY = "schema_file_name"
DATA_VALIDATION_ARTIFACT_DIR = "data_validation"
DATA_VALIDATION_REPORT_FILE_NAME_KEY = "report_file_name"
DATA_VALIDATION_REPORT_PAGE_FILE_NAME_KEY = "report_page_file_name"

# Data Transformation related variables
DATA_TRANSFORMATION_CONFIG_KEY = "data_transformation_config"
DATA_TRANSFORMATION_DIR_KEY = "data_transformation"
# DATA_TRANSFORMATION_GENERATE_CLEAN_DATE_COLS_KEY = "generate_clean_date_cols"
DATA_TRANSFORMATION_TRANSFORMED_DIR_KEY = "transformed_dir"
DATA_TRANSFORMATION_TRAIN_DIR_KEY = "transformed_train_dir"
DATA_TRANSFORMATION_VALIDATION_DIR_KEY = "transformed_validation_dir"
DATA_TRANSFORMATION_PREPROCESSING_DIR_KEY = "preprocessing_dir"
DATA_TRANSFORMATION_PREPROCESSED_OBJECT_FILE_NAME_KEY = "preprocessed_object_file_name"

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> cross check these variables <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# Dataset schema related variables
SCHEMA_COLUMNS_KEY = "columns"
SCHEMA_CLEAN_CATEGORICAL_COLUMNS_KEY = "clean_categorical_columns"
SCHEMA_DOMAIN_VALUE_KEY = "domain_values"
SCHEMA_UNCLEAN_COLUMNS_KEY = "unclean_columns"
SCHEMA_TARGET_COLUMN_KEY = "target_column"
# SCHEMA_DROP_COLUMNS_KEY = "drop_columns"

# Column names
COLUMN_DATE_OF_JOURNEY = "Date_of_Journey"
COLUMN_DEP_TIME = "Dep_Time"
COLUMN_ARRIVAL_TIME = "Arrival_Time"

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Newly used variables <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
COLUMN_DURATION = "Duration"
COLUMN_ADDITIONAL_INFO = "Additional_Info"

# Model trainer related variables
MODEL_TRAINER_ARTIFACT_DIR = "model_trainer"
MODEL_TRAINER_CONFIG_KEY = "model_trainer_config"
MODEL_TRAINER_CONFIG_DIR_KEY = "model_config_dir"
MODEL_TRAINER_TRAINED_MODEL_DIR_KEY = "trained_model_dir"
MODEL_TRAINER_MODEL_FILE_NAME_KEY = "model_file_name"
MODEL_TRAINER_BASE_ACCURACY_KEY = "base_accuracy"
MODEL_TRAINER_CONFIG_FILE_NAME_KEY = "model_config_file_name"
# print("os.getcwd(): ", os.getcwd
# ())

# print(CURRENT_TIME_STAMP, type(CURRENT_TIME_STAMP))