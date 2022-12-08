__kernel void miller_rabin_gpu(
  __global int* testValue_buf,
  __global int* powerOfTwo_buf,
  __global int* testValueMinusOne_buf,
  __global int* random_values_buf,
  __global int* result_buf
)
{
  int gid = get_global_id(0);

  int testValue = testValue_buf[gid];
  int powerOfTwo = powerOfTwo_buf[gid];
  int testValueMinusOne = testValueMinusOne_buf[gid];
  int randomNumber = random_values_buf[gid];

  int isPrimeResult = 1;
  int x = 1;

  for (int i = 0; i < testValueMinusOne; ++i) {
    x = (x * randomNumber) % testValue;
  }

  if (x != 1 && x != testValue - 1) {
    int i = 0;
    while (i < powerOfTwo && x != testValue - 1) {
      x = (x * x) % testValue;
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