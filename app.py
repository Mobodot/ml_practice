import json
import os.path
import sys

from flight.exception import FlightException
from flight.pipeline.pipeline import Pipeline
from flight.logger import logging, get_log_dataframe
from flight.config.configuration import Configuration
from flight.utils.utils import write_yaml, read_yaml
from flight.constant import get_current_time_stamp, CONFIG_DIR
from flight.entity.flight_predictor import FlightData, FlightPredictor
from flask import Flask, render_template, abort, send_file, request


app = Flask(__name__)


ROOT_DIR = os.getcwd()
PIPELINE_FOLDER_NAME = "flight"
LOG_FOLDER_NAME = "logs"
SAVED_MODELS_DIR_NAME = "saved_models"
MODEL_CONFIG_FILE_PATH = os.path.join(ROOT_DIR, CONFIG_DIR, "model.yaml")
LOG_DIR = os.path.join(ROOT_DIR, LOG_FOLDER_NAME)
PIPELINE_DIR = os.path.join(ROOT_DIR, PIPELINE_FOLDER_NAME)
MODEL_DIR = os.path.join(ROOT_DIR, SAVED_MODELS_DIR_NAME)

PRICE_KEY = "Price"
FLIGHT_DATA_KEY = "flight_data"

@app.route("/artifact", defaults={"req_path": "flight"})
@app.route("/artifact/<path:req_path>")
def render_artifact_dir(req_path):
    os.makedirs("flight", exist_ok=True)
    # Joining the base and the requested path
    print(f"req_path: {req_path}")
    abs_path = os.path.join(req_path)
    print(f"abs_path: {abs_path}")
    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        if ".html" in abs_path:
            with open(abs_path, "r", encoding="utf-8") as file:
                content = ""
                for line in file.readlines():
                    content = f"{content}{line}"
                return content
        return send_file(abs_path)

    # Show directory contents
    files = {os.path.join(abs_path, file_name): file_name for file_name in os.listdir(abs_path) if
             "artifact" in os.path.join(abs_path, file_name)}

    result = {
        "files": files,
        "parent_folder": os.path.dirname(abs_path),
        "parent_label": abs_path
    }
    return render_template("files.html", result=result)

@app.route("/", methods=["GET", "POST"])
def index():
    try:
        return render_template("index.html")
    except Exception as e:
        return str(e)

@app.route("/view_experiment_hist", methods=["GET", "POST"])
def view_experiment_history():
    experiment_df = Pipeline.get_experiment_status()
    context = {
        "experiment": experiment_df.to_html(classes="table table-striped col-12")
    }
    return render_template("experiment_history.html", context=context)

@app.route("/train", methods=["GET", "POST"])
def train():
    message = ""
    pipeline = Pipeline(
        config=Configuration(current_time_stamp=get_current_time_stamp())
    )
    if not pipeline.experiment.running_status:
        message = "Training started."
        pipeline.start()
    else:
        message = "Training is already in progress."
    context = {
        "experiment": pipeline.get_experiment_status().to_html(classes="table table-striped col-12"),
        "message": message
    }
    return render_template("train.html", context=context)

@app.route("/predict", methods=["GET", "POST"])
def predict():
    context = {
        FLIGHT_DATA_KEY: None,
        PRICE_KEY: None
    }
    if request.method == "POST":
        airline = request.form["airline"]
        date_of_journey = request.form["date_of_journey"]
        source = request.form["source"]
        destination = request.form["destination"]
        duration = request.form["duration"]
        total_stops = request.form["total_stops"]
        additional_info = request.form["additional_info"]
        arrival_time = request.form["arrival_time"]
        dep_time = request.form["dep_time"]

        # print(request.values)
        flight_data = FlightData(airline=airline,
                                 date_of_journey=date_of_journey,
                                 source=source,
                                 destination=destination,
                                 duration=duration,
                                 additional_info=additional_info,
                                 total_stops=total_stops,
                                 arrival_time=arrival_time,
                                 dep_time=dep_time)
        flight_df = flight_data.get_flight_input_data_frame()
        flight_predictor = FlightPredictor(model_dir=MODEL_DIR)
        price = flight_predictor.predict(X=flight_df)
        context = {
            FLIGHT_DATA_KEY: flight_data.get_flight_data_as_dict(),
            PRICE_KEY: price
        }
        print(f"context: {context}")
        return render_template("predict.html", context=context)
    return render_template("predict.html", context=context)

@app.route("/saved_models", defaults={"req_path": "saved_models"})
@app.route("/saved_models/<path:req_path>")
def saved_models_dir(req_path):
    os.makedirs("saved_models", exist_ok=True)
    # Joining the base and the requested path
    print(f"req_path: {req_path}")
    abs_path = os.path.join(req_path)
    print(abs_path)
    # return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        return send_file(abs_path)

    # show directory contents
    files = {os.path.join(abs_path, file): file  for file in os.listdir(abs_path)}

    result = {
        "files": files,
        "parent_folder": os.path.dirname(abs_path),
        "parent_label": abs_path
    }
    return render_template("saved_models_files.html", result=result)

@app.route("/update_model_config", methods=["GET", "POST"])
def update_model_config():
    try:
        if request.method == "POST":
            model_config = request.form["new_model_config"]
            model_config = model_config.replace("'", '"')
            print(model_config)
            model_config = json.loads(model_config)

            write_yaml(file_path=MODEL_CONFIG_FILE_PATH,
                       data=model_config)

        model_config = read_yaml(file_path=MODEL_CONFIG_FILE_PATH)
        return render_template("update_model.html",
                               result={"model_config": model_config})
    except Exception as e:
        logging.exception(e)
        return str(e)

@app.route(f"/logs", defaults={"req_path": f"{LOG_FOLDER_NAME}"})
@app.route(f"/{LOG_FOLDER_NAME}/<path:req_path>")
def render_log_dir(req_path):
    os.makedirs(LOG_FOLDER_NAME, exist_ok=True)
    # Joining the base and the request path
    logging.info(f"req_path: {req_path}")
    abs_path = os.path.join(req_path)
    print(abs_path)
    # Return 404 if path doesn't exist
    if not os.path.exists((abs_path)):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        log_df = get_log_dataframe(abs_path)
        context = {"log": log_df.to_html(classes="table-striped", index=False)}
        return render_template("log.html", context=context)

    # Show directory contents
    files = {os.path.join(abs_path, file): file for file in os.listdir(abs_path)}

    result = {
        "files": files,
        "parent_folder": os.path.dirname(abs_path),
        "parent_label": abs_path
    }
    print(result)
    return render_template("log_files.html", result=result)

if __name__ == "__main__":
    app.run()