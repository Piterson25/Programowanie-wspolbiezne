import random


class Board:
    def __init__(self, cols=6, rows=4):
        self.cols = cols
        self.rows = rows
        self.cards = [chr(ord('A') + i) for i in range(cols * rows // 2)]
        self.board = [[''] * self.cols for _ in range(self.rows)]

    def generate_pairs(self):
        all_letters = self.cards * 2
        random.shuffle(all_letters)

        k = 0
        for i in range(self.rows):
            for j in range(self.cols):
                self.board[i][j] = all_letters[k]
                k += 1

    def display_full_board(self):
        board_str = ""
        for row in self.board:
            for card in row:
                board_str += card
            board_str += '\n'
        return board_str

    def display_board(self, y, x):
        board_str = ""
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if i is x and j is y:
                    board_str += self.board[i][j]
                elif self.board[i][j] != '_':
                    board_str += 'X'
                else:
                    board_str += '_'
            board_str += '\n'
        return board_str

    def display_board_x(self):
        board_str = ""
        for row in self.board:
            for _ in row:
                board_str += 'X'
            board_str += '\n'
        return board_str

    def check_matching(self, coords1, coords2):
        x1 = coords2[0]
        y1 = coords2[1]
        x2 = coords1[0]
        y2 = coords1[1]

        def is_valid_coordinate(x, y):
            return 0 <= x < self.rows and 0 <= y < self.cols

        print(x1, y1, x2, y2, self.board[x1][y1], self.board[x2][y2])
        print(self.board)

        if is_valid_coordinate(x1, y1) and is_valid_coordinate(x2, y2):
            if self.board[x1][y1] == self.board[x2][y2]:
                self.board[x1][y1] = '_'
                self.board[x2][y2] = '_'
                return True
        return False
