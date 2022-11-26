import os
from cpu.cpu import miller_rabin_cpu
from helpers.stopwatch import stopwatch
import gpu.gpu as gpu
import time
import numpy as np

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


def run_menu():
    select = -1
    while select != 0:
        select2 = -1
        clear_screen()
        print("\nMiller–Rabin primality test.\n")
        print("1. Run algorithm on CPU implementation.")
        print("2. Run algorithm on GPU implementation.")
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

                    input("\nPress Enter to continue...")

                elif select2 == 2:
                    clear_screen()
                    print("\nGPU implementation with data from file.\n")
                    file_name = input("Enter file name: ")

                    input("\nPress Enter to continue...")

    print("\nEXIT")


if __name__ == '__main__':
    # run_menu()
    val = 100003157
    start = time.time()
    x = (miller_rabin_cpu(val, 100000))
    end = time.time()
    print(x, end-start)
    start = time.time()
    y = gpu.gpu_power(val, 100000)
    end = time.time()
    print(y, end-start)

