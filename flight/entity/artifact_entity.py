from collections import namedtuple

DataIngestionArtifact = namedtuple("DataIngestionArtifact", ["test_file_path",
                                                             "train_file_path",
                                                             "validation_file_path",
                                                             "is_ingested",
                                                             "message"])

DataValidationArtifact = namedtuple("DataValidationArtifact", ["schema_file_path",
                                                               "report_file_path",
                                                               "report_file_page_path",
                                                               "is_validated",
                                                               "message"])

DataTransformationArtifact = namedtuple("DataTransformationArtifact", ["is_transformed",
                                                                       "message",
                                                                       "transformed_train_file_path",
                                                                       "transformed_validation_file_path",
                                                                       "preprocessed_object_file_path"])