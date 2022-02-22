
"""Graph represents a colletion of nodes with rules saying which nodes can reach which other nodes.
   The graph must be acyclic or our algorithm will get stuck in an endless loop."""

class Graph(object):
    def __init__(self):
        self.nodes = {}
        self.verbose = False
 
    def get_previous(self, node):
        """Get all nodes that can reach the given node"""
        raise Exception("Not implemented")

    def get_successors(self, node):
        """Get all nodes that can be reached from the given node."""
        raise Exception("Not implemented""")

    def analyze(self):
        done = False
        while not done:
            done = True
            for key in self.nodes:
                node = self.nodes[key]
                if node.analyzed:
                    continue
                for node2 in self.get_successors(node):
                    if node2.terminal and node2.winner:
                        node.analyzed = True
                        node.winner = True
                        done = False
                        if self.verbose:
                            print("Node {} is a winner (move to terminal {})".format(node.name, node2.name))
                        break
                if node.analyzed:
                    continue
                progress = True
                for node2 in self.get_successors(node):
                    if not node2.analyzed:
                        progress = False
                        break
                    if node2.terminal: # do not move to terminal loser
                        continue
                    if not node2.winner:
                        node.analyzed = True
                        node.winner = True
                        done = False
                        if self.verbose:
                            print("Node {} is a winner (move to loser {})".format(node.name, node2.name))
                        break
                if progress and not node.analyzed:
                    node.analyzed = True
                    node.winner = False
                    done = False
                    if self.verbose:
                        print("Node {} is a loser".format(node.name))
