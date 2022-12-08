#if defined(cl_khr_fp64)  // Khronos extension available?
#pragma OPENCL EXTENSION cl_khr_fp64 : enable
#define DOUBLE_SUPPORT_AVAILABLE
#elif defined(cl_amd_fp64)  // AMD extension available?
#pragma OPENCL EXTENSION cl_amd_fp64 : enable
#define DOUBLE_SUPPORT_AVAILABLE
#endif

__kernel void miller_rabin_gpu(
  __global double* testValue_buf,
  __global int* powerOfTwo_buf,
  __global int* testValueMinusOne_buf,
  __global float* random_values_buf,
  __global int* result_buf
)
{
  int gid = get_global_id(0);

  double testValue = testValue_buf[gid];
  int powerOfTwo = powerOfTwo_buf[gid];
  int testValueMinusOne = testValueMinusOne_buf[gid];
  float randomNumber = random_values_buf[gid];

  int isPrimeResult = 1;

  double x = pown(randomNumber, testValueMinusOne);
  printf("1 randomNumber: %f, x: %f, %f, %d\n", randomNumber, x, testValue, testValueMinusOne);
  x = fmod(x, testValue);
  printf("2 randomNumber: %f, x: %f, %f, %d\n", randomNumber, x, testValue, testValueMinusOne);

  if (x != 1 && x != testValue - 1) {
    int i = 0;
    while (i < powerOfTwo && x != testValue - 1) {
      x = pown(x, 2);
      x = fmod(x, testValue);
      // printf("1 x: %f", x);
      if (x == 1) {
        isPrimeResult = 0;
        break;
      }
      i++;
    }

    if (x != testValue - 1) {
      // printf("2 x: %f", x);
      isPrimeResult = 0;
    }
  }

  result_buf[gid] = isPrimeResult;
}