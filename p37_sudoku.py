# TODO
# 数独を解く
# - [ ] 確定できる数字を置く
#   - [x] 横一行だけで確定できる数字を置く
#   - [x] 数字を確定できない場合
#   - [ ] 縦一列だけで確定できる数字を置く
#   - [ ] 3x3ブロックだけで確定できる数字を置く
#   - [ ] 組み合わせで確定できる数字を置く
# - [ ] 数字を仮置きして進める
# - [ ] 行き詰まったら仮置きを戻す (バックトラック)
# - [ ] 現在の状態を保持する


def test_確定できる数字を置く():
    # arrange
    sudoku = Sudoku([[".", "8", "7", "6", "5", "4", "3", "2", "1"]])
    # act
    value = sudoku.get_cell_value_if_fixed(0, 0)
    # assert
    assert value == "9"


def test_確定できる数字を置く_2行目 ():
    # arrange
    sudoku = Sudoku([[], [".", "8", "7", "6", "5", "4", "3", "2", "1"]])
    # act
    value = sudoku.get_cell_value_if_fixed(0, 1)
    # assert
    assert value == "9"

def test_確定できる数字を置く_数字を確定できない場合():
    # arrange
    sudoku = Sudoku([["."]])
    # act
    value = sudoku.get_cell_value_if_fixed(0, 0)
    # assert
    assert value == None

def test_確定できる数字を置く_組み合わせ():
    # arrange
    sudoku = Sudoku([
        [".", ".", ".", ".", ".", ".", "3", "2", "1"],
        [".", "8", "."],
        [".", ".", "7"],
        ["6"],
        ["5"],
        ["4"],
        ["."],
        ["."],
        ["."],
    ])
    # act
    value = sudoku.get_cell_value_if_fixed(0, 0)
    # assert
    assert value == "9"



class Sudoku:
    def __init__(self, cells: list[list[str]]):
        self.cells = cells

    def get_cell_value_if_fixed(self, col: int, row: int) -> str | None:
        available = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
        for c in self.cells[row]:
            if c == ".":
                continue
            available.remove(c)
        if len(available) == 1:
            return available[0]
        else:
            return None


