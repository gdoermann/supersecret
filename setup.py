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

version = open(os.path.join(os.path.dirname(__file__), 'src', 'supersecret', 'VERSION.txt')).read().strip()

# Parse Requirements
with open("requirements.txt") as f:
    required = f.read().splitlines()


setup(
    name='supersecret',
    version=version,
    description='A Python project for parsing and caching secrets from AWS Secrets Manager',
    long_description=README,
    long_description_content_type='text/markdown',
    author='Greg Doermann',
    author_email='greg@doermann.me',
    packages=find_packages('src/supersecret'),
    test_suite='tests',
    install_requires=required,
)
