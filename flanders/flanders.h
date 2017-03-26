#ifndef CPP_INTERFACE_H_INCLUDED
#define CPP_INTERFACE_H_INCLUDED

#ifndef FLANDERS_API
#include "flanders_export.h"
#define FLANDERS_API flanders_EXPORT
#endif

#ifdef __cplusplus
extern "C" {
#endif

struct context_s;
typedef struct context_s context_t;

FLANDERS_API
context_t *new_context(const int num_points,
                       const double x_coordinates[],
                       const double y_coordinates[]);

FLANDERS_API
void free_context(context_t *context);

// Returns index of nearest point to the point number ref_index.
// By default, only the distance counts. If use_angles is true,
// then the view vector and angle are taken into account.
// In the latter case it is possible that no nearest neighbor exists,
// and in this case the function returns -1.
FLANDERS_API
void search_neighbor_xy(const context_t *context,
                        const int num_indices,
                        int indices[],
                        const double x[],
                        const double y[],
                        const bool use_angles,
                        const double vx[],
                        const double vy[],
                        const double angles_deg[],
                        const bool naive);

FLANDERS_API
void search_neighbor_index(const context_t *context,
                           const int num_indices,
                           int indices[],
                           const int ref_indices[],
                           const bool use_angles,
                           const double vx[],
                           const double vy[],
                           const double angles_deg[],
                           const bool naive);

#ifdef __cplusplus
}
#endif

#endif /* CPP_INTERFACE_H_INCLUDED */
