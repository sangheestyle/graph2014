import numpy as np
from sklearn import covariance
import networkx as nx


class BrainData(object):

    """
    Represents formatted FMRI data

    """

    def __init__(self, data):
        self._data = None
        self._name = None
        self._set = False
        self._init_data(data)
        self._model = None
        self._model_name = None
        self._modeled = False
        self._graph = None

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

    @property
    def model(self):
        """
        Access model
        """
        return self._model

    @property
    def graph(self):
        """
        Access graph generated by covariance
        """
        return self._graph

    def calc_covariance(self, method="graphlassocv", values="cov"):
        """
        Cacl coveriance matrix to make graph
        parameters
        ----------
        method: string
            Type of algorithm for covariance, graphlassocv
        values: string
            Type of values for matrix for graph
            cov: covariance_
            pre: precision_
        """
        if method == "graphlassocv":
            self._model = covariance.GraphLassoCV()
        else:
            assert NotImplementedError
        self._model_name = method
        self._model.fit(self._data)
        if values == "cov":
            self._graph = nx.from_numpy_matrix(self._model.covariance_)
        elif values == "pre":
            self._graph = nx.from_numpy_matrix(self._model.precision_)
        else:
            assert NotImplementedError
        self._modeled = True
