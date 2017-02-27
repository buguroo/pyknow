Activations / Capturations problems
-----------------------------------

Currently, we make the product of the capturations against
the activations to match facts against other activations.

That means this::

    Rule(Fact(a=C('a')), Fact(b=V('a')))

    declare(Fact(a=1))
    declare(Fact(b=1))

Would work nicely, but this::

    Rule(Fact(a=C('a'), b=V('a')))

    declare(Fact(a=1, b=1))
    declare(Fact(a=1, b=3))


Will launch 2 activations, as it will try to match fact 2 against fact 1's extracted
context, and it'll match.
