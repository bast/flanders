#include <limits>

#include "cpp_interface.h"
#include "helpers.h"


// Returns index of nearest point to the point number ref_index.
// By default, only the distance counts. If use_angles is true,
// then the view vector and angle are taken into account.
// In the latter case it is possible that no nearest neighbor exists,
// and in this case the function returns -1.
int find_neighbor_naive(
    const int    ref_index,
    const int    num_points,
    const double x_coordinates[],
    const double y_coordinates[],
    const bool   use_angles,
    const double view_vector[2],
    const double view_angle_deg
    )
{
    double ref_point[2] = {x_coordinates[ref_index], y_coordinates[ref_index]};

    double d = std::numeric_limits<double>::max();
    int index_found = -1;

    for (int i = 0; i < num_points; i++)
    {
        if (i != ref_index)
        {
            double point[2] = {x_coordinates[i], y_coordinates[i]};
            bool is_in_view = true;
            if (use_angles)
            {
                is_in_view = point_within_view_angle(
                                 point,
                                 ref_point,
                                 view_vector,
                                 view_angle_deg
                                 );
            }
            if (is_in_view)
            {
                double d_loc = get_distance(
                                   point,
                                   ref_point
                                   );
                if (d_loc < d)
                {
                    d = d_loc;
                    index_found = i;
                }
            }
        }
    }

    return index_found;
}
