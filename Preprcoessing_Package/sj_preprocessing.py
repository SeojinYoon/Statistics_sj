
def flags(list, condition):
    """
    return data of flags

    :param list: data
    :param condition: check data function
    :return: flags of data
    """
    return [True if condition(e) else False for e in list]

def choice(list1, list2, flags):
    """
    if flag is True then select list1's component
    otherwise select list2's component

    :param list1: first set of data
    :param list2: second set of data
    :param flags: criteria of choice algorithm
    :return:
    """
    if len(list1) == len(list2) == len(flags):
        result = []
        for i in range(0, len(flags)):
            if flags[i] == True:
                result.append(list1[i])
            else:
                result.append(list2[i])
        return result
    else:
        raise Exception("length is not compatible among list1, list2 and flags")

def counter(data, bin_ranges, equal_direction = "None"):
    """
    It counts number of data according to a range of bin
    if equal_direction is Left, equal sign of inequality is attached at lower bound
        so it means that if we check 3 and equal_direction is Left, we check the condition like lower_bound <= 3 < upperbound
        if equal_direction is None, we check the condition like lower_bound < 3 < upperbound

    :param data: list ex) [1,2,3,4]
    :param bin_ranges: range of bin ex) [(0,1), (1,2), (2,3)]
    :param equal_direction: direction of equal(None, Left, Right) ex) "Left"
    :return: number of data ex) { (0,1) : 3, (1,2) : 2 }
    """
    method_left_equal = lambda x, lower_bound, upper_bound: True if (x >= lower_bound and x < upper_bound) else False
    method_right_equal = lambda x, lower_bound, upper_bound: True if (x > lower_bound and x <= upper_bound) else False
    method_none_equal = lambda x, lower_bound, upper_bound: True if (x > lower_bound and x < upper_bound) else False


    if equal_direction == "None":
        selected_method = method_none_equal
    elif equal_direction == "Left":
        selected_method = method_left_equal
    elif equal_direction == "Right":
        selected_method = method_right_equal

    result = {}
    for key in bin_ranges:
        result[key] = 0

    for e in data:
        for range in bin_ranges:
            lower_b = range[0]
            upper_b = range[1]
            if selected_method(e, lower_b, upper_b) == True:
                result[range] = result[range] + 1
                break
    return result

def df_to_series(data):
    return list(map(lambda x: x[1], list(data.iterrows())))
