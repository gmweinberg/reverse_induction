#!/usr/bin/env python
"""Try to solve the final coin puzzle discussed here
https://www.reddit.com/r/GAMETHEORY/comments/s7b1bb/can_you_take_the_final_coin_a_game_theory_puzzle/

For this problem the 'name' of a node is a tuple specifying the partitions of the set of coins in decending order 
e.g. 15 coins all connected is just (15,), 
a partition of  8 coins and 5 coins is (8, 5).

If a partition is size 1 or 2 we can remove it completely.
If it is size 2 or more we can reduce it by size 1 or 2 (2 removes it)
If it is size 3 or more we can split it into 2 partitions with size that totals to 1 or 2 less than the previous size.

"""

def pieces(size):
    """Find the possible sub-partitions of a prtion with the given size
       returns a list of lists, each of which will have size 1 or 2."""
    # In this function we do not include the empty partition we can get from a size 1 or 2 partition.
    result = []
    if size > 1:
        result.append([size - 1])
    if size > 2:
        result.append([size - 2])
    n = 1
    while n < size - n:
        result.append([size - (n + 1), n])
        if n + 1 < size - n:
            result.append([size - (n + 2), n])
        n += 1
    return result



from graph import Graph
from node import Node
class LastCoin(Graph):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nodes = {}
        name = tuple()
        node = Node(name, terminal=True, winner=True)
        self.nodes[name] = node

    def get_successors(self, node):
        used = set()
        lname = list(node.name)
        result = []
        for index in range(len(lname)):
            others = list(lname)
            del others[index]
            child_pieces = pieces(lname[index])
            for piece in child_pieces:
                temp = list(others)
                temp.extend(piece)
                temp.sort(reverse=True)
                childname = tuple(temp)
                if childname in used:
                    continue
                used.add(childname)
                if childname in self.nodes:
                    #print("appending {}".format(childname))
                    result.append(self.nodes[childname])
                else:
                    node = self.generate_node(childname)
                    self.nodes[childname] = node
                    #print("appending {}".format(childname))
                    result.append(node)
        if len(lname) == 1 and lname[0] in [1,2]:
            result.append(self.nodes[tuple()])
        return result


if __name__ == '__main__':
    size = 14
    #print('pieces', pieces(size))
    lc = LastCoin(verbose=True)
    start = lc.generate_node((size,))
    # lc.get_successors(start)
    lc.solve_from(start.name)

