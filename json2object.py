def json_2_object(data):
    curr_obj = None

    if isinstance(data, dict):
        curr_obj = type('J2O', (), {})

        for k, v in data.items():
            if isinstance(v, dict):
                setattr(curr_obj, k, json_2_object(v))

            elif isinstance(v, list):
                setattr(curr_obj, k, [])
                lst = getattr(curr_obj, k)
                lst += json_2_object(v)

            else:
                setattr(curr_obj, k, v)

    if isinstance(data, list):
        curr_obj = []
        for item in data:
            if type(item) in (dict, list):
                curr_obj.append(json_2_object(item))

            else:
                curr_obj.append(item)

    return curr_obj
