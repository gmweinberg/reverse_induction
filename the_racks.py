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
import time
import random
import psutil
from copy import deepcopy
from graph import Graph
from node import Node

class TheRacks(Graph):
    def __init__(self, columns, **kwargs):
        if 'default_start' not in kwargs:
            kwargs['default_start'] = tuple([tuple() for ii in range(columns)])
        super().__init__(**kwargs)
        self.columns = columns
        self.maxmax = None
        self.added = 0

    def  get_successors(self, node, includeTerminals=True) -> list:
        """Return the names of child nodes for the given node."""
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
            childname  = tuple([tuple(elm) for elm in nlc])
            if includeTerminals or not self.is_terminal(childname, colIndex=ii): 
                result.append(tuple([tuple(elm) for elm in nlc]))
            if was_empty:
                break
        return result

    def generate_graph(self, start=None):
        if start is None:
            start = self.default_start
        self.nodes[start] = Node(name=start, winner=None, terminal=False)
        self.add_children(start)

    def random_path(self, steps, start=None) -> tuple:
        """Generate a random path steps nodes deep.  Returnd the name of the last node generated."""
        if start is None:
            start = self.default_start
        start = tuple([tuple() for ii in range(self.columns)])
        self.nodes[start] = Node(name=start, winner=None, terminal=False)
        new_node = self.nodes[start]
        for astep in range(steps):
            successors = self.get_successors(new_node, includeTerminals = False)
            if not successors:
                print("random_path no successors node {}".format(nodename))
                return nodename
            nodename = random.choice(successors)
            self.nodes[nodename] = Node(name=nodename, winner=None, terminal=False)
            new_node = self.nodes[nodename]
        return nodename


    def add_children(self, nodename):
        theNode = self.nodes[nodename]
        for childname in self.get_successors(theNode):
            if childname not in self.nodes:
                self.added += 1
                if self.added > 26 * 1000 * 1000:
                    print("last childname {} maxmax {}".format(childname, self.maxmax))
                    print(psutil.virtual_memory())
                    raise Exception("Too Bookoo")
                if self.is_terminal(childname):
                    self.nodes[childname] = Node(name=childname, winner=False, terminal=True)
                else:
                    self.nodes[childname] = Node(name=childname, winner=None, terminal=False)
                    self.add_children(childname)


    def is_terminal(self, nodename,colIndex = None):
        if colIndex is None:
            max_ = None
            for ii, acolumn in enumerate(nodename):
                for elm in acolumn:
                    if max_ is None or elm > max_:
                        max_ = elm
                        colIndex = ii
            if colIndex is None:
                return False
        else:
            max_ = nodename[colIndex][-1]
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
    from ast import literal_eval
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('--columns', default=2, type=int)
    parser.add_argument('--random', default=None, type=int, help="start with a random path")
    parser.add_argument('--start', default=None, help="start with named node")
    parser.add_argument('--verbose', action='store_true')
    parser.add_argument('--max', action='store_true', dest='max_')
    parser.add_argument('--analyze', action='store_true')
    parser.add_argument('--terminal', action='store_true', help="list termnal nodes")
    args = parser.parse_args()
    started = time.time()
    theRacks = TheRacks(columns=args.columns, verbose=args.verbose)
    #print([name for name in theRacks.nodes])
    try:
        if args.random:
            startfrom = theRacks.random_path(args.random)
            print('starting from random ', startfrom)
            theRacks.add_children(startfrom)
            print('maxmax', theRacks.maxmax)
        elif args.start:
            name = literal_eval(args.start)
            theRacks.generate_node(name)
            theRacks.add_children(name)
            print('maxmax', theRacks.maxmax)
        else:

            theRacks.generate_graph()
            if args.analyze:
                theRacks.analyze()
            if args.max_:
                print(theRacks.maxmax)
            if args.terminal:
                for node in theRacks.get_terminal_nodes():
                    print(node.name)
    except Exception as ex:
        raise
        print(ex)
    print('elapsed {}'.format(round(time.time() - started, 2)))

# ./the_racks.py --col 2 --verbose --max
# ./the_racks.py --col 2 --start "((1,5,9,12,19), (2,6,10,14,17), (3,7,11,15,19), (4,8,13,16))"
