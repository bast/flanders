use pyo3::prelude::*;
use rayon::prelude::*;

use std::collections::HashMap;

use crate::distance;
use crate::intersections;
use crate::vector;
use crate::vector::Vector;
use crate::view;

#[derive(Clone, Debug)]
struct Range {
    min: f64,
    max: f64,
}

#[pyclass]
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
#[pyfunction]
pub fn build_search_tree(points: Vec<(f64, f64)>) -> HashMap<usize, Node> {
    let mut tree = HashMap::new();

    let points = vector::tuples_to_vectors(&points);

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

#[pyfunction]
pub fn nearest_indices_from_indices(
    tree: HashMap<usize, Node>,
    observer_indices: Vec<usize>,
    view_vectors: Vec<(f64, f64)>,
    view_angles_deg: Vec<f64>,
) -> Vec<i32> {
    let view_vectors = vector::tuples_to_vectors(&view_vectors);

    observer_indices
        .par_iter()
        .enumerate()
        .map(|(i, oi)| wrap_nearest_from_index(&tree, *oi, &view_vectors[i], view_angles_deg[i]))
        .collect()
}

#[pyfunction]
pub fn nearest_indices_from_coordinates(
    tree: HashMap<usize, Node>,
    observer_coordinates: Vec<(f64, f64)>,
    view_vectors: Vec<(f64, f64)>,
    view_angles_deg: Vec<f64>,
) -> Vec<i32> {
    let observer_coordinates = vector::tuples_to_vectors(&observer_coordinates);
    let view_vectors = vector::tuples_to_vectors(&view_vectors);

    observer_coordinates
        .par_iter()
        .enumerate()
        .map(|(i, oc)| {
            wrap_nearest_from_coordinate(&tree, &oc, &view_vectors[i], view_angles_deg[i])
        })
        .collect()
}

fn wrap_nearest_from_index(
    tree: &HashMap<usize, Node>,
    observer_index: usize,
    view_vector: &Vector,
    view_angles_deg: f64,
) -> i32 {
    let large_number = std::f64::MAX;
    let (index, _) = nearest_index(
        0,
        -1,
        large_number,
        &tree,
        None,
        Some(observer_index),
        &view_vector,
        view_angles_deg,
    );
    index
}

fn wrap_nearest_from_coordinate(
    tree: &HashMap<usize, Node>,
    observer_coordinate: &Vector,
    view_vector: &Vector,
    view_angles_deg: f64,
) -> i32 {
    let large_number = std::f64::MAX;
    let (index, _) = nearest_index(
        0,
        -1,
        large_number,
        &tree,
        Some(*observer_coordinate),
        None,
        &view_vector,
        view_angles_deg,
    );
    index
}

fn nearest_index(
    current_index: usize,
    best_index: i32,
    best_distance: f64,
    tree: &HashMap<usize, Node>,
    observer_coordinate_option: Option<Vector>,
    observer_index_option: Option<usize>,
    view_vector: &Vector,
    view_angle_deg: f64,
) -> (i32, f64) {
    let mut new_best_index = best_index;
    let mut new_best_distance = best_distance;

    let observer_coordinate = match (observer_coordinate_option, observer_index_option) {
        (Some(c), None) => c,
        (None, Some(i)) => {
            let n = tree.get(&i).unwrap();
            Vector {
                x: n.coordinates[0],
                y: n.coordinates[1],
            }
        }
        (_, _) => panic!("unexpected combination in nearest_index"),
    };

    let node = tree.get(&current_index).unwrap();

    // if we search by index, we don't want to consider the current index
    let skip_index = match observer_index_option {
        Some(i) => i == current_index,
        None => false,
    };

    if !skip_index {
        let c = Vector {
            x: node.coordinates[0],
            y: node.coordinates[1],
        };
        if view::point_within_angle(&c, &observer_coordinate, &view_vector, view_angle_deg) {
            let d = distance::distance(&observer_coordinate, &c);
            if d < new_best_distance {
                new_best_distance = d;
                new_best_index = current_index as i32;
            }
        }
    }

    let coordinates = vec![observer_coordinate.x, observer_coordinate.y];
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
                &observer_coordinate,
                &view_vector,
                view_angle_deg,
            );
        }
    } else {
        check_more = node.child_more.is_some();
        if node.child_less.is_some() && distance_to_split < best_distance {
            check_less = node_is_in_view(
                &tree.get(&node.child_less.unwrap()).unwrap(),
                &observer_coordinate,
                &view_vector,
                view_angle_deg,
            );
        }
    }

    if check_less {
        let (i, d) = nearest_index(
            node.child_less.unwrap(),
            new_best_index,
            new_best_distance,
            &tree,
            observer_coordinate_option,
            observer_index_option,
            &view_vector,
            view_angle_deg,
        );
        if d < new_best_distance {
            new_best_distance = d;
            new_best_index = i;
        }
    }

    if check_more {
        let (i, d) = nearest_index(
            node.child_more.unwrap(),
            new_best_index,
            new_best_distance,
            &tree,
            observer_coordinate_option,
            observer_index_option,
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
    // to check this we go around the four corners
    //  corner2 -----.  corner1 --corner2
    //    |          |    |          |
    //    |          | -> |          | -> ....
    //    |          |    |          |
    //  corner1 -----.    .----------.

    for (corner1, corner2) in [
        (
            Vector {
                x: node.bounds[0].min,
                y: node.bounds[1].min,
            },
            Vector {
                x: node.bounds[0].min,
                y: node.bounds[1].max,
            },
        ),
        (
            Vector {
                x: node.bounds[0].min,
                y: node.bounds[1].max,
            },
            Vector {
                x: node.bounds[0].max,
                y: node.bounds[1].max,
            },
        ),
        (
            Vector {
                x: node.bounds[0].max,
                y: node.bounds[1].min,
            },
            Vector {
                x: node.bounds[0].max,
                y: node.bounds[1].max,
            },
        ),
        (
            Vector {
                x: node.bounds[0].min,
                y: node.bounds[1].min,
            },
            Vector {
                x: node.bounds[0].max,
                y: node.bounds[1].min,
            },
        ),
    ]
    .iter()
    {
        if intersections::view_cone_and_line_intersect(
            &corner1,
            &corner2,
            &observer,
            &view_vector,
            view_angle_deg,
        ) {
            return true;
        }
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
