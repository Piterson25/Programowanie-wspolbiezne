import socket


def main():
    IP = "127.0.0.1"
    PORT = 5001
    BUF_SIZE = 1024
    game = False

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (IP, PORT)

    try:
        client_socket.connect(server_address)

        client_socket.sendto("Connect".encode('utf-8'), server_address)
        print("Witaj w grze Papier, Kamień, Nożyce!")
        print("Aby zakończyć grę, wpisz 'koniec'.")

        while True:
            response, _ = client_socket.recvfrom(BUF_SIZE)
            response = response.decode('utf-8')

            if response == "Connect":
                print("> Polaczono z serwerem, czekamy na przeciwnika")
            elif response == "Start":
                game = True
                print("\tROZPOCZYNAMY GRĘ")

            if response in ["Wygrałeś rundę!", "Przegrałeś rundę.", "Remis!"]:
                print(response)
                response, _ = client_socket.recvfrom(BUF_SIZE)
                response = response.decode('utf-8')
                print(response)
            if game:
                choice = input("Twój wybór: ")
                client_socket.sendto(choice.encode('utf-8'), server_address)

                if choice.lower() == 'koniec':
                    print("Zakończyłeś grę.")
                    break

                print("Czekanie na odpowiedź przeciwnika...")



    except socket.error as e:
        print(f"Wystąpił błąd: {e}")
    finally:
        client_socket.close()


if __name__ == "__main__":
    main()
