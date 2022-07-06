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

def download_data() -> str:
    urlpath = "https://www.kaggle.com/datasets/nikhilmittal/flight-fare-prediction-mh/download"
    od.download(urlpath, os.getcwd()+"/flight")
    print("done")


# print(download_data())

# print(os.getcwd())