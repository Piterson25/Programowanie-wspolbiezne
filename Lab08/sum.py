import threading
import os


def sum_part(arr, start, end, result, lock):
    partial_sum = sum(arr[start:end])
    with lock:
        result.append(partial_sum)


def sum_list_in_threads(arr, num_threads):
    result = []
    lock = threading.Lock()

    threads = []
    length = len(arr)
    chunk_size = length // num_threads
    remaining = length % num_threads
    start = 0

    for i in range(num_threads):
        end = start + chunk_size + (1 if i < remaining else 0)
        thread = threading.Thread(target=sum_part, args=(arr, start, end, result, lock))
        thread.start()
        threads.append(thread)
        start = end

    for thread in threads:
        thread.join()

    total_sum = sum(result)
    return total_sum


my_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

available_threads = os.cpu_count()
num_threads = int(input("Podaj liczbę wątków: "))

if num_threads < 1:
    print("Nie można uruchomić programu z zerową liczbą wątków")
elif num_threads > available_threads:
    print("Podano więcej wątków niż posiada komputer")
else:
    total = sum_list_in_threads(my_list, num_threads)
    print("Suma elementów listy:", total)
