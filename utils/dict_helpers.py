def flatten(d):
    out = {}
    if d is None:
        return out
    for key, value in d.items():
        if isinstance(value, dict):
            value = [value]
        if isinstance(value, list):
            index = 0
            for subdict in value:
                index = int(index) + 1
                deeper = flatten(subdict).items()
                out.update({
                    key + ' <b>(' + str(index) + '/' + str(len(value)) + ')</b>.' + key2: value2 for key2, value2 in deeper
                })
        else:
            out[key] = value
    return out