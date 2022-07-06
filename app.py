import sys
from flask import Flask
from flight.logger import logging
from flight.exception import FlightException

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    try:
        12/0
        # raise Exception("this should not work")
        return "this is the index page"
    except Exception as e:
        housing = FlightException(e, sys)
        logging.error(housing.error_message)
        # logging.info(HousingException(e, sys))


if __name__ == "__main__":
    app.run(debug=True)