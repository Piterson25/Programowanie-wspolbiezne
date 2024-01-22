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
        print(f"Oczekiwanie na graczy (0/2)")

    def send_msg(self, message, address):
        self.server_socket.sendto(message.encode('utf-8'), address)

    def game_loop(self):
        while True:
            data, address = self.server_socket.recvfrom(self.BUF_SIZE)
            response = data.decode('utf-8')

            if response == "CONNECT" and len(self.players) != 2:
                self.players[address] = Player(response)
                print(
                    f"> Połączył się nowy gracz: {address} ({len(self.players)}/2)")
                self.send_msg("CONNECT", address)

                if len(self.players) == 2:
                    player1_address = list(self.players.keys())[0]
                    player2_address = list(self.players.keys())[1]
                    self.players[address].turn = 0

                    print("\tROZPOCZYNAMY GRĘ")
                    print(self.board.display_full_board())

                    for address in self.players:
                        self.players[address].choice = None
                        self.send_msg("START", address)

                    self.send_msg('1' + self.board.display_board_x(),
                                  player1_address)
                    self.send_msg('0' + self.board.display_board_x(),
                                  player2_address)
            else:
                self.players[address].choice = response

                if len(self.players) == 2:
                    player1_address = list(self.players.keys())[0]
                    player2_address = list(self.players.keys())[1]
                    player1 = self.players[player1_address]
                    player2 = self.players[player2_address]

                    print(player1.choice)
                    print(player2.choice)

                    if player1.turn and player1.choice and player1.moves > 0:
                        x = int(player1.choice.split()[0])
                        y = int(player1.choice.split()[1])

                        player1.moves -= 1

                        if player1.moves == 0:
                            player2.moves = 2
                            self.send_msg('0' + self.board.display_board(x, y),
                                          player1_address)
                            self.send_msg('1' + self.board.display_board(x, y),
                                          player2_address)
                            player1.turn = False
                            player2.turn = True
                        else:
                            self.send_msg('b' + self.board.display_board(x, y),
                                          player1_address)
                            self.send_msg('b' + self.board.display_board(x, y),
                                          player2_address)
                    elif player2.turn and player2.choice and player2.moves > 0:
                        x = int(player2.choice.split()[0])
                        y = int(player2.choice.split()[1])

                        player2.moves -= 1
                        if player2.moves == 0:
                            player1.moves = 2
                            self.send_msg('0' + self.board.display_board(x, y),
                                          player2_address)
                            self.send_msg('1' + self.board.display_board(x, y),
                                          player1_address)
                            player1.turn = True
                            player2.turn = False
                        else:
                            self.send_msg('b' + self.board.display_board(x, y),
                                          player1_address)
                            self.send_msg('b' + self.board.display_board(x, y),
                                          player2_address)


def main():
    game = MemoryGame()
    game.game_loop()


if __name__ == "__main__":
    main()
