import os

import yaml
import sys
import pickle
import numpy as np
from flight.exception import FlightException



def read_yaml(file_path: str) -> dict:
    """This function reads a yaml file and returns a dict"""
    try:
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise FlightException(e, sys) from e

def save_object(file_path: str, obj):
    """train_data
    :param file_path: str
    :param obj: Save any sort of object
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)
    except Exception as e:
        raise FlightException(e, sys)

def load_object(file_path: str) -> object:
    """
    :param file_path: str
    :return: object
    """
    try:
        with open(file_path, "rb") as file_obj:
            return pickle.load(file_obj)
    except Exception as e:
        raise FlightException(e, sys)

def save_numpy_array_data(file_path:str, array: np.array) -> None:
    """
    Save numpy array data to file
    :param file_path: str location of file to save
    :param array: np.array to save
    :return:
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise FlightException(e, sys)

def load_numpy_array_data(file_path:str) -> np.array:
    """
    Load numpy array data from file
    :param file_path: str location of file to load
    :return: np.array data loaded
    """
    try:
        with open(file_path, "rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise FlightException(e, sys)
# print(read_yaml("config/config.yaml"))

# import os
# print(os.getcwd())
# print(os.path.basename(os.getcwd()))