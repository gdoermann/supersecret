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
    url='https://github.com/gdoermann/supersecret',
    long_description=README,
    long_description_content_type='text/markdown',
    author='Greg Doermann',
    author_email='greg@doermann.me',
    packages=find_packages('src/supersecret'),
    test_suite='tests',
    install_requires=required,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Security :: Cryptography',
        'Topic :: Utilities',
    ],
    project_urls={
        'source': 'https://github.com/gdoermann/supersecret',
    }
)
