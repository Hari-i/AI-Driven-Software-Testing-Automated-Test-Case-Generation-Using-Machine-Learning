import pytest
from math_utils import subtract, divide, factorial

def test_subtract():
    assert subtract(5, 3) == 2
    assert subtract(10, 0) == 10
    assert subtract(0, 8) == -8

def test_divide():
    assert divide(10, 2) == 5.0
    assert divide(9, 3) == 3.0
    with pytest.raises(ValueError):
        divide(10, 0)

def test_factorial():
    assert factorial(3) == 6
    assert factorial(5) == 120
    assert factorial(0) == 1
    assert factorial(1) == 1
    with pytest.raises(ValueError):
        factorial(-1)