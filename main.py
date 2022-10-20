def run_menu():
    select = -1
    while select != 0:
        select2 = -1
        print("\nMiller–Rabin primality test.\n")
        print("1. Run algorithm on CPU implementation.")
        print("2. Run algorithm on GPU implementation.")
        print("0. Exit.")
        select = int(input("Type appropriate value: "))

        if select == 1:
            while select2 != 0:
                print("\nCPU implementation.\n")
                print("1. Enter data from the keyboard.")
                print("2. Get data from file.")
                print("0. Go back.")
                select2 = int(input("Type appropriate value: "))

                if select2 == 1:
                    print("\nCPU implementation with data from the keyboard.\n")
                    n = int(input("Enter odd integer to be tested for primality: "))
                    k = int(input("Enter number of rounds of testing to perform: "))

                elif select2 == 2:
                    print("\nCPU implementation with data from file.\n")
                    file_name = input("Enter file name: ")

            print("\nGO BACK")

        elif select == 2:
            while select2 != 0:
                print("\nGPU implementation.\n")
                print("1. Enter data from the keyboard.")
                print("2. Get data from file.")
                print("0. Go back.")
                select2 = int(input("Type appropriate value: "))

                if select2 == 1:
                    print("\nGPU implementation with data from the keyboard.\n")
                    n = int(input("Enter odd integer to be tested for primality: "))
                    k = int(input("Enter number of rounds of testing to perform: "))

                elif select2 == 2:
                    print("\nGPU implementation with data from file.\n")
                    file_name = input("Enter file name: ")

            print("\nGO BACK")

    print("\nEXIT")


if __name__ == '__main__':
    run_menu()
