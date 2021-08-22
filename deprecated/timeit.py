import time


# @timeit
def timeit(method):
    def timed(*args, **kw):
        start = time.time()
        result = method(*args, **kw)
        end = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((end - start) * 1000)
        else:
            print(f"Function: %r \nExecution Time: %2.2f ms" % (method.__name__, (end - start) * 1000))
        return result

    return timed
