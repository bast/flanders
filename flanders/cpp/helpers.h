#ifndef HELPERS_H_INCLUDED
#define HELPERS_H_INCLUDED

double get_distance(
    const double p1x,
    const double p1y,
    const double p2x,
    const double p2y
    );

bool point_within_view_angle(
    const double point_x,
    const double point_y,
    const double view_origin_x,
    const double view_origin_y,
    const double view_vector_x,
    const double view_vector_y,
    const double view_angle_deg
    );

#endif /* HELPERS_H_INCLUDED */
