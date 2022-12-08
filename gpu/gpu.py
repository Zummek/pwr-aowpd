from random import random
import pyopencl as cl
import numpy as np

# Initialization of PyOpenCl
# Select the first platform [0]
platform = cl.get_platforms()[0]

# Select the first device on this platform [0]
device = platform.get_devices()[0]

# setup context and queue
ctx = cl.Context([device])
queue = cl.CommandQueue(ctx)

mf = cl.mem_flags


def miller_rabin_gpu(testValue, repetitions):
    # Find max power of 2 that divides testValue - 1
    powerOfTwo = 0
    testValueMinusOne = testValue - 1

    while testValueMinusOne % 2 == 0:
        testValueMinusOne //= 2
        powerOfTwo += 1

    # generate rundom int number between 2 and testValue - 2
    random_values_arr = np.array(
        [int(random() * (testValue - 3) + 2) for _ in range(repetitions)], dtype=np.int32)
    results = np.full(repetitions, 1, dtype=np.int32)
    testValues_arr = np.full(repetitions, testValue)
    powerOfTwo_arr = np.full(repetitions, powerOfTwo)
    testValueMinusOne_arr = np.full(repetitions, testValueMinusOne)

    # Create a buffers for the data
    testValue_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=np.array(
        testValues_arr, dtype=np.int32))
    powerOfTwo_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=np.array(
        powerOfTwo_arr, dtype=np.int32))
    testValueMinusOne_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=np.array(
        testValueMinusOne_arr, dtype=np.int32))
    random_values_buf = cl.Buffer(
        ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=random_values_arr)

    # Create a buffer for the result
    result_buf = cl.Buffer(ctx, mf.WRITE_ONLY, results.nbytes)

    # Read the kernel code from the file
    with open('gpu/gpu_kernel.cl', 'r') as kernel_file:
        kernel_code = kernel_file.read()

    # Compile the Kernel
    prg = cl.Program(ctx, kernel_code).build()

    # Execute the kernel
    prg.miller_rabin_gpu(queue, testValues_arr.shape, None, testValue_buf, powerOfTwo_buf,
                         testValueMinusOne_buf, random_values_buf, result_buf)

    # Read the result
    cl.enqueue_copy(queue, results, result_buf)

    # Check if any of the processes found a composite number
    for result in results:
        if result == 0:
            return False

    # If we got this far, testValue is probably prime
    return True
