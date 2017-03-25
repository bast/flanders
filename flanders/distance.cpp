#include <math.h>

#include "btree.h"

double get_distance(const node *leaf, const double coordinates[2])
{
    return sqrt(pow(coordinates[0] - leaf->coordinates[0], 2.0) +
                pow(coordinates[1] - leaf->coordinates[1], 2.0));
}

double signed_distance_to_split(const node *leaf, const double coordinates[2])
{
    int d = leaf->split_dimension;
    return leaf->coordinates[d] - coordinates[d];
}

int get_position(const node *leaf, const double coordinates[2])
{
    if (signed_distance_to_split(leaf, coordinates) > 0.0)
    {
        // insert "left"
        return 0;
    }
    else
    {
        // insert "right"
        return 1;
    }
}
