# 6.0002 Problem Set 5
# Graph optimization
# Name:
# Collaborators:
# Time:

#
# Finding shortest paths through MIT buildings
#
import unittest
from graph import Digraph, Node, WeightedEdge

#
# Problem 2: Building up the Campus Map
#
# Problem 2a: Designing your graph
#
# What do the graph's nodes represent in this problem? What
# do the graph's edges represent? Where are the distances
# represented?
#
# Answer:
# The graph's nodes represent the building in the campus,the graph's
# edges represent that there's a route from one building to another
# the distances are represented in the weighted edge in the directed graph


# Problem 2b: Implementing load_map
def load_map(map_filename):
    mit_graph = Digraph()
    f = open(map_filename,'r')
    for line in f:
        line = line.strip('\n')
        info = line.split(' ')
        src = Node(info[0])
        dest = Node(info[1])
        weighted_edge = WeightedEdge(src,dest,info[2],info[3])
        try:
            mit_graph.add_node(src)
        except ValueError:
            pass
        try:
            mit_graph.add_node(dest)
        except ValueError:
            pass
        try:
            mit_graph.add_edge(weighted_edge)
        except ValueError:
            pass
    print("Loading map from file...")
    return mit_graph

# Problem 2c: Testing load_map
# Include the lines used to test load_map below, but comment them out
#test_graph = load_map("test_load_map.txt")
#print(test_graph.__str__())
#
# Problem 3: Finding the Shorest Path using Optimized Search Method
#
# Problem 3a: Objective function
#
# What is the objective function for this problem? What are the constraints?
#
# Answer:
# get_best_path:using dfs to find the shortest path from one node to another
# directed_dfs:using get_best_path to find the shortest path from start to end

# Problem 3b: Implement get_best_path
def get_best_path(digraph, start, end, path, max_dist_outdoors, best_dist,
                  best_path):
    tmp_st = Node(start)
    tmp_ed = Node(end)
    if not digraph.has_node(tmp_st) or not digraph.has_node(tmp_ed):
        raise ValueError
    path_list = path[0] + [start]
    cur_dist = path[1]
    cur_out_dist = path[2]
    if cur_out_dist > max_dist_outdoors or (best_dist != None and cur_dist >= best_dist):
        return None
    if start == end:
        return (path_list,cur_dist)
    else:
        for edge in digraph.get_edges_for_node(tmp_st):
            node = edge.dest
            if node.name not in path[0]:
                if best_dist == None or path[1] < best_dist:
                    newPath = get_best_path(digraph,node.name,end,[path_list,cur_dist+edge.total_distance,cur_out_dist+edge.outdoor_distance],max_dist_outdoors,best_dist,best_path)
                    if newPath != None:
                        best_path = newPath[0]
                        best_dist = newPath[1]
    return (best_path,best_dist)

# Problem 3c: Implement directed_dfs
def directed_dfs(digraph, start, end, max_total_dist, max_dist_outdoors):
    try:
        my_path = get_best_path(digraph,start,end,[[],0,0],max_dist_outdoors,None,None)
    except ValueError:
        raise ValueError
    if my_path == None or my_path[0] == None or my_path[1] == None:
        raise ValueError
    if my_path[1] > max_total_dist:
        raise ValueError
    return my_path[0]
# ================================================================
# Begin tests -- you do not need to modify anything below this line
# ================================================================

class Ps2Test(unittest.TestCase):
    LARGE_DIST = 99999

    def setUp(self):
        self.graph = load_map("mit_map.txt")

    def test_load_map_basic(self):
        self.assertTrue(isinstance(self.graph, Digraph))
        self.assertEqual(len(self.graph.nodes), 37)
        all_edges = []
        for _, edges in self.graph.edges.items():
            all_edges += edges  # edges must be dict of node -> list of edges
        all_edges = set(all_edges)
        self.assertEqual(len(all_edges), 129)

    def _print_path_description(self, start, end, total_dist, outdoor_dist):
        constraint = ""
        if outdoor_dist != Ps2Test.LARGE_DIST:
            constraint = "without walking more than {}m outdoors".format(
                outdoor_dist)
        if total_dist != Ps2Test.LARGE_DIST:
            if constraint:
                constraint += ' or {}m total'.format(total_dist)
            else:
                constraint = "without walking more than {}m total".format(
                    total_dist)

        print("------------------------")
        print("Shortest path from Building {} to {} {}".format(
            start, end, constraint))

    def _test_path(self,
                   expectedPath,
                   total_dist=LARGE_DIST,
                   outdoor_dist=LARGE_DIST):
        start, end = expectedPath[0], expectedPath[-1]
        self._print_path_description(start, end, total_dist, outdoor_dist)
        dfsPath = directed_dfs(self.graph, start, end, total_dist, outdoor_dist)
        print("Expected: ", expectedPath)
        print("DFS: ", dfsPath)
        self.assertEqual(expectedPath, dfsPath)

    def _test_impossible_path(self,
                              start,
                              end,
                              total_dist=LARGE_DIST,
                              outdoor_dist=LARGE_DIST):
        self._print_path_description(start, end, total_dist, outdoor_dist)
        with self.assertRaises(ValueError):
            directed_dfs(self.graph, start, end, total_dist, outdoor_dist)

    def test_path_one_step(self):
        self._test_path(expectedPath=['32', '56'])

    def test_path_no_outdoors(self):
        self._test_path(
            expectedPath=['32', '36', '26', '16', '56'], outdoor_dist=0)

    def test_path_multi_step(self):
        self._test_path(expectedPath=['2', '3', '7', '9'])

    def test_path_multi_step_no_outdoors(self):
        self._test_path(
            expectedPath=['2', '4', '10', '13', '9'], outdoor_dist=0)

    def test_path_multi_step2(self):
        self._test_path(expectedPath=['1', '4', '12', '32'])

    def test_path_multi_step_no_outdoors2(self):
        self._test_path(
            expectedPath=['1', '3', '10', '4', '12', '24', '34', '36', '32'],
            outdoor_dist=0)

    def test_impossible_path1(self):
        self._test_impossible_path('8', '50', outdoor_dist=0)

    def test_impossible_path2(self):
        self._test_impossible_path('10', '32', total_dist=100)


if __name__ == "__main__":
    unittest.main()
