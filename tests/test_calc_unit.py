import pytest
from app.calc import compute

def test_compute_add():
    assert compute("add", 2, 3) == 5.0

def test_compute_div_zero():
    with pytest.raises(ValueError):
        compute("div", 1, 0)

def test_compute_pow():
    assert compute("pow", 2, 4) == 16.0
