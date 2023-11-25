import sysv_ipc
import sys

KEY = 316
CHOICES = ['A', 'B', 'C']
ROUNDS = 3


def create_semaphore(key):
    try:
        sem = sysv_ipc.Semaphore(key, sysv_ipc.IPC_CREX, 0o700)
        return sem, True
    except sysv_ipc.ExistentialError:
        sem = sysv_ipc.Semaphore(key)
        return sem, False


def create_shared_mem(key):
    try:
        mem = sysv_ipc.SharedMemory(key, sysv_ipc.IPC_CREX)
        return mem
    except sysv_ipc.ExistentialError:
        mem = sysv_ipc.SharedMemory(key)
        return mem


first_sem, is_first = create_semaphore(KEY)
second_sem, _ = create_semaphore(KEY + 1)
first_mem = create_shared_mem(KEY)
second_mem = create_shared_mem(KEY + 1)

if is_first:
    print("GRACZ 1")
else:
    print("GRACZ 2")


def play(my_mem, opp_mem, my_sem, opp_sem):
    while True:
        choice = input("Podaj literę (A/B/C): ").upper()
        if choice in CHOICES:
            print(choice)
            break

    my_mem.write(choice.encode())
    my_sem.release()

    try:
        opp_sem.acquire()
    except sysv_ipc.ExistentialError:
        sys.exit(2)

    opp_choice = opp_mem.read().strip().decode()
    return choice, opp_choice


won = 0
for i in range(ROUNDS):
    print(f"\t\tRunda {i + 1} z {ROUNDS}")
    choice, opp_choice = play(first_mem if is_first else second_mem,
                              second_mem if is_first else first_mem,
                              first_sem if is_first else second_sem,
                              second_sem if is_first else first_sem)
    print("Przeciwnik wybrał", opp_choice)

    if is_first != (choice == opp_choice):
        print("Wygrana! :)")
        won += 1
    else:
        print("Przegrana :(")

    print()

print(f"Wygrano {won} rund")

if is_first:
    first_sem.remove()
    first_mem.remove()
else:
    second_sem.remove()
    second_mem.remove()
