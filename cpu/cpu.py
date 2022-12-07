
from random import random


def miller_rabin_cpu(testValue, repetitions):
    """Returns True if testValue is probably prime, False if it's definitely composite."""
    if testValue < 3:
        return False

    # Find max power of 2 that divides testValue - 1
    powerOfTwo = 0
    testValueMinusOne = testValue - 1
    while testValueMinusOne % 2 == 0:
        testValueMinusOne //= 2
        powerOfTwo += 1

    # for _ in range(1, repetitions):
    bbb = [6,  9,  5,  9,  4, 15, 13, 10, 12, 15, 13,  5, 14,  3,  6,  2,  8,  5,
           2,  9, 13,  5,  6, 15, 13,  3,  4,  9, 11,  9]
    for randomValue in bbb:
        # Choose a random number between 2 and testValue - 2
        # randomValue = int(random() * (testValue - 3)) + 2

        # Calculate randomValue^testValueMinusOne mod testValue
        x = pow(randomValue, testValueMinusOne, testValue)
        print("randomValue:", randomValue, ", x: ", x)

        # If x is 1 or testValue - 1, we don't know if testValue is prime, so we'll try again
        if x == 1 or x == testValue - 1:
            continue

        # Otherwise, we'll keep squaring x and checking if it's equal to testValue - 1
        for _ in range(1, powerOfTwo):
            if x == testValue - 1:
                break

            x = pow(x, 2, testValue)
            # print("1 x: ", x)
            if x == 1:
                return False

        # If x != testValue - 1, then we know that testValue is definitely composite
        if x != testValue - 1:
            # print("x != testValue - 1: ", x)
            return False

    # If we got this far, testValue is probably prime
    return True
