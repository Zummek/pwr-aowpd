from random import random
import pyopencl as cl
import numpy as np
import sys





def gpu_power(testValue, powerOfTwo, repetitions):

    # uncomment to print whole array (for big arrays)
    # np.set_printoptions(threshold=sys.maxsize)

    random_values = np.random.randint(2, testValue-2, size=repetitions)

    testVal_arr = np.empty_like(random_values)
    testVal_arr.fill(testValue)

    powerOfTwo_arr = np.empty_like(random_values)
    powerOfTwo_arr.fill(powerOfTwo)

    c_np = np.empty_like(random_values)

    # Initialization of PyOpenCl
    platform = cl.get_platforms()[0]  # Select the first platform [0]
    device = platform.get_devices()[0]  # Select the first device on this platform [0]

    # platform and device check
    print(platform, device)

    # setup context and queue
    ctx = cl.Context([device])
    queue = cl.CommandQueue(ctx)

    mf = cl.mem_flags

    # Create buffers
    a_g = cl.Buffer(ctx, mf.COPY_HOST_PTR, hostbuf=random_values)
    b_g = cl.Buffer(ctx, mf.COPY_HOST_PTR, hostbuf=testVal_arr)
    c_g = cl.Buffer(ctx, mf.COPY_HOST_PTR, hostbuf=powerOfTwo_arr)
    res_g = cl.Buffer(ctx, mf.WRITE_ONLY, c_np.nbytes)

    # params in kernel
    "a_g / x - number" \
    "b_g / z - modulus" \
    "c_g / y - power"
    # set up function on kernel
    prg = cl.Program(ctx, """
    __kernel void pow(
        __global const int *a_g, __global const int *b_g, __global const int *c_g, __global int *res_g)
        {
          int gid = get_global_id(0);
          unsigned long number=1;
          unsigned short x = a_g[gid];
          unsigned long z = b_g[gid];
          unsigned short y = c_g[gid];
          while (y)
            {
                if (y & 1)
                    number = number * x % z;
                y >>= 1;
                x = (unsigned long)x * x % z;
            }
          
          res_g[gid] = number;
        }
    """).build()
    krnl = prg.pow

    # run kernel func
    krnl(queue, random_values.shape , None, a_g, b_g, c_g, res_g) # queue, size of array, None, params to func pow

    np_arrays = [random_values, testVal_arr, powerOfTwo_arr, c_np]
    cl_arrays = [a_g, b_g, c_g, res_g]

    # copy data from c back to arrays in Python
    for x in range(4):
        cl.enqueue_copy(queue, np_arrays[x], cl_arrays[x] )
    queue.finish()

    # check results
    for x in np_arrays:
        print(x)

def testing_value(powerOfTwo, testValue):
    randomValue = 2 + random() % (testValue - 4)

    x = pow(randomValue, powerOfTwo, testValue)

    if x == 1 or x == testValue - 1:
        return True

    while powerOfTwo != testValue - 1:
        # Divide between gpu cores?
        x = pow(x, 2, testValue)
        powerOfTwo *= 2

        if x == 1:
            return False
        if x == testValue - 1:
            return True
    # if "all cores return True":
    #     return True
    # else:
    #     return False
    return False


def miller_rabin_gpu(testValue, repetitions):
    if testValue <= 1 or testValue == 4:
        return False
    if testValue <= 3:
        return True

    powerOfTwo = testValue - 1
    while powerOfTwo % 2 == 0:
        powerOfTwo /= 2

    for _ in range(1, repetitions):
        # Divide between gpu cores?
        if not testing_value(powerOfTwo, testValue):
            return False
    # if "all cores return True":
    #     return True
    # else:
    #     return False
    return True

# def check_squared_value(x, xSquer, testValue):
#     if x != testValue - 1:
#         return False
#     elif xSquer == 1:
#         return False
#     else:
#         return True


# Run function on gpu "repetitions" cores
# def testing_value(testValue, testValueMinusOne, powerOfTwo):
#     # Choose a random number between 2 and testValue - 2
#     randomValue = int(random() * (testValue - 3)) + 2
#
#     # Calculate randomValue^testValueMinusOne mod testValue
#     x = pow(randomValue, testValueMinusOne, testValue)
#
#     # If x is 1 or testValue - 1, we don't know if testValue is prime, so we'll try again
#     if x == 1 or x == testValue - 1:
#         return True
#
#     # For "powerOfTwo" gpu cores:
#     for _ in range(1, powerOfTwo):
#
#         # Divide between gpu cores?
#         #
#         xSquer = pow(x, 2, testValue)
#         check_squared_value(x, xSquer, testValue)
#         x = xSquer
#         #
#
#     # if "all cores return True":
#     #     return True
#     # else:
#     #     return False


# def miller_rabin_gpu(testValue, repetitions):
#     """Returns True if testValue is probably prime, False if it's definitely composite."""
#     if testValue < 3:
#         return False
#
#     # Find max power of 2 that divides testValue - 1
#     powerOfTwo = 0
#     testValueMinusOne = testValue - 1
#     while testValueMinusOne % 2 == 0:
#         testValueMinusOne //= 2
#         powerOfTwo += 1
#
#     # For "repetitions" gpu cores:
#     for _ in range(1, repetitions):
#
#         # Divide between gpu cores?
#         #
#         testing_value(testValue, testValueMinusOne, powerOfTwo)
#         #
#
#     # if "all cores return True":
#     #     return True
#     # else:
#     #     return False