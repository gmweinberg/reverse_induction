#!/usr/bin/python

"""Solve the capture the bishop probelm discussed here
   https://youtu.be/kLuqHhfRDJA
"""
from graph import Graph
from node import Node
class CTB(Graph):
    def __init__(self, rows, columns, **kwargs):
        super().__init__(**kwargs)
        self.rows = rows
        self.columns = columns

    def generate_graph(self):
        for ii in range(self.columns):
            for iii in range(self.rows):
                name = (ii, iii)
                if ii == 0 and iii == 0:
                    node = Node(name, terminal=True, winner=True)
                elif ii == iii:
                    node = Node(name, terminal=True, winner=False)
                else:
                    node = Node(name)
                self.nodes[name] = node

    def get_successors(self, node) -> list:
        x = node.name[0]
        y = node.name[1]
        suc = []
        for ii in range(x-1, -1, -1):
            suc.append((ii, y))
        for iii in range(y-1, -1, -1):
            suc.append((x, iii))
        return suc

if __name__ == '__main__':
    ctb = CTB(6, 12)
    ctb.generate_graph()
    ctb.verbose = True
    ctb.analyze()



