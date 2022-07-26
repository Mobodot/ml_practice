import sys

from typing import List
from flight.logger import logging
from flight.exception import FlightException
from flight.entity.config_entity import ModelTrainerConfig
from flight.entity.model_factory import evaluate_regression_model
from flight.utils.utils import load_numpy_array_data, load_object, save_object
from flight.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact
from flight.entity.model_factory import ModelFactory, GridSearchedBestModel, \
    MetricInfoArtifact


class FlightEstimatorModel:
    def __init__(self, preprocessing_object, trained_model_object):
        """
        TrainedModel constructor
        :param preprocessing_object: preprocessing_object
        :param trained_model_object: trained_model_object
        """
        self.preprocessing_object = preprocessing_object
        self.trained_model_object = trained_model_object

    def predict(self, X):
        """
        This function accepts raw inputs then transforms the raw
        input using preprocessing_object which guarantees that the
        inputs are in the same form as the training data.
        Finally it performs prediction on transformed features
        """
        transformed_feature = self.preprocessing_object.transform(X)
        return self.trained_model_object.predict(transformed_feature)

    def __repr__(self):
        return f"{type(self.trained_model_object).__name__}()"

    def __str__(self):
        return f"{type(self.trained_model_object).__name__}()"


class ModelTrainer:
    def __init__(self,
                 model_trainer_config: ModelTrainerConfig,
                 data_transformation_artifact: DataTransformationArtifact):
        try:
            logging.info(f"{'>>' * 30}Model trainer log started.{'<<' * 30} ")
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise FlightException(e, sys)

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            logging.info("Loading transformed training dataset")
            transformed_train_file_path = \
                self.data_transformation_artifact.transformed_train_file_path
            train_array = load_numpy_array_data(transformed_train_file_path)

            logging.info("Loading transformed validation dataset")
            transformed_validation_file_path = \
                self.data_transformation_artifact.transformed_validation_file_path
            validation_array = load_numpy_array_data(transformed_validation_file_path)

            logging.info("Splitting training and validation input and target features")
            x_train, y_train, x_test, y_test = \
                train_array[:, :-1], train_array[:, -1], validation_array[:, :-1], validation_array[:, -1]

            logging.info("Extracting model config file path")
            model_config_file_path = self.model_trainer_config.model_config_file_path

            logging.info(f"Initializing model factory class using above model config file: {model_config_file_path}")
            model_factory = ModelFactory(model_config_path=model_config_file_path)

            base_accuracy = self.model_trainer_config.base_accuracy
            logging.info(f"Expected accuracy: {base_accuracy}")

            logging.info("Initiating model selection operation")
            best_model = model_factory.get_best_model(X=x_train, y=y_train, base_accuracy=base_accuracy)

            logging.info(f"Best model found on training dataset: {best_model}")

            logging.info("Extracting trained model list.")
            grid_searched_best_model_list: List[GridSearchedBestModel] = \
                model_factory.grid_searched_best_model_list

            model_list = [model.best_model for model in grid_searched_best_model_list]
            logging.info("Evaluation of all trained models on training and validation dataset both")
            metric_info: MetricInfoArtifact = evaluate_regression_model(
                model_list=model_list,
                X_train=x_train,
                y_train=y_train,
                X_test=x_test,
                y_test=y_test,
                base_accuracy=base_accuracy
            )

            logging.info("Best found model on both training and validation dataset")

            preprocessing_obj = load_object(
                file_path=self.data_transformation_artifact.preprocessed_object_file_path
            )
            model_object = metric_info.model_object

            trained_model_file_path = self.model_trainer_config.trained_model_file_path
            flight_model = FlightEstimatorModel(preprocessing_object=preprocessing_obj,
                                                trained_model_object=model_object)
            logging.info(f"Saving model at path: {trained_model_file_path}")
            save_object(file_path=trained_model_file_path, obj=flight_model)

            model_trainer_artifact = ModelTrainerArtifact(
                is_trained=True,
                message="Model Trained successfully",
                trained_model_file_path=trained_model_file_path,
                train_rmse=metric_info.train_rmse,
                validation_rmse=metric_info.validation_rmse,
                train_accuracy=metric_info.train_accuracy,
                validation_accuracy=metric_info.validation_accuracy,
                model_accuracy=metric_info.model_accuracy
            )
            logging.info(f"Model Trainer Artifact: {model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
            raise FlightException(e, sys)

    def __del__(self):
        logging.info(f"{'>>' * 30} Model trainer log completed. {'<<' * 30}")


# Code summary:
"""
1. loading transformed training and validation dataset.
2. reading model config file.
3. getting best model on training dataset.
4. evaluation models on both training & validation dataset --> model object
5. loading preprocessing object
6. custom model object by combining both preprocessing obj and model obj
7. saving custom model object
8. return model_trainer_artifact
"""