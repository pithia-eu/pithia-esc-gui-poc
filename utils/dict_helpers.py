# Credit: https://stackoverflow.com/a/52081812/10640126.
# Minor modifications made to original linked code.
def flatten(d, number_list_items=True):
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
                        key + '.' + key_deeper: val_deeper for key_deeper, val_deeper in deeper
                    })
                else:
                    out.update({
                        key + ' (' + str(index) + '/' + str(len(value)) + ').' + key_deeper: value2 for key_deeper, value2 in deeper
                    })
        else:
            out[key] = value
    return out