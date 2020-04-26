import matplotlib.pyplot as plt


def plot(ns, time):
    """ Plot result of measure_execution_time.
    """
    min_time, max_time = min(time), max(time)
    time_range = max(time) - min(time)
    min_y = min_time - 0.05 * time_range
    max_y = max_time + 0.05 * time_range
    plt.ylim(min_y, max_y)
    plt.scatter(ns, time)
    plt.plot(ns, time)
    plt.show()
