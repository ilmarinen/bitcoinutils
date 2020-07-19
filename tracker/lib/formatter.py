def make(data_object, data_format):
    result = {}
    for key, val in data_format.items():
        if isinstance(val, str):
            result[key] = getattr(data_object, val)
        else:
            result[key] = val(data_object)

    return result
