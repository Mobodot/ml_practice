import os
import sys
import numpy as np
import pandas as pd

from typing import Tuple
from flight.constant import *
from flight.logger import logging
from sklearn.pipeline import Pipeline
from flight.utils.utils import *
from sklearn.impute import SimpleImputer
from flight.exception import FlightException
from sklearn.compose import ColumnTransformer
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import StandardScaler, OrdinalEncoder
from flight.entity.config_entity import DataTransformationConfig
from flight.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact


class CleanAddInfoCol(BaseEstimator, TransformerMixin):
    """This class performs data cleaning operations on the ADDITIONAL_INFO col"""

    def __init__(self):
        try:
            self.add_info_status = False
            self.add_info_col = COLUMN_ADDITIONAL_INFO
        except Exception as e:
            raise FlightException(e, sys)

    def clean_additional_info(self, X):
        try:
            logging.info("Cleaning Additional Info col started.")
            if len(X.loc[:, self.add_info_col].unique()) > 9:
                if "No Info" in X.loc[:, self.add_info_col].unique():
                    clean_add_info = \
                        X.loc[:, self.add_info_col].apply(lambda x: "No info" if x == "No Info" else x)
                    self.add_info_status = True
                    logging.info(f"Incorrect value 'No Info' present: [{self.add_info_status}]")
                    logging.info("Additional info column cleaned successfully!")
                else:
                    raise Exception(
                        "Incorrect domain values found in Additional_Info column, Please confirm with schema.yaml"
                    )
                return clean_add_info
            else:
                logging.info(f"Incorrect value 'No Info' present: [{self.add_info_status}]")
                return X
        except Exception as e:
            raise FlightException(e, sys)

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        try:
            clean_add_info = self.clean_additional_info(X)
            clean_add_info_arr = np.array(clean_add_info).reshape(-1, 1)
            return clean_add_info_arr
        except Exception as e:
            raise FlightException(e, sys)


class CleanDurationCol(BaseEstimator, TransformerMixin):
    """This class performs data cleaning operations on the DURATION col"""

    def __init__(self):
        try:
            self.duration_col = COLUMN_DURATION
        except Exception as e:
            raise FlightException(e, sys)

    def convert_duration_to_minutes(self, X):
        try:
            logging.info("Converting duration column to minutes")
            clean_duration = \
                X.loc[:, self.duration_col].str.replace("h", '*60').str.replace(' ', '+').str.replace('m',  '*1').apply(eval)
            logging.info("Conversion of duration column to minutes successfully!")
            return clean_duration
        except Exception as e:
            raise FlightException(e, sys)

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        try:
            clean_dur = self.convert_duration_to_minutes(X)
            clean_dur_arr = np.array(clean_dur).reshape(-1, 1)
            return clean_dur_arr
        except Exception as e:
            raise FlightException(e, sys)


class DateTimeExtractor(BaseEstimator, TransformerMixin):
    """This class performs date extraction operations on:
    DATE_OF_JOURNEY,
    ARRIVAL_TIME,
    DEP_TIME cols"""

    def __init__(self):
        try:
            self.date_of_journey = COLUMN_DATE_OF_JOURNEY
            self.arrival_time = COLUMN_ARRIVAL_TIME
            self.dep_time = COLUMN_DEP_TIME
        except Exception as e:
            raise FlightException(e, sys)

    def extract_date_and_time(self, X):
        try:
            logging.info("Extracting date and time from cols: [date_of_journey, arrival_time and dep_time]")
            journey_day = X.loc[:, self.date_of_journey].str.split('/').str[0].astype(int)
            journey_month = X.loc[:, self.date_of_journey].str.split('/').str[1].astype(int)
            dep_hour = pd.to_datetime(X.loc[:, self.dep_time]).dt.hour
            dep_min = pd.to_datetime(X.loc[:, self.dep_time]).dt.minute
            arrival_hour = pd.to_datetime(X.loc[:, self.arrival_time]).dt.hour
            arrival_min = pd.to_datetime(X.loc[:, self.arrival_time]).dt.minute
            logging.info("Extraction completed successfully!")
            return np.c_[journey_day, journey_month, dep_hour, dep_min, arrival_hour, arrival_min]
        except Exception as e:
            raise FlightException(e, sys)

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        try:
            date_time_feats = self.extract_date_and_time(X)
            date_time_feats_arr = date_time_feats
            return date_time_feats_arr
        except Exception as e:
            raise FlightException(e, sys)


class DataTransformation:

    def __init__(self,
                 data_transformation_config: DataTransformationConfig,
                 data_ingestion_artifact: DataIngestionArtifact,
                 data_validation_artifact: DataValidationArtifact):
        try:
            self.data_transformation_config = data_transformation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_artifact = data_validation_artifact
        except Exception as e:
            raise FlightException(e, sys)

    def get_data_transformer_object(self) -> ColumnTransformer:
        try:
            schema_file_path = self.data_validation_artifact.schema_file_path
            schema_file = read_yaml(file_path=schema_file_path)

            categorical_columns = schema_file[SCHEMA_CLEAN_CATEGORICAL_COLUMNS_KEY]
            unclean_columns = schema_file[SCHEMA_UNCLEAN_COLUMNS_KEY]

            # preprocessing steps
            categorical_pipeline = Pipeline(steps=[
                ("imputer", SimpleImputer(strategy="most_frequent")),
                ("ordinal_enc", OrdinalEncoder()),
                ("scaler", StandardScaler(with_mean=False))
            ])

            clean_additional_info_col_pipeline = Pipeline(steps=[
                ("clean_add_info_col", CleanAddInfoCol()),
                ("impute", SimpleImputer(strategy="most_frequent")),
                ("ordinal_enc", OrdinalEncoder()),
                ("scaler", StandardScaler(with_mean=False))
            ])

            clean_duration_col_pipeline = Pipeline(steps=[
                ("clean_duration_col", CleanDurationCol()),
                ("impute", SimpleImputer(strategy="mean")),
                ("scaler", StandardScaler())
            ])

            numerical_col_pipeline = Pipeline(steps=[
                ("numerical_features", DateTimeExtractor()),
                ("impute", SimpleImputer(strategy="most_frequent")),
                ("scaler", StandardScaler())
            ])

            preprocessing = ColumnTransformer([
                ("cat_pipeline", categorical_pipeline, categorical_columns),
                ("clean_add_info_pipeline", clean_additional_info_col_pipeline, [unclean_columns[0]]),
                ("clean_dur_pipeline", clean_duration_col_pipeline, [unclean_columns[-1]]),
                ("numerical_col_pipeline", numerical_col_pipeline, unclean_columns[1:-1])
            ])
            return preprocessing

        except Exception as e:
            raise FlightException(e, sys)

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            logging.info("Obtaining preprocessing object")
            preprocessing_obj = self.get_data_transformer_object()

            logging.info("Obtaining train and test file path")
            train_file_path = self.data_ingestion_artifact.train_file_path
            validation_file_path = self.data_ingestion_artifact.validation_file_path

            schema_file_path = self.data_validation_artifact.schema_file_path

            logging.info("Loading training and validation data as a dataframe")
            train_df = pd.read_excel(train_file_path)
            validation_df = pd.read_excel(validation_file_path)
            schema_file = read_yaml(file_path=schema_file_path)

            target_column_name = schema_file[SCHEMA_TARGET_COLUMN_KEY]

            logging.info("Splitting input and target feature from training data")
            input_train_feature_df = train_df.drop(columns=[target_column_name], axis=1)
            target_feature_train_df = train_df[target_column_name]

            input_validation_feature_df = validation_df.drop(columns="Price", axis=1)
            target_feature_validation_df = validation_df[target_column_name]

            logging.info("Applying preprocessing object on training and validation dataframe")
            input_feature_train_arr = preprocessing_obj.fit_transform(
                input_train_feature_df
            )
            input_feature_validation_arr = preprocessing_obj.transform(
                input_validation_feature_df
            )

            train_arr = np.c_[input_feature_train_arr, target_feature_train_df]
            validation_arr = np.c_[input_feature_validation_arr, target_feature_validation_df]

            transformed_train_dir = \
                self.data_transformation_config.transformed_train_dir
            transformed_validation_dir = \
                self.data_transformation_config.transformed_validation_dir

            train_file_name = \
                os.path.basename(train_file_path).replace(".xlsx", ".npz")
            validation_file_name = \
                os.path.basename(validation_file_path).replace(".xlsx", ".npz")

            transformed_train_file_path = os.path.join(
                transformed_train_dir,
                train_file_name
            )

            transformed_validation_file_path = os.path.join(
                transformed_validation_dir,
                validation_file_name
            )

            logging.info("Saving transformed training and validation array")
            save_numpy_array_data(transformed_train_file_path, train_arr)
            save_numpy_array_data(transformed_validation_file_path, validation_arr)

            preprocessing_obj_file_path = \
                self.data_transformation_config.preprocessed_object_file_path

            logging.info("Saving preprocessing object.")
            save_object(file_path=preprocessing_obj_file_path,
                        obj=preprocessing_obj)

            data_transformation_artifact = DataTransformationArtifact(
                transformed_train_file_path=transformed_train_file_path,
                transformed_validation_file_path=transformed_validation_file_path,
                message="Data Transformation successful!",
                is_transformed=True,
                preprocessed_object_file_path=preprocessing_obj_file_path
            )

            logging.info(f"Data transformation artifact: [{data_transformation_artifact}]")
            return data_transformation_artifact
        except Exception as e:
            raise FlightException(e, sys)

    def __del__(self):
        logging.info(f"{'>>'*20}Data Transformation log completed.{'<<'*20} \n\n")


# code testing
# def get_data_transformer_object():
#     # schema_file_path = self.data_validation_artifact.schema_file_path
#     # schema_file = read_yaml(file_path=schema_file_path)
#
#     # categorical_columns = schema_file[SCHEMA_CLEAN_CATEGORICAL_COLUMNS_KEY]
#     # unclean_columns = schema_file[SCHEMA_UNCLEAN_COLUMNS_KEY]
#
#     cat_columns = ["Airline", "Source", "Destination", "Total_Stops"]
#     unclean_columns = ["Additional_Info", "Date_of_Journey", "Arrival_Time", "Dep_Time", "Duration"]
#
#
#     cat_columns = ["Airline", "Source", "Destination", "Total_Stops"]
#     cat_columns1 = ["Additional_Info"]
#     num_column1 = ["Duration"]
#     num_columns = ["Date_of_Journey", "Arrival_Time", "Dep_Time"]
#
#     # preprocessing steps
#     categorical_pipeline = Pipeline(steps=[
#         ("imputer", SimpleImputer(strategy="most_frequent")),
#         ("ordinal_enc", OrdinalEncoder()),
#         ("scaler", StandardScaler(with_mean=False))
#     ])
#
#     clean_additional_info_col_pipeline = Pipeline(steps=[
#         ("clean_add_info_col", CleanAddInfoCol()),
#         ("impute", SimpleImputer(strategy="most_frequent")),
#         ("ordinal_enc", OrdinalEncoder()),
#         ("scaler", StandardScaler(with_mean=False))
#     ])
#
#     clean_duration_col_pipeline = Pipeline(steps=[
#         ("clean_duration_col", CleanDurationCol()),
#         ("impute", SimpleImputer(strategy="mean")),
#         ("scaler", StandardScaler())
#     ])
#
#     numerical_col_pipeline = Pipeline(steps=[
#         ("numerical_features", DateTimeExtractor()),
#         ("impute", SimpleImputer(strategy="most_frequent")),
#         ("scaler", StandardScaler())
#     ])
#
#     preprocessing = ColumnTransformer([
#         ("cat_pipeline", categorical_pipeline, cat_columns),
#         ("clean_add_info_pipeline", clean_additional_info_col_pipeline, [unclean_columns[0]]),
#         ("clean_dur_pipeline", clean_duration_col_pipeline, [unclean_columns[-1]]),
#         ("numerical_col_pipeline", numerical_col_pipeline, unclean_columns[1:-1])
#     ])
#     return preprocessing

# preprocessing_obj = get_data_transformer_object()
#
# df = pd.read_excel("/home/mobo/Documents/Ineuron/Live_Class/ML/PracticeML/ml_practice/flight/artifact/data_ingestion/2022-07-18 12:46:56/ingested_data/train/Data_Train.xlsx")
# X = df.drop("Price", axis=1)
# y = df["Price"]
#
# new_x = preprocessing_obj.fit_transform(X)
# print(new_x)

# class DataTransformation(DataCleaning):
#     def __init__(self,
#                  data_transformation_config: DataTransformationConfig,
#                  **kwargs):
#         try:
#             logging.info(f"{'>>' * 30} Data Transformation log started. {'<<' * 30}")
#
#             DataCleaning.__init__(self, **kwargs)
#             self.data_transformation_config = data_transformation_config
#
#         except Exception as e:
#             raise FlightException(e, sys)
#
#     def get_data_transformer_object(self) -> ColumnTransformer:
#         try:
#             dataset_schema = read_yaml(file_path=self.schema_file_path)
#
#             columns = [COLUMN_DATE_OF_JOURNEY, COLUMN_DEP_TIME, COLUMN_ARRIVAL_TIME]
#
#             categorical_columns = dataset_schema[SCHEMA_CATEGORICAL_COLUMNS_KEY]
#             cat_pipeline = Pipeline(steps=[
#                 ("impute", SimpleImputer(strategy="most_frequent")),
#                 ("label_encoder", LabelEncoder()),
#                 ("scaler", StandardScaler())
#             ])
#
#             numerical_columns = [COLUMN_JOURNEY_DAY,
#                                  COLUMN_JOURNEY_MONTH,
#                                  COLUMN_DEP_HOUR,
#                                  COLUMN_DEP_MIN,
#                                  COLUMN_ARRIVAL_HOUR,
#                                  COLUMN_ARRIVAL_MIN,
#                                  COLUMN_DURATION]
#
#             num_pipeline = Pipeline(steps=[
#                 ("imputer", SimpleImputer(strategy="median")),
#                 ("feature_generator", FeatureGenerator(
#                     generate_clean_date_cols=self.data_transformation_config.generate_clean_date_cols,
#                     columns=columns
#                 )),
#                 ("scaler", StandardScaler())
#             ])
#
#             logging.info(f"Categorical columns: [{categorical_columns}]")
#             logging.info(f"Numerical feature generated columns: [{numerical_columns}]")
#
#             preprocessing = ColumnTransformer([
#                 ("cat_pipeline", cat_pipeline, categorical_columns),
#                 ("num_pipeline", num_pipeline, numerical_columns)
#             ])
#             return preprocessing
#         except Exception as e:
#             raise FlightException(e, sys)
#
#     def initiate_data_transformation(self) -> DataTransformationArtifact:
#         try:
#             self.initiate_data_cleaning()
#
#             logging.info(f"Obtaining preprocessing object.")
#             preprocessing_obj = self.get_data_transformer_object()
#             schema_file = read_yaml(file_path=self.schema_file_path)
#
#             target_column_name = schema_file[SCHEMA_TARGET_COLUMN_KEY]
#
#             logging.info("Extracting independent and dependent features from training and testing dataframe")
#             input_feature_train_df = self.train_df.drop(columns=schema_file[SCHEMA_DROP_COLUMNS_KEY], axis=1)
#             target_feature_train_df = self.train_df[target_column_name]
#
#             input_feature_test_df = self.test_df.drop(columns=schema_file[SCHEMA_DROP_COLUMNS_KEY][:-1], axis=1)
#
#             logging.info("Applying preprocessing object on training and testing dataframe")
#             input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
#             input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)
#
#             train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
#             test_arr = input_feature_test_arr
#
#             transformed_train_dir = self.data_transformation_config.transformed_train_dir
#             transformed_test_dir = self.data_transformation_config.transformed_test_dir
#             train_file_path = self.data_ingestion_artifact.train_file_path
#             test_file_path = self.data_ingestion_artifact.test_file_path
#
#             train_file_name = os.path.basename(train_file_path)
#             test_file_name = os.path.basename(test_file_path)
#
#             transformed_train_file_path = os.path.join(transformed_train_dir, train_file_name)
#             transformed_test_file_path = os.path.join(transformed_test_dir, test_file_name)
#
#             # logging.info("Saving transformed training and testing array.")
#
#             preprocessing_obj_file_path = self.data_transformation_config.preprocessed_object_file_path
#             logging.info("Saving preprocessing object.")
#             save_object(file_path=preprocessing_obj_file_path, obj=preprocessing_obj)
#
#             data_transformation_artifact = DataTransformationArtifact(is_transformed=True,
#                                                                       message="Data transformation successful.",
#                                                                       transformed_train_file_path=transformed_train_file_path,
#                                                                       transformed_test_file_path=transformed_test_file_path,
#                                                                       preprocessed_object_file_path=preprocessing_obj_file_path)
#             logging.info(f"Data transformation artifact: {data_transformation_artifact}")
#
#         except Exception as e:
#             raise FlightException(e, sys)
#
#     def __del__(self):
#         logging.info(f"{'>>'*30}Data Transformation log completed.{'<<'*30} \n\n")
