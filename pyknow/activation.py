"""
Activations represent rules that matches against a specific factlist.
Its a namedtuple containing the rule and the facts that match against it

"""
from collections import namedtuple

Activation = namedtuple('Activation', ['rule', 'facts'])
