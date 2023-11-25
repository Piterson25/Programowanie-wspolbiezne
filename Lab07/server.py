import socket


def main():
    IP = "127.0.0.1"
    PORT = 5001
    BUF_SIZE = 1024
    CHOICES = ['PAPIER', 'KAMIEŃ', 'NOŻYCE']

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((IP, PORT))
    print("Serwer UDP jest uruchomiony")

    players = {}
    scores = {}
    print(f"Oczekiwanie na graczy ({len(players)}/2)")

    while True:
        data, address = server_socket.recvfrom(BUF_SIZE)

        choice = data.decode('utf-8')

        if choice == "Connect" and len(players) != 2:
            players[address] = choice
            scores[address] = 0
            print(f"> Połączył się nowy gracz: {address} ({len(players)}/2)")

            server_socket.sendto("Connect".encode('utf-8'), address)
            if len(players) == 2:
                print("\tROZPOCZYNAMY GRĘ")
                for address in players:
                    server_socket.sendto("Start".encode('utf-8'), address)
        else:
            players[address] = choice

            if len(players) == 2:
                player1_address = list(players.keys())[0]
                player2_address = list(players.keys())[1]
                player1_choice = players[player1_address].upper()
                player2_choice = players[player2_address].upper()

                if player1_choice in CHOICES and player2_choice in CHOICES:
                    result = determine_winner(player1_choice, player2_choice)

                    if result == 1:
                        scores[player1_address] += 1
                        server_socket.sendto("Wygrałeś rundę!".encode('utf-8'), player1_address)
                        server_socket.sendto("Przegrałeś rundę.".encode('utf-8'), player2_address)
                    elif result == -1:
                        scores[player2_address] += 1
                        server_socket.sendto("Przegrałeś rundę.".encode('utf-8'), player1_address)
                        server_socket.sendto("Wygrałeś rundę!".encode('utf-8'), player2_address)
                    else:
                        server_socket.sendto("Remis!".encode('utf-8'), player1_address)
                        server_socket.sendto("Remis!".encode('utf-8'), player2_address)

                    server_socket.sendto(f"Ty: {scores[player1_address]} Przeciwnik: {scores[player2_address]}".encode('utf-8'), player1_address)
                    server_socket.sendto(f"Ty: {scores[player2_address]} Przeciwnik: {scores[player1_address]}".encode('utf-8'), player2_address)

                    print(
                        f"Gracz {player1_address} wybrał: {player1_choice}, Gracz {player2_address} wybrał: {player2_choice}")
                    print(
                        f"Wyniki: Gracz {player1_address}: {scores[player1_address]}, Gracz {player2_address}: {scores[player2_address]}")

                    players[player1_address] = "O"
                    players[player2_address] = "O"

                elif choice.lower() == "koniec":
                    other_choice = server_socket.recvfrom(BUF_SIZE)[0].decode('utf-8')
                    if other_choice.lower() == "koniec":
                        scores[player1_address] = 0
                        scores[player2_address] = 0
                        players.clear()
                        print("Gra zresetowana. Oczekiwanie na nowych graczy...")


def determine_winner(choice1, choice2):
    if choice1 == choice2:
        return 0
    elif (choice1 == 'KAMIEŃ' and choice2 == 'NOŻYCE') or \
            (choice1 == 'PAPIER' and choice2 == 'KAMIEŃ') or \
            (choice1 == 'NOŻYCE' and choice2 == 'PAPIER'):
        return 1
    else:
        return -1


if __name__ == "__main__":
    main()
