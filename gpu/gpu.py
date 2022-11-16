from random import random


def check_squared_value(x, xSquer, testValue):
    if x == testValue - 1:
        if x != testValue - 1:
            return False
        else:
            return True
    if xSquer == 1:
        return False


# Run function on gpu "repetitions" cores
def testing_value(testValue, testValueMinusOne, powerOfTwo):
    # Choose a random number between 2 and testValue - 2
    randomValue = int(random() * (testValue - 3)) + 2

    # Calculate randomValue^testValueMinusOne mod testValue
    x = pow(randomValue, testValueMinusOne, testValue)

    # If x is 1 or testValue - 1, we don't know if testValue is prime, so we'll try again
    if x == 1 or x == testValue - 1:
        return True

    # For "powerOfTwo" gpu cores:
    for _ in range(1, powerOfTwo):

        # Divide between gpu cores?
        #
        xSquer = pow(x, 2, testValue)
        check_squared_value(x, xSquer, testValue)
        x = xSquer
        #

    # if "all cores return True":
    #     return True
    # else:
    #     return False


def miller_rabin_gpu(testValue, repetitions):
    """Returns True if testValue is probably prime, False if it's definitely composite."""
    if testValue < 3:
        return False

    # Find max power of 2 that divides testValue - 1
    powerOfTwo = 0
    testValueMinusOne = testValue - 1
    while testValueMinusOne % 2 == 0:
        testValueMinusOne //= 2
        powerOfTwo += 1

    # For "repetitions" gpu cores:
    for _ in range(1, repetitions):

        # Divide between gpu cores?
        #
        testing_value(testValue, testValueMinusOne, powerOfTwo)
        #

    # if "all cores return True":
    #     return True
    # else:
    #     return False
