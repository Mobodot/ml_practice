from collections import namedtuple

DataIngestionConfig = namedtuple("DataIngestionConfig", ["dataset_download_url",
                                                         "raw_data_dir",
                                                         "zip_download_dir",
                                                         "ingested_dir",
                                                         "ingested_train_dir",
                                                         "ingested_test_dir"])

DataValidationConfig = namedtuple("DataValidationConfig", ["schema_file_name"])

DataTransformationConfig = namedtuple("DataTransformationConfig", ["transformed_dir",
                                                                   "transformed_train_dir",
                                                                   "transformed_test_dir",
                                                                   "preprocessing_dir",
                                                                   "preprocessed_object_file_name"])

ModelTrainerConfig = namedtuple("ModelTrainerconfig", ["trained_model_dir",
                                                       "model_file_name",
                                                       "base_accuracy"])

ModelPusherConfig = namedtuple("ModelPusherConfig", ["model_export_dir"])

TrainingPipelineConfig = namedtuple("TrainingPipelineConfig", ["artifact_dir"])
