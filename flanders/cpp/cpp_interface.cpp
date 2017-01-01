#include <math.h>
#include <limits>


#include "cpp_interface.h"
#include "helpers.h"


// Returns index of nearest point to the point number ref_index.
// By default, only the distance counts. If use_angles is true,
// then the view vector and angle are taken into account.
// In the latter case it is possible that no nearest neighbor exists,
// and in this case the function returns -1.
int get_neighbor_index_naive(
    const int    ref_index,
    const int    num_points,
    const double points[],
    const bool   use_angles,
    const double view_vector_x,
    const double view_vector_y,
    const double view_angle_deg
    )
{
    double ref_point_x = points[2*ref_index];
    double ref_point_y = points[2*ref_index + 1];

    double d = std::numeric_limits<double>::max();
    int index = -1;

    for (int i = 0; i < num_points; i++)
    {
        if (i != ref_index)
        {
            bool is_in_view = true;
                if (use_angles)
                {
                    is_in_view = point_within_view_angle(
                                     points[2*i],
                                     points[2*i + 1],
                                     ref_point_x,
                                     ref_point_y,
                                     view_vector_x,
                                     view_vector_y,
                                     view_angle_deg
                                     );
                }
            if (is_in_view)
            {
                double d_loc = get_distance(
                                   points[2*i],
                                   points[2*i + 1],
                                   ref_point_x,
                                   ref_point_y
                                   );
                if (d_loc < d)
                {
                    d = d_loc;
                    index = i;
                }
            }
        }
    }

    return index;
}
