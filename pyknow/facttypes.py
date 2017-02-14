"""
FactTypes
---------

Fact's values must be a facttype instantiated,
that is:

    - ``pyknow.fact.L`` - Literal
    - ``pyknow.fact.W`` - Wildcard
    - ``pyknow.fact.C`` - Capture
    - ``pyknow.fact.T`` - Test (callable)
    - ``pyknow.fact.V`` - Value (captured value)
    - ``pyknow.fact.N`` - NOT value (captured value)

In this module we provide those facttypes and its
helper methods, plus the valueset objects we'll use
to group them and match them by type.

Fact matching process is as follows::

    - Fact.matches(other) -> extract fact's keys and values
                          -> extract other's keys and values
                          -> If not all our keys are present in other's keys
                             return False
                          -> If our type is not the same as the other, return
                             False
                          -> group ours' and others' values by FactType
                          -> compare each group, if any of them returns
                             False (that'll mean both have the KEY but
                             non-matching values) return False
                          -> Return True

"""

from contextlib import suppress
from .config import PYKNOW_STRICT

# pylint: disable=invalid-name, too-few-public-methods, no-member


class FactType:
    """

    Base FactType, defaults to a simple literal and provide
    fact type resolution methods to determine the type
    of a given `Fact` child.

    This is the base implementation of a ``Pattern CE``, able
    to handle object resolution and identification to
    match via valuesets

    """
    def __init__(self, value):
        self.value = value
        self.key = False

    def resolve(self, _=False):
        """
        Basic resolution of the value.

        """
        return self.value

    def __eq__(self, other):
        if not other.__class__ == self.__class__:
            return False
        return self.value == other.value

    def __hash__(self):
        return hash(self.value)

    def __repr__(self):
        return "{}(\"{}\")".format(self.__class__.__name__, self.resolve())


class L(FactType):
    """
    ``Literal constraint``

    This is a basic-types constraint (integers, strings, booleans)

    """

    pass


class T(FactType):
    """
    ``Predicate constraint.``

    This is the equivalent to using a variable binding, calling a predicate
    function and return a boolean state

    """
    def __init__(self, value):
        super().__init__(value)
        self.callable = value

    def resolve(self, to_what=L(False)):
        """
        Allows:

        Fact(name=T(lambda c, x: x.startswith('foo'))
        Fact(name=T(lambda c, x: L("foo")))
        Fact(name=T(lambda c, x='foo': L(x)))

        Defaults to L(False)
        """

        return self.callable(self.context, to_what.resolve())

    def __repr__(self):
        return "{}(\"{}\")".format(self.__class__.__name__,
                                   self.callable.__name__)


def N(dest):
    """
    Matcher using ``pyknow.fact.T`` returning
    True if the given context's value is NOT the same as our own.
    """
    return T(lambda context, value: context[dest] != value)


def V(dest):
    """
    Matcher using ``pyknow.fact.T`` returning
    True if the given context's value is the same as our own.
    """
    return T(lambda context, value: context[dest] == value)


class C(FactType):
    """
    Captures a value in the :obj:`pyknow.engine.KnowledgeEngine`'s
    :obj:`pyknow.fact.Context` by its assigned name. This way we can
    compare values from different `pyknow.fact.FactType`.

    """
    pass


class W(FactType):
    """
    Almost like the literal facttype

    Except only allowing True/False, this one
    will be used as a "key wildcard" when compared within
    WValueSet.
    """

    def __init__(self, value):
        super().__init__(value)
        if not isinstance(value, bool):
            raise ValueError("Wildcard value must be True/False")
        self.value = value
        self.key = False


class ValueSet:
    """
    Represents a valueset as an iterator able to resolve itself

    Facts are grouped by its `pyknow.fact.FactType`, and in the
    base valueset we only allow literal types
    (see :func:`pyknow.fact.FactType.is_literal`)

    """

    def __init__(self, parent, type_):
        self.value = set()
        self._resolved = None
        self.current = 0
        self.parent = parent
        self.type_ = type_

    def matches(self, other):
        """
        Returns, depending on the type we're matching,
        its matched value
        """
        return getattr(self, "matches_{}".format(self.type_))(other)

    @property
    def keyset(self):
        """
        Convert our value keys to a set for
        faster comparision
        """
        return set([a for a, b in self.value])

    @property
    def valueset(self):
        """
        Convert our value values to a set for
        faster comparision
        """
        return set([b for a, b in self.value])

    @property
    def context(self):
        """
        Returns the asigned :obj:`pyknow.engine.KnowledgeEngine`'s
        :obj:`pyknow.fact.Context`
        """

        return self.parent.context

    @property
    def resolved(self):
        """
        For each FactType declared as value for this fact,
        that we have in this valueset (thus matches our defined
        FactType), resolve its value and keep it cached
        """

        if self._resolved is None:
            self._resolved = {(a, b.resolve()) for a, b in self.value}
        return self._resolved

    def __iter__(self):
        return self

    def __next__(self):
        with suppress(KeyError):
            return self.resolved.pop()
        raise StopIteration()

    def __len__(self):
        return len(self.resolved)

    def matches_L(self, other):
        """
        Matches literal valueset.

        If we don't have any literal values in this fact,
        returns true so we can continue testing others.

        Otherwise, check that the other fact contains AT
        LEAST all our values.

        .. note:: this means that, if the other value has
                  MORE values, we'll still match.
        """

        if not self.resolved:
            return True
        return other.valuesets['L'].resolved.issuperset(self.resolved)

    def matches_T(self, other):
        """
        Evaluate callable, returns evaluation result
        """
        if not self.value:
            return True

        if self.keyset - other.keyset:
            # If we have any key that the other item
            # does not have, we cannot match
            return False

        for key, value in self.value:
            # pylint: disable=broad-except
            try:
                return value.resolve(other.value[key])
            except Exception:
                if PYKNOW_STRICT:
                    raise
                return False

    def matches_W(self, other):
        """
        - If ANY value is True and is not in keyset, False
        - If ANY value is False and is in keyset, False
        - Otherwise, True
        """
        for key, value in self:
            present = key in other.keyset
            if value and (not present):
                return False
            elif (not value) and present:
                return False
        return True

    def matches_C(self, other):
        """
        Gets a resolved value from the ``other`` fact.
        If the other fact didn't contain the value, return False

        """

        if self.keyset - other.keyset:
            # If there is any key on our keyset
            # that we don't have in the other fact's keyset,
            # it means we cannot capture a fact value, so
            # we don't match
            return False

        for key, value in self.value:
            key_ = value.resolve(other.value[key])
            self.context[key_] = other.value[key].resolve()

        return True

FACT_TYPES = ["L", "C", "T", "W"]
