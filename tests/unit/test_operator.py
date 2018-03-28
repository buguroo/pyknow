import pytest
import re

from pyknow import KnowledgeEngine, Rule, Fact
from pyknow.operator import TRUTH, LT, LE, EQ, NE, GE, GT, IS, IS_NOT
from pyknow.operator import CONTAINS, BETWEEN, CALL, REGEX, LIKE, ILIKE


@pytest.mark.parametrize("operator,x,expected", [
    (TRUTH, 1, True),
    (TRUTH, 0, False),
    (LT(3), 2, True),
    (LT(3), 3, False),
    (LE(3), 3, True),
    (LE(3), 4, False),
    (EQ(3), 3, True),
    (EQ(3), 2, False),
    (NE(3), 2, True),
    (NE(3), 3, False),
    (GE(3), 3, True),
    (GE(3), 2, False),
    (GT(3), 4, True),
    (GT(3), 3, False),
    (IS(None), None, True),
    (IS(True), False, False),
    (IS_NOT(None), False, True),
    (IS_NOT(None), None, False),
    (CONTAINS(1), [1, 2, 3], True),
    (CONTAINS(1), [2, 3, 4], False),
    (BETWEEN(2, 3), 2, True),
    (BETWEEN(2, 3), 4, False),
    (CALL.startswith("Y"), "Yes", True),
    (CALL.startswith("Y"), "No", False),
    (REGEX(r"^A[0-9]$"), "A5", True),
    (REGEX(r"^A[0-9]$"), "A5 ", False),
    (REGEX(r"^A[0-9]$", flags=re.IGNORECASE), "a5", True),
    (REGEX(r"^A[0-9]$", flags=re.IGNORECASE), "a5 ", False),
    (LIKE("*.txt"), "file.txt", True),
    (LIKE("*.txt"), "file.pdf", False),
    (ILIKE("*.txt"), "FILE.PDF", False),
    (ILIKE("*.txt"), "FILE.PDF", False)])
def test_comparators(operator, x, expected):

    class KE(KnowledgeEngine):
        result = False

        @Rule(Fact(operator))
        def istrue(self):
            self.result = True

    ke = KE()
    ke.reset()
    ke.declare(Fact(x))
    ke.run()

    assert ke.result == expected
