#include <stdlib.h>
#include <stdio.h>

#include "btree.h"


int main()
{
    int num_points = 1000000;

    double *x = new double[num_points];
    double *y = new double[num_points];

    srand(0);

    for (int i = 0; i < num_points; i++)
    {
        x[i] = ((float) rand()) / (float) RAND_MAX;
        y[i] = ((float) rand()) / (float) RAND_MAX;
//      printf("x=%f y=%f\n", x[i], y[i]);
    }

    btree tree(num_points, x, y);

    delete[] x;
    delete[] y;

    return 0;
}
