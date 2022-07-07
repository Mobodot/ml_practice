import sys
import os
import json
import pandas as pd

from flight.exception import FlightException
from flight.logger import logging
from flight.entity.config_entity import DataValidationConfig
from flight.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection
from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab
import json

class DataValidation:
    """
    This class is responsible for performing validation checks on our dataset
    """
    def __init__(self, data_validation_config: DataValidationConfig,
                 data_ingestion_artifact: DataIngestionArtifact):
        try:
            logging.info(f"{'='*20} Data Validation log started. -{'='*20} \n\n")
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
        except Exception as e:
            raise FlightException(e, sys)

    def is_train_test_file_exists(self) -> bool:
        try:
            logging.info("Checking if training and test file are available")
            is_train_file_exists = False
            is_test_file_exists = False

            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            is_train_file_exists = os.path.exists(train_file_path)
            is_test_file_exists = os.path.exists(test_file_path)
            is_available = is_train_file_exists and is_test_file_exists
            logging.info(f"Train and test file exists? {is_available}")

            if not is_available:
                training_file = self.data_ingestion_artifact.train_file_path
                testing_file = self.data_ingestion_artifact.test_file_path
                logging.info(f"Training file {training_file} or Testing file {testing_file} is not present")
            return is_available
        except Exception as e:
            raise FlightException(e, sys)

    def get_train_and_test_df(self) -> pd.DataFrame:
        try:
            train_df = pd.read_excel(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_excel(self.data_ingestion_artifact.test_file_path)
            return train_df, test_df
        except Exception as e:
            raise FlightException(e, sys)

    def validate_dataset_schema(self) -> bool:
        try:
            validation_status = False

            validation_status = True
            return validation_status
        except Exception as e:
            raise FlightException(e, sys)

    def get_and_save_data_drift_report_json(self) -> dict:
        try:
            logging.info("Generating json data drift report")
            profile = Profile(sections=[DataDriftProfileSection()])
            train_df, test_df = self.get_train_and_test_df()
            profile.calculate(train_df, test_df)
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
        try:
            logging.info("Generating data drift report page")
            dashboard = Dashboard(tabs=[DataDriftTab()])
            train_df, test_df = self.get_train_and_test_df()
            dashboard.calculate(train_df, test_df)

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
            self.is_train_test_file_exists()
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
        logging.info(f"{'=*20'} Data validation log completed. {'='*20} \n\n")