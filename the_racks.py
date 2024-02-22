#!/usr/bin/env python

"""Game from here
https://www.reddit.com/r/GAMETHEORY/comments/1auljia/need_help_finding_a_winning_strategy_in_this/
Players alternate playing integers in up to n columns.
Loser is player who places an integer m such that two numbers already in the column add up to m.
I rule that an integer cannot be placed in a column unless the lower-indexed columns all contain at least one element
(e.g. th1 1 must go in column 0), this doesn't change the game at all but simplifies the game tree.

Node names are a tuple of tuples with the integers in a column in order e.g if after 2 moves in a 2 column game
1 and 2 are in different columns, the node looks like
((1,), (2,))"""

from graph import Graph
from node import Node
from copy import deepcopy

class TheRacks(Graph):
    def __init__(self, columns, **kwargs):
        super().__init__(**kwargs)
        self.columns = columns
        self.maxmax = None

    def  get_successors(self, node) -> list:
        node = node.name
        result = []
        max_ = 0
        for acolumn in node:
            if len(acolumn):
                if acolumn[-1] > max_:
                    max_ = acolumn[-1]
        new = max_ + 1
        nodelist = [list(acolumn) for acolumn in node]

        for ii, acolumn in enumerate(node):
            was_empty = len(acolumn) == 0
            nlc = deepcopy(nodelist)
            nlc[ii].append(new)
            result.append(tuple([tuple(elm) for elm in nlc]))
            if was_empty:
                break
        return result

    def generate_graph(self):
        start = tuple([tuple() for ii in range(self.columns)])
        self.nodes[start] = Node(name=start, winner=None, terminal=False)
        self._add_children(start)

    def _add_children(self, nodename):
        theNode = self.nodes[nodename]
        for childname in self.get_successors(theNode):
            if childname not in self.nodes:
                if self._is_terminal(childname):
                    self.nodes[childname] = Node(name=childname, winner=False, terminal=True)
                else:
                    self.nodes[childname] = Node(name=childname, winner=None, terminal=False)
                    self._add_children(childname)


    def _is_terminal(self, nodename):
        colIndex = None
        max_ = None
        for ii, acolumn in enumerate(nodename):
            for elm in acolumn:
                if max_ is None or elm > max_:
                    max_ = elm
                    colIndex = ii
        if colIndex is None:
            return False
        if self.maxmax is None or max_ > self.maxmax:
            self.maxmax = max_
        theColumn = nodename[colIndex]
        for elm in theColumn:
            if elm * 2 == max_:
                continue
            if max_ - elm in theColumn:
                return True
        return False



if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('--columns', default=2, type=int)
    parser.add_argument('--verbose', action='store_true')
    parser.add_argument('--max', action='store_true', dest='max_')
    parser.add_argument('--analyze', action='store_true')
    parser.add_argument('--terminal', action='store_true', help="list termnal nodes")
    args = parser.parse_args()
    theRacks = TheRacks(columns=args.columns, verbose=args.verbose)
    theRacks.generate_graph()
    #print([name for name in theRacks.nodes])
    if args.analyze:
        theRacks.analyze()
    if args.max_:
        print(theRacks.maxmax)
    if args.terminal:
        for node in theRacks.get_terminal_nodes():
            print(node.name)

# ./the_racks --col 2 --verbose --max
