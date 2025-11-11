import sys
import os

# caetra imports
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from caetra_exceptions import ConfigurationError

def validate_dict_structure(expected_structure, data, structure_name):
    for key, value in expected_structure.items():
        msgerr = f"Missing key: '{key}' on configuration: '{structure_name}'"
        if key not in data:
            raise ConfigurationError(msgerr)
        if isinstance(value, dict):
            if not isinstance(data[key], dict):
                raise ConfigurationError(msgerr)
            if not validate_dict_structure(data[key]):
                raise ConfigurationError(msgerr)
        else:
            if not isinstance(data[key], value):
                raise ConfigurationError(msgerr)


