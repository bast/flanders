#include <algorithm>
#include <math.h>


// rotate vector v by angle_deg
double *rotate(
    const double v[2],
    const double angle_deg
    )
{
    double angle_rad = angle_deg*M_PI/180.0;
    double *v_rotated = new double[2];

    v_rotated[0] = v[0]*cos(angle_rad) - v[1]*sin(angle_rad);
    v_rotated[1] = v[0]*sin(angle_rad) + v[1]*cos(angle_rad);

    return v_rotated;
}


// return line-line intersection using homogeneous coordinates
double *get_intersection(
    const double u1[3],
    const double u2[3]
    )
{
    double *res = new double[3];

    res[0] = u1[1]*u2[2] - u2[1]*u1[2];
    res[1] = u1[2]*u2[0] - u2[2]*u1[0];
    res[2] = u1[0]*u2[1] - u2[0]*u1[1];

    return res;
}


// http://stackoverflow.com/a/4609795
template <typename T> int sgn(T val) {
    return (T(0) < val) - (val < T(0));
}


// find (a, b, c) in ax + bx + c = 0 from two points on that line
double *line_coeffs_from_two_points(
    const double p1[2],
    const double p2[2]
    )
{
    double *res = new double[3];

    res[0] = p1[1] - p2[1];
    res[1] = p2[0] - p1[0];
    res[2] = (p1[0] - p2[0])*p1[1] + (p2[1] - p1[1])*p1[0];

    return res;
}


// From the reference point r there is a ray with vector v.
// This function finds the intersection point u between the ray
// and a line p1-p2. If an intersection point exists, function returns true.
bool intersection_point_exists(
    const double p1[2],
    const double p2[2],
    const double r[2],
    const double v[2]
    )
{
    const double TINY = 1.0e-20;

    double r2[2] = {r[0] + v[0], r[1] + v[1]};
    double *ray = line_coeffs_from_two_points(r, r2);

    double *line = line_coeffs_from_two_points(p1, p2);
    double *coef = get_intersection(line, ray);

    if (fabs(coef[2]) < TINY) return false;

    double u[2] = {coef[0]/coef[2], coef[1]/coef[2]};

    // check whether intersection is in the direction of the ray
    if (sgn(u[0] - r[0]) != sgn(v[0])) return false;
    if (sgn(u[1] - r[1]) != sgn(v[1])) return false;

    // check whether intersection is not outside line bounds
    for (int dim = 0; dim < 2; dim++)
    {
        double min_loc = std::min(p1[dim], p2[dim]);
        double max_loc = std::max(p1[dim], p2[dim]);
        if (fabs(max_loc - min_loc) > TINY)
        {
            if (std::min(u[dim], min_loc) == u[dim]) return false;
            if (std::max(u[dim], max_loc) == u[dim]) return false;
        }
    }

    // an intersection point exists
    return true;
}


// Computes number of intersection of two rays starting from view_origin
// intersecting with line between p1 and p2.
// Returns 0, 1, or 2.
int get_num_intersections(
    const double p1[2],
    const double p2[2],
    const double view_origin[2],
    const double view_vector[2],
    const double view_angle_deg
    )
{
    int n = 0;

    double *v_left = rotate(view_vector, -view_angle_deg/2.0);
    if (intersection_point_exists(p1, p2, view_origin, v_left)) n++;

    double *v_right = rotate(view_vector, +view_angle_deg/2.0);
    if (intersection_point_exists(p1, p2, view_origin, v_right)) n++;

    return n;
}
