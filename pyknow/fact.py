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


class FactType:
    """
        Base FactType, defaults to a simple literal
    """
    def __init__(self, value):
        self.value = value

    def resolve(self, extra=False):
        """ Basic resolution of the value. """
        return self.value

    @property
    def is_wildcard(self):
        """ Check if we are a wildcard """
        return not self.is_callable and self.value in FactState

    @property
    def is_literal(self):
        """ Check if we are a literal type """
        return not self.is_callable and not self.is_wildcard

    @property
    def is_callable(self):
        """ Check if we are a callable type """
        return hasattr(self, 'callable')


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


class ValueSet:
    """
        Represents a valueset as an iterator able to resolve itself
    """
    cond = "is_literal"

    def __init__(self, fact):
        self.fact = fact
        self.value = set()
        self._resolved_values = None
        self.current = 0

    @property
    def resolved(self):
        """ Resolve """
        if self._resolved_values is None:
            self._resolved_values = {(a, b.resolve()) for a, b in self.value}
        return self._resolved_values

    def condition(self, value):
        """ How to decide if a value is for this set """
        return getattr(value, self.cond)

    def add(self, key, value):
        """ Add an item if it meets condition """
        if self.condition(value):
            self.value.add((key, value))

    def __iter__(self):
        return self

    def __next__(self):
        with suppress(KeyError):
            return self.resolved.pop()
        raise StopIteration()

    def __len__(self):
        return len(self.resolved)

    def __contains__(self, other):
        for key, value in self.resolved:
            if self.fact.skip_key(key):
                continue
            else:
                if not (key, value) in other.resolved:
                    return False
        return True


class CValueSet(ValueSet):
    """ Valueset evaluable for Callable facttypes"""
    cond = "is_callable"

    def __contains__(self, other):
        if not self.value:
            return True
        for key, value in self.value:
            if key not in other.keyset:
                return False
            try:
                othervalue = dict(other.resolved)[key]
                result = value.callable(othervalue)
                assert result
                return True
            except Exception:
                return False


class WValueSet(ValueSet):
    """ Wildcard value set """
    cond = "is_wildcard"

    def __contains__(self, fact):
        """
            - If ANY value is DEFINED and is not in keyset, fail
            - If ANY value is UNDEFINED and is in keyset, fail
            - Otherwise, true
        """
        def _contains():
            for key, value in self:
                if value is FactState.DEFINED and key not in fact.keyset:
                    return False
                elif value is FactState.UNDEFINED and key in fact.keyset:
                    return False
                fact.add_key_to_skip(key)
            return True
        return not _contains()


class Fact:
    """
        Base Fact class
    """
    def __init__(self, **value):
        self.value = value

        for val in value.values():
            if not isinstance(val, FactType):
                raise TypeError("Fact values inherit from FactType")

        self._keys_to_skip = set()
        self.keyset = set(value.keys())

        self.valueset = ValueSet(self)
        self.wcvalueset = WValueSet(self)
        self.callablevalueset = CValueSet(self)

        for key, value in self.value.items():
            self.valueset.add(key, value)
            self.wcvalueset.add(key, value)
            self.callablevalueset.add(key, value)

    def add_key_to_skip(self, key):
        """ Add a key to the ignore list """
        self._keys_to_skip.add(key)

    def skip_key(self, key):
        """ Checks if a key is to be skipped """
        return key in self._keys_to_skip

    def _contain_wcvalueset(self, other):
        """
            If we contain a wildcard, apply the needed logic
            for __contains__
        """
        # We have some wildcards.
        if other not in self.callablevalueset:
            return False

        elif other in self.wcvalueset:
            return False

        elif other not in self.valueset:
            return False
        return True

    def _contains_valueset(self, other):
        """
            If we contain a valueset, apply the needed logic
            for __contains__
        """
        if other not in self.callablevalueset:
            return False

        return self.valueset.resolved.issuperset(other.valueset.resolved)

    def __contains__(self, other):
        """Does this Fact contain ``other``?."""
        if self.__class__ != other.__class__:
            return False
        elif not self.value:
            return True
        elif self.wcvalueset:
            return self._contain_wcvalueset(other)
        else:
            return self._contains_valueset(other)
        return True

    def __eq__(self, other):
        return self.value == other.value


class InitialFact(Fact):
    """
        InitialFact
    """
    pass
