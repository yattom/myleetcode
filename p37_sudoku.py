# TODO
# 数独を解く
# - [ ] 確定できる数字を置く
# - [ ] 数字を仮置きして進める
# - [ ] 行き詰まったら仮置きを戻す (バックトラック)
# - [ ] 現在の状態を保持する


def test_確定できる数字を置く():
    # arrange
    sudoku = Sudoku([[".", "8", "7", "6", "5", "4", "3", "2", "1"]])
    # act
    value = sudoku.fix_cell(0, 0)
    # assert
    assert value == "9"


class Sudoku:
    def __init__(self, cells: list[list[str]]):
        self.cells = cells

    def fix_cell(self, col: int, row: int) -> str:
        available = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
        for c in self.cells[row]:
            if c == ".":
                continue
            available.remove(c)
        return available[0]


