import socket
from player import Player
from board import Board


class MemoryGame:
    def __init__(self):
        self.IP = "127.0.0.1"
        self.PORT = 5001
        self.BUF_SIZE = 1024
        self.board = Board()

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind((self.IP, self.PORT))
        print("Serwer UDP jest uruchomiony")

        self.players = {}
        self.choice1 = tuple()
        self.choice2 = tuple()
        self.loop = True
        print(f"Oczekiwanie na graczy (0/2)")

    def send_msg(self, message, address):
        self.server_socket.sendto(message.encode('utf-8'), address)

    def game_loop(self):
        while self.loop:
            data, address = self.server_socket.recvfrom(self.BUF_SIZE)
            response = data.decode('utf-8')

            if response == "CONNECT" and len(self.players) != 2:
                self.players[address] = Player(response)
                print(
                    f"> Połączył się nowy gracz: {address} ({len(self.players)}/2)")
                self.send_msg("CONNECT", address)
                self.start_game()
            else:
                self.players[address].choice = response

                if len(self.players) == 2:
                    self.game()

        print("Zakonczono pracę serwera")

    def start_game(self):
        if len(self.players) == 2:
            self.board.generate_pairs()
            player1_address = list(self.players.keys())[0]
            player2_address = list(self.players.keys())[1]
            self.players[player1_address].turn = 1

            print("\tROZPOCZYNAMY GRĘ")
            print(self.board.display_full_board())

            for address in self.players:
                self.players[address].choice = tuple()
                self.send_msg("START", address)

            self.send_msg('B' + self.board.display_board_x(),
                          player1_address)
            self.send_msg('B' + self.board.display_board_x(),
                          player2_address)
            self.send_msg('1', player1_address)
            self.send_msg("MOVE", player1_address)
            self.send_msg('0', player2_address)

    def game(self):
        player1_address = list(self.players.keys())[0]
        player2_address = list(self.players.keys())[1]
        player1 = self.players[player1_address]
        player2 = self.players[player2_address]

        print(player1.choice)
        print(player2.choice)

        if player1.turn and player1.choice and player1.moves > 0:
            x, y = map(int, player1.choice.split())

            self.send_msg('B' + self.board.display_board(x, y),
                          player1_address)
            self.send_msg('B' + self.board.display_board(x, y),
                          player2_address)

            player1.moves -= 1

            if player1.moves == 1:
                self.choice1 = (x, y)
            elif player1.moves == 0:
                self.choice2 = (x, y)

                if self.board.check_matching(self.choice1,
                                             self.choice2):
                    player1.moves = 2
                    player1.score += 1
                    self.send_msg('S' + str(player1.score), player1_address)
                    self.send_msg('B' + self.board.display_board(x, y),
                                  player1_address)
                    print("Gracz1 zdobyl punkt!")
                else:
                    player2.moves = 2
                    self.send_msg('0', player1_address)
                    self.send_msg('1', player2_address)
                    player1.turn = False
                    player2.turn = True

        elif player2.turn and player2.choice and player2.moves > 0:
            x, y = map(int, player2.choice.split())

            self.send_msg('B' + self.board.display_board(x, y),
                          player1_address)
            self.send_msg('B' + self.board.display_board(x, y),
                          player2_address)

            player2.moves -= 1

            if player2.moves == 1:
                self.choice1 = (x, y)
            elif player2.moves == 0:
                self.choice2 = (x, y)

                if self.board.check_matching(self.choice1,
                                             self.choice2):
                    player2.moves = 2
                    player2.score += 1
                    self.send_msg('S' + str(player2.score), player2_address)
                    self.send_msg('B' + self.board.display_board(x, y),
                                  player2_address)
                    print("Gracz2 zdobyl punkt!")
                else:
                    player1.moves = 2
                    self.send_msg('1', player1_address)
                    self.send_msg('0', player2_address)
                    player1.turn = True
                    player2.turn = False
        if player1.turn:
            self.send_msg("MOVE", player1_address)
        elif player2.turn:
            self.send_msg("MOVE", player2_address)


def main():
    game = MemoryGame()
    game.game_loop()


if __name__ == "__main__":
    main()
