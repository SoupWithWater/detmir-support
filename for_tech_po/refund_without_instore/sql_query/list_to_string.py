
def list_to_string(list):
    returned_string = ''

    for string in list:
        returned_string = returned_string + ("'" + string + "',")

    returned_string = returned_string[0:-1]
    return returned_string
