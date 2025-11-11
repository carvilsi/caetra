def validate_dict_structure(expected_structure, data):
    for key, value in expected_structure.items():
        if key not in data:
            return False
        if isinstance(value, dict):
            if not isinstance(data[key], dict):
                return False
            if not validate_dict_structure(data[key]):
                return False
        else:
            if not isinstance(data[key], value):
                return False

    return True

