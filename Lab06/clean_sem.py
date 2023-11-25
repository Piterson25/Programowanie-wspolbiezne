import sysv_ipc

KEY = 10000


def create_semaphore(key):
    try:
        sem = sysv_ipc.Semaphore(key, sysv_ipc.IPC_CREX, 0o700)
        return sem, True
    except sysv_ipc.ExistentialError:
        sem = sysv_ipc.Semaphore(key)

    return sem, False


sem_p1, _ = create_semaphore(KEY)
sem_p2, _ = create_semaphore(KEY + 1)
sem_p1.remove()
sem_p2.remove()
