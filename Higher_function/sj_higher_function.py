from inspect import signature
import itertools

def apply_composition_function(x, functions):
    """
    data is applied to functions
    ex)
    if functions is [f,g] then x is applied as f(g(x))

    :param x: data
    :param functions: function list ex) [lambda x: x + 1, lambda x: x * 2]
    :return: data applied composition function
    """
    data_type = type(x)
    if len(functions) == 1:
        return data_type(map(functions[0], x))
    else:
        return data_type(map(functions[0], apply_composition_function(x, functions[1:])))

def recursive_map(x, function):
    """
    each element of x is applied to function
    :param x: data ex) [1, [1, [2,5,3,5]], 4]
    :param function: function ex) lambda x: lambda x: round(x,1)
    :return: return the data that is applied to function recursively
    """
    if isinstance(x, (list, tuple, set)):
        t = type(x)
        return t(map(lambda e: recursive_map(e, function), x))
    else:
        return function(x)

def curry(func):
    # to keep the name of the curried function:
    curry.__curried_func_name__ = func.__name__
    f_args, f_kwargs = [], {}

    def f(*args, **kwargs):
        nonlocal f_args, f_kwargs
        if args or kwargs:
            f_args += args
            f_kwargs.update(kwargs)
            return f
        else:
            result = func(*f_args, *f_kwargs)
            f_args, f_kwargs = [], {}
            return result

    return f

def apply_function(f, args):
    """
    It applies function like f(args)

    :param f: function ex) lambda x,y: x+y
    :param args: values for appling f ex) [1,1]
    :return: scalar, f(args)
    """
    if len(signature(f).parameters) == len(args):
        func = curry(f)
        for arg_value in args:
            func = func(arg_value)
        return func()
    else:
        raise Exception("the number of function's parameter is not matched args")

def flatten_2d(a_2dlist):
    """
    flatten list 2d -> 1d

    :param a_2dlist: 2d list
    :return: 1d list
    """
    return list(itertools.chain(*a_2dlist))

def flatten(l):
    try:
        return flatten(l[0]) + (flatten(l[1:]) if len(l) > 1 else []) if type(l) is list else [l]
    except IndexError:
        return []

class Mapping:
    """
    This class is for defining mapping function

    This class is used for namespace
    """

    @staticmethod
    def one_to_many(domain, codomain, mapping_condition):
        """

        :param domain: domain
        :type domain: list
        :param codomain: codomain
        :type codomain: list
        :param mapping_condition: mapping condition (argument count is 2)
        :type mapping_condition: function

        :return: mapped list(domain to codomain)
        :rtype: 2d list
        """
        return list(map(lambda x: Mapping.one_value_to_many(x, list(filter(lambda y: mapping_condition(x, y), codomain))), domain))

    @staticmethod
    def one_value_to_many(x, Y):
        """

        :param x: a value
        :type x: scalar
        :param Y: codomain
        :type Y: list
        :return: [[x, y1], [x, y2], ...]
        :rtype: list
        """
        return [[x, y] for y in Y]

    @staticmethod
    def one_to_one(X, Y, condition):
        """
        one_to_one mapping
        if one value is selected then the value is not mapped any more(successively)
        :param X:
        :type X: list
        :param Y:
        :type Y: list
        :param condition: mapping condition
        :type condition: (x, y) -> Flag
        :return: mapped values
        :rtype: 2d list
        """
        default_value_format = "None {0}"
        default_count = 0

        target_Y = Y[:]
        result = []
        for x in X:
            is_mapping_occurred = False
            for y in target_Y:
                if condition(x,y):
                    result.append([x, y])
                    target_Y.remove(y) # remove first occurred value y
                    is_mapping_occurred = True
                    break

            if is_mapping_occurred == False:
                defalut_value = str.format(default_value_format, str(default_count))
                result.append([x, defalut_value])
                default_count += 1
        return result

if __name__ == "__main__":
    apply_function(lambda x,a,b: x+a+b, [1,2,3])

    curry(lambda x,a,b: x+a+b)(3)(2)(1)()

    recursive_map([1, [2, 3, [4],5],6], lambda x: x**2)

    apply_composition_function([1,2,3], [lambda x: x*2, lambda x: x**2])

    flatten_2d([[1,2], [3,4]])

    Mapping.one_to_many([1, 2, 3], [4, 5, 6], lambda x, y: y > x)
    Mapping.one_to_one([1, 2, 3], [4, 5, 6], lambda x, y: (x + y) > 7)