"""
    Fact and FactTypes.
    -------------------

    Facts are used both as definitions on rules and as facts.
    Facts MUST be of type ``Fact`` and its values should be of type
    ``FactType``.

    When declaring a fact in a KnowledgeEngine, fact must only be
    of type ``L``, or not inherit from ``FactType`` (wich defaults to L)

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


class Context(dict):
    """
        Context that will be used in facttypes
    """
    def __init__(self):
        self._facts = []
        self._others = []

    def set_fact(self, fact):
        """ Set fact """
        self._facts.append(fact)

    def set_other(self, other):
        """ Set other """
        self._others.append(other)

    def capture(self, key, value):
        self[key] = value


class FactType:
    """
        Base FactType, defaults to a simple literal
    """
    def __init__(self, value):
        self.value = value
        self.key = False

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
        return isinstance(self, C)


class L(FactType):
    """
        Literal FactType, just compare values
    """
    def __repr__(self):
        return "<pyknow.fact.L({}>".format(self.resolve())


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
        othervalue = to_what.resolve()
        return self.callable(othervalue)


class C(FactType):
    """
        Capture a value
    """
    pass


class V(FactType):
    """
        Use a captured value
    """
    def resolve(self, to_what):
        """ Get a value from the context """
        if not self.context:
            raise ValueError("Cant use C/V types without asigning a context")
        return self.context[to_what]


class ValueSet:
    """
        Represents a valueset as an iterator able to resolve itself
    """
    cond = "is_literal"

    def __init__(self, parent):
        self.value = set()
        self._resolved_values = None
        self._cached_values = set()
        self.current = 0
        self.parent = parent

    @property
    def context(self):
        """ Use fact context """
        return self.parent.context

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
            value.key = key
            self.value.add((key, value))

    def reset(self):
        """ Restarts resolved """
        self.resolved
        self._resolved_values = self._cached_values.copy()

    def __iter__(self):
        return self

    def __next__(self):
        self.parent.populate()
        with suppress(KeyError):
            return self.resolved.pop()
        raise StopIteration()

    def __len__(self):
        return len(self.resolved)

    def matches(self, other):
        """
            Checks if our valueset is a superset of the other valueset
        """
        self.resolved
        self.context.set_fact(self)
        self.context.set_other(other)


class LValueSet(ValueSet):
    """ Literal value set """
    def matches(self, other):
        """
            Foo
        """
        super().matches(other)
        if not self.resolved:
            return True
        other.populate()
        return other.valueset.resolved.issuperset(self.resolved)


class CValueSet(ValueSet):
    """ Valueset evaluable for Callable facttypes"""
    cond = "is_callable"

    def matches(self, other):
        super().matches(other)

        if not self.value:
            return True
        for key, value in self.value:
            if key not in other.keyset:
                return False
            try:
                result = value.resolve(other.value[key])
                assert result
                return True
            except Exception:
                return False

    @property
    def resolved(self):
        """ Resolve """
        if self._resolved_values is None:
            self._resolved_values = {(a, b) for a, b in self.value}
            self._cached_values = self._resolved_values.copy()
        return self._resolved_values



class WValueSet(ValueSet):
    """ Wildcard value set """
    cond = "is_wildcard"

    def matches(self, other):
        """
            - If ANY value is DEFINED and is not in keyset, fail
            - If ANY value is UNDEFINED and is in keyset, fail
            - Otherwise, true
        """
        super().matches(other)
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
        super().matches(other)
        atleastone = False

        for key, value in self.value:
            if key not in other.keyset:
                continue
            atleastone = True
            self.context.capture(key, value.resolve(other.value[key]))

        if atleastone:
            return True

        return False


class ValValueSet(ValueSet):
    """ Captured values value set"""
    cond = "is_capturedvalue"

    @property
    def resolved(self):
        """ Resolve """
        if self._resolved_values is None:
            self._resolved_values = {(a, b.resolve(a)) for a, b in self.value}
            self._cached_values = self._resolved_values.copy()
        return self._resolved_values


class Fact:
    """
        Base Fact class
    """
    def __init__(self, **value):
        self.is_matcher = False
        for key, val in value.items():
            if isinstance(val, FactType) and not isinstance(val, L):
                self.is_matcher = True
            if not isinstance(val, FactType):
                value[key] = L(val)

        self.value = value
        self.keyset = set(value.keys())
        self.populated = False
        self._context = False
        self._valueset = False
        self._capvalueset = False
        self._wcvalueset = False
        self._callablevalueset = False
        self.rule = False

    def __repr__(self):
        return "<pyknow.fact.Fact object with value [{}] >".format(self.value)

    @property
    def context(self):
        if self.rule:
            if self.rule.context is not None:
                return self.rule.context
            else:
                return Context()
        return self._context

    @property
    def valueset(self):
        if not self._valueset:
            self.populate()
        return self._valueset

    @property
    def callablevalueset(self):
        if not self._callablevalueset:
            self.populate()
        return self._callablevalueset

    @property
    def wcvalueset(self):
        if not self._wcvalueset:
            self.populate()
        return self._wcvalueset

    @property
    def capvalueset(self):
        if not self._capvalueset:
            self.populate()
        return self._capvalueset

    def populate(self, context=False):
        """
            Load data, if not already done.
            This has been forced outside init because we need to
            lazy-load it so it can have the context object available,
            wich is done after Rule() initialization
        """
        if not self.context:
            if context:
                self._context = context
            else:
                self._context = Context()

        if not self.populated:
            self._valueset = LValueSet(self)
            self._wcvalueset = WValueSet(self)
            self._callablevalueset = CValueSet(self)
            self._capvalueset = CapValueSet(self)

            for key, value in self.value.items():
                self._valueset.add(key, value)
                self._wcvalueset.add(key, value)
                self._callablevalueset.add(key, value)
                self._capvalueset.add(key, value)

    def _contains(self, other):
        """
            If we contain a wildcard, apply the needed logic
            for __contains__
        """
        self.populate()
        # Get cap values
        self.capvalueset.matches(self)

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
        if not other.value.keys() == self.value.keys():
            return False
        for key, value in self.value.items():
            if not value.__class__ == value.__class__:
                return False
            if not other.value[key].value == self.value[key].value:
                return False
        return True


class InitialFact(Fact):
    """
        InitialFact
    """
    pass
