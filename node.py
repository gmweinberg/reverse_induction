#
""" 
Node is just a data structure
Name is the key in the dicctionary. I probably should rename it to key.
Most likely it will be a tuple.
Terminal indicates this node is a terminal node.
If terminal is true, then winner true means a player reachin this node wins, false means he loses.
If terminal is false, winner true means a winner reaching this node can win, false means if a player
gets suck here the other player can force a win. None means it is not yet analyzed.
Analyzed is a little redundant since analyzed will be true exactly when winner is not None.
"""
class Node(object):
    def __init__(self, name, terminal=False, winner=None):
        self.name = name
        self.terminal = terminal
        self.winner = winner
        self.analyzed = self.terminal


