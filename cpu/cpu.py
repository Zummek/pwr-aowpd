
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

    for _ in range(1, repetitions):
        # Choose a random number between 2 and testValue - 2
        randomValue = int(random() * (testValue - 3)) + 2

        # Calculate randomValue^testValueMinusOne mod testValue
        x = pow(randomValue, testValueMinusOne, testValue)

        # If x is 1 or testValue - 1, we don't know if testValue is prime, so we'll try again
        if x == 1 or x == testValue - 1:
            continue

        # Otherwise, we'll keep squaring x and checking if it's equal to testValue - 1
        for _ in range(1, powerOfTwo):
            if x == testValue - 1:
                break

            x = pow(x, 2, testValue)
            if x == 1:
                return False

        # If x != testValue - 1, then we know that testValue is definitely composite
        if x != testValue - 1:
            return False

    # If we got this far, testValue is probably prime
    return True
