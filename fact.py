import time
from multiprocessing import Pool, cpu_count

def factorize(number):
    factors = []
    for i in range(1, number + 1):
        if number % i == 0:
            factors.append(i)
    return factors


def factorize_standart(*numbers):
    start_time = time.time()
    results = list(map(factorize, numbers))
    end_time = time.time()
    a, b, c, d = results
    return a, b, c, d, end_time - start_time


def factorize_pool(*numbers):
    num_processes = cpu_count()
    print(f"Number of CPU cores: {num_processes}")

    start_time = time.time()
    with Pool(processes=num_processes) as pool:
        results = pool.map(factorize, numbers)
    end_time = time.time()

    a, b, c, d = results
    return a, b, c, d, end_time - start_time


if __name__ == '__main__':

    numbers = (128, 255, 99999, 10651060)

    a, b, c, d, execution_time_standart = factorize_standart(*numbers)
    
    print(f"factors of 128: {a}")
    print(f"factors of 255: {b}")
    print(f"factors of 99999: {c}")
    print(f"factors of 10651060: {d}")

    a, b, c, d, execution_time_pool = factorize_pool(*numbers)

    print(f"Execution time (standart): {execution_time_standart:.5f} seconds")
    print(f"Execution time (parallel): {execution_time_pool:.5f} seconds")

    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]