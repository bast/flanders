#ifndef BTREE_H_INCLUDED
#define BTREE_H_INCLUDED

#include <vector>  /* vector */

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
        btree(const int num_points, const double in_bounds[2][2]);
        ~btree();

        void insert(const double coordinates[2], const int index);

        int find_neighbor(
            const int    index,
            const bool   use_angles,
            const double view_vector[2],
            const double view_angle_deg
            ) const;

    private:
        btree(const btree &rhs);            // not implemented
        btree &operator=(const btree &rhs); // not implemented

        void destroy_tree();
        void destroy_tree(node *leaf);

        void insert(const double coordinates[2], const int index, node *leaf);

        node *guess_node(const double coordinates[2]) const;
        node *guess_node(const double coordinates[2], node *leaf) const;

        int traverse(
            node *leaf,
            const int ref_index,
            const double ref_point[2],
            const int index,
                  double &distance,
                  std::vector<int> &indices_traversed,
            const bool use_angles,
            const double view_vector[2],
            const double view_angle_deg
            ) const;

        node *root;

        double bounds[2][2];
        double *x_coordinates;
        double *y_coordinates;
};

#endif /* BTREE_H_INCLUDED */
