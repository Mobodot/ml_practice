from collections import namedtuple

DataIngestionArtifact = namedtuple("DataIngestionArtifact", ["test_file_path",
                                                             "train_file_path",
                                                             "is_ingested",
                                                             "message"])