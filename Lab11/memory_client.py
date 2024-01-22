import socket


class Client:
    def __init__(self):
        self.IP = "127.0.0.1"
        self.PORT = 5001
        self.BUF_SIZE = 1024
        self.turn = False
        self.board = []

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_address = (self.IP, self.PORT)

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

    def game(self):
        while True:
            response, _ = self.client_socket.recvfrom(self.BUF_SIZE)
            response = response.decode('utf-8')

            if response == "CONNECT":
                print("> Połączono z serwerem, czekamy na przeciwnika")
            elif response == "START":
                print("\tROZPOCZYNAMY GRĘ")

            if response[0] == 'b' or response[0] == '0' or response[0] == '1':
                self.board = response[1:]
                print(self.board)
                if response[0] == '0':
                    self.turn = False
                    print("Przeciwnik ma turę...")
                elif response[0] == '1':
                    self.turn = True
                    print('> Twoja tura!')

            if self.turn:
                col = int(input('Podaj nr kolumny: '))
                while col <= 0 or col > len(self.board.split()[0]):
                    col = int(input('Podaj nr kolumny: '))

                row = int(input('Podaj nr rzędu: '))
                while row <= 0 or row > len(self.board.split()):
                    row = int(input('Podaj nr rzędu: '))

                print('\n')

                choice = str(col - 1) + ' ' + str(row - 1)
                self.send_msg(choice, self.server_address)

            if response.lower() == 'koniec':
                print("Zakończyłeś grę.")
                break


def main():
    client = Client()
    client.connect()


if __name__ == "__main__":
    main()
