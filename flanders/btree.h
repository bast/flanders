#pragma once

#include <vector>

struct node
{
    int index;
    node *children[2];
    node *parent;
    int split_dimension;
    double bounds[2][2];
    double coordinates[2];
};

class btree
{
  public:
    btree(const int num_points, const double x[], const double y[]);
    ~btree();

    void search_neighbors_by_coordinates(const int num_indices,
                                         int indices[],
                                         const double x[],
                                         const double y[],
                                         const bool use_angles,
                                         const double vx[],
                                         const double vy[],
                                         const double angles_deg[],
                                         const bool naive) const;

    void search_neighbor_by_indices(const int num_indices,
                                    int indices[],
                                    const int ref_indices[],
                                    const bool use_angles,
                                    const double vx[],
                                    const double vy[],
                                    const double angles_deg[],
                                    const bool naive) const;

  private:
    btree(const btree &rhs);            // not implemented
    btree &operator=(const btree &rhs); // not implemented

    void destroy_tree();
    void destroy_tree(node *leaf);

    void insert(const double x, const double y, const int index);
    void insert(const double x, const double y, const int index, node *leaf);

    node *guess_node(const double coordinates[2]) const;
    node *guess_node(const double coordinates[2], node *leaf) const;

    int traverse(node *leaf,
                 const bool skip_ref_index,
                 const int ref_index,
                 const double ref_point[2],
                 const int index,
                 double &distance,
                 std::vector<int> &indices_traversed,
                 const bool use_angles,
                 const double vx,
                 const double vy,
                 const double angle_deg) const;

    int search_neighbor_naive(const bool skip_ref_index,
                              const int ref_index,
                              const double x,
                              const double y,
                              const bool use_angles,
                              const double vx,
                              const double vy,
                              const double angle_deg) const;

    int search_neighbor_fast(const bool skip_ref_index,
                             const int ref_index,
                             const double x,
                             const double y,
                             const bool use_angles,
                             const double vx,
                             const double vy,
                             const double angle_deg) const;

    node *root;

    double bounds[2][2];
    double *x_coordinates;
    double *y_coordinates;
    int num_points;

    void check_that_context_is_initialized() const;
    bool is_initialized = false;
};
