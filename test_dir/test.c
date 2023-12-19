#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "init_dyn_array.h"
//#include <pips_runtime.h>

#define matSize 2048L
#define maxTest 3


int main(int argc, const char* argv[])
{
srand(time(NULL));

int **A = create_two_dim_int(4096, 4096, "random");
int tests,i,j,k,l;
double t, tLoop, rate;
clock_t start = clock();

tLoop = 1.0e10;
for (tests=0; tests<maxTest; tests++){
#pragma @ICE loop=matmul
for ( i = 0; i < 4096; i++)
for ( j = 0; j < 8; j++)
for ( k = 0; k < 4096; k++)
{
A[k][i]=A[k][i]+A[k][i+5]+90;
}

clock_t stop = clock();
t = stop - start;
if (t<tLoop) tLoop = t;
}
printf("Matrix size = %ld | ", matSize);
printf("Time        = %7.5lf ms | ", tLoop * 1.0e3);
rate = (2.0 * matSize) * matSize * (matSize / tLoop);
printf("Rate        = %.2e MFLOP/s", rate * 1.0e-6);
deallocate_2d_array(A, 4096, 4096);
return 0;
}