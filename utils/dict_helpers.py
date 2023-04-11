def flatten(d, number_list_items=True):
    # Credit: https://stackoverflow.com/a/52081812/10640126
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
                deeper = flatten(subdict, number_list_items=number_list_items).items()
                if number_list_items == False:
                    out.update({
                        key + '.' + key2: val2 for key2, val2 in deeper
                    })
                else:
                    out.update({
                        key + ' <b>(' + str(index) + '/' + str(len(value)) + ')</b>.' + key2: value2 for key2, value2 in deeper
                    })
        else:
            out[key] = value
    return out