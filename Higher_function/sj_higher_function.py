from inspect import signature

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

if __name__ == "__main__":
    apply_function(lambda x,a,b: x+a+b, [1,2,3])

    curry(lambda x,a,b: x+a+b)(3)(2)(1)()

    recursive_map([1, [2, 3, [4],5],6], lambda x: x**2)

    apply_composition_function([1,2,3], [lambda x: x*2, lambda x: x**2])
