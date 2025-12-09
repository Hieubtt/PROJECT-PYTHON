nested = { 'a': { 'b': { 'c': 1, 'd': 2 }, 'e': 3 }, 'f': 4 }
def lam_phang_dict(data,prefix = ''):
    result = {}

    for keys,values in data.items():
        if prefix !='':
            new_key = prefix + '.' + keys
        else:
            new_key = keys
        print(new_key)
        if isinstance(values,dict):
            result.update(lam_phang_dict(values,new_key))
        else:
            result[new_key] = values
            # print(result[new_key])
    return result


print(lam_phang_dict(nested))
