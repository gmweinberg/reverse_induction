#!/usr/bin/env python
#https://www.reddit.com/r/GAMETHEORY/comments/sjtrm5/chomp_the_long_and_skinny_version/

from graph import Graph
from node import Node
class LongAndSkinny(Graph):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        name = (0, 0)
        node = Node(name, terminal=True, winner=False)
        self.nodes[name] = node

    def get_successors(self, node):
        name = node.name
        result = []
        top = name[1]
        bottom = name[0]
        if self.verbose:
            print('get_successors getting succesors for {}'.format(node.name))
        if bottom > top:
            ii = 1
            while bottom >= top + ii:
                childname = (bottom - ii, top)
                if self.verbose:
                    print('get_successors appending {}'.format(childname))
                result.append(childname)
                ii += 1
        else:
            ii = 1
            while top >= ii:
                childname = (bottom, top - ii)
                if self.verbose:
                    print('get_successors appending {}'.format(childname))
                result.append(childname)
                ii += 1

        ii = 1
        while bottom >= ii:
            childname = (bottom - ii, bottom - ii)
            if self.verbose:
                print('get_successors appending {}'.format(childname))
            result.append((childname))
            ii += 1
        if not result:
            raise Exception('No successors for {}'.format(name))
        return result

if __name__ == '__main__':
    verbose = True
    #verbose = False
    las = LongAndSkinny(verbose=verbose)
    #node_ = las.generate_node((1,0))
    #las.get_successors(node_)
    las.solve_from((12, 12))
