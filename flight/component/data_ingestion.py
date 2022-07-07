import os
import shutil
import sys
import pandas as pd
import opendatasets

from flight.entity.config_entity import DataIngestionConfig
from flight.entity.artifact_entity import DataIngestionArtifact
from flight.exception import FlightException
from flight.logger import logging


class DataIngestion:
    """This class is responsible for carrying out all data ingestion processes"""

    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            logging.info(f"{'='*20} Data Ingestion log started. -{'='*20}")
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise FlightException(e, sys)

    # def download_flight_dataset(self) -> str:
    #     try:
    #         # extract dataset url
    #         download_url = self.data_ingestion_config.dataset_download_url
    #
    #         # location to download zip data
    #         zip_download_dir = self.data_ingestion_config.zip_download_dir
    #
    #         if os.path.exists(zip_download_dir):
    #             os.remove(zip_download_dir)
    #
    #         os.makedirs(zip_download_dir, exist_ok=True)
    #
    #         # flight_pred_name = self.data_ingestion_config.dataset_download_url.split("/")[-2]
    #         # zip_download_file_path = os.path.join(zip_download_dir, flight_pred_name)
    #         # flight_pred_name = os.path.basename(download_url)
    #         zip_download_file_path = os.path.join(zip_download_dir, flight_pred_name)
    #
    #         logging.info(f"Downloading file from [{download_url}] into: [{zip_download_file_path}]")
    #         urllib.request.urlretrieve(download_url, zip_download_file_path)
    #         logging.info(f"File: [{zip_download_file_path}] has been downloaded successfully")
    #         return zip_download_file_path
    #
    #     except Exception as e:
    #         raise FlightException(e, sys)

    def download_flight_data(self) -> str:
        try:
            download_url = self.data_ingestion_config.dataset_download_url
            raw_data_dir = self.data_ingestion_config.raw_data_dir

            if os.path.exists(raw_data_dir):
                os.remove(raw_data_dir)

            os.makedirs(raw_data_dir, exist_ok=True)
            logging.info(f"Downloading file from [{download_url}] into: [{raw_data_dir}]")

            # requires kaggle name and api key gotten from your kaggle account setting kaggle.json file
            opendatasets.download(download_url, raw_data_dir+"/")
            logging.info(f"File {raw_data_dir} downloaded successfully!")
            raw_data_dir_filename = os.listdir(raw_data_dir)[0]
            return raw_data_dir_filename
        except Exception as e:
            raise FlightException(e, sys)

    # def extract_zip_file(self, zip_download_file_path: str) -> None:
    #     try:
    #         raw_data_dir = self.data_ingestion_config.raw_data_dir
    #
    #         if os.path.exists(raw_data_dir):
    #             os.remove(raw_data_dir)
    #         os.makedirs(raw_data_dir)
    #
    #         logging.info(f"Extracting zip file: [{zip_download_file_path}]")
    #         with ZipFile.open(zip_download_file_path)as unzipped_file_obj:
    #             unzipped_file_obj.extractall(path=raw_data_dir)
    #         logging.info(f"Extraction complete!")
    #
    #     except Exception as e:
    #         raise FlightException(e, sys)

    def get_train_and_test_data(self, raw_data_dir_filename: str) -> DataIngestionArtifact:
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir
            raw_data_dir_path = os.path.join(raw_data_dir, raw_data_dir_filename)
            train_data_filename = os.listdir(raw_data_dir_path)[1]
            train_data_filepath = os.path.join(raw_data_dir_path, train_data_filename)

            test_data_filename = os.listdir(raw_data_dir_path)[-1]
            test_data_filepath = os.path.join(raw_data_dir_path, test_data_filename)
            test_dataframe = pd.read_excel(test_data_filepath)

            target_result_test_data_filename = os.listdir(raw_data_dir_path)[0]
            target_result_test_data_filepath = os.path.join(raw_data_dir_path, target_result_test_data_filename)
            target_result_test_dataframe = pd.read_excel(target_result_test_data_filepath)

            # combining the test_dataframe and its target value
            test_dataframe = pd.concat([test_dataframe,
                                        target_result_test_dataframe], axis=1)

            train_file_path = os.path.join(self.data_ingestion_config.ingested_train_dir,
                                           train_data_filename)

            test_file_path = os.path.join(self.data_ingestion_config.ingested_test_dir,
                                          test_data_filename)

            if train_data_filename:
                os.makedirs(self.data_ingestion_config.ingested_train_dir, exist_ok=True)
                logging.info(f"Copying training data to file: [{train_file_path}]")
                shutil.copy(train_data_filepath, train_file_path)

            if test_data_filename:
                os.makedirs(self.data_ingestion_config.ingested_test_dir, exist_ok=True)
                logging.info(f"Creating test data file in: [{test_file_path}]")
                test_dataframe.to_excel(test_file_path, index=False)

            data_ingestion_artifact = DataIngestionArtifact(test_file_path=test_file_path,
                                                            train_file_path=train_file_path,
                                                            is_ingested=True,
                                                            message="Data ingestion completed successfully!")

            logging.info(f"Data Ingestion Artifact: [{data_ingestion_artifact}]")
            return data_ingestion_artifact
        except Exception as e:
            raise FlightException(e, sys)

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            raw_data_dir_filename = self.download_flight_data()
            return self.get_train_and_test_data(raw_data_dir_filename=raw_data_dir_filename)
        except Exception as e:
            raise FlightException(e, sys)

    def __del__(self):
        logging.info(f"{'=' * 20}Data Ingestion log completed.{'=' * 20} \n\n")