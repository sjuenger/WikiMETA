def found_in_array(elem, array):
    if array:
        for var in array:
            if var == elem:
                return True
    return False
