#include <cmath>
#include <math.h>
#include <stdlib.h>  /* abs */


#include "helpers.h"


// compute the distance between two points
double get_distance(
    const double p1x,
    const double p1y,
    const double p2x,
    const double p2y
    )
{
    return sqrt(pow(p2x - p1x, 2.0) + pow(p2y - p1y, 2.0));
}


// Check whether point is in view described by view_origin, view_vector,
// and view_angle.
bool point_within_view_angle(
    const double point_x,
    const double point_y,
    const double view_origin_x,
    const double view_origin_y,
    const double view_vector_x,
    const double view_vector_y,
    const double view_angle_deg
    )
{
    double origin_point_vector_x = point_x - view_origin_x;
    double origin_point_vector_y = point_y - view_origin_y;

    double rec_view_vector_length = 1.0/sqrt(pow(view_vector_x, 2.0) + pow(view_vector_y, 2.0));

    double norm_view_vector_x = view_vector_x*rec_view_vector_length;
    double norm_view_vector_y = view_vector_y*rec_view_vector_length;

    double rec_origin_point_vector_length = 1.0/sqrt(pow(origin_point_vector_x, 2.0) + pow(origin_point_vector_y, 2.0));

    origin_point_vector_x *= rec_origin_point_vector_length;
    origin_point_vector_y *= rec_origin_point_vector_length;

    double angle_rad = acos(norm_view_vector_x*origin_point_vector_x
                          + norm_view_vector_y*origin_point_vector_y);

    double angle_deg = angle_rad*180.0/M_PI;

    return (abs(angle_deg) <= abs(view_angle_deg/2.0));
}
