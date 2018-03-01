class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Board:
    def __init__(self, board):
        self.board = board
        self.dim = len(board)
        self.free_count = 0
        for i in range(self.dim):
            for j in range(self.dim):
                if self.isempty(i, j):
                    self.free_count += 1
        self.move = [None] * 81

    def fill_square(self, pos, val):
        self.board[pos.x][pos.y] = val
        self.free_count -= 1

    def free_square(self, pos):
        self.board[pos.x][pos.y] = 0
        self.free_count += 1

    def next_square(self):
        next_pos = None
        for i in range(self.dim):
            for j in range(self.dim):
                if self.isempty(i, j):
                    pos_vals = set([i for i in range(1, 10)])
                    for k in range(self.dim):
                        if not self.isempty(i, k):
                            pos_vals.discard(self.board[i][k])
                        if not self.isempty(k, j):
                            pos_vals.discard(self.board[k][j])

                    ith_sec = i - i % 3
                    jth_sec = j - j % 3

                    for a in range(ith_sec, ith_sec + 3):
                        for b in range(jth_sec, jth_sec + 3):
                            if not self.isempty(a, b):
                                pos_vals.discard(self.board[a][b])
                    if next_pos is None or len(next_pos[2]) > len(pos_vals):
                        next_pos = (i, j, pos_vals)
        if len(next_pos[2]) == 0:
            return -1, -1, None
        return next_pos

    def isempty(self, i, j):
        return self.board[i][j] == 0

    def write(self, file):
        stng = self.__str__()
        with open(file, 'w') as out:
            out.write(stng)

    def __str__(self):
        stng = ""
        for i in range(self.dim):
            if i % 3 == 0:
                stng += '-' * 19 + '\n'
            for j in range(self.dim):
                if j % 3 == 0:
                    stng += '|'
                stng += str(self.board[i][j])
                if (j + 1) % 3 != 0:
                    stng += ' '
            stng += '|\n'
        stng += '-' * 19 + '\n'

        return stng


finished = False


def construct_cand(a, k, board):
    x, y, possible = board.next_square()
    board.move[k] = Point(x, y)

    ncand = 0
    c = []
    if x < 0 and y < 0:
        return c, ncand

    for i in possible:
        c.append(i)
        ncand += 1
    return c, ncand


def make_move(a, k, board):
    board.fill_square(board.move[k], a[k])


def unmake_move(a, k, board):
    board.free_square(board.move[k])


def is_a_soln(a, k, board):
    if board.free_count == 0:
        return True
    else:
        return False


def process_soln(a, k, board):
    board.write('output.txt')
    finished = True


def backtrack(a, k, inp):
    global finished

    if is_a_soln(a, k, inp):
        process_soln(a, k, inp)

    else:
        k += 1
        c, ncand = construct_cand(a, k, inp)
        for i in range(ncand):
            a[k] = c[i]
            make_move(a, k, inp)
            backtrack(a, k, inp)
            unmake_move(a, k, inp)
            if finished:
                return


def main():
    with open("input.txt") as inp:
        board = []
        for i in range(9):
            board.append(list(map(int, inp.readline().split())))
        board = Board(board)
        a = [None] * 81
        backtrack(a, 0, board)


if __name__ == '__main__':
    main()
