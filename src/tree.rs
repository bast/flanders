use std::collections::HashMap;

use crate::vector::Vector;

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
        },
    );

    for (i, point) in points.iter().enumerate().skip(1) {
        let mut parent = 0;
        let mut num_divisions = 0;

        let coordinates = vec![point.x, point.y];

        let mut bounds: Vec<Range> = Vec::new();

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

        tree.insert(
            i,
            Node {
                coordinates,
                bounds,
                child_less: None,
                child_more: None,
            },
        );
    }

    tree
}
