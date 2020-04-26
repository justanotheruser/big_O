def log(*args, **kwargs):
    if 'verbose' not in kwargs.keys():
        raise Exception("'verbose' value not provided for 'log' function")
    verbose = kwargs['verbose']
    del kwargs['verbose']

    if verbose:
        print(*args, **kwargs)