from flight.entity.config_entity import DataIngestionConfig, DataValidationConfig, DataTransformationConfig,\
    ModelTrainerConfig, ModelPusherConfig, TrainingPipelineConfig
from datetime import datetime
from flight.utils.utils import read_yaml
from flight.logger import logging
from flight.exception import FlightException
from flight.constant import *
import sys


class Configuration:
    """
    This class is responsible for creating configuration settings to
    be used by the components in creating artifacts.
    """

    def __init__(self,
                 config_file_path: str=CONFIG_FILE_PATH,
                 current_time_stamp: str=CURRENT_TIME_STAMP):
        try:
            self.config_info = read_yaml(CONFIG_FILE_PATH)
            self.training_pipeline_config = self.get_training_pipeline_config()
            self.current_time_stamp = current_time_stamp
        except Exception as e:
            raise FlightException(e, sys)

    def get_data_ingestion_config(self) -> DataIngestionConfig:

        try:
            artifact_dir = self.training_pipeline_config.artifact_dir

            data_ingestion_artifact_dir = os.path.join(artifact_dir,
                                                       DATA_INGESTION_ARTIFACT_DIR,
                                                       CURRENT_TIME_STAMP)

            data_ingestion_info = self.config_info[DATA_INGESTION_CONFIG_KEY]
            dataset_download_url = data_ingestion_info[DATASET_DOWNLOAD_URL_KEY]
            raw_data_dir = os.path.join(data_ingestion_artifact_dir,
                                        data_ingestion_info[RAW_DATA_DIR_KEY])
            zip_download_dir = os.path.join(data_ingestion_artifact_dir,
                                            data_ingestion_info[ZIP_DOWNLOAD_DIR_KEY])
            ingested_dir = os.path.join(data_ingestion_artifact_dir,
                                        data_ingestion_info[INGESTED_DIR_KEY])
            ingested_train_dir = os.path.join(data_ingestion_artifact_dir,
                                              ingested_dir,
                                              data_ingestion_info[INGESTED_TRAIN_DIR_KEY])
            ingested_validation_dir = os.path.join(data_ingestion_artifact_dir,
                                                   ingested_dir,
                                                   data_ingestion_info[INGESTED_VALIDATION_DIR_KEY])
            ingested_test_dir = os.path.join(data_ingestion_artifact_dir,
                                             ingested_dir,
                                             data_ingestion_info[INGESTED_TEST_DIR_KEY])

            data_ingestion_config = DataIngestionConfig(dataset_download_url=dataset_download_url,
                                                        raw_data_dir=raw_data_dir,
                                                        zip_download_dir=zip_download_dir,
                                                        ingested_dir=ingested_dir,
                                                        ingested_train_dir=ingested_train_dir,
                                                        ingested_validation_dir=ingested_validation_dir,
                                                        ingested_test_dir=ingested_test_dir)
            # print(data_ingestion_config)
            logging.info(f"Data Ingestion config: {data_ingestion_config}")
            return data_ingestion_config
        except Exception as e:
            raise FlightException(e, sys)

    def get_data_validation_config(self) -> DataValidationConfig:
        try:
            artifact_dir = self.training_pipeline_config.artifact_dir
            data_validation_artifact_dir = os.path.join(artifact_dir,
                                                        DATA_VALIDATION_ARTIFACT_DIR,
                                                        self.current_time_stamp)
            data_validation_config = self.config_info[DATA_VALIDATION_CONFIG_KEY]
            schema_dir = os.path.join(ROOT_DIR, CONFIG_DIR)
            schema_file_path = os.path.join(schema_dir,
                                            data_validation_config[DATA_VALIDATION_SCHEMA_FILE_NAME_KEY])

            report_file_path = os.path.join(data_validation_artifact_dir,
                                            data_validation_config[DATA_VALIDATION_REPORT_FILE_NAME_KEY])

            report_page_file_path = os.path.join(data_validation_artifact_dir,
                                                 data_validation_config[DATA_VALIDATION_REPORT_PAGE_FILE_NAME_KEY])

            data_validation_config = DataValidationConfig(schema_dir=schema_dir,
                                                          schema_file_path=schema_file_path,
                                                          report_file_path=report_file_path,
                                                          report_page_file_path=report_page_file_path)

            logging.info(f"Data Validation config: [{data_validation_config}]")
            return data_validation_config
        except Exception as e:
            raise FlightException(e, sys)


    def get_data_transformation_config(self) -> DataTransformationConfig:
        try:
            artifact_dir = self.training_pipeline_config.artifact_dir
            data_transformation_config = self.config_info[DATA_TRANSFORMATION_CONFIG_KEY]

            # generate_clean_date_cols = data_transformation_config[DATA_TRANSFORMATION_GENERATE_CLEAN_DATE_COLS_KEY]
            data_transformation_dir = os.path.join(artifact_dir,
                                           DATA_TRANSFORMATION_DIR_KEY,
                                           self.current_time_stamp)

            preprocessed_object_file_path = os.path.join(data_transformation_dir,
                                                         data_transformation_config[DATA_TRANSFORMATION_PREPROCESSING_DIR_KEY],
                                                         data_transformation_config[DATA_TRANSFORMATION_PREPROCESSED_OBJECT_FILE_NAME_KEY])

            transformed_dir = os.path.join(data_transformation_dir,
                                           data_transformation_config[DATA_TRANSFORMATION_TRANSFORMED_DIR_KEY])

            transformed_train_dir = os.path.join(transformed_dir,
                                                 data_transformation_config[DATA_TRANSFORMATION_TRAIN_DIR_KEY])

            transformed_validation_dir = os.path.join(transformed_dir,
                                                      data_transformation_config[DATA_TRANSFORMATION_VALIDATION_DIR_KEY])

            # preprocessing_dir = os.path.join(data_transformation_dir,
            #                                  DATA_TRANSFORMATION_PREPROCESSING_DIR_KEY)

            # preprocessed_object_file_name = os.path.join(preprocessed_object_file_path,
            #                                               data_transformation_config[DATA_TRANSFORMATION_PREPROCESSED_OBJECT_FILE_NAME_KEY])

            data_transformation_config = DataTransformationConfig(# generate_clean_date_cols=generate_clean_date_cols,
                                                                  transformed_dir=transformed_dir,
                                                                  transformed_train_dir=transformed_train_dir,
                                                                  transformed_validation_dir=transformed_validation_dir,
                                                                  # transformed_test_dir=transformed_test_dir,
                                                                  # preprocessing_dir=preprocessing_dir,
                                                                  preprocessed_object_file_path=preprocessed_object_file_path)
            logging.info(f"Data Transformation Config: [{data_transformation_config}]")
            return data_transformation_config
        except Exception as e:
            raise FlightException(e, sys)

    def get_model_trainer_config(self) -> ModelTrainerConfig:
        pass

    def get_model_pusher_config(self) -> ModelPusherConfig:
        pass

    def get_training_pipeline_config(self) -> ModelTrainerConfig:
        try:
            training_pipeline_config = self.config_info[TRAINING_PIPELINE_CONFIG_KEY]
            artifact_dir = os.path.join(ROOT_DIR,
                                        training_pipeline_config[TRAINING_PIPELINE_NAME_KEY],
                                        training_pipeline_config[TRAINING_PIPELINE_ARTIFACT_DIR_KEY])
            training_pipeline_config = TrainingPipelineConfig(artifact_dir=artifact_dir)
            logging.info(f"Training pipeline config: {training_pipeline_config}")
            # print(training_pipeline_config)
            return TrainingPipelineConfig(artifact_dir=artifact_dir)
        except Exception as e:
            raise FlightException(e, sys)


# c = Configuration()
# print(c.config_info)
# c.get_training_pipeline_config()
# c.get_data_ingestion_config()
# print(CONFIG_FILE_PATH)


