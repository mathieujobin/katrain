import pytest

from board import Board, IllegalMoveException
from move import Move


class TestBoard:
    def nonempty_chains(self, b):
        return [c for c in b.chains if c]

    def test_merge(self):
        b = Board(9)
        b.play(Move(gtpcoords="B9", player=0))
        b.play(Move(gtpcoords="A3", player=0))
        b.play(Move(gtpcoords="A9", player=0))
        assert 2 == len(self.nonempty_chains(b))
        assert 3 == len(b.stones)
        assert 0 == len(b.prisoners)

    def test_collide(self):
        b = Board(9)
        b.play(Move(gtpcoords="B9", player=0))
        with pytest.raises(IllegalMoveException):
            b.play(Move(gtpcoords="B9", player=1))
        assert 1 == len(self.nonempty_chains(b))
        assert 1 == len(b.stones)
        assert 0 == len(b.prisoners)

    def test_capture(self):
        b = Board(9)
        b.play(Move(gtpcoords="A2", player=0))
        b.play(Move(gtpcoords="B1", player=1))
        b.play(Move(gtpcoords="A1", player=1))
        b.play(Move(gtpcoords="C1", player=0))
        assert 3 == len(self.nonempty_chains(b))
        assert 4 == len(b.stones)
        assert 0 == len(b.prisoners)
        b.play(Move(gtpcoords="B2", player=0))
        assert 2 == len(self.nonempty_chains(b))
        assert 3 == len(b.stones)
        assert 2 == len(b.prisoners)
        b.play(Move(gtpcoords="B1", player=0))
        with pytest.raises(IllegalMoveException) as exc:
            b.play(Move(gtpcoords="A1", player=1))
        assert "Suicide" in str(exc.value)
        assert 1 == len(self.nonempty_chains(b))
        assert 4 == len(b.stones)
        assert 2 == len(b.prisoners)

    def test_snapback(self):
        b = Board(9)
        for move in ["C1", "D1", "E1", "C2", "D3", "E4", "F2", "F3", "F4"]:
            b.play(Move(gtpcoords=move, player=0))
        for move in ["D2", "E2", "C3", "D4", "C4"]:
            b.play(Move(gtpcoords=move, player=1))
        assert 5 == len(self.nonempty_chains(b))
        assert 14 == len(b.stones)
        assert 0 == len(b.prisoners)
        b.play(Move(gtpcoords="E3", player=1))
        assert 4 == len(self.nonempty_chains(b))
        assert 14 == len(b.stones)
        assert 1 == len(b.prisoners)
        b.play(Move(gtpcoords="D3", player=0))
        assert 4 == len(self.nonempty_chains(b))
        assert 12 == len(b.stones)
        assert 4 == len(b.prisoners)

    def test_ko(self):
        b = Board(9)
        for move in ["A2", "B1"]:
            b.play(Move(gtpcoords=move, player=0))

        for move in ["B2", "C1"]:
            b.play(Move(gtpcoords=move, player=1))
        b.play(Move(gtpcoords="A1", player=1))
        assert 4 == len(self.nonempty_chains(b))
        assert 4 == len(b.stones)
        assert 1 == len(b.prisoners)
        with pytest.raises(IllegalMoveException) as exc:
            b.play(Move(gtpcoords="B1", player=0))
        assert "Ko" in str(exc.value)

        b.play(Move(gtpcoords="B1", player=0), ignore_ko=True)
        assert 2 == len(b.prisoners)

        with pytest.raises(IllegalMoveException) as exc:
            b.play(Move(gtpcoords="A1", player=1))

        b.play(Move(gtpcoords="F1", player=1))
        b.play(Move(coords=(None, None), player=0))
        b.play(Move(gtpcoords="A1", player=1))
        assert 3 == len(b.prisoners)
