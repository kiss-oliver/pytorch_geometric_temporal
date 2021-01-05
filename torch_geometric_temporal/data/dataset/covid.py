import io
import json
import numpy as np
from six.moves import urllib
from torch_geometric_temporal.data.discrete.static_graph_discrete_signal import StaticGraphDiscreteSignal

class CovidDatasetLoader(object):
    """A dataset of county level covid cases in the United States starting
    in February 2020 combining a set of publicly available data sources.
    The underlying graph is static, nodes are counties and edges are 
    neighborhoods. The dataset contains mainland US counties, i.e. Alaska,
    Hawaii and oversees territories are not included. Vertex features are
    Google Mobility indicators in different locations (e.g. retail, parks,
    etc.). The target is the daily new covid-19 cases (integers). The data
    contains more than 300 days.
    """
    def __init__(self):
        self._read_web_data()

    def _read_web_data(self):
        url = "https://raw.githubusercontent.com/benedekrozemberczki/pytorch_geometric_temporal/master/dataset/discrete/covid-spatiotemporal.json"
        self._dataset = json.loads(urllib.request.urlopen(url).read())

    def _get_edges(self):
        self._edges = np.array(self._dataset["edges"]).T

    def _get_edge_weights(self):
        self._edge_weights = np.ones(self._edges.shape[1])

    def _get_features(self):
        self.features = []
        for time in range(self._dataset["time_periods"]):
            self.features.append(np.array(self._dataset[str(time)]["X"]))

    def _get_targets(self):
        self.targets = []
        for time in range(self._dataset["time_periods"]):
            self.targets.append(np.array(self._dataset[str(time)]["y"]))

    def get_dataset(self) -> StaticGraphDiscreteSignal:
        """Returning the Covid US spatiotemporal data iterator.

        Return types:
            * **dataset** *(StaticGraphDiscreteSignal)* - The covid dataset.
        """
        self._get_edges()
        self._get_edge_weights()
        self._get_features()
        self._get_targets()
        dataset = StaticGraphDiscreteSignal(self._edges, self._edge_weights, self.features, self.targets)
        return dataset

