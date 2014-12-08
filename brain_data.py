import numpy as np


class BrainData(object):

    """
    Represents formatted FMRI data

    """

    def __init__(self, data):
        self._data = None
        self._name = None
        self._set = False
        self._init_data(data)

    def _init_data(self, data):
        """
        Read data from a dictionary
        """
        assert type(data) is dict, "dict expected: %r" % type(data)
        assert len(data) is 1, "size of dict should be 1: %r" % len(data)
        self._name = data.keys()[0]
        self._data = np.asarray(data[self._name])
        self._set = True

    @property
    def data(self):
        """
        Raw FMRI data
        """
        return self._data

    @property
    def name(self):
        """
        Data name
        """
        return self._name
