import os
import time
import errno

while True:
    while True:
        try:
            lockfile_esists = os.path.isfile("lockfile")
            if lockfile_esists:
                break
        except OSError as e:
            if e.errno != errno.EEXIST:
                print("Czekam na połączenie klienta")
                raise
            time.sleep(0.05)
    print("Znaleziono plik zamkowy")

    while True:
        try:
            with open("server_buffer.txt", "r") as buffer_file:
                client_filename = buffer_file.readline().strip()
                client_message = buffer_file.read()

            os.remove("server_buffer.txt")

            print("\nWiadomość od klienta:")
            print(client_message)

            response = input("Wprowadź odpowiedź do klienta: ")

            with open(client_filename, "w") as response_file:
                response_file.write(f"\t{response}")
            print(f"Odpowiedź wysłana do klienta: {client_filename}")
            print("\n Serwer czeka na dalsze połączenia")
            break

        except FileNotFoundError:
            time.sleep(2)
        except PermissionError:
            time.sleep(1)
            continue
    time.sleep(2)
