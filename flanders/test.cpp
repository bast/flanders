#include <stdlib.h>
#include <stdio.h>

#include "btree.h"


int main()
{
    int num_points = 20;

    double *x = new double[num_points];
    double *y = new double[num_points];

    srand(0);

    for (int i = 0; i < num_points; i++)
    {
        x[i] = ((float) rand()) / (float) RAND_MAX;
        y[i] = ((float) rand()) / (float) RAND_MAX;
    }

    btree tree(num_points, x, y);

    for (int i = 0; i < num_points; i++)
    {
        double view_vector[2] = {1.0, 1.0};
        double view_angle_deg = 20.0;
        int index = tree.find_neighbor(i, true, view_vector, view_angle_deg);
        printf("i=%i nearest=%i\n", i, index);
    }

    delete[] x;
    delete[] y;

    return 0;
}
