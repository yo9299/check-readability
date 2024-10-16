import unittest
import networkx as nx 
import numpy as np 
from algorithm import undesiredOverlaps,isFeasible,isSol

class TestFunctions(unittest.TestCase):
    def setUp(self):
        self.D = nx.DiGraph()
        self.D.add_nodes_from([0, 2], bipartite=0)
        self.D.add_nodes_from([1, 3], bipartite=1)
        self.D.add_weighted_edges_from([(0, 1, 2), (0, 3, 1), (2, 1, 1), (2, 3, 2)])
        nx.set_node_attributes(self.D, {i: np.array([1, 2]) for i in self.D.nodes}, name="label")
    def test_undesiredOverlaps(self):
        
        print("Running test_undesiredOverlaps...")  # Debug print statement
        #self.assertFalse(undesiredOverlaps(D, 0, 1, 2, 2))
        self.assertTrue(undesiredOverlaps(self.D, 0, 3, 2, 2))
        self.D.nodes[3]["label"] = np.array([3,2])
        self.assertFalse(undesiredOverlaps(self.D, 0, 3, 2, 2))
    def test_isFeasible(self):
        self.assertFalse(isFeasible(self.D, 2))
        self.D.edges[(0,3)]['weight'] = 2 
        self.D.edges[(2,1)]['weight'] = 2 
        self.assertTrue(isFeasible(self.D, 2))
        self.D.nodes[2]['label'] = np.array([0,0])
        self.assertTrue(isFeasible(self.D, 2))
    def test_isSol(self):
        self.assertFalse(isSol(self.D, 2))
        self.D.edges[(0,3)]['weight'] = 2 
        self.D.edges[(2,1)]['weight'] = 2 
        self.assertTrue(isSol(self.D, 2))


if __name__ == '__main__':
    print("in main")
    unittest.main()