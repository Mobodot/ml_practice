import os
import sys

from flight.logger import logging
from flight.pipeline.pipeline import Pipeline
from flight.exception import FlightException
from flight.config.configuration import Configuration


def main():
    try:
        config_path = os.path.join("config", "config.yaml")
        # pipeline = Pipeline()
        # pipeline.run_pipeline()
        pipeline = Pipeline(Configuration(config_file_path=config_path))
        pipeline.start()
        logging.info("main function execution completed.")
    except Exception as e:
        logging.error(f"{e}")
        raise FlightException(e, sys)


if __name__ == "__main__":
    main()