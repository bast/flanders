#ifndef HELPERS_H_INCLUDED
#define HELPERS_H_INCLUDED

double get_distance(const double p1[2], const double p2[2]);

bool point_within_view_angle(const double point[2],
                             const double view_origin[2],
                             const double view_vector[2],
                             const double view_angle_deg);

#endif /* HELPERS_H_INCLUDED */
