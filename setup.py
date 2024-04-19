import os
from setuptools import find_packages, setup

DIR = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(DIR, "VERSION"), "r") as file:
    VERSION = file.read()

with open(os.path.join(DIR, "README.md"), "r") as file:
    LONG_DESCRIPTION = file.read()

long_description = LONG_DESCRIPTION,

setup(
    name='cshd',
    packages=find_packages(),
    include_package_data=True,
    version = VERSION,
    description='Crop Sowing and Harvesting Detection Service based on Phenolopy and Digital Earth Australia.',
    author='Gabriel Sansigolo',
    author_email = "gabrielsansigolo@gmail.com",
    url = "https://github.com/GSansigolo/cshd",
    install_requires= [
        "dask==2024.4.1",
        "statsmodels==0.14.2",
        "datacube==1.8.18",
        "rioxarray==0.15.4",
        "xarray==2024.3.0"
    ],
    long_description = LONG_DESCRIPTION,
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)
