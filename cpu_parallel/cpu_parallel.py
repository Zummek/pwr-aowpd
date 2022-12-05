
from random import random
from multiprocessing import Process, Manager
import numpy as np
import psutil
import math

def miller_rabin_cpu_parallel(testValue, repetitions):
    """Returns True if testValue is probably prime, False if it's definitely composite."""
    if testValue < 3:
        return False

    # Find max power of 2 that divides testValue - 1
    powerOfTwo = 0
    testValueMinusOne = testValue - 1
    while testValueMinusOne % 2 == 0:
        testValueMinusOne //= 2
        powerOfTwo += 1
    # Get number of cores on cpu
    n_cpus = psutil.cpu_count()

    # List for result
    primeList = np.empty(repetitions)

    # List for jobs
    jobs = []

    reps = math.ceil(repetitions / n_cpus)

    # Run algorithm on cores
    for x in range(n_cpus):
        job = Process(target=cpu_check_number, args=[x, testValue, powerOfTwo, primeList, reps], )
        jobs.append(job)

    for job in jobs:
        job.start()

    for job in jobs:
        job.join()

    return not (np.all(primeList))


def cpu_check_number(index, testValue, powerOfTwo, primeList, reps):

    for _ in range(1, reps):
        # Choose a random number between 2 and testValue - 2
        randomValue = int(random() * (testValue - 3)) + 2

        # Calculate randomValue^testValueMinusOne mod testValue
        x = pow(randomValue, testValue - 1, testValue)

        # If x is 1 or testValue - 1, we don't know if testValue is prime, so we'll try again
        if x == 1 or x == testValue - 1:

            continue

        # Otherwise, we'll keep squaring x and checking if it's equal to testValue - 1
        for _ in range(1, powerOfTwo):
            if x == testValue - 1:
                break

            x = pow(x, 2, testValue)
            if x == 1:
                primeList[index] = 1
                break

        # If x != testValue - 1, then we know that testValue is definitely composite
        if x != testValue - 1:
            primeList[index] = 1
            break

    # If we got this far, testValue is probably prime
    primeList[index] = 0
    return True
