import sys
import numpy as np
import pandas as pd

from flight.constant import *
from flight.logger import logging
from flight.exception import FlightException
from flight.entity.config_entity import ModelEvaluationConfig
from flight.entity.model_factory import evaluate_regression_model
from flight.utils.utils import load_object, read_yaml, write_yaml
from flight.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, \
    ModelTrainerArtifact, ModelEvaluationArtifact


class ModelEvaluation:

    def __init__(self,
                 model_evaluation_config: ModelEvaluationConfig,
                 data_ingestion_artifact: DataIngestionArtifact,
                 data_validation_artifact: DataValidationArtifact,
                 model_trainer_artifact: ModelTrainerArtifact):
        try:
            logging.info(f"{'>>' * 30} Model Evaluation log started. {'<<' * 30}")
            self.model_evaluation_config = model_evaluation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_artifact = data_validation_artifact
            self.model_trainer_artifact = model_trainer_artifact
        except Exception as e:
            raise FlightException(e, sys)

    def get_best_model(self):
        try:
            model = None
            model_evaluation_file_path = self.model_evaluation_config.model_evaluation_file_path

            # no model found
            if not os.path.exists(model_evaluation_file_path):
                write_yaml(file_path=model_evaluation_file_path)
                return model
            model_eval_file_content = read_yaml(file_path=model_evaluation_file_path)

            # create empty dict to write contents of yaml file if model is not found
            model_eval_file_content = dict() if model_eval_file_content is None else model_eval_file_content

            if BEST_MODEL_KEY not in model_eval_file_content:
                return model

            # model found
            model = load_object(file_path=model_eval_file_content[BEST_MODEL_KEY][MODEL_PATH_KEY])
            return model
        except Exception as e:
            raise FlightException(e, sys)

    def update_evaluation_report(self,
                                 model_evaluation_artifact: ModelEvaluationArtifact):
        try:
            eval_file_path = self.model_evaluation_config.model_evaluation_file_path
            model_eval_content = read_yaml(file_path=eval_file_path)
            model_eval_content = dict() if model_eval_content is None else model_eval_content

            previous_best_model = None
            if BEST_MODEL_KEY in model_eval_content:
                previous_best_model = model_eval_content[BEST_MODEL_KEY]
            logging.info(f"Previous eval result: {model_eval_content}")
            eval_result = {
                BEST_MODEL_KEY: {
                    MODEL_PATH_KEY: model_evaluation_artifact.evaluated_model_path
                }
            }

            if previous_best_model is not None:
                model_history = {self.model_evaluation_config.time_stamp: previous_best_model}
                if HISTORY_KEY not in model_eval_content:
                    history = {HISTORY_KEY: model_history}
                    eval_result.update(history)
                else:
                    model_eval_content[HISTORY_KEY].update(model_history)

            model_eval_content.update(eval_result)
            logging.info(f"Updated eval result: {model_eval_content}")
            write_yaml(file_path=eval_file_path, data=model_eval_content)
        except Exception as e:
            raise FlightException(e, sys)

    def initiate_model_evaluation(self) -> ModelEvaluationArtifact:
        try:
            trained_model_file_path = self.model_trainer_artifact.trained_model_file_path
            trained_model_object = load_object(file_path=trained_model_file_path)

            train_file_path = self.data_ingestion_artifact.train_file_path
            validation_file_path = self.data_ingestion_artifact.validation_file_path

            schema_file_path = self.data_validation_artifact.schema_file_path

            train_dataframe = pd.read_excel(train_file_path)
            validation_dataframe = pd.read_excel(validation_file_path)

            schema_content = read_yaml(file_path=schema_file_path)
            target_column_name = schema_content[SCHEMA_TARGET_COLUMN_KEY]

            # target_column
            logging.info("Converting target column into numpy array.")
            train_target_arr = np.array(train_dataframe[target_column_name])
            validation_target_arr = np.array(validation_dataframe[target_column_name])
            logging.info("Target column conversion to numpy array successful.")

            # dropping target column from the dataframe
            logging.info("Dropping target column from the dataframe.")
            train_dataframe.drop(target_column_name, axis=1, inplace=True)
            validation_dataframe.drop(target_column_name, axis=1, inplace=True)
            logging.info(f"Dropping target column from train and validation dataframe successful.")

            model = self.get_best_model()

            if model is None:
                logging.info("Not found any existing model. Hence accepting trained model.")
                model_evaluation_artifact = ModelEvaluationArtifact(
                    evaluated_model_path=trained_model_file_path,
                    is_model_accepted=True
                )
                self.update_evaluation_report(model_evaluation_artifact=model_evaluation_artifact)
                logging.info(f"Model accepted. Model evaluation artifact {model_evaluation_artifact} created.")
                return model_evaluation_artifact

            model_list = [model, trained_model_object]

            metric_info_artifact = evaluate_regression_model(
                model_list=model_list,
                X_train=train_dataframe,
                y_train=train_target_arr,
                X_test=validation_dataframe,
                y_test=validation_target_arr,
                base_accuracy=self.model_trainer_artifact.model_accuracy
            )
            logging.info(f"Model evaluation completed. Model metric artifact: {metric_info_artifact}")

            if metric_info_artifact is None:
                response = ModelEvaluationArtifact(
                    is_model_accepted=False,
                    evaluated_model_path=trained_model_file_path
                )
                logging.info(response)
                return response

            if metric_info_artifact.index_number == 1:
                model_evaluation_artifact = ModelEvaluationArtifact(
                    is_model_accepted=True,
                    evaluated_model_path=trained_model_file_path
                )
                self.update_evaluation_report(model_evaluation_artifact=model_evaluation_artifact)
                logging.info(f"Model accepted. Model eval artifact {model_evaluation_artifact} created.")
            else:
                logging.info("Trained model is no better than existing model hence not accepting trained model.")
                model_evaluation_artifact = ModelEvaluationArtifact(is_model_accepted=False,
                                                                    evaluated_model_path=trained_model_file_path)
                return model_evaluation_artifact
        except Exception as e:
            raise FlightException(e, sys)

    def __del__(self):
        logging.info(f"{'=' * 20}Model Evaluation log completed.{'=' * 20} ")
