import pytest
import random
from BandOfHorses import BandOfHorses
from Horse import Horse

def test_deep_copy_horses_independent():
    original = [Horse(i, False) for i in range(1,4)]
    band = BandOfHorses(original)
    copy = band.deep_copy_horses()
    assert copy is not band
    original[0].set_victory(True)
    assert not copy._get_horses()[0].was_victorious()

def test_is_first():
    horses = [Horse(1, False), Horse(2, False)]
    band = BandOfHorses(horses)
    assert band.is_first(horses[0])
    assert not band.is_first(horses[1])

def test_figure_out_winner_monkeypatched(monkeypatch):
    seq = [Horse(1, False), Horse(2, False), Horse(3, False)]
    band = BandOfHorses(seq)
    def fake_shuffle(x):
        x[:] = [seq[2], seq[1], seq[0]]
    monkeypatch.setattr(random, "shuffle", fake_shuffle)

    new_band = band.figure_out_winner()
    ranking = new_band._get_horses()
    # new first horse gets victory flag
    assert ranking[0].was_victorious()
    # returns fresh BandOfHorses
    assert isinstance(new_band, BandOfHorses)
