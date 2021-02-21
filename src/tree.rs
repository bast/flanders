use std::collections::HashMap;

use crate::distance;
use crate::intersections;
use crate::vector::Vector;
use crate::view;

#[derive(Clone, Debug)]
struct Range {
    min: f64,
    max: f64,
}

#[derive(Clone, Debug)]
pub struct Node {
    coordinates: Vec<f64>,
    bounds: Vec<Range>,
    child_less: Option<usize>,
    child_more: Option<usize>,
    split_dimension: usize,
}

fn get_bbox(points: &[Vector]) -> (f64, f64, f64, f64) {
    let large_number = std::f64::MAX;

    let mut xmin = large_number;
    let mut xmax = -large_number;
    let mut ymin = large_number;
    let mut ymax = -large_number;

    for point in points {
        xmin = xmin.min(point.x);
        xmax = xmax.max(point.x);
        ymin = ymin.min(point.y);
        ymax = ymax.max(point.y);
    }

    (xmin, xmax, ymin, ymax)
}

// for these points:
// 0  0.142 -0.142
// 1  0.156 -0.587
// 2  0.626  0.647
// 3  0.306 -0.679
// 4  0.041 -0.344
// 5 -0.500  0.905
// 6  0.993 -0.910
// 7  0.720  0.206
// 8 -0.236 -0.432
// 9  0.349 -0.086   .
//
// we construct this tree:
//                 0           split on: x
//                / \
//               /   \
//              /     \
//             4       1                y
//            / \     / \
//           /   \   /   \
//          8     5 3     2             x
//                   \   / \
//                    6 9   7           y
pub fn build_tree(points: &[Vector]) -> HashMap<usize, Node> {
    let mut tree = HashMap::new();

    let (xmin, xmax, ymin, ymax) = get_bbox(&points);

    // create root node
    tree.insert(
        0,
        Node {
            coordinates: vec![points[0].x, points[0].y],
            bounds: vec![
                Range {
                    min: xmin,
                    max: xmax,
                },
                Range {
                    min: ymin,
                    max: ymax,
                },
            ],
            child_less: None,
            child_more: None,
            split_dimension: 0,
        },
    );

    for (i, point) in points.iter().enumerate().skip(1) {
        let mut parent = 0;
        let mut num_divisions = 0;

        let coordinates = vec![point.x, point.y];

        let mut bounds;

        loop {
            let split_dimension = num_divisions % 2;
            let parent_node = tree.get_mut(&parent).unwrap();

            if coordinates[split_dimension] < parent_node.coordinates[split_dimension] {
                match parent_node.child_less {
                    Some(p) => parent = p,
                    None => {
                        parent_node.child_less = Some(i);
                        bounds = parent_node.bounds.clone();
                        bounds[split_dimension].max = parent_node.coordinates[split_dimension];
                        break;
                    }
                }
            } else {
                match parent_node.child_more {
                    Some(p) => parent = p,
                    None => {
                        parent_node.child_more = Some(i);
                        bounds = parent_node.bounds.clone();
                        bounds[split_dimension].min = parent_node.coordinates[split_dimension];
                        break;
                    }
                }
            }

            num_divisions += 1;
        }

        num_divisions += 1;

        tree.insert(
            i,
            Node {
                coordinates,
                bounds,
                child_less: None,
                child_more: None,
                split_dimension: num_divisions % 2,
            },
        );
    }

    tree
}

pub fn nearest_index_from_coordinates(
    current_index: usize,
    best_index: i32,
    best_distance: f64,
    tree: &HashMap<usize, Node>,
    observer: &Vector,
    view_vector: &Vector,
    view_angle_deg: f64,
) -> (i32, f64) {
    let mut new_best_index = best_index;
    let mut new_best_distance = best_distance;

    let node = tree.get(&current_index).unwrap();
    let c = Vector {
        x: node.coordinates[0],
        y: node.coordinates[1],
    };
    if view::point_within_angle(&c, &observer, &view_vector, view_angle_deg) {
        let d = distance::distance(&observer, &c);
        if d < new_best_distance {
            new_best_distance = d;
            new_best_index = current_index as i32;
        }
    }

    let coordinates = vec![observer.x, observer.y];
    let signed_distance_to_split =
        coordinates[node.split_dimension] - node.coordinates[node.split_dimension];
    let distance_to_split = signed_distance_to_split.abs();

    let mut check_less = false;
    let mut check_more = false;

    if signed_distance_to_split < 0.0 {
        check_less = node.child_less.is_some();
        if node.child_more.is_some() && distance_to_split < best_distance {
            check_more = node_is_in_view(
                &tree.get(&node.child_more.unwrap()).unwrap(),
                &observer,
                &view_vector,
                view_angle_deg,
            );
        }
    } else {
        check_more = node.child_more.is_some();
        if node.child_less.is_some() && distance_to_split < best_distance {
            check_less = node_is_in_view(
                &tree.get(&node.child_less.unwrap()).unwrap(),
                &observer,
                &view_vector,
                view_angle_deg,
            );
        }
    }

    if check_less {
        let (i, d) = nearest_index_from_coordinates(
            node.child_less.unwrap(),
            new_best_index,
            new_best_distance,
            &tree,
            &observer,
            &view_vector,
            view_angle_deg,
        );
        if d < new_best_distance {
            new_best_distance = d;
            new_best_index = i;
        }
    }

    if check_more {
        let (i, d) = nearest_index_from_coordinates(
            node.child_more.unwrap(),
            new_best_index,
            new_best_distance,
            &tree,
            &observer,
            &view_vector,
            view_angle_deg,
        );
        if d < new_best_distance {
            new_best_distance = d;
            new_best_index = i;
        }
    }

    (new_best_index, new_best_distance)
}

fn node_is_in_view(
    node: &Node,
    observer: &Vector,
    view_vector: &Vector,
    view_angle_deg: f64,
) -> bool {
    // if there is no intersection, it is possible that
    // the ray covers entire
    // area, in this case all boundary points are in the
    // view cone and
    // it is enough to check whether one of the boundary
    // points is in view
    node_intersected_by_rays(&node, &observer, &view_vector, view_angle_deg)
        || node_boundary_corner_in_view_cone(&node, &observer, &view_vector, view_angle_deg)
}

// check whether at least one ray intersects the bounds of a node
fn node_intersected_by_rays(
    node: &Node,
    observer: &Vector,
    view_vector: &Vector,
    view_angle_deg: f64,
) -> bool {
    // to check this we go around the four corners, clockwise
    //  corner2 -----.  corner1 --corner2
    //    |          |    |          |
    //    |          | -> |          | -> ....
    //    |          |    |          |
    //  corner1 -----.    .----------.

    let corner1 = Vector {
        x: node.bounds[0].min,
        y: node.bounds[1].min,
    };
    let corner2 = Vector {
        x: node.bounds[0].min,
        y: node.bounds[1].max,
    };
    if intersections::num_intersections(&corner1, &corner2, &observer, &view_vector, view_angle_deg)
        > 0
    {
        return true;
    }

    let corner1 = Vector {
        x: node.bounds[0].min,
        y: node.bounds[1].max,
    };
    let corner2 = Vector {
        x: node.bounds[0].max,
        y: node.bounds[1].max,
    };
    if intersections::num_intersections(&corner1, &corner2, &observer, &view_vector, view_angle_deg)
        > 0
    {
        return true;
    }

    let corner1 = Vector {
        x: node.bounds[0].max,
        y: node.bounds[1].max,
    };
    let corner2 = Vector {
        x: node.bounds[0].max,
        y: node.bounds[1].min,
    };
    if intersections::num_intersections(&corner1, &corner2, &observer, &view_vector, view_angle_deg)
        > 0
    {
        return true;
    }

    let corner1 = Vector {
        x: node.bounds[0].max,
        y: node.bounds[1].min,
    };
    let corner2 = Vector {
        x: node.bounds[0].min,
        y: node.bounds[1].min,
    };
    if intersections::num_intersections(&corner1, &corner2, &observer, &view_vector, view_angle_deg)
        > 0
    {
        return true;
    }

    false
}

fn node_boundary_corner_in_view_cone(
    node: &Node,
    observer: &Vector,
    view_vector: &Vector,
    view_angle_deg: f64,
) -> bool {
    let one_corner = Vector {
        x: node.bounds[0].min,
        y: node.bounds[1].min,
    };

    view::point_within_angle(&one_corner, &observer, &view_vector, view_angle_deg)
}
