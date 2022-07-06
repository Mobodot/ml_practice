import yaml
import sys
# from flight.exception import FlightException
from flight.exception import FlightException



def read_yaml(file_path: str) -> dict:
    """This function reads a yaml file and returns a dict"""
    try:
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise FlightException(e, sys) from e

# print(read_yaml("config/config.yaml"))

# import os
# print(os.getcwd())
# print(os.path.basename(os.getcwd()))