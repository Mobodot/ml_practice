from collections import namedtuple

DataIngestionArtifact = namedtuple("DataIngestionArtifact", ["test_file_path",
                                                             "train_file_path",
                                                             "is_ingested",
                                                             "message"])

DataValidationArtifact = namedtuple("DataValidationArtifact", ["schema_file_path",
                                                               "report_file_path",
                                                               "report_file_page_path",
                                                               "is_validated",
                                                               "message"])