import pandas as pd
import numpy as np


class Graph():
    # A constructor to iniltialize the values
    def __init__(self, nodes):
        # distance array initialization
        self.distArray = [0 for i in range(nodes)]
        # visited nodes initialization
        self.vistSet = [0 for i in range(nodes)]
        # initializing the number of nodes
        self.V = nodes
        # initializing the infinity value
        self.INF = 1000000
        # initializing the graph matrix
        self.graph = [[0 for column in range(nodes)]
                      for row in range(nodes)]

    def dijkstra(self, srcNode):
        for i in range(self.V):
            # initialise the distances to infinity first
            self.distArray[i] = self.INF
            # set the visited nodes set to false for each node
            self.vistSet[i] = False
        # initialise the first distance to 0
        self.distArray[srcNode] = 0
        for i in range(self.V):

            # Pick the minimum distance node from
            # the set of nodes not yet processed.
            # u is always equal to srcNode in first iteration
            u = self.minDistance(self.distArray, self.vistSet)

            # Put the minimum distance node in the
            # visited nodes set
            self.vistSet[u] = True

            # Update dist[v] only if is not in vistSet, there is an edge from
            # u to v, and total weight of path from src to  v through u is
            # smaller than current value of dist[v]
            for v in range(self.V):
                if self.graph[u][v] > 0 and self.vistSet[v] == False and self.distArray[v] > self.distArray[u] + \
                        self.graph[u][v]:
                    self.distArray[v] = self.distArray[u] + self.graph[u][v]

        self.printSolution(self.distArray)

    # A utility function to find the node with minimum distance value, from
    # the set of nodes not yet included in shortest path tree
    def minDistance(self, distArray, vistSet):

        # Initilaize minimum distance for next node
        min = self.INF

        # Search not nearest node not in the
        # unvisited nodes
        for v in range(self.V):
            if distArray[v] < min and vistSet[v] == False:
                min = distArray[v]
                min_index = v

        return min_index

    def printSolution(self, distArray):
        print("Node \tDistance from 0")
        for i in range(self.V):
            print(i, "\t", distArray[i])


# Display our table
ourGraph = Graph(97)
################## ##########################
new_df = pd.read_json("weights.json")
cities = list(new_df.columns)
cities = {k: v for k, v in enumerate(cities, start=0)}
for key in cities:
    print(str(key) + '\t' + cities[key])  # TODO ask for source node
array = new_df.to_numpy()
weights = array.tolist()
ourGraph.graph = weights
################## ##########################

ourGraph.dijkstra(0)
