#include <algorithm>
#include <math.h>

// rotate vector v by angle_deg
void rotate(const double vx,
            const double vy,
            const double angle_deg,
            double &v_rotated_x,
            double &v_rotated_y)
{
    double angle_rad = angle_deg * M_PI / 180.0;

    v_rotated_x = vx * cos(angle_rad) - vy * sin(angle_rad);
    v_rotated_y = vx * sin(angle_rad) + vy * cos(angle_rad);
}

// return line-line intersection coefficients using homogeneous coordinates
void get_intersection(
    const double u1[3], const double u2[3], double &a, double &b, double &c)
{
    a = u1[1] * u2[2] - u2[1] * u1[2];
    b = u1[2] * u2[0] - u2[2] * u1[0];
    c = u1[0] * u2[1] - u2[0] * u1[1];
}

// http://stackoverflow.com/a/4609795
template <typename T> int sgn(T val) { return (T(0) < val) - (val < T(0)); }

// find (a, b, c) in ax + bx + c = 0 from two points on that line
void line_coeffs_from_two_points(
    const double p1[2], const double p2[2], double &a, double &b, double &c)
{
    a = p1[1] - p2[1];
    b = p2[0] - p1[0];
    c = (p1[0] - p2[0]) * p1[1] + (p2[1] - p1[1]) * p1[0];
}

// From the reference point r there is a ray with vector v.
// This function finds the intersection point u between the ray
// and a line p1-p2. If an intersection point exists, function returns true.
bool intersection_point_exists(const double p1[2],
                               const double p2[2],
                               const double r[2],
                               const double v[2])
{
    const double TINY = 1.0e-20;

    double r2[2] = {r[0] + v[0], r[1] + v[1]};

    double ray[3];
    line_coeffs_from_two_points(r, r2, ray[0], ray[1], ray[2]);

    double line[3];
    line_coeffs_from_two_points(p1, p2, line[0], line[1], line[2]);

    double a, b, c;
    get_intersection(line, ray, a, b, c);

    if (fabs(c) < TINY)
        return false;

    double u[2] = {a / c, b / c};

    // check whether intersection is in the direction of the ray
    if (sgn(u[0] - r[0]) != sgn(v[0]))
        return false;
    if (sgn(u[1] - r[1]) != sgn(v[1]))
        return false;

    // check whether intersection is not outside line bounds
    for (int dim = 0; dim < 2; dim++)
    {
        double min_loc = std::min(p1[dim], p2[dim]);
        double max_loc = std::max(p1[dim], p2[dim]);
        if (fabs(max_loc - min_loc) > TINY)
        {
            if (std::min(u[dim], min_loc) == u[dim])
                return false;
            if (std::max(u[dim], max_loc) == u[dim])
                return false;
        }
    }

    // an intersection point exists
    return true;
}

// Computes number of intersection of two rays starting from view_origin
// intersecting with line between p1 and p2.
// Returns 0, 1, or 2.
int get_num_intersections(const double p1[2],
                          const double p2[2],
                          const double view_origin[2],
                          const double vx,
                          const double vy,
                          const double view_angle_deg)
{
    int n = 0;
    double v_rotated[2];

    rotate(vx, vy, -view_angle_deg / 2.0, v_rotated[0], v_rotated[1]);
    if (intersection_point_exists(p1, p2, view_origin, v_rotated))
        n++;

    rotate(vx, vy, +view_angle_deg / 2.0, v_rotated[0], v_rotated[1]);
    if (intersection_point_exists(p1, p2, view_origin, v_rotated))
        n++;

    return n;
}
