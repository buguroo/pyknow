"""
    Fact and FactTypes.
    -------------------

    Facts are used both as definitions on rules and as facts.
    Facts MUST be of type ``Fact`` and its values must be of type
    ``FactType``.

"""
import enum
from contextlib import suppress


class FactState(enum.Enum):
    """
        '''Magic''' FactState.
        Defines two keys that, when used as literals, will
        be handled as wildcards.
    """
    DEFINED = 'DEFINED'
    UNDEFINED = 'UNDEFINED'


class FactTypeContext:
    """
        Context that will be used in facttypes
    """
    def __init__(self):
        self.facts_set = set()
        self.others_set = set()
        self.fact = False
        self.other = False

    def set_fact(self, fact):
        """ Set fact """
        self.facts_set.add(fact)
        self.fact = fact

    def set_other(self, other):
        """ Set other """
        self.other = other
        self.others_set.add(other)


class FactType:
    """
        Base FactType, defaults to a simple literal
    """
    def __init__(self, value):
        self.value = value
        self.context = False

    def resolve(self, _=False):
        """ Basic resolution of the value. """
        return self.value

    @property
    def is_wildcard(self):
        """ Check if we are a wildcard """
        if not isinstance(self, L):
            return False
        return self.value in FactState

    @property
    def is_literal(self):
        """ Check if we are a literal type """
        if not isinstance(self, L):
            return False
        return not self.is_wildcard

    @property
    def is_callable(self):
        """ Check if we are a callable type """
        return isinstance(self, T)

    @property
    def is_capturedvalue(self):
        """ Check if we are a captured value type"""
        return isinstance(self, V)

    @property
    def is_capture(self):
        """ Check if we are a capture-order value type"""
        print("--------------")
        return isinstance(self, C)


class L(FactType):
    """
        Literal FactType, just compare values
    """
    pass


class T(FactType):
    """
        Test Facttype, evaulates a callable against "other".
    """
    def __init__(self, value):
        super().__init__(value)
        self.callable = value

    def resolve(self, to_what=L(False)):
        """
            Allows:

            Rule(Fact(name=T(lambda x: x.startswith('foo')))
            Fact(name=T(lambda x: L("foo")))
            Fact(name=T(lambda x='foo': L(x)))

            Defaults to L(False)
        """
        self.callable(to_what.resolve())


class C(FactType):
    """
        Capture a value
    """
    pass


class V(FactType):
    """
        Use a captured value
    """
    pass


class ValueSet:
    """
        Represents a valueset as an iterator able to resolve itself
    """
    cond = "is_literal"

    def __init__(self):
        self.value = set()
        self._resolved_values = None
        self._cached_values = False
        self.current = 0
        self.context = FactTypeContext()

    @property
    def resolved(self):
        """ Resolve """
        if self._resolved_values is None:
            self._resolved_values = {(a, b.resolve()) for a, b in self.value}
            self._cached_values = self._resolved_values.copy()
        return self._resolved_values

    def condition(self, value):
        """ How to decide if a value is for this set """
        return getattr(value, self.cond)

    def add(self, key, value):
        """ Add an item if it meets condition """
        if self.condition(value):
            value.context = self.context
            self.value.add((key, value))

    def reset(self):
        """ Restarts resolved """
        self._resolved_values = self._cached_values.copy()

    def __iter__(self):
        return self

    def __next__(self):
        with suppress(KeyError):
            return self.resolved.pop()
        raise StopIteration()

    def __len__(self):
        return len(self.resolved)

    def matches(self, other):
        """
            Checks if our valueset is a superset of the other valueset
        """
        if not self.resolved:
            return True
        return self.resolved.issuperset(other.valueset.resolved)


class CValueSet(ValueSet):
    """ Valueset evaluable for Callable facttypes"""
    cond = "is_callable"

    def matches(self, other):
        # self.context.other = other
        if not self.value:
            return True
        for key, value in self.value:
            if key not in other.keyset:
                return False
            try:
                othervalue = other.value[key]
                result = value.callable(othervalue.resolve())
                assert result
                return True
            except Exception:
                return False


class WValueSet(ValueSet):
    """ Wildcard value set """
    cond = "is_wildcard"

    def matches(self, other):
        """
            - If ANY value is DEFINED and is not in keyset, fail
            - If ANY value is UNDEFINED and is in keyset, fail
            - Otherwise, true
        """
        for key, value in self:
            if value is FactState.DEFINED and key not in other.keyset:
                return False
            elif value is FactState.UNDEFINED and key in other.keyset:
                return False
        return True


class CapValueSet(ValueSet):
    """ Capture value value set """
    cond = "is_capture"

    def matches(self, other):
        pass


class ValValueSet(ValueSet):
    """ Captured values value set"""
    cond = "is_capturedvalue"

    def matches(self, other):
        pass


class Fact:
    """
        Base Fact class
    """
    def __init__(self, **value):
        self.value = value

        for val in value.values():
            val.context.set_fact(self)
            if not isinstance(val, FactType):
                raise TypeError("Fact values inherit from FactType")

        self.keyset = set(value.keys())

        self.valueset = ValueSet()
        self.wcvalueset = WValueSet()
        self.callablevalueset = CValueSet()

        for key, value in self.value.items():
            self.valueset.add(key, value)
            self.wcvalueset.add(key, value)
            self.callablevalueset.add(key, value)

    def _contains(self, other):
        """
            If we contain a wildcard, apply the needed logic
            for __contains__
        """
        # We have some wildcards.

        if not self.wcvalueset.matches(other):
            return False
        elif not self.callablevalueset.matches(other):
            return False
        elif not self.valueset.matches(other):
            # If wildcards match or we don't have wildcards
            self.wcvalueset.reset()
            if self.wcvalueset.resolved:
                # Maybe the other has wildcards
                return other.valueset.matches(self)
            return False

        return True

    def __contains__(self, other):
        """Does this Fact contain ``other``?."""
        if self.__class__ != other.__class__:
            return False
        elif not self.value:
            return True
        return self._contains(other)

    def __eq__(self, other):
        return self.value == other.value


class InitialFact(Fact):
    """
        InitialFact
    """
    pass
