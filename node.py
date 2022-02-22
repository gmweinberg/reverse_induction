#
""" """
class Node(object):
    def __init__(self, name, terminal=False, winner=None):
        self.name = name
        self.terminal = terminal
        self.winner = winner
        self.analyzed = self.terminal


