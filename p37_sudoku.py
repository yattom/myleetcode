# TODO
# 数独を解く
# - [x] 確定できる数字を置く
#   - [x] 横一行だけで確定できる数字を置く
#   - [x] 数字を確定できない場合
#   - [ ] 縦一列だけで確定できる数字を置く
#   - [ ] 3x3ブロックだけで確定できる数字を置く
#   - [x] 組み合わせで確定できる数字を置く
# - [ ] 行き詰まったら仮置きを戻す (バックトラック)
#   - [x] 可能な手をすべて確認する
#   - [x] 可能な手を見つけてさらに探索する
#   - [x] 行き詰まったらバックトラックする
#   - [ ] バックトラックしたとき状態も戻す
# - [ ] 数字を仮置きして進める
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


class Testバックトラック:
    @staticmethod
    def try_possibilities(solve_by, search_next_moves):
        moves = []
        while True:
            moves = search_next_moves() + moves
            if not moves:
                break
            m = moves.pop(0)
            if solve_by(m):
                return True
        return False

    def test_可能な手をすべて確認する(self):
        # arrange
        tried = []
        def _1はNGで2はOK(p):
            tried.append(p)
            return p == 2
        def search_next_moves():
            return [1, 2] if not tried else []
        # act
        solved = Testバックトラック.try_possibilities(solve_by=_1はNGで2はOK,
                                                      search_next_moves=search_next_moves)
        # assert
        assert solved
        assert tried == [1, 2]

    def test_可能な手を見つけてさらに探索する(self):
        # arrange
        tried = []
        def _1の後2はNGで3の後4はOK(p):
            tried.append(p)
            return len(tried) >= 2 and tried[-2] == 3 and tried[-1] == 4

        def 最初は1_3で1の後2を試し3の後は4を試す():
            if len(tried) == 0:
                return [1, 3]
            if tried[-1] == 1:
                return [2]
            if tried[-1] == 3:
                return [4]
            return []

        # act
        solved = Testバックトラック.try_possibilities(solve_by=_1の後2はNGで3の後4はOK,
                                                      search_next_moves=最初は1_3で1の後2を試し3の後は4を試す)
        # assert
        assert solved
        assert tried == [1, 2, 3, 4]

    def test_行き詰まったらバックトラックする(self):
        # arrange
        tried = []
        def _1の後2はNGで3の後4はOK(p):
            tried.append(p)
            return len(tried) >= 2 and tried[-2] == 3 and tried[-1] == 4

        def 最初は101と201と301でそれぞれプラス1ずつして1桁が3に達したら行き詰まる():
            seqs = [[101, 102, 103], [201, 202, 203], [301, 302, 303]]
            if len(tried) == 0:
                return [a[0] for a in seqs]
            for a in seqs:
                for i, v in enumerate(a):
                    if v == tried[-1]:
                        if i + 1 < len(a):
                            return [a[i + 1]]
                        return []

        # act
        solved = Testバックトラック.try_possibilities(solve_by=_1の後2はNGで3の後4はOK,
                                                      search_next_moves=最初は101と201と301でそれぞれプラス1ずつして1桁が3に達したら行き詰まる)
        # assert
        assert not solved
        assert tried == [101, 102, 103, 201, 202, 203, 301, 302, 303]


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

