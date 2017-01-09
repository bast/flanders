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
        btree();
        ~btree();

        int get_neighbor_index(
            const double coordinates[2],
            const int    index,
            const bool   use_angles,
            const double view_vector[2],
            const double view_angle_deg
            );
        //  ) const;
        void set_bounds(const double in_bounds[2][2]);
        void insert(const double coordinates[2], const int index);
        node *guess_node(const double coordinates[2]) const; // FIXME move to private
        int traverse(  // FIXME make private and rename parameters
            node *leaf,
            const int ref_index,
            const double ref_point[2],
            const int index,
                  double &distance,
                  std::vector<int> &indices_traversed,
            const bool use_angles,
            const double view_vector[2],
            const double view_angle_deg
            );

    private:
        btree(const btree &rhs);            // not implemented
        btree &operator=(const btree &rhs); // not implemented

        void destroy_tree();
        void destroy_tree(node *leaf);

        void insert(const double coordinates[2], const int index, node *leaf);
        node *guess_node(const double coordinates[2], node *leaf) const;

        node *root;
        double bounds[2][2];
};

#endif /* BTREE_H_INCLUDED */
