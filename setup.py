from distutils.core import setup
from setuptools import find_packages

setup(
    # Application name:
    name="yousirs",

    # Version number (initial):
    version="1.0",

    # Application author details:
    author="Joel Preas",
    author_email="JoelPreas@gmail.com",

    # Packages
    packages=find_packages(),

    # Include additional files into the package
    include_package_data=True,

    # Details
    url="https://github.com/JoelInTheory/random_coding_thangs"
)

