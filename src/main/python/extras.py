def check(inp):
    """
    inp:

    return:
    """
    if isinstance(inp, list):
        return [check(elem) for elem in inp]
    elif isinstance(inp, dict):
        return { check(k): check(v) for k, v in inp.iteritems() }
    elif isinstance(inp, str):
        return str(inp).strip() if inp is not None else ''
    elif inp is None:
        return ''
    else:
        return inp

def flatten(structure, key='', path='', flattened=None):
    """
    structure:
    key:
    path:
    flattened:

    return:
    """
    if flattened is None:
        flattened = {}
    if not isinstance(structure, (dict, list)):
        flattened[((path + "_") if path else "") + key] = structure
    elif isinstance(structure, list):
        for i, item in enumerate(structure):
            flatten(item, "%d" % i, "".join(filter(None,[path,key])), flattened)
    else:
        for new_key, value in structure.items():
            flatten(value, new_key, "".join(filter(None,[path,key])), flattened)

    return flattened
