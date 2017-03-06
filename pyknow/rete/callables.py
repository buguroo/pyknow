"""
Callables to be used by alpha nodes
"""

from . import PRIORITIES

THIRD = PRIORITIES[2]


class Callables:
    """
    Alpha nodes callables
    """

    @staticmethod
    def and_match(left, right):
        """
        Returns true if all the items in the left dictionary are
        contained in the right dictionary and all the common values
        are the same.
        """
        return not set(left.items()) - set(right.items())

    @staticmethod
    def match_W(key, value):
        """ Returns alpha for a given key/value pair for type W """
        # pylint: disable=invalid-name
        def _has_key(fact):
            if not value:
                return fact.get(key, None) is None
            else:
                return fact.get(key, None) is not None
        return _has_key

    @staticmethod
    def match_V(key, value):
        """ Returns alpha for a given key/value pair for type V """
        # pylint: disable=invalid-name
        def _get_context(fact):
            if fact.get(key, None) is not None:
                return {value: fact.get(key)}
            return {}

        return _get_context

    @staticmethod
    def match_T(key, value):
        """ Returns alpha for a given key/value pair for type T """
        # pylint: disable=invalid-name
        return lambda fact: value(fact.get(key))

    @staticmethod
    def match_L(key, value):
        """ Returns alpha for a given key/value pair for type L """
        # pylint: disable=invalid-name
        return lambda fact: fact.get(key, None) == value

    @staticmethod
    def has_key(key):
        """
        Return base alpha element for this fact type
        By default we check that we've got the remote key.
        You must preferibly override ``get_alpha``
        if you require that condition to not be met.

        This checks that we've got the key in the checked fact
        """
        return lambda fact: hasattr(fact, key)

    @staticmethod
    def same_class(parent_class):
        """
        Compare fact classes
        """
        return lambda fact: type(fact) is parent_class.__class__

    @staticmethod
    def compatible_facts(fact):
        """
        Check if fact keys is a subset of the other fact keys
        """
        return lambda other: set(fact.keys()).issubset(other.keys())

    @staticmethod
    def get_callable(key, value):
        """
        Return compare method for specific class, defaults to literal
        comparision
        """
        name = value.__class__.__name__
        getter = getattr(Callables, "match_{}".format(name), Callables.match_L)
        return getter(key, value)
