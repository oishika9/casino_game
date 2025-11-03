import pytest
from Horse import Horse

def test_horse_copy_and_victory():
    h = Horse(3, False)
    assert h.get_number() == 3
    assert not h.was_victorious()

    h2 = Horse.copy(h)
    assert h2 is not h
    assert h2.get_number() == 3
    assert not h2.was_victorious()

    h2.set_victory(True)
    assert h2.was_victorious()
    assert not h.was_victorious()

def test_invalid_init():
    with pytest.raises(AssertionError):
        Horse("one", False)
    with pytest.raises(AssertionError):
        Horse(1, "yes")
