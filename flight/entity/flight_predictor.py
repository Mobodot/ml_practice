import os
import sys

import pandas as pd
from flight.exception import FlightException
from flight.utils.utils import load_object


class FlightData:

    def __init__(self,
                 airline: str,
                 date_of_journey: str,
                 source: str,
                 destination: str,
                 duration: str,
                 total_stops: str,
                 additional_info: str,
                 arrival_time: str,
                 dep_time: str):
        try:
            self.airline = airline
            self.date_of_journey = date_of_journey
            self.source = source
            self.destination = destination
            self.duration = duration
            self.total_stops = total_stops
            self.additional_info = additional_info
            self.arrival_time = arrival_time
            self.dep_time = dep_time
        except Exception as e:
            raise FlightException(e, sys)

    def get_flight_input_data_frame(self):
        try:
            flight_input_dict = self.get_flight_data_as_dict()
            return pd.DataFrame(flight_input_dict)
        except Exception as e:
            raise FlightException(e, sys)

    def get_flight_data_as_dict(self):
        try:
            input_data = {
                "Airline": [self.airline],
                "Date_of_Journey": [self.date_of_journey],
                "Source": [self.source],
                "Destination": [self.destination],
                "Duration": [self.duration],
                "Total_Stops": [self.total_stops],
                "Additional_Info": [self.additional_info],
                "Arrival_Time": [self.arrival_time],
                "Dep_Time": [self.dep_time],
            }
            return input_data
        except Exception as e:
            raise FlightException(e, sys)


class FlightPredictor:

    def __init__(self, model_dir):
        try:
            self.model_dir = model_dir
        except Exception as e:
            raise FlightException(e, sys)

    def get_latest_model_path(self):
        try:
            folder_name = list(map(int, os.listdir(self.model_dir)))
            latest_model_dir = os.path.join(self.model_dir, f"{max(folder_name)}")
            file_name = os.listdir(latest_model_dir)[0]
            latest_model_path = os.path.join(latest_model_dir, file_name)
            return latest_model_path
        except Exception as e:
            raise FlightException(e, sys)

    def predict(self, X):
        try:
            model_path = self.get_latest_model_path()
            model = load_object(file_path=model_path)
            price = model.predict(X)
            return price
        except Exception as e:
            raise FlightException(e, sys)