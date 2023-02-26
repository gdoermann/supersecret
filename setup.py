"""
SuperSecrets
A Python project for parsing and caching secrets from AWS Secrets Manager.
"""
import os
from setuptools import setup, find_packages


# Allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

with open(os.path.join(os.path.dirname(__file__), "README.md")) as readme:
    README = readme.read()

original_dir = os.getcwd()
os.chdir(os.path.join(os.path.dirname(__file__), "src"))

version = __import__("supersecret").__version__

os.chdir(original_dir)
# Parse Requirements
with open("requirements.txt") as f:
    required = f.read().splitlines()


setup(
    name='supersecret',
    version=version,
    description='A Python project for parsing and caching secrets from AWS Secrets Manager',
    long_description=README,
    author='Greg Doermann',
    author_email='greg@doermann.me',
    packages=find_packages('src/supersecret'),
    test_suite='tests',
    install_requires=required,
)
