from setuptools import setup, find_packages
from typing import List, Type

# declaring variables for setup function
PROJECT_NAME = "flight"
VERSION = "0.0.1"
AUTHOR = "MOBO"
PACKAGE_NAME = "flight"
DESCRIPTION = "This is the flight price project integrated with CI/CD pipeline"


def get_requirements_list() -> List:
    """
    This function removes "-e ." from requirements.txt file
    :return: A list of libraries contained in requirements.txt
    """
    with open("requirements.txt") as requirements_file:
        return requirements_file.readlines().remove("-e .")


setup(
    name=PROJECT_NAME,
    version=VERSION,
    author=AUTHOR,
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=get_requirements_list()
)