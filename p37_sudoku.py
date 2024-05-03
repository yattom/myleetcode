# TODO
# 数独を解く
# - [x] 確定できる数字を置く
#   - [x] 横一行だけで確定できる数字を置く
#   - [x] 数字を確定できない場合
#   - [ ] 縦一列だけで確定できる数字を置く
#   - [ ] 3x3ブロックだけで確定できる数字を置く
#   - [x] 組み合わせで確定できる数字を置く
# - [ ] 数字を仮置きして進める
# - [ ] 行き詰まったら仮置きを戻す (バックトラック)
# - [ ] 現在の状態を保持する


class Test確定できる数字を置く:
    def test_横一列で確定できる(self):
        # arrange
        sudoku = Sudoku([[".", "8", "7", "6", "5", "4", "3", "2", "1"]])
        # act
        value = sudoku.get_cell_value_if_fixed(0, 0)
        # assert
        assert value == "9"

    def test_確定できない(self):
        # arrange
        sudoku = Sudoku([["."]])
        # act
        value = sudoku.get_cell_value_if_fixed(0, 0)
        # assert
        assert value == None

    def test_組み合わせで確定できる(self):
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

    def get_row(self, row: int) -> list[str]:
        return [c for c in self.cells[row]]

    def get_col(self, col: int) -> list[str]:
        return [r[col] for r in self.cells if len(r) > col]

    def get_block(self, col: int, row: int) -> list[str]:
        return [self.get_cell((row // 3) * 3 + r, (col // 3) * 3 + c) for c in range(3) for r in range(3)]

    def get_cell(self, row: int, col: int) -> str:
        if len(self.cells) <= row or len(self.cells[row]) <= col:
            return "."
        return self.cells[row][col]

    def get_cell_value_if_fixed(self, col: int, row: int) -> str | None:
        available = set(["1", "2", "3", "4", "5", "6", "7", "8", "9"])
        used = set(self.get_row(row) + self.get_col(col) + self.get_block(row, col)) - set(["."])
        possible = available - used
        if len(possible) == 1:
            return possible.pop()
        else:
            return None

