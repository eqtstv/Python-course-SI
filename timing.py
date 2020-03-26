from timeit import default_timer as timer

def timing(function):
    def wrap(*args, **kwargs):
        time1 = timer()
        result = function(*args, **kwargs)
        time2 = timer()
        print('{} function with {} took {:.2} ms'.format(function.__name__, args[2].__name__ ,(time2-time1)*1000.0))
        return result
    return wrap