
"""Graph represents a colletion of nodes with rules saying which nodes can reach which other nodes.
   The graph must be acyclic or our algorithm will get stuck in an endless loop."""
from node import Node
class Graph(object):
    def __init__(self, *args, **kwargs):
        self.nodes = {}
        if "verbose" in kwargs:
            self.verbose = kwargs["verbose"]
        else:
            self.verbose = False
 
    def get_previous(self, node):
        """Get all nodes that can reach the given node"""
        raise Exception("Not implemented")

    def get_successors(self, node):
        """Get all nodes that can be reached from the given node."""
        raise Exception("Not implemented""")

    def analyze(self):
        """Analyze assumes the entire dictionary already exists and classifies every node as a 'winner' or loser'"""
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

    def generate_node(self, name):
        """create a new node with the given name and add it to the dictionary."""
        node_ = Node(name)
        self.nodes[name] = node_
        return node_

    def solve_from(self, name)-> bool:
        """Determine whether this node is a winner or loser. Generate new nodes if necessary."""
        if name not in self.nodes:
            self.generate_node(name)
        node_ = self.nodes[name]
        for node2 in self.get_successors(node_):
            loser = True
            if node2.terminal and node2.winner:
                node_.winner = True
                node_.analyzed = True
                print('node {} is a winner. send to terminal {}'.format(node_.name, node2.name))
                return True
            if node2.terminal:
                continue
            if node2.analyzed:
                bad = node2.winner
                if not bad:
                    loser = False
                    node_.analyzed = True
                    node_.winner = True
                    print('node {} is a winner. send to loser {}'.format(node_.name, node2.name))
                    return True
            else:
                bad = self.solve_from(node2.name)
                if not bad:
                    loser = False
                    node_.analyzed = True
                    node_.winner = True
                    return True
        node_.analyzed = True
        node_.winner = False
        if self.verbose:
            print('node {} is a loser'.format(node_.name))
        return False

