#include <math.h>

// compute the distance between two points
double get_distance(const double p1[2], const double p2[2])
{
    return sqrt(pow(p2[0] - p1[0], 2.0) + pow(p2[1] - p1[1], 2.0));
}

// Check whether point is in view described by view_origin, view_vector,
// and view_angle.
bool point_within_angle(const double point[2],
                        const double view_origin[2],
                        const double vx,
                        const double vy,
                        const double view_angle_deg)
{
    double origin_point_vector[2] = {point[0] - view_origin[0],
                                     point[1] - view_origin[1]};

    double rec_view_vector_length = 1.0 / sqrt(pow(vx, 2.0) + pow(vy, 2.0));

    double norm_view_vector[2] = {vx * rec_view_vector_length,
                                  vy * rec_view_vector_length};

    double rec_origin_point_vector_length =
        1.0 / sqrt(pow(origin_point_vector[0], 2.0) +
                   pow(origin_point_vector[1], 2.0));

    origin_point_vector[0] *= rec_origin_point_vector_length;
    origin_point_vector[1] *= rec_origin_point_vector_length;

    double angle_rad = acos(norm_view_vector[0] * origin_point_vector[0] +
                            norm_view_vector[1] * origin_point_vector[1]);

    double angle_deg = angle_rad * 180.0 / M_PI;

    return (fabs(angle_deg) <= fabs(view_angle_deg / 2.0));
}
