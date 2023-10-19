import os
import time
import errno

client_filename = f"client_{os.getpid()}.txt"
print("Pliku klienta:", client_filename)

while True:
    try:
        fd = os.open("lockfile", os.O_CREAT | os.O_EXCL | os.O_RDWR)
        break
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
        else:
            print("Serwer zajęty, poczekaj")
            time.sleep(1)

with open("server_buffer.txt", "a") as bs:
    bs.write(client_filename + "\n")
    while True:
        user_input = input("Napisz wiadomość ('Send' aby wysłać): ")
        if user_input.lower() == "send":
            break

        bs.write(user_input + "\n")

while not os.path.exists(client_filename):
    print("Czekam na odpowiedź od serwera")
    time.sleep(3)

with open(client_filename, "r") as response_file:
    response = response_file.read()
    print("Odpowiedź od serwera: \n", response)

os.close(fd)
os.unlink("lockfile")
os.remove(client_filename)
