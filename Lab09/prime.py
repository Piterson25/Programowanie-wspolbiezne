import math
import threading
import os


def prime(k):
    if k < 2:
        return False
    sqrt_k = math.isqrt(k)
    for i in range(2, sqrt_k + 1):
        if k % i == 0:
            return False
    return True


def find_primes(start, end, result, barrier):
    primes = []
    for i in range(start, end + 1):
        if prime(i):
            primes.append(i)
    result.extend(primes)
    barrier.wait()


def prime_factors():
    l = int(input("Podaj początek przedziału: "))
    r = int(input("Podaj koniec przedziału: "))
    threads_count = int(input("Podaj liczbę wątków: "))

    if l >= r:
        print("Początek przedziału musi być mniejszy od końca przedziału")
        return

    available_threads = os.cpu_count()
    if threads_count > available_threads:
        print(f"Liczba wątków nie może przekroczyć {available_threads} wątków")
        return

    chunk_size = (r - l + 1) // threads_count
    threads = []
    primes = []
    barrier = threading.Barrier(threads_count + 1)

    for i in range(threads_count):
        start = l + i * chunk_size
        end = start + chunk_size - 1 if i != threads_count - 1 else r
        thread = threading.Thread(target=find_primes, args=(start, end, primes, barrier))
        threads.append(thread)
        thread.start()

    barrier.wait()
    print("Liczby pierwsze:", primes)


prime_factors()
