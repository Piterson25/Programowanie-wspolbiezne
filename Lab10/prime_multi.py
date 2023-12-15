import math
import os
import time
from multiprocessing import Pool


def prime(k):
    if k <= 1:
        return False
    for i in range(2, int(math.sqrt(k)) + 1):
        if k % i == 0:
            return False
    return True


def find_similar_prime(interval):
    start, end = interval
    result = []
    for i in range(start, end - 1):
        if prime(i) and prime(i + 2):
            result.append((i, i + 2))
    return result


def find_similar_prime_parallel(l, r, threads_count):
    chunk_size = (r - l) // threads_count
    chunks = []
    start = l
    for _ in range(threads_count):
        chunk_end = min(start + chunk_size, r)
        chunks.append((start, chunk_end))
        start = chunk_end

    with Pool(processes=threads_count) as pool:
        results = pool.imap(find_similar_prime, chunks)

        result = []
        for sublist in results:
            result.extend(sublist)
    return result


if __name__ == '__main__':
    l = int(input("Podaj początek przedziału: "))
    r = int(input("Podaj koniec przedziału: "))
    threads_count = int(input("Podaj liczbę wątków: "))

    if l >= r:
        print("Początek przedziału musi być mniejszy od końca przedziału")
        exit()

    available_threads = os.cpu_count()
    if threads_count > available_threads:
        print(f"Liczba wątków nie może przekroczyć {available_threads} wątków")
        exit()

    start = time.time()
    result_seq = find_similar_prime((l, r))
    time_seq = time.time() - start

    print(
        f"Liczba bliźniaczych liczb pierwszych sekwencyjnie: {len(result_seq)}")
    print(f"Czas wykonania sekwencyjnego: {time_seq} sekund")

    start = time.time()
    result_parallel = find_similar_prime_parallel(l, r, threads_count)
    time_parallel = time.time() - start

    print(
        f"Liczba bliźniaczych liczb pierwszych równolegle: {len(result_parallel)}")
    print(
        f"Czas wykonania równoległego z {threads_count} procesami: {time_parallel} sekund")
