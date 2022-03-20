from yaml import safe_load


def strToYAML(yaml):
    string = f"""{yaml}"""
    # print(string)
    result = safe_load(string)
    return result
