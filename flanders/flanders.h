#ifndef CPP_INTERFACE_H_INCLUDED
#define CPP_INTERFACE_H_INCLUDED

#ifndef CPP_INTERFACE_API
#  ifdef _WIN32
#    if defined(CPP_INTERFACE_BUILD_SHARED) /* build dll */
#      define CPP_INTERFACE_API __declspec(dllexport)
#    elif !defined(CPP_INTERFACE_BUILD_STATIC) /* use dll */
#      define CPP_INTERFACE_API __declspec(dllimport)
#    else /* static library */
#      define CPP_INTERFACE_API
#    endif
#  else
#    if __GNUC__ >= 4
#      define CPP_INTERFACE_API __attribute__((visibility("default")))
#    else
#      define CPP_INTERFACE_API
#    endif
#  endif
#endif

#ifdef __cplusplus
extern "C" {
#endif

struct context_s;
typedef struct context_s context_t;

CPP_INTERFACE_API
context_t *new_context(const int num_points,
                       const double x_coordinates[],
                       const double y_coordinates[]);

CPP_INTERFACE_API
void free_context(context_t *context);

// Returns index of nearest point to the point number ref_index.
// By default, only the distance counts. If use_angles is true,
// then the view vector and angle are taken into account.
// In the latter case it is possible that no nearest neighbor exists,
// and in this case the function returns -1.
CPP_INTERFACE_API
int search_neighbor(const context_t *context,
                    const double x,
                    const double y,
                    const bool use_angles,
                    const double view_vector[2],
                    const double view_angle_deg,
                    const bool naive);

CPP_INTERFACE_API
int search_neighbor_by_index(const context_t *context,
                             const int ref_index,
                             const bool use_angles,
                             const double view_vector[2],
                             const double view_angle_deg,
                             const bool naive);

#ifdef __cplusplus
}
#endif

#endif /* CPP_INTERFACE_H_INCLUDED */
