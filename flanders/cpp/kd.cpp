#include <cstddef>  /* NULL */
#include <stdio.h>  /* printf */
#include <vector>  /* vector */
#include <algorithm>  /* find */
#include <math.h>  /* sqrt */


#include "kd.h"
#include "helpers.h"
#include "intersect.h"
#include "distance.h"
#include "cpp_interface.h"



#define AS_TYPE(Type, Obj) reinterpret_cast<Type *>(Obj)
#define AS_CTYPE(Type, Obj) reinterpret_cast<const Type *>(Obj)


context_t *new_context()
{
    return AS_TYPE(context_t, new btree());
}
btree::btree()
{
    root = NULL;
}


void free_context(context_t *context)
{
    if (!context) return;
    delete AS_TYPE(btree, context);
}
btree::~btree()
{
    destroy_tree();
}


CPP_INTERFACE_API
void set_bounds(
    context_t *context,
    const double bounds[2][2]
    )
{
    return AS_TYPE(btree, context)->set_bounds(bounds);
}
void btree::set_bounds(const double in_bounds[2][2])
{
    bounds[0][0] = in_bounds[0][0];
    bounds[0][1] = in_bounds[0][1];
    bounds[1][0] = in_bounds[1][0];
    bounds[1][1] = in_bounds[1][1];
}


void btree::destroy_tree()
{
    destroy_tree(root);
}


void btree::destroy_tree(node *leaf)
{
    if (leaf != NULL)
    {
        destroy_tree(leaf->children[0]);
        destroy_tree(leaf->children[1]);
        delete leaf;
    }
}


node *btree::guess_node(const double coordinates[2]) const
{
    return guess_node(coordinates, root);
}


node *btree::guess_node(const double coordinates[2], node *leaf) const
{
    int position = get_position(leaf, coordinates);

    if (leaf->children[position] == NULL)
    {
        return leaf;
    }
    else
    {
        return guess_node(coordinates, leaf->children[position]);
    }
}


CPP_INTERFACE_API
void insert(
    context_t *context,
    const double coordinates[2],
    const int    index
    )
{
    return AS_TYPE(btree, context)->insert(coordinates, index);
}
void btree::insert(const double coordinates[2], const int index)
{
    if (root == NULL)
    {
        // root does not exist, we create it
        root = new node;
        root->index = index;
        root->children[0] = NULL;
        root->children[1] = NULL;
        root->parent = NULL;
        root->split_dimension = 0;
        root->bounds[0][0] = bounds[0][0];
        root->bounds[0][1] = bounds[0][1];
        root->bounds[1][0] = bounds[1][0];
        root->bounds[1][1] = bounds[1][1];
        root->coordinates[0] = coordinates[0];
        root->coordinates[1] = coordinates[1];
    }
    else
    {
        // root exists, we insert to the root node
        insert(coordinates, index, root);
    }
}


void btree::insert(const double coordinates[2], const int index, node *leaf)
{
    // figure out whether we insert "left" or "right"
    int position = get_position(leaf, coordinates);

    if (leaf->children[position] == NULL)
    {
        // child position is vacant, create child

        // figure out new split dimension
        int new_split_dimension;
        if (leaf->split_dimension == 0)
        {
            new_split_dimension = 1;
        }
        else
        {
            new_split_dimension = 0;
        }

        // figure out new bounds
        double new_bounds[2][2];
        new_bounds[0][0] = leaf->bounds[0][0];
        new_bounds[0][1] = leaf->bounds[0][1];
        new_bounds[1][0] = leaf->bounds[1][0];
        new_bounds[1][1] = leaf->bounds[1][1];
        if (position == 0)
        {
            new_bounds[leaf->split_dimension][1] = leaf->coordinates[leaf->split_dimension];
        }
        else
        {
            new_bounds[leaf->split_dimension][0] = leaf->coordinates[leaf->split_dimension];
        }

        // create the child node
        node *child = new node;
        child->index = index;
        child->children[0] = NULL;
        child->children[1] = NULL;
        child->parent = leaf;
        child->split_dimension = new_split_dimension;
        child->bounds[0][0] = new_bounds[0][0];
        child->bounds[0][1] = new_bounds[0][1];
        child->bounds[1][0] = new_bounds[1][0];
        child->bounds[1][1] = new_bounds[1][1];
        child->coordinates[0] = coordinates[0];
        child->coordinates[1] = coordinates[1];
        leaf->children[position] = child;
    }
    else
    {
        // child position is full, delegate insertion to the child node
        insert(coordinates, index, leaf->children[position]);
    }
}


// Returns index of nearest point to points[ref_index].
// By default, only the distance counts. If angle and view vector
// are both not None, they are taken into account.
// In the latter case it is possible that no nearest neighbor exists,
// and in this case the function returns -1.
int btree::traverse(
    node *leaf,
    const int ref_index,
    const double ref_point[2],
    const int index,
          double &distance,
          std::vector<int> &indices_traversed,
    const bool use_angles,
    const double view_vector[2],
    const double view_angle_deg
    )
{
    int i = leaf->index;
    bool this_node_already_verified = (std::find(indices_traversed.begin(), indices_traversed.end(), i) != indices_traversed.end());

    if (this_node_already_verified)
    {
        // indices_traversed contains i
        // in case we have already checked this node, we return
        return index;
    }
    else
    {
        indices_traversed.push_back(i);
    }

    int new_index = index;

    double d = get_distance(leaf, ref_point);

    // we need to make sure that we skip the node which is the reference point
    if (i != ref_index)
    {
        bool is_in_view = true;
        if (use_angles)
        {
            is_in_view = point_within_view_angle(
                             leaf->coordinates[0],
                             leaf->coordinates[1],
                             ref_point[0],
                             ref_point[1],
                             view_vector[0],
                             view_vector[1],
                             view_angle_deg
                             );
        }
        if (is_in_view)
        {
            if (d < distance)
            {
                new_index = i;
                distance = d;
            }
        }
    }

    double ref_to_split = signed_distance_to_split(leaf, ref_point);

    for (int child_index = 0; child_index < 2; child_index++)
    {
        node *child = leaf->children[child_index];
        if (child != NULL)
        {
            double child_to_split = signed_distance_to_split(leaf, child->coordinates);

            bool consider_child = false;

            if (ref_to_split*child_to_split > 0.0)
            {
                // child is on the same side as the reference point
                consider_child = true;
            }
            else
            {
                // child is on the other side
                if (abs(ref_to_split) < distance)
                {
                    // radius is larger than distance to split line
                    if (not use_angles)
                    {
                        consider_child = true;
                    }
                    else
                    {
                        if (i == ref_index)
                        {
                            // reference point is the node
                            // for simplicity we will consider both children
                            // TODO here a shortcut is possible
                            // for this check the sign of the vector component perpendicular to
                            // the dividing split, if both ray vector components have same sign and opposite
                            // sign that the child, then one could skip the child
                            consider_child = true;
                        }
                        else
                        {
                            // if at least one ray intersects the bounds, we consider the child
                            // to check this we go around the four corners clock-wise
                            // starting from bottom left
                            //  corner2 -----.  corner1 --corner2
                            //    |          |    |          |
                            //    |          | -> |          | -> ....
                            //    |          |    |          |
                            //  corner1 -----.    .----------.
                            int corner1_x[4] = {0, 0, 1, 1};
                            int corner2_x[4] = {0, 1, 1, 0};
                            int corner1_y[4] = {0, 1, 1, 0};
                            int corner2_y[4] = {1, 1, 0, 0};

                            double p1[2];
                            double p2[2];

                            for (int icorner = 0; icorner < 4; icorner++)
                            {
                                p1[0] = leaf->bounds[0][corner1_x[icorner]];
                                p1[1] = leaf->bounds[1][corner1_y[icorner]];
                                p2[0] = leaf->bounds[0][corner2_x[icorner]];
                                p2[1] = leaf->bounds[1][corner2_y[icorner]];

                                int num_intersections;
                                if (not consider_child)
                                {
                                    num_intersections = get_num_intersections(
                                                            p1,
                                                            p2,
                                                            ref_point,
                                                            view_vector,
                                                            view_angle_deg
                                                            );
                                }
                                consider_child = (num_intersections > 0);
                            }

                            // if there is no intersection, it is possible that the ray covers entire
                            // area, in this case all boundary points are in the view cone and
                            // it is enough to check whether one of the boundary points is in view
                            if (not consider_child)
                            {
                                consider_child = point_within_view_angle(
                                                     leaf->bounds[0][0],
                                                     leaf->bounds[1][0],
                                                     ref_point[0],
                                                     ref_point[1],
                                                     view_vector[0],
                                                     view_vector[1],
                                                     view_angle_deg
                                                     );
                            }
                        }
                    }
                }
            }
            if (consider_child)
            {
                new_index = traverse(
                                child,
                                ref_index,
                                ref_point,
                                new_index,
                                distance,
                                indices_traversed,
                                use_angles,
                                view_vector,
                                view_angle_deg
                                );
            }
        }
    }

    if (leaf->parent == NULL)
    {
        // we have reached the root so we are done
        return new_index;
    }
    else
    {
        // we have changed both child nodes
        // and we are not yet at the root
        // so we go one level up
        return traverse(
                   leaf->parent,
                   ref_index,
                   ref_point,
                   new_index,
                   distance,
                   indices_traversed,
                   use_angles,
                   view_vector,
                   view_angle_deg
                   );
    }
}


int main()
{
    double bounds[2][2];
    bounds[0][0] = 0.04133871927984911;
    bounds[0][1] = 0.6266425027146401;
    bounds[1][0] = -0.6795408869623607;
    bounds[1][1] = 0.647177745066891;

    btree tree;
    tree.set_bounds(bounds);

    double coordinates[2];

    coordinates[0] = 0.142805189379827;
    coordinates[1] = -0.14222189064977075;
    tree.insert(coordinates, 0);

    coordinates[0] = 0.15618260226894076;
    coordinates[1] = -0.5878035357209965;
    tree.insert(coordinates, 1);

    coordinates[0] = 0.6266425027146401;
    coordinates[1] = 0.647177745066891;
    tree.insert(coordinates, 2);

    coordinates[0] = 0.30694506780235153;
    coordinates[1] = -0.6795408869623607;
    tree.insert(coordinates, 3);

    coordinates[0] = 0.04133871927984911;
    coordinates[1] = -0.3444543767558137;
    tree.insert(coordinates, 4);

    coordinates[0] = 0.3;
    coordinates[1] = -0.8;
    node *guess;
    guess = tree.guess_node(coordinates);
    printf("guess: %i\n", guess->index);

    coordinates[0] = 0.15618260226894076;
    coordinates[1] = -0.5878035357209965;
    int ref_index = 1;
    guess = tree.guess_node(coordinates);

    double d = std::numeric_limits<double>::max();
    int index_best = -1;
    double view_vector[2] = {0.9931139850789104, -0.9108872350991339};
    double view_angle_deg = 63.09231600261756;
    std::vector<int> indices_traversed;
    indices_traversed.clear();
    index_best = tree.traverse(
                     guess,
                     ref_index,
                     coordinates,
                     index_best,
                     d,
                     indices_traversed,
                     true,
                     view_vector,
                     view_angle_deg
                     );
    printf("found: %i\n", index_best);

    coordinates[0] = 0.6266425027146401;
    coordinates[1] = 0.647177745066891;
    ref_index = 2;
    guess = tree.guess_node(coordinates);

    view_vector[0] = 0.720322074572582;
    view_vector[1] = 0.2063812219363701;
    view_angle_deg = 36.648907235610;
    indices_traversed.clear();
    index_best = -1;
    d = std::numeric_limits<double>::max();
    index_best = tree.traverse(
                     guess,
                     ref_index,
                     coordinates,
                     index_best,
                     d,
                     indices_traversed,
                     true,
                     view_vector,
                     view_angle_deg
                     );
    printf("found: %i\n", index_best);

    return 0;
}


CPP_INTERFACE_API
int get_neighbor_index(
          context_t *context,
    const double coordinates[2],
    const int    index,
    const bool   use_angles,
    const double view_vector[2],
    const double view_angle_deg
    )
{
    return AS_TYPE(btree, context)->get_neighbor_index(
                                        coordinates,
                                        index,
                                        use_angles,
                                        view_vector,
                                        view_angle_deg
                                        );
}
int btree::get_neighbor_index(
    const double coordinates[2],
    const int    index,
    const bool   use_angles,
    const double view_vector[2],
    const double view_angle_deg
    ) // const FIXME?
{
    node *guess = guess_node(coordinates);

    double d = std::numeric_limits<double>::max();

    std::vector<int> indices_traversed;
    indices_traversed.clear();

    int index_best = -1;

    index_best = traverse(
                 guess,
                 index,
                 coordinates,
                 index_best,
                 d,
                 indices_traversed,
                 true,
                 view_vector,
                 view_angle_deg
                 );

    return index_best;
}
