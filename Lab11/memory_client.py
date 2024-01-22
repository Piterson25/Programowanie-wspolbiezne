import socket
from cards import Cards


class Client:
    def __init__(self):
        self.IP = "127.0.0.1"
        self.PORT = 5001
        self.BUF_SIZE = 1024
        self.board = []

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_address = (self.IP, self.PORT)
        self.loop = True

    def send_msg(self, message, address):
        self.client_socket.sendto(message.encode('utf-8'), address)

    def connect(self):
        try:
            self.client_socket.connect(self.server_address)
            self.send_msg("CONNECT", self.server_address)

            print("Witaj w grze Memory!")
            self.game()

        except socket.error as e:
            print(f"Wystąpił błąd: {e}")
        finally:
            self.client_socket.close()

    def print_board(self):
        for row in self.board.split('\n'):
            row_str = ""
            for char in row:
                if char in Cards.cards:
                    row_str += f"{Cards.cards[char]}{char}\033[0m"
                else:
                    row_str += char
            print(row_str)

    def game(self):
        while self.loop:
            response, _ = self.client_socket.recvfrom(self.BUF_SIZE)
            response = response.decode('utf-8')

            if response == "CONNECT":
                print("> Połączono z serwerem, czekamy na przeciwnika")
                continue
            elif response == "START":
                print("\tROZPOCZYNAMY GRĘ")
                continue
            elif response == 'MOVE':
                col = int(input('Podaj nr kolumny (1-6): '))
                while col <= 0 or col > len(self.board.split()[0]):
                    col = int(input('Podaj nr kolumny (1-6): '))

                row = int(input('Podaj nr rzędu (1-4): '))
                while row <= 0 or row > len(self.board.split()):
                    row = int(input('Podaj nr rzędu (1-4): '))
                print('\n')

                choice = str(col - 1) + ' ' + str(row - 1)
                self.send_msg(choice, self.server_address)
                continue
            elif response[0] == 'B':
                self.board = response[1:]
                self.print_board()
                continue
            elif response[0] == 'S':
                score = response[1:]
                print(f"Wow zdobyłes 1 punkt! Masz łacznie {score} punktów")
                continue
            elif response[0] == 'E':
                scores = response[1:].split()
                your_score = scores[0]
                enemy_score = scores[1]
                print("KONIEC GRY!")
                if your_score > enemy_score:
                    print(f"{Cards.cards['B']}{"ZWYCIĘSKO WYGRAŁEŚ!"}\033[0m")
                elif enemy_score > your_score:
                    print(f"{Cards.cards['A']}{"SROMOTNIE PRZEGRAŁEŚ!"}\033[0m")
                else:
                    print(f"{Cards.cards['C']}{"REMISSS"}\033[0m")

                print(f"Ty: {your_score} Przeciwnik: {enemy_score}")

                self.loop = False
            elif response == '0':
                print("Przeciwnik ma turę...")
                continue
            elif response == '1':
                print('> Twoja tura!')
                continue
            elif response.lower() == 'koniec':
                print("Zakończyłeś grę.")
                self.loop = False


def main():
    client = Client()
    client.connect()


if __name__ == "__main__":
    main()
