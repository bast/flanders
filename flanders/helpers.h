#pragma once

double get_distance(const double p1[2], const double p2[2]);

bool point_within_angle(const double point[2],
                        const double view_origin[2],
                        const double vx,
                        const double vy,
                        const double view_angle_deg);
