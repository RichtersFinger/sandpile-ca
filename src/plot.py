"""Simple matplotlib-based plotter."""
import matplotlib.pyplot as plt
import numpy as np

class Plotter():
    """Simple matplotlib-based plotter class."""
    def __init__(self):
        pass

    def plot2d(self, data=None, block=True, interval=None):
        """
        Plot a heatmap of data.

        Keyword arguments:
        data -- numpy array of data to be plotted
                (default None)
        block -- determine whether to plot in a blocking way
                 (default True)
        interval -- determine the length of a pause in case of non-blocking
                    (default None)
        """

        # if no data provided, plot test-image
        if data is None:
            data = np.random.random((16, 16))

        plt.imshow(data, cmap='hot', interpolation='nearest')
        plt.show(block=block)
        if interval is not None:
            plt.pause(interval)
