from __future__ import absolute_import

from timeit import Timer

import numpy as np

from big_o.complexities import ALL_CLASSES
from big_o.logging import log


def measure_execution_time(func, data_generator,
                           min_n=100, max_n=100000, n_measures=10,
                           n_repeats=1, n_timings=1, verbose=False):
    """ Measure the execution time of a function for increasing N.

    Input:
    ------

    func -- Function of which the execution time is measured.
            The function is called as func(data), where data is returned
            by the argument `data_generator`

    data_generator -- Function returning input data of 'length' N.
                      Input data for the argument `func` is created as
                      `data_generator(N)`. Common data generators are defined
                      in the submodule `big_o.datagen`

    min_n, max_n, n_measures -- The execution time of func is measured
                                at `n_measures` points between `min_n` and
                                `max_n` (included)

    n_repeats -- Number of times func is called to compute execution time
                 (return the cumulative time of execution)

    n_timings -- Number of times the timing measurement is repeated.
                 The minimum time for all the measurements is kept.

    verbose -- If True, print measured time for each tested value of n as soon
               as it is measured

    Output:
    -------

    n -- List of N's used as input to `data_generator`

    time -- List of total execution time for each N in seconds
    """

    # we need a wrapper that holds a reference to func and the generated data
    # for the timeit.Timer object
    class func_wrapper(object):

        def __init__(self, n):
            self.data = data_generator(n)

        def __call__(self):
            return func(self.data)

    # TODO: check that max_n is not larger than max int64
    ns = np.linspace(min_n, max_n, n_measures).astype('int64')
    execution_time = np.empty(n_measures)
    for i, n in enumerate(ns):
        timer = Timer(func_wrapper(n))
        measurements = timer.repeat(n_timings, n_repeats)
        execution_time[i] = np.min(measurements)
        log(f'n={n}: {execution_time[i]}', verbose=verbose)
    return ns, execution_time


def infer_big_o_class(ns, time, classes=ALL_CLASSES, verbose=False):
    """Infer the complexity class from execution times.

    Input:
    ------

    ns -- Array of values of N for which execution time has been measured.

    time -- Array of execution times for each N in seconds.

    classes -- The complexity classes to consider. This is a list of subclasses
               of `big_o.complexities.ComplexityClass`.
               Default: all the classes in `big_o.complexities.ALL_CLASSES`

    verbose -- If True, print parameters and residuals of the fit for each
               complexity class

    Output:
    -------

    best_class -- Object representing the complexity class that best fits
                  the measured execution times.
                  Instance of `big_o.complexities.ComplexityClass`.

    fitted -- A dictionary of fittest complexity classes to the fit residuals
    """

    best_class = None
    best_residuals = np.inf
    fitted = {}
    for class_ in classes:
        inst = class_()
        residuals = inst.fit(ns, time)
        fitted[inst] = residuals

        # NOTE: subtract 1e-6 for tiny preference for simpler methods
        # TODO: improve simplicity bias (AIC/BIC)?
        if residuals < best_residuals - 1e-6:
            best_residuals = residuals
            best_class = inst
        log(inst, '(r={:f})'.format(residuals), verbose=verbose)
    return best_class, fitted


def big_o(func, data_generator,
          min_n=100, max_n=100000, n_measures=10,
          n_repeats=1, n_timings=1, classes=ALL_CLASSES, verbose=False, return_raw_data=False):
    """ Estimate time complexity class of a function from execution time.

    Input:
    ------

    func -- Function of which the execution time is measured.
            The function is called as func(data), where data is returned
            by the argument `data_generator`

    data_generator -- Function returning input data of 'length' N.
                      Input data for the argument `func` is created as
                      `data_generator(N)`. Common data generators are defined
                      in the submodule `big_o.datagen`

    min_n, max_n, n_measures -- The execution time of func is measured
                                at `n_measures` points between `min_n` and
                                `max_n` (included)

    n_repeats -- Number of times func is called to compute execution time
                 (return the cumulative time of execution)

    n_timings -- Number of times the timing measurement is repeated.
                 The minimum time for all the measurements is kept.

    classes -- The complexity classes to consider. This is a list of subclasses
               of `big_o.complexities.ComplexityClass`.
               Default: all the classes in `big_o.complexities.ALL_CLASSES`

    verbose -- If True, print 1) measured time for each tested value of n as soon
               as it is measured; 2) print parameters and residuals of the fit for
               each complexity class

    return_raw_data -- If True, the function returns the measure points and its 
                       corresponding execution times as part of the fitted dictionary
                       of complexity classes. When this flag is true, fitted will 
                       contain the entries: 
                       {... 'measures': [<int>+], 'times': [<float>+] ...}

    Output:
    -------

    best_class -- Object representing the complexity class that best fits
                  the measured execution times.
                  Instance of `big_o.complexities.ComplexityClass`.

    fitted -- A dictionary of fittest complexity classes to the fit residuals
    """

    ns, time = measure_execution_time(func, data_generator,
                                      min_n, max_n, n_measures, n_repeats,
                                      n_timings, verbose)
    best, fitted = infer_big_o_class(ns, time, classes, verbose=verbose)

    if return_raw_data:
        fitted['measures'] = ns
        fitted['times'] = time

    return best, fitted
