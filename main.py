import os

from cpu_parallel.cpu_test import test_miller_rabin_cpu_parallel
from helpers.stopwatch import stopwatch
from gpu.gpu import miller_rabin_gpu
from cpu.cpu import miller_rabin_cpu
from cpu_parallel.cpu_parallel import miller_rabin_cpu_parallel

import time


def clear_screen():
    if (os.name == 'posix'):
        os.system('clear')
    else:
        os.system('cls')


def select_menu_option(default_value):
    try:
        return int(input("Type appropriate value: "))
    except ValueError:
        print("\nWrong value! Try again.")
        input("Press Enter to continue...")
        return default_value


def run_both(val, quality):
    result = stopwatch(miller_rabin_cpu)(val, quality)
    print("CPU: ", result)
    result = stopwatch(miller_rabin_cpu_parallel)(val, quality)
    print("CPU parallel: ", result)
    result = stopwatch(miller_rabin_gpu)(val, quality)
    print("GPU: ", result)

def run_both_test(val, quality, iterations):
    result_true_cpu = 0
    start = time.time()
    for i in range(iterations):
        if stopwatch(miller_rabin_cpu)(val, quality):
            result_true_cpu += 1
    end = time.time()
    time_cpu = (end - start) / iterations

    result_true_cpu_parallel = 0
    start = time.time()
    for i in range(iterations):
        if stopwatch(miller_rabin_cpu_parallel)(val, quality):
            result_true_cpu_parallel += 1
    end = time.time()
    time_cpu_parallel = (end - start) / iterations

    result_true_gpu = 0
    start = time.time()
    for i in range(iterations):
        if stopwatch(miller_rabin_gpu)(val, quality):
            result_true_gpu += 1
    end = time.time()
    time_gpu = (end - start) / iterations

    print("\n")
    print("CPU for", iterations, "iterations took", time_cpu, "s and returned TRUE", result_true_cpu, "times.")
    print("CPU parallel for", iterations, "iterations took", time_cpu_parallel, "s and returned TRUE",
          result_true_cpu_parallel, "times.")
    print("GPU for", iterations, "iterations took", time_gpu, "s and returned TRUE", result_true_gpu, "times.")


def run_menu():
    select = -1
    while select != 0:
        select2 = -1
        clear_screen()
        print("\nMiller–Rabin primality test.\n")
        print("1. Run algorithm on CPU implementation.")
        print("2. Run algorithm on GPU implementation.")
        print("3. Run both algorithms implementation.")
        print("0. Exit.")
        select = select_menu_option(select)

        if select == 1:
            while select2 != 0:
                clear_screen()
                print("\nCPU implementation.\n")
                print("1. Enter data from the keyboard.")
                print("2. Get data from file.")
                print("0. Go back.")
                select2 = select_menu_option(select2)

                if select2 == 1:
                    clear_screen()
                    print("\nCPU implementation with data from the keyboard.\n")
                    n = int(input("Enter odd integer to be tested for primality: "))
                    k = int(input("Enter number of rounds of testing to perform: "))

                    print("Result: ", stopwatch(miller_rabin_cpu)(n, k))
                    input("\nPress Enter to continue...")

                elif select2 == 2:
                    clear_screen()
                    print("\nCPU implementation with data from file.\n")
                    file_name = input("Enter file name: ")
                    input("\nPress Enter to continue...")

        elif select == 2:
            while select2 != 0:
                clear_screen()
                print("\nGPU implementation.\n")
                print("1. Enter data from the keyboard.")
                print("2. Get data from file.")
                print("0. Go back.")
                select2 = select_menu_option(select2)

                if select2 == 1:
                    clear_screen()
                    print("\nGPU implementation with data from the keyboard.\n")
                    n = int(input("Enter odd integer to be tested for primality: "))
                    k = int(input("Enter number of rounds of testing to perform: "))

                    print("Result: ", stopwatch(miller_rabin_gpu)(n, k))
                    input("\nPress Enter to continue...")

                elif select2 == 2:
                    clear_screen()
                    print("\nGPU implementation with data from file.\n")
                    file_name = input("Enter file name: ")

                    input("\nPress Enter to continue...")

        elif select == 3:
            while select2 != 0:
                clear_screen()
                print("\nBoth algorithms implementation.\n")
                print("1. Enter data from the keyboard.")
                print("0. Go back.")
                select2 = select_menu_option(select2)

                if select2 == 1:
                    clear_screen()
                    print("\nEnter data from the keyboard.\n")
                    n = int(input("Enter odd integer to be tested for primality: "))
                    k = int(input("Enter number of rounds of testing to perform: "))

                    run_both(n, k)
                    input("\nPress Enter to continue...")

    print("\nEXIT")


if __name__ == '__main__':
    # run_both(46337, 1000000)
    # run_both_test(997, 1000000, 100)
    miller_rabin_cpu(46337, 1000000)