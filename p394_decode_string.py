INT = int
STR = str
OPEN = '['
CLOSE = ']'


def tokenize(s):
    tokens = []
    i = 0
    while i < len(s):
        if s[i].isdigit():
            j = i
            while j < len(s) and s[j].isdigit():
                j += 1
            tokens.append((INT, int(s[i:j])))
            i = j
        elif s[i].isalpha():
            j = i
            while j < len(s) and s[j].isalpha():
                j += 1
            tokens.append((STR, s[i:j]))
            i = j
        elif s[i] == OPEN:
            tokens.append((OPEN, OPEN))
            i += 1
        elif s[i] == CLOSE:
            tokens.append((CLOSE, CLOSE))
            i += 1
    return tokens


class Repeat:
    def __init__(self, n, child):
        self.n = n
        self.child = child

    def __eq__(self, other):
        return self.n == other.n and self.child == other.child


class Str:
    def __init__(self, s):
        self.s = s

    def __eq__(self, other):
        return self.s == other.s


class Concat:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __eq__(self, other):
        return self.a == other.a and self.b == other.b


def build_tree(tokens):
    stack = []
    for token in tokens:
        if token[0] == INT:
            stack.append(token[1])  # Push the integer directly onto the stack
        elif token[0] == STR:
            stack.append(Str(token[1]))  # Create and push a Str node
        elif token[0] == OPEN:
            continue  # Do nothing for an open bracket
        elif token[0] == CLOSE:
            temp_stack = []
            while not isinstance(stack[-1], int):
                temp_stack.append(stack.pop())  # Pop until an integer is found
            n = stack.pop()  # Pop the integer (number of repetitions)
            # Reverse the temp_stack to maintain the correct order
            child = temp_stack.pop() if len(temp_stack) == 1 else Concat(temp_stack.pop(), temp_stack.pop())
            while temp_stack:  # If there are more nodes, keep concatenating
                child = Concat(child, temp_stack.pop())
            stack.append(Repeat(n, child))  # Create and push a Repeat node
    # Combine all remaining nodes into a single Concat node, if necessary
    if len(stack) > 1:
        result = stack.pop()
        while stack:
            result = Concat(stack.pop(), result)
        return result
    return stack[0]  # Return the single node or the combined node


def decode_tree(node):
    if isinstance(node, Str):
        return node.s
    elif isinstance(node, Repeat):
        return decode_tree(node.child) * node.n
    elif isinstance(node, Concat):
        return decode_tree(node.a) + decode_tree(node.b)
    else:
        return ''


def decode_string(s) -> str:
    tokens = tokenize(s)
    tree = build_tree(tokens)
    return decode_tree(tree)


class TestTokenize:
    def test_start(self):
        tokens = tokenize('3')
        assert tokens == [(INT, 3)]

    def test_simple(self):
        tokens = tokenize('3[a]')
        assert tokens == [(INT, 3), (OPEN, '['), (STR, 'a'), (CLOSE, ']')]

    def test_nested(self):
        tokens = tokenize('3[a20[bc]]')
        assert tokens == [(INT, 3), (OPEN, '['), (STR, 'a'), (INT, 20), (OPEN, '['), (STR, 'bc'), (CLOSE, ']'),
                          (CLOSE, ']')]

    def test_plain_str(self):
        tokens = tokenize('3[a]bc')
        assert tokens == [(INT, 3), (OPEN, '['), (STR, 'a'), (CLOSE, ']'), (STR, 'bc')]


class TestBuildTree:
    def test_simple(self):
        tree = build_tree([(INT, 3), (OPEN, '['), (STR, 'a'), (CLOSE, ']')])
        assert tree == Repeat(3, Str('a'))

    def test_nested(self):
        tree = build_tree(
            [(INT, 3), (OPEN, '['), (STR, 'a'), (INT, 20), (OPEN, '['), (STR, 'bc'), (CLOSE, ']'), (CLOSE, ']')])
        assert tree == Repeat(3, Concat(Str('a'), Repeat(20, Str('bc'))))


class TestDecodeString:
    def test_simple(self):
        assert decode_string('3[a]') == 'aaa'

    def test_nested(self):
        assert decode_string('3[a20[bc]]') == ('a' + 'bc' * 20) * 3

    def test_plain_str(self):
        assert decode_string('3[a]bc') == 'aaabc'
