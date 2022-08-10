import sys
import os
import json
import pandas as pd

from typing import List
from flight.constant import *
from flight.utils.utils import read_yaml
from flight.exception import FlightException
from flight.logger import logging
from flight.entity.config_entity import DataValidationConfig
from flight.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection
from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab


class DataValidation:
    """
    This class is responsible for performing validation checks on our dataset
    and producing Data validation artifacts.
    """
    def __init__(self,
                 data_validation_config: DataValidationConfig,
                 data_ingestion_artifact: DataIngestionArtifact):
        try:
            logging.info(f"{'='*20} Data Validation log started. {'='*20} \n\n")
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
        except Exception as e:
            raise FlightException(e, sys)

    def is_train_validation_file_exists(self) -> bool:
        """
        Checks if train and validation file are available.
        :return: bool
        """
        try:
            logging.info("Checking if training and validation file are available")
            is_train_file_exists = False
            is_validation_file_exists = False

            train_file_path = self.data_ingestion_artifact.train_file_path
            validation_file_path = self.data_ingestion_artifact.validation_file_path

            is_train_file_exists = os.path.exists(train_file_path)
            is_validation_file_exists = os.path.exists(validation_file_path)
            is_available = is_train_file_exists and is_validation_file_exists
            logging.info(f"Train and Validation file exists? {is_available}")

            if not is_available:
                training_file = self.data_ingestion_artifact.train_file_path
                validation_file = self.data_ingestion_artifact.validation_file_path
                logging.info(f"Training file {training_file} or Testing file {validation_file} is not present")
            return is_available
        except Exception as e:
            raise FlightException(e, sys)

    def get_train_and_validation_df(self) -> pd.DataFrame:
        """
        :return: train and validation dataframe: pd.DataFrame
        """
        try:
            train_df = pd.read_excel(self.data_ingestion_artifact.train_file_path)
            validation_df = pd.read_excel(self.data_ingestion_artifact.validation_file_path)
            return train_df, validation_df
        except Exception as e:
            raise FlightException(e, sys)

    def dataset_column_validation(self) -> bool:
        """
        Compares the train df schema with that in config/schema.yaml file
        :return: bool
        """
        try:
            validation_status = False
            schema_file_path = self.data_validation_config.schema_file_path
            schema_file = read_yaml(schema_file_path)
            train_df, _ = self.get_train_and_validation_df()

            logging.info("Starting dataset column name and datatype validation")
            # ============
            logging.info(f"type of train_df: {train_df}")
            logging.info(f"train_df.columns: {train_df}")
            # ==============
            schema_columns = schema_file[SCHEMA_COLUMNS_KEY]
            if len(train_df.columns) == len(schema_columns):
                for col_name in train_df.columns:
                    if col_name in schema_columns:
                        if train_df[col_name].dtypes == schema_columns[col_name]:
                            pass
                        else:
                            logging.info(f"""Column datatype mismatch with schema file datatype: 
                            [{col_name}: {train_df[col_name].dtypes}] != [{col_name}: {schema_columns[col_name]}]""")
                            raise Exception("Dataframe datatype and schema file datatype mismatch")
                    else:
                        logging.info(f"Column name {col_name} not in schema file")
                        raise Exception(f"Column name {col_name} not in schema file ")
                validation_status = True
                logging.info(f"Column name and data type validation with schema file successful? {validation_status}")
            else:
                logging.info(f"Number of columns mismatch: Dataframe col = {len(train_df.columns)} while Schema file col = {schema_columns}")
                raise Exception("No of dataframe cols doesn't match that of schema file")
            return validation_status
        except Exception as e:
            raise FlightException(e, sys)

    # def cat_column_domain_values_validation(self, cat_columns: List[str]):
    #     # commented because bugs occur when missing values are present
    #     try:
    #         validation_status = False
    #         schema_file_path = self.data_validation_config.schema_file_path
    #         train_df, test_df = self.get_train_and_test_df()
    #         schema_file = read_yaml(schema_file_path)
    #         # schema_file_categorical = schema_file[SCHEMA_CATEGORICAL_COLUMNS_KEY]
    #         for col_name in cat_columns:
    #             for value in train_df[col_name].unique():
    #                 if len(train_df[col_name].unique()) == len(schema_file[SCHEMA_DOMAIN_VALUE_KEY][col_name]):
    #                     if value not in schema_file[SCHEMA_DOMAIN_VALUE_KEY][col_name]:
    #                         logging.info(f"Dataframe col [{col_name}] with domain value [{value}] is not in schema file col [{col_name}]")
    #                         raise Exception(f"Domain value: [{value}] not in schema file [{col_name}] domain values")
    #                 else:
    #                     raise Exception(f"Dataframe domain values in {col_name} = {len(train_df[col_name].unique())} while schema file domain_values of [{col_name}] = {len(schema_file[SCHEMA_DOMAIN_VALUE_KEY][col_name])} ")
    #             logging.info(f"Domain_value validation for {col_name} successful")
    #
    #         validation_status = True
    #         logging.info(f"All columns domain values validated successfully? {validation_status}")
    #         return validation_status
    #     except Exception as e:
    #         raise FlightException(e, sys)

    def validate_dataset_schema(self) -> bool:
        try:
            validation_status = False
            # 1. Number of Column
            # 2. Check the value of Source column
            # acceptable values E.g    Banglore
            # Kolkata
            # Delhi
            # Chennai
            # Mumbai
            # 3. Check column names
            validation_status = self.dataset_column_validation()
            return validation_status
        except Exception as e:
            raise FlightException(e, sys)

    def get_and_save_data_drift_report_json(self) -> dict:
        """
        Generate a json report of train and validation dataset.
        NB: This report is not visually easy to understand.
        To understand the report look at the html version
        generated by save_data_drift_report_page_html().
        :return: dict
        """
        try:
            logging.info("Generating json data drift report")
            profile = Profile(sections=[DataDriftProfileSection()])
            train_df, validation_df = self.get_train_and_validation_df()
            profile.calculate(train_df, validation_df)
            report = json.loads(profile.json())

            report_file_path = self.data_validation_config.report_file_path
            report_dir = os.path.dirname(report_file_path)
            os.makedirs(report_dir)

            with open(report_file_path, "w") as report_file:
                json.dump(report, report_file, indent=6)
            logging.info(f"Json data drift report saved at {report_file_path}")
            return report
        except Exception as e:
            raise FlightException(e, sys)

    def save_data_drift_report_page_html(self) -> None:
        """
        Save the report of train and validation data in html
        :return:
        """
        try:
            logging.info("Generating data drift report page")
            dashboard = Dashboard(tabs=[DataDriftTab()])
            train_df, validation_df = self.get_train_and_validation_df()
            dashboard.calculate(train_df, validation_df)

            report_page_file_path = self.data_validation_config.report_page_file_path
            report_page_dir = os.path.dirname(report_page_file_path)
            os.makedirs(report_page_dir, exist_ok=True)
            dashboard.save(report_page_file_path)
            logging.info(f"Data drift report page saved at: {report_page_file_path}")
        except Exception as e:
            raise FlightException(e, sys)

    def is_data_drift_found(self) -> bool:
        try:
            report = self.get_and_save_data_drift_report_json()
            self.save_data_drift_report_page_html()
            return True
        except Exception as e:
            raise FlightException(e, sys)

    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            self.is_train_validation_file_exists()
            self.dataset_column_validation()
            # self.cat_column_domain_values_validation(cat_columns=["Airline",
            #                                                       "Source",
            #                                                       "Destination",
            #                                                       "Total_Stops",
            #                                                       "Additional_Info"])
            self.validate_dataset_schema()
            self.is_data_drift_found()
            data_validation_artifact = DataValidationArtifact(
                schema_file_path=self.data_validation_config.schema_file_path,
                report_file_path=self.data_validation_config.report_file_path,
                report_file_page_path=self.data_validation_config.report_page_file_path,
                is_validated=True,
                message="Data Validation performed successfully"
            )
            logging.info(f"Data validation artifact: {data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise FlightException(e, sys)

    def __del__(self):
        logging.info(f"{'=' * 20} Data validation log completed. {'='*20} \n\n")