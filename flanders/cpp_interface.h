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
context_t *new_context(
    const int    num_points,
    const double x_coordinates[],
    const double y_coordinates[]
    );

CPP_INTERFACE_API
void free_context(context_t *context);

CPP_INTERFACE_API
void insert(
    context_t *context,
    const double x,
    const double y,
    const int    index
    );

CPP_INTERFACE_API
int find_neighbor(
    const context_t *context,
    const int    index,
    const bool   use_angles,
    const double view_vector[2],
    const double view_angle_deg
    );

CPP_INTERFACE_API
int find_neighbor_naive(
    const int    ref_index,
    const int    num_points,
    const double x_coordinates[],
    const double y_coordinates[],
    const bool   use_angles,
    const double view_vector[2],
    const double view_angle_deg
    );

#ifdef __cplusplus
}
#endif

#endif /* CPP_INTERFACE_H_INCLUDED */
