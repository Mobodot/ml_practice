from zipfile import ZipFile
import requests
from six.moves import urllib

import opendatasets as od

import os




# def download_data() -> str:
#     urlpath = "https://www.kaggle.com/datasets/nikhilmittal/flight-fare-prediction-mh/download/"
#     r = requests.get(urlpath)
#     filename = "download.zip"
#     with open(filename, "wb") as output_file:
#         output_file.write(r.content)
#     print(r.status_code)
#     return "file downloaded"

# def download_data() -> str:
#     urlpath = "https://www.kaggle.com/datasets/nikhilmittal/flight-fare-prediction-mh/download"
#     wget.download(urlpath)
#     filename = wget.filename_from_url(url=urlpath)
#     return filename

# def download_data() -> str:
#     urlpath = "https://www.kaggle.com/datasets/nikhilmittal/flight-fare-prediction-mh/download"
#     od.download(urlpath, os.getcwd()+"/flight")
#     print("done")


# print(download_data())

# print(os.getcwd())

print("Hello friends my name is \n"
      "sam and i am going home")

# import pandas as pd
#
# new_val = pd.read_excel('/home/mobo/Documents/Ineuron/Live_Class/ML/PracticeML/ml_practice/flight/artifact/data_ingestion/2022-07-14 11:22:16/ingested_data/test/Test_set.xlsx')
# print(new_val.shape)

from flask import Flask, request

app = Flask(__name__)


LOG_FOLDER_NAME = "logged"

# @app.route(f"/logs", defaults={"req_path": f"{LOG_FOLDER_NAME}"})
# @app.route(f"/{LOG_FOLDER_NAME}/<path:req_path>")
# def render_log_dir(req_path):
#     if request.method == "GET":
#         # print(request.method)
#         print(type(request.path))
#         return "hello worldSS",  request.path

@app.route("/logs", defaults={"req_path": "bullshit"})
@app.route("/logs/<path:req_path>")
def trial(req_path):
    # os.makedirs("delme", exist_ok=True)
    print(req_path)
    print("hello fools")
    abs_path = os.path.join(req_path)
    print(abs_path)

    return "hello friends", request.path

crap = {'file': {'logs/log_2022-08-01-11-23-38.log': 'log_2022-08-01-11-23-38.log', 'logs/log_2022-08-01-11-26-29.log': 'log_2022-08-01-11-26-29.log', 'logs/log_2022-08-01-11-24-50.log': 'log_2022-08-01-11-24-50.log', 'logs/log_2022-08-01-11-24-18.log': 'log_2022-08-01-11-24-18.log', 'logs/log_2022-08-01-11-09-01.log': 'log_2022-08-01-11-09-01.log', 'logs/log_2022-08-01-11-46-31.log': 'log_2022-08-01-11-46-31.log', 'logs/log_2022-08-01-11-22-25.log': 'log_2022-08-01-11-22-25.log', 'logs/log_2022-08-01-11-24-51.log': 'log_2022-08-01-11-24-51.log', 'logs/log_2022-08-01-11-08-39.log': 'log_2022-08-01-11-08-39.log', 'logs/log_2022-08-01-11-46-33.log': 'log_2022-08-01-11-46-33.log', 'logs/log_2022-08-01-11-24-19.log': 'log_2022-08-01-11-24-19.log', 'logs/log_2022-08-01-11-23-40.log': 'log_2022-08-01-11-23-40.log', 'logs/log_2022-07-29-23-25-33.log': 'log_2022-07-29-23-25-33.log', 'logs/log_2022-07-29-23-25-43.log': 'log_2022-07-29-23-25-43.log'}, 'parent_folder': '', 'parent_label': 'logs'}
# print("logs" in crap)

# print(crap.items())
# for href, labels in crap.items():
#     print(href, labels)

# if __name__ == "__main__":
#     app.run(port=5001)

val = {
    "Airline": ["Jet Airways Business"],
    "Date_of_Journey": "24/03/2019",
    "Source": ["Banglore"],
    "Destination": ["Banglore"],
    # "route": "BLR -> DEL",
    "Arrival_Time": ["15:00"],
    "Dep_Time": ["09:25"],
    "Duration": ["2h 40m"],
    "Total_Stops": ["non-stop"],
    "Additional_Info": ["Business class"],
}

path = "/home/mobo/Documents/Ineuron/Live_Class/ML/PracticeML/ml_practice/saved_models/20220801125501/model.pkl"
path1 = "/home/mobo/Documents/Ineuron/Live_Class/ML/PracticeML/ml_practice/flight/artifact/data_ingestion/2022-08-01 12:53:51/ingested_data/test/Test_set.xlsx"

import pickle
import pandas as pd
from collections import namedtuple

new_val = pd.read_excel(path1)
print(new_val.Airline.unique())

with open(path, 'rb') as file_path:
    model = pickle.load(file_path)
# print(model.__dict__)

val_df = pd.DataFrame(val)
print(val_df)

# print([list(val.values())])
#
result = model.predict(val_df)
print(result)