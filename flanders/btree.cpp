#include <algorithm>
#include <limits>
#include <math.h>
#include <stdio.h>

#include "btree.h"
#include "distance.h"
#include "flanders.h"
#include "helpers.h"
#include "intersect.h"

#define AS_TYPE(Type, Obj) reinterpret_cast<Type *>(Obj)
#define AS_CTYPE(Type, Obj) reinterpret_cast<const Type *>(Obj)

context_t *new_context(const int num_points, const double x[], const double y[])
{
    return AS_TYPE(context_t, new btree(num_points, x, y));
}
btree::btree(const int num_points, const double x[], const double y[])
{
    root = NULL;

    x_coordinates = new double[num_points];
    y_coordinates = new double[num_points];

    bounds[0][0] = std::numeric_limits<double>::max();
    bounds[0][1] = -bounds[0][0];
    bounds[1][0] = bounds[0][0];
    bounds[1][1] = -bounds[0][0];

    for (int i = 0; i < num_points; i++)
    {
        bounds[0][0] = std::min(bounds[0][0], x[i]);
        bounds[0][1] = std::max(bounds[0][1], x[i]);
        bounds[1][0] = std::min(bounds[1][0], y[i]);
        bounds[1][1] = std::max(bounds[1][1], y[i]);
    }

    for (int i = 0; i < num_points; i++)
    {
        insert(x[i], y[i], i);
    }
}

void free_context(context_t *context)
{
    if (!context)
        return;
    delete AS_TYPE(btree, context);
}
btree::~btree()
{
    destroy_tree();
    delete[] x_coordinates;
    delete[] y_coordinates;
}

void btree::destroy_tree() { destroy_tree(root); }

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

void btree::insert(const double x, const double y, const int index)
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
        root->coordinates[0] = x;
        root->coordinates[1] = y;
        x_coordinates[index] = x;
        y_coordinates[index] = y;
    }
    else
    {
        // root exists, we insert to the root node
        insert(x, y, index, root);
    }
}

void btree::insert(const double x, const double y, const int index, node *leaf)
{
    // figure out whether we insert "left" or "right"
    double coordinates[2] = {x, y};
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
            new_bounds[leaf->split_dimension][1] =
                leaf->coordinates[leaf->split_dimension];
        }
        else
        {
            new_bounds[leaf->split_dimension][0] =
                leaf->coordinates[leaf->split_dimension];
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
        x_coordinates[index] = coordinates[0];
        y_coordinates[index] = coordinates[1];
    }
    else
    {
        // child position is full, delegate insertion to the child node
        insert(x, y, index, leaf->children[position]);
    }
}

// Returns index of nearest point to points[ref_index].
// By default, only the distance counts. If angle and view vector
// are both not None, they are taken into account.
// In the latter case it is possible that no nearest neighbor exists,
// and in this case the function returns -1.
int btree::traverse(node *leaf,
                    const int ref_index,
                    const double ref_point[2],
                    const int index,
                    double &distance,
                    std::vector<int> &indices_traversed,
                    const bool use_angles,
                    const double view_vector[2],
                    const double view_angle_deg) const
{
    int i = leaf->index;
    bool this_node_already_verified =
        (std::find(indices_traversed.begin(), indices_traversed.end(), i) !=
         indices_traversed.end());

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
                leaf->coordinates, ref_point, view_vector, view_angle_deg);
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
            double child_to_split =
                signed_distance_to_split(leaf, child->coordinates);

            bool consider_child = false;

            if (ref_to_split * child_to_split > 0.0)
            {
                // child is on the same side as the reference point
                consider_child = true;
            }
            else
            {
                // child is on the other side
                if (fabs(ref_to_split) < distance)
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
                            // for this check the sign of the vector component
                            // perpendicular to
                            // the dividing split, if both ray vector components
                            // have same sign and opposite
                            // sign that the child, then one could skip the
                            // child
                            consider_child = true;
                        }
                        else
                        {
                            // if at least one ray intersects the bounds, we
                            // consider the child
                            // to check this we go around the four corners
                            // clock-wise
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
                                    num_intersections =
                                        get_num_intersections(p1,
                                                              p2,
                                                              ref_point,
                                                              view_vector,
                                                              view_angle_deg);
                                }
                                consider_child = (num_intersections > 0);
                            }

                            // if there is no intersection, it is possible that
                            // the ray covers entire
                            // area, in this case all boundary points are in the
                            // view cone and
                            // it is enough to check whether one of the boundary
                            // points is in view
                            if (not consider_child)
                            {
                                double corner_point[2] = {leaf->bounds[0][0],
                                                          leaf->bounds[1][0]};
                                consider_child =
                                    point_within_view_angle(corner_point,
                                                            ref_point,
                                                            view_vector,
                                                            view_angle_deg);
                            }
                        }
                    }
                }
            }
            if (consider_child)
            {
                new_index = traverse(child,
                                     ref_index,
                                     ref_point,
                                     new_index,
                                     distance,
                                     indices_traversed,
                                     use_angles,
                                     view_vector,
                                     view_angle_deg);
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
        return traverse(leaf->parent,
                        ref_index,
                        ref_point,
                        new_index,
                        distance,
                        indices_traversed,
                        use_angles,
                        view_vector,
                        view_angle_deg);
    }
}

CPP_INTERFACE_API
int search_neighbor(const context_t *context,
                    const int ref_index,
                    const bool use_angles,
                    const double view_vector[2],
                    const double view_angle_deg)
{
    return AS_CTYPE(btree, context)
        ->search_neighbor(ref_index, use_angles, view_vector, view_angle_deg);
}
int btree::search_neighbor(const int ref_index,
                           const bool use_angles,
                           const double view_vector[2],
                           const double view_angle_deg) const
{
    double coordinates[2] = {x_coordinates[ref_index],
                             y_coordinates[ref_index]};
    node *guess = guess_node(coordinates);

    double d = std::numeric_limits<double>::max();

    std::vector<int> indices_traversed;
    indices_traversed.clear();

    int index_best = -1;

    index_best = traverse(guess,
                          ref_index,
                          coordinates,
                          index_best,
                          d,
                          indices_traversed,
                          use_angles,
                          view_vector,
                          view_angle_deg);

    return index_best;
}
