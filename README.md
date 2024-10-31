# check-readability
Given a bipartite graph with edge weights, checks whether it has readability r with this edge weights. 

# Requirements 
  Networkx 
  
# Usage
The method algo(g, r) from algorithm.py returns whether graph g (networkx object) with a specific edge weight assignment has readability r. (Note that a labeling of the vertices can be obtained by calling printLabels afterwards). 

The method getSol(graph, readability) returns all the feasible weight assignments of graph graph such that it has readability readability. 


