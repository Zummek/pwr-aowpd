from random import random
import pyopencl as cl
import numpy as np
import sys
import time

# Initialization of PyOpenCl
# Select the first platform [0]
platform = cl.get_platforms()[0]

# Select the first device on this platform [0]
device = platform.get_devices()[0]

# platform and device check
# print(platform, device)

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

    # generate rundom numbers
    random_values = np.random.randint(2, testValue-2, size=repetitions)

    testVal_arr = np.empty_like(random_values)
    testVal_arr.fill(testValue)

    powerOfTwo_arr = np.empty_like(random_values)
    powerOfTwo_arr.fill(powerOfTwo)

    c_np = np.empty_like(random_values)

    # Create buffers
    a_g = cl.Buffer(ctx, mf.COPY_HOST_PTR, hostbuf=random_values)
    b_g = cl.Buffer(ctx, mf.COPY_HOST_PTR, hostbuf=testVal_arr)
    c_g = cl.Buffer(ctx, mf.COPY_HOST_PTR, hostbuf=powerOfTwo_arr)
    res_g = cl.Buffer(ctx, mf.WRITE_ONLY, c_np.nbytes)

    # params in kernel
    "a_g / x - number random" \
        "b_g / z - modulus test val" \
        "c_g / y - power powerof two"

    prg = cl.Program(ctx, """
            __kernel void power(
                __global const int *a_g, __global const int *b_g, __global const int *c_g, __global int *res_g)
                {
                      int gid = get_global_id(0);
                      unsigned long number = 1;
                      unsigned long x = a_g[gid];
                      unsigned long z = b_g[gid];
                      unsigned long y = c_g[gid];
    
                      while (y)
                        {
                            if (y & 1)
                                number = number * x % z;
                            y >>= 1;
                            x = (unsigned long)x * x % z;
                        }
    
                    res_g[gid] = 1;
    
                    if(number != 1 && number != b_g[gid] - 1){
                        int powerOfTwo = c_g[gid];
                        while( powerOfTwo != b_g[gid] - 1 ){
                            number = 1;
                            x = a_g[gid];
                            z = b_g[gid];
                                y = powerOfTwo;
                                while (y){
                                    if (y & 1)
                                    number = number * x % z;
                                    y >>= 1;
                                    x = (unsigned long)x * x % z;
                                }
                                powerOfTwo *= 2;
    
                                if(number == 1 || number == b_g[gid] -1){
                                    if(number == 1){
                                        res_g[gid] = 0;
                                        break;
                                    } else {
                                        res_g[gid] = 1;
                                        break;
                                    }
                                }
                            }
    
                        }
                    }
                """).build()

    krnl = prg.power

    # run kernel func
    # queue, size of array, None, params to func pow
    krnl(queue, random_values.shape, None, a_g, b_g, c_g, res_g)

    # copy data from c back to array in Python
    cl.enqueue_copy(queue, c_np, res_g)
    queue.finish()

    return not (np.all(c_np))
