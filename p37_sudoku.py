# TODO
# 数独を解く
# - [x] get_cell()の引数を入れ替える
# - [x] 確定できる数字を置く
#   - [x] 横一行だけで確定できる数字を置く
#   - [x] 数字を確定できない場合
#   - [-] 縦一列だけで確定できる数字を置く
#   - [-] 3x3ブロックだけで確定できる数字を置く
#   - [x] 組み合わせで確定できる数字を置く
# - [ ] 行き詰まったら仮置きを戻す (バックトラック)
#   - [x] 可能な手をすべて確認する
#   - [x] 可能な手を見つけてさらに探索する
#   - [x] 行き詰まったらバックトラックする
#   - [ ] バックトラックしたとき状態も戻す
# - [ ] 全体を動かす
#   - [x] すでに解けている問題を解く
#   - [x] 自明な問題を解く
#   - [ ] 仮置きが必要な問題を解く
#     - [x] try_possibilities()をプロダクトコードにする
#     - [x] solve_by()を実装する
#       - [x] 仮置きを前提に、確定できる数字を置く
#       - [x] 確定できなくなったら、また仮置きする
#     - [ ] search_next_moves()を実装する
#     - [ ] バックトラックするときに元の状態に戻す
#       - [ ] 進むときの手を保存する
#       - [ ] 保存した手を使って元に戻す
#   - [ ] まともな問題を解いて時間の様子を見る
# - [-] 数字を仮置きして進める
# - [-] 現在の状態を保持する
# - [x] 無限ループを直す
#   - [x] 問題が間違ってないか調べる
#   - [x] 途中経過を表示して何が起きているか調べる
#   - [-] 1ステップずつ結果を確認するようなテストを書く
#   - [x] テストを構造化
#     - [x] 無限ループのテストを整理して確定のテストにする
#     - [x] get_colのテスト
# - [ ] 座標の取り扱い
#   - [ ] 座標オブジェクト
#   - [ ] colとrowを別の型にする
# - [ ] 全網羅する自動テストを書く
#   - やらない

import pytest


def make_sudoku(s):
    return Sudoku([list(l.replace(' ', '')) for l in s.split('\n') if len(l) > 0])


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

    def test_確定できないセルの先に確定できるセルがある(self):
        sudoku = make_sudoku(
'''
            . 3 . 6 7 8 9 1 2
            6 7 2 1 9 5 3 4 8
            1 9 8 3 4 2 5 6 7
            8 5 9 7 6 1 4 2 3
            . 2 6 8 5 3 7 9 1
            7 1 3 9 2 4 8 5 6
            9 6 1 5 3 7 2 8 4
            2 8 7 4 1 9 6 3 5
            3 4 . 2 8 6 1 7 9
'''
        )
        # act
        value = sudoku.get_cell_value_if_fixed(0, 4)
        # assert
        assert value == "4"

    class Test横列の網羅:
        def test_最初の行(self):
            sudoku = make_sudoku(
'''
                . 3 4 6 7 8 9 1 2
                6 7 2 1 9 5 3 4 8
                1 9 8 3 4 2 5 6 7
                8 5 9 7 6 1 4 2 3
                4 2 6 8 5 3 7 9 1
                7 1 3 9 2 4 8 5 6
                9 6 1 5 3 7 2 8 4
                2 8 7 4 1 9 6 3 5
                3 4 5 2 8 6 1 7 9
'''
            )
            # act
            value = sudoku.get_cell_value_if_fixed(0, 0)
            # assert
            assert value == "5"

        def test_左上のブロック(self):
            sudoku = make_sudoku(
'''
                5 3 4 6 7 8 9 1 2
                . 7 2 1 9 5 3 4 8
                1 9 8 3 4 2 5 6 7
                8 5 9 7 6 1 4 2 3
                4 2 6 8 5 3 7 9 1
                7 1 3 9 2 4 8 5 6
                9 6 1 5 3 7 2 8 4
                2 8 7 4 1 9 6 3 5
                3 4 5 2 8 6 1 7 9
'''
            )
            # act
            value = sudoku.get_cell_value_if_fixed(0, 1)
            # assert
            assert value == "6"

        def test_左中のブロック(self):
            sudoku = make_sudoku(
'''
                5 3 4 6 7 8 9 1 2
                6 7 2 1 9 5 3 4 8
                1 9 8 3 4 2 5 6 7
                8 5 9 7 6 1 4 2 3
                . 2 6 8 5 3 7 9 1
                7 1 3 9 2 4 8 5 6
                9 6 1 5 3 7 2 8 4
                2 8 7 4 1 9 6 3 5
                3 4 5 2 8 6 1 7 9
'''
            )
            # act
            value = sudoku.get_cell_value_if_fixed(0, 4)
            # assert
            assert value == "4"

        def test_最後の行(self):
            # arrange
            sudoku = make_sudoku(
'''
                5 3 4 6 7 8 9 1 2
                6 7 2 1 9 5 3 4 8
                1 9 8 3 4 2 5 6 7
                8 5 9 7 6 1 4 2 3
                4 2 6 8 5 3 7 9 1
                7 1 3 9 2 4 8 5 6
                9 6 1 5 3 7 2 8 4
                2 8 7 4 1 9 6 3 5
                . 4 5 2 8 6 1 7 9
'''
            )
            # act
            value = sudoku.get_cell_value_if_fixed(0, 8)
            # assert
            assert value == "3"


class Test行や列やブロックの取得:
    def test_get_block(self):
        # arrange
        sudoku = make_sudoku(
'''
            5 3 4 6 7 8 9 1 2
            6 7 2 1 9 5 3 4 8
            1 9 8 3 4 2 5 6 7
            8 5 9 7 6 1 4 2 3
            . 2 6 8 5 3 7 9 1
            7 1 3 9 2 4 8 5 6
            9 6 1 5 3 7 2 8 4
            2 8 7 4 1 9 6 3 5
            3 4 5 2 8 6 1 7 9
'''
        )
        # act
        block = sudoku.get_block(0, 4)
        # assert
        assert block == ['8', '5', '9', '.', '2', '6', '7', '1', '3']

    def test_get_row(self):
        # arrange
        sudoku = make_sudoku(
'''
            5 3 4 6 7 8 9 1 2
            6 7 2 1 9 5 3 4 8
            1 9 8 3 4 2 5 6 7
            8 5 9 7 6 1 4 2 3
            . 2 6 8 5 3 7 9 1
            7 1 3 9 2 4 8 5 6
            9 6 1 5 3 7 2 8 4
            2 8 7 4 1 9 6 3 5
            3 4 5 2 8 6 1 7 9
'''
        )
        # act
        block = sudoku.get_row(4)
        # assert
        assert block == ['.', '2', '6', '8', '5', '3', '7', '9', '1']

    def test_get_col(self):
        # arrange
        sudoku = make_sudoku(
'''
            5 3 4 6 7 8 9 1 2
            6 7 2 1 9 5 3 4 8
            1 9 8 3 4 2 5 6 7
            8 5 9 7 6 1 4 2 3
            6 2 6 8 5 3 . 9 1
            7 1 3 9 2 4 8 5 6
            9 6 1 5 3 7 2 8 4
            2 8 7 4 1 9 6 3 5
            3 4 5 2 8 6 1 7 9
'''
        )
        # act
        block = sudoku.get_col(6)
        # assert
        assert block == ['9', '3', '5', '4', '.', '8', '2', '6', '1']


class Testバックトラック:
    def test_可能な手をすべて確認する(self):
        # arrange
        tried = []
        def _1はNGで2はOK(p):
            tried.append(p)
            return p == 2
        def search_next_moves():
            return [1, 2] if not tried else []
        # act
        solved = try_possibilities(solve_by=_1はNGで2はOK,
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
        solved = try_possibilities(solve_by=_1の後2はNGで3の後4はOK,
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
        solved = try_possibilities(solve_by=_1の後2はNGで3の後4はOK,
                                   search_next_moves=最初は101と201と301でそれぞれプラス1ずつして1桁が3に達したら行き詰まる)
        # assert
        assert not solved
        assert tried == [101, 102, 103, 201, 202, 203, 301, 302, 303]

    class Test本物のSolveBy:
        def test_行き詰まる手(self):
            # arrange
            sudoku = make_sudoku(
            # (0, 0)に9を仮置きすると、(1, 0)に入るものがなくなる
'''
            . . 7 6 5 4 3 2 1
            .
            .
            . 8
'''
            )
            # act
            move = (0, 0, "9")
            # assert
            assert not sudoku.solve_by(move)

        def test_次に進める手(self):
            # arrange
            sudoku = make_sudoku(
            # (0, 0)に9を仮置きすると、(1, 0)に8が入る
'''
            . . 7 6 5 4 3 2 1
            .
'''
            )
            # act
            move = (0, 0, "9")
            # assert
            assert sudoku.solve_by(move)

    class Test本物のsearch_next_moves:
        def test_次に進める手(self):
            # arrange
            sudoku = make_sudoku(
            # (0, 0)には7か8か9が入る
'''
            . 6 5 4 3 2 1
'''
            )
            # act
            # assert
            assert sudoku.search_next_moves() == [
                    (0, 0, '7'),
                    (0, 0, '8'),
                    (0, 0, '9')]


class Test全体を動かす:
    def test_すでに解けている問題(self):
        # arrange
        # problem is taken from Wikipedia https://en.wikipedia.org/wiki/Sudoku
        sudoku = make_sudoku(
'''
            5 3 4 6 7 8 9 1 2
            6 7 2 1 9 5 3 4 8
            1 9 8 3 4 2 5 6 7
            8 5 9 7 6 1 4 2 3
            4 2 6 8 5 3 7 9 1
            7 1 3 9 2 4 8 5 6
            9 6 1 5 3 7 2 8 4
            2 8 7 4 1 9 6 3 5
            3 4 5 2 8 6 1 7 9
'''
        )
        # act
        solved = sudoku.solve()
        # assert
        assert solved is True

    def test_自明な問題_空きが1つだけ(self):
        # arrange
        # problem is taken from Wikipedia https://en.wikipedia.org/wiki/Sudoku
        sudoku = make_sudoku(
'''
            . 3 4 6 7 8 9 1 2
            6 7 2 1 9 5 3 4 8
            1 9 8 3 4 2 5 6 7
            8 5 9 7 6 1 4 2 3
            4 2 6 8 5 3 7 9 1
            7 1 3 9 2 4 8 5 6
            9 6 1 5 3 7 2 8 4
            2 8 7 4 1 9 6 3 5
            3 4 5 2 8 6 1 7 9
'''
        )
        # act
        solved = sudoku.solve()
        # assert
        assert solved is True
        assert sudoku.get_cell(0, 0) == '5'

    def test_自明な問題_空きが複数(self):
        # arrange
        # problem is taken from Wikipedia https://en.wikipedia.org/wiki/Sudoku
        sudoku = make_sudoku(
'''
            . 3 . 6 7 8 9 1 2
            6 7 2 1 9 5 3 4 8
            1 9 8 3 4 2 5 6 7
            8 5 9 7 6 1 4 2 3
            . 2 6 8 5 3 7 9 1
            7 1 3 9 2 4 8 5 6
            9 6 1 5 3 7 2 8 4
            2 8 7 4 1 9 6 3 5
            3 4 . 2 8 6 1 7 9
'''
        )
        # act
        solved = sudoku.solve()
        # assert
        assert solved is True
        assert sudoku.get_cell(0, 0) == '5'

    @pytest.mark.integration
    def test_仮置きが必要(self):
        # arrange
        # problem is taken from Wikipedia https://en.wikipedia.org/wiki/Sudoku
        sudoku = make_sudoku(
'''
            . . . 6 7 8 9 1 2
            . . . 1 9 5 3 4 8
            . . . 3 4 2 5 6 7
            . . . . . 1 4 2 3
            . . . . . 3 7 9 1
            . . . . . 4 8 5 6
            9 6 1 5 3 7 2 8 4
            2 8 7 4 1 9 6 3 5
            3 4 5 2 8 6 1 7 9
'''
        )
        # act
        solved = sudoku.solve()
        # assert
        assert solved is True
        assert sudoku.get_cell(0, 0) == '5'

    def test_解けない場合(self):
        # arrange
        sudoku = make_sudoku(
'''
            . 9 9 9 9 9 9 9 9
            9 9 9 9 9 9 9 9 9
            9 9 9 9 9 9 9 9 9
            9 9 9 9 9 9 9 9 9
            9 9 9 9 9 9 9 9 9
            9 9 9 9 9 9 9 9 9
            9 9 9 9 9 9 9 9 9
            9 9 9 9 9 9 9 9 9
            9 9 9 9 9 9 9 9 9
'''
        )
        # act
        solved = sudoku.solve()
        # assert
        assert solved is False


class TestIsSolved:
    def test_解けている(self):
        # arrange
        # problem is taken from Wikipedia https://en.wikipedia.org/wiki/Sudoku
        sudoku = make_sudoku(
'''
            5 3 4 6 7 8 9 1 2
            6 7 2 1 9 5 3 4 8
            1 9 8 3 4 2 5 6 7
            8 5 9 7 6 1 4 2 3
            4 2 6 8 5 3 7 9 1
            7 1 3 9 2 4 8 5 6
            9 6 1 5 3 7 2 8 4
            2 8 7 4 1 9 6 3 5
            3 4 5 2 8 6 1 7 9
'''
        )
        # act
        # assert
        assert sudoku.is_solved()

    def test_解けていない(self):
        # arrange
        # problem is taken from Wikipedia https://en.wikipedia.org/wiki/Sudoku
        sudoku = make_sudoku(
'''
            5 3 4 6 7 8 9 1 2
            6 7 2 1 9 5 3 4 8
            1 9 8 3 4 2 5 6 7
            8 5 9 7 6 1 4 2 3
            4 2 6 8 5 3 7 9 1
            7 1 3 9 2 4 8 5 6
            9 6 1 5 3 7 2 8 4
            2 8 7 4 1 9 6 3 5
            3 4 5 2 8 6 1 7 .
'''
        )
        # act
        # assert
        assert not sudoku.is_solved()

    def test_妥当性は確認しない(self):
        # arrange
        # problem is taken from Wikipedia https://en.wikipedia.org/wiki/Sudoku
        sudoku = make_sudoku(
'''
            0 0 0 0 9 9 9 9 9
            0 0 0 0 9 9 9 9 9
            0 0 0 0 9 9 9 9 9
            0
            1 2 3 4 5 6 7 8 9
            1 2 3 4 5 6 7 8 9
            1 2 3 4 5 6 7 8 9
            1 2 3 4 5 6 7 8 9
'''
            # 9行目が足りない
        )
        # act
        # assert
        # 数独のルールを守っているかは確認しない
        assert sudoku.is_solved()




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



class Sudoku:
    def __init__(self, cells: list[list[str]]):
        self.cells = cells

    def get_row(self, row: int) -> list[str]:
        if len(self.cells) <= row:
            return []
        return [c for c in self.cells[row]]

    def get_col(self, col: int) -> list[str]:
        return [r[col] for r in self.cells if len(r) > col]

    def get_block(self, col: int, row: int) -> list[str]:
        return [self.get_cell((col // 3) * 3 + r, (row // 3) * 3 + c) for c in range(3) for r in range(3)]

    def get_cell(self, col: int, row: int) -> str:
        if len(self.cells) <= row or len(self.cells[row]) <= col:
            return "."
        return self.cells[row][col]

    def set_cell(self, col: int, row: int, val: str) -> None:
        self.cells[row][col] = val

    def get_possible_values_for_cell(self, col: int, row: int) -> list[str]:
        available = set(["1", "2", "3", "4", "5", "6", "7", "8", "9"])
        used = set(self.get_row(row) + self.get_col(col) + self.get_block(col, row))
        possible = available - used
        return possible

    def get_cell_value_if_fixed(self, col: int, row: int) -> str | None:
        possible = self.get_possible_values_for_cell(col, row)
        if len(possible) == 1:
            return possible.pop()
        else:
            return None

    def should_continue(self):
        for c, r, _ in self.for_each_empty_cell():
            possible = self.get_possible_values_for_cell(c, r)
            if not possible:
                return False
        return True

    def solve_by(self, move):
        col, row, value = move
        self.set_cell(col, row, value)
        self.fix_all_possible_cells()
        return self.should_continue()

    def fix_all_possible_cells(self) -> None:
        while True:
            for col, row, value in self.for_each_empty_cell():
                new_value = self.get_cell_value_if_fixed(col, row)
                if new_value:
                    self.set_cell(col, row, new_value)
                    break
            else:
                return

    def is_solved(self):
        return not '.' in ''.join([''.join(s) for s in self.cells])

    def search_next_moves(self):
        col, row, _ = list(self.for_each_empty_cell())[0]
        return [(col, row, p) for p in sorted(self.get_possible_values_for_cell(col, row))]

    def solve(self):
        self.fix_all_possible_cells()
        return self.is_solved()

    def for_each_cell(self):
        for col in range(9):
            for row in range(9):
                yield (col, row, self.get_cell(col, row))

    def for_each_empty_cell(self):
        for col, row, value in self.for_each_cell():
            value = self.get_cell(col, row)
            if value == '.':
                yield (col, row, value)



