import sys

from flight.logger import logging
from flight.pipeline.pipeline import Pipeline
from flight.exception import FlightException


def main():
    try:
        pipeline = Pipeline()
        pipeline.run_pipeline()
    except Exception as e:
        logging.error(f"{e}")
        raise FlightException(e, sys)


if __name__ == "__main__":
    main()