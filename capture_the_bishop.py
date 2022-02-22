#!/usr/bin/python

"""Solve the capture the bishop probelm discussed here
   https://youtu.be/kLuqHhfRDJA
"""
from graph import Graph
from node import Node
class CTB(Graph):
    def __init__(self):
        self.nodes = {} 
        for ii in range(6):
            for iii in range(12):
                name = (ii, iii) # use tuple as name, why not?
                if ii == 0 and iii == 0:
                    node = Node(name, terminal=True, winner=True)
                elif ii == iii:
                    node = Node(name, terminal=True, winner=False)
                else:
                    node = Node(name)
                self.nodes[name] = node

    def get_successors(self, node) -> Node:
        x = node.name[0]
        y = node.name[1]
        suc = []
        for ii in range(x-1, -1, -1):
            suc.append(self.nodes[(ii, y)])
        for iii in range(y-1, -1, -1):
            suc.append(self.nodes[(x, iii)])
        return suc

if __name__ == '__main__':
    ctb = CTB()
    ctb.verbose = True
    ctb.analyze()



