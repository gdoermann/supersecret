Super Secret Library
====================

This is a library that does super secret things.  

AWS Secrets Manager is an amazing service that allows you to store secrets in a secure way.  
This package will allow you to load the secrets from AWS Secrets Manager.

# Features
* Parse secrets from AWS Secrets Manager
* Lazy connection to AWS
* Default to environment variables if secret key is not found (everything is optional!)
* Environment variable overrides
* Type casting (int, float, bool, list, dict, str)
* Framework-agnostic, but integrates well with [Flask](https://flask.palletsprojects.com/en/1.1.x/) and [Django](https://www.djangoproject.com/)


# Installation

```bash
pip install supersecret
```

You must have AWS credentials configured either through environment variables or through a credentials file.
This library uses boto3 to connect to AWS, so you can read more about that [here](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html).

# Basic Usage

After setting up some environment variables:
```bash
####################################
# AWS Settings
####################################
# AWS Secret Manager Secret Name
export SECRET_NAME=Dev_Secret

```

Now you can use the library to parse the secret values:

```python
from supersecret.manager import SecretManager
from supersecret import fields

secret_manager = SecretManager("SECRET_NAME", region_name="us-east-1") # `region` is optional

# If you want to force the secret manager to connect to AWS and parse the secret
secret_manager.load()

# If not, when called, secret manager will connect to AWS and parse the secret
secret_key = secret_manager.str("SECRET_KEY")

# You can also type cast the value
max_connections = secret_manager.int("max_connections", default=100)
default_charge = secret_manager.float("default_charge")
some_decimal = secret_manager.decimal("some_decimal")
debug = secret_manager.bool("debug")

allowed_hosts = secret_manager.list("allowed_hosts", delimiter=",", subcast=fields.Str)
admins = secret_manager.choices("admins")

datetime_modified = secret_manager.datetime("datetime_modified", format="%Y-%m-%d %H:%M:%S")
created_date = secret_manager.date("created_date", format="%Y-%m-%d")

default_start_time = secret_manager.time("default_start_time", format="%H:%M:%S")
default_end_time = secret_manager.time("default_end_time", format="%H:%M:%S")

min_time_between_calls = secret_manager.timedelta("time_between_calls")
max_time_between_calls = secret_manager.timedelta_seconds("max_time_between_calls") # parse from seconds

service_uuid = secret_manager.uuid("service_id", version=1)
log_level = secret_manager.log_level("log_level")

media_path = secret_manager.path("media_path") # Parses to pathlib.Path object

# Parsing a dictionary is a little different. Keys must all start with the same prefix.
# The prefix is removed from the key when parsing the dictionary and the `dict` method returns
# an AttrDict object.  Prefix should be formatted as follows: "PREFIX__KEY"

database_settings = secret_manager.dict("database_settings", subcast_keys=fields.Str, subcast_values=fields.Int)

```

If a value does not exist in the secret file, we will check the environment variables for a value.
If no value is found, you can specify a default value to return. 
If no default value is specified, we will raise a `KeyError`.


# Supported Types
* `str`: String - This is the default type
* `int`: Integer
* `float`: Float
* `decimal`: decimal.Decimal
* `bool`: Boolean
* `list`: List - You can specify a `delimiter` and a `subcast` type for list elements
* `choices`: List[tuple] - You can specify a `delimiter` and a `subcast` type for list elements. Returns the form: [(key, value), (key, value)]
* `datetime`: datetime.datetime - You can specify a `format` for the datetime string
* `date`: datetime.date - You can specify a `format` for the date string
* `time`: datetime.time - You can specify a `format` for the time string
* `timedelta`: datetime.timedelta - Format must be in the form: "HH:MM:SS"
* `timedelta_seconds`: datetime.timedelta - Parses from seconds
* `uuid`: uuid.UUID - You can specify a `version` for the UUID. 1=Time-based, 3=Name-based, 4=Random, 5=Name-based
* `log_level`: int - Parses a log level string to an int
* `path`: pathlib.Path - Parses a string to a pathlib.Path object
* `dict`: AttrDict - You can specify a `prefix` for the dictionary keys, a `subcast_keys` type, and a `subcast_values` type


# Advanced Usage
## Multiple Secret Merging
You can merge multiple secrets into a single secret manager.  
This is useful if you have multiple secrets you want to read from AWS manager and merge the values into a single object.
An example of this is if you have a `default` secret that has all the standard settings and then a `service` secret that has
service specific settings that may override the default settings.

```python
from supersecret.manager import SecretManager

secret_manager = SecretManager(
    default_secret_name="my_default_secret",
    region_name="us-east-1"
)

secret_manager.load("second_secret") # Loads with the same profile and region as the default secret

# You can also connect to a completely different aws environment
from botocore.config import Config
import boto3

my_config = Config(
    region_name = 'us-west-2',
    signature_version = 'v4',
    retries = {
        'max_attempts': 10,
        'mode': 'standard'
    }
)

new_client = boto3.client('secretsmanager', config=my_config)

secret_manager.load("service", client=new_client) # Loads from a completely different AWS environment/config

```

When you `load` a new secret, it will override any values in the existing secret. 
The multi secret manager behaves like a single secret manager, so you can use the same methods to parse values.



# Dependencies
This package requires the following libraries:
* [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) library to connect to AWS.
* [requests](https://requests.readthedocs.io/en/master/) library to make HTTP requests.
* [marshmallow](https://marshmallow.readthedocs.io/en/stable/) library to type cast values.


