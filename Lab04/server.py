import os
import signal
import sys
import errno

FIFO_PATH = "db_fifo"


def create_fifo(fifo_path):
    try:
        os.mkfifo(fifo_path)
    except OSError as oe:
        if oe.errno != errno.EEXIST:
            raise


def get_requests():
    requests_str = ""

    create_fifo(FIFO_PATH)

    fifo = os.open(FIFO_PATH, os.O_RDONLY)

    while input_str := os.read(fifo, 128).decode():
        requests_str += input_str

    os.close(fifo)

    requests = []
    for r in requests_str.strip().split("\n"):
        id, client_path = r.split(",")
        requests.append((int(id), client_path))

    return requests


# Obsługa sygnału ignorowania
def ignore_signal(signum, frame):
    pass


# Obsługa sygnału SIGUSR1
def handle_sigusr1(signum, frame):
    os.remove(FIFO_PATH)
    sys.exit(0)


signal.signal(signal.SIGHUP, ignore_signal)
signal.signal(signal.SIGTERM, ignore_signal)
signal.signal(signal.SIGUSR1, handle_sigusr1)
print("PID:", os.getpid())

db = {
    0: "Kowalski",
    1: "Lewandowski",
    2: "Hyc",
    3: "Wiśniewska",
    4: "Boczek",
    5: "Strzelecki",
    6: "Polak",
}

while True:
    for id, client_path in get_requests():
        # Wyszukanie danych w bazie
        query_result = db.get(id, "nie ma")
        print(f"{id} {client_path}: {query_result}")

        # Wysłanie wyniku do klienta
        fifo = os.open(client_path, os.O_WRONLY)
        os.write(fifo, f"{query_result}\n".encode())
        os.close(fifo)
