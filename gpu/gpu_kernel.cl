__kernel void miller_rabin_gpu(
  __global float* testValue_buf,
  __global int* powerOfTwo_buf,
  __global float* testValueMinusOne_buf,
  __global float* random_values_buf,
  __global int* result_buf
)
{
  int gid = get_global_id(0);

  float testValue = testValue_buf[gid];
  int powerOfTwo = powerOfTwo_buf[gid];
  float testValueMinusOne = testValueMinusOne_buf[gid];
  float randomNumber = random_values_buf[gid];

  int isPrimeResult = 1;

  float x = pow(randomNumber, testValueMinusOne);
  x = fmod(x, testValue);

  if (x != 1 && x != testValue - 1) {
    int i = 0;
    while (i < powerOfTwo && x != testValue - 1) {
      x = pow(x, 2);
      x = fmod(x, testValue);
      if (x == 1) {
        isPrimeResult = 0;
        break;
      }
      i++;
    }

    if (x != testValue - 1) {
      isPrimeResult = 0;
    }
  }

  result_buf[gid] = isPrimeResult;
}