use crate::distance;
use crate::vector::Vector;

// Check whether point is in view described by observer, view_vector,
// and view_angle.
pub fn point_within_angle(
    point: &Vector,
    observer: &Vector,
    view_vector: &Vector,
    view_angle_deg: f64,
) -> bool {
    let op = Vector {
        x: point.x - observer.x,
        y: point.y - observer.y,
    };

    let norm_view_vector = view_vector.scale(1.0 / view_vector.length());

    let op_normalized = op.scale(1.0 / op.length());

    let angle_rad =
        (norm_view_vector.x * op_normalized.x + norm_view_vector.y * op_normalized.y).acos();

    let angle_deg = angle_rad * 180.0 / std::f64::consts::PI;

    angle_deg.abs() <= (view_angle_deg / 2.0).abs()
}

pub fn nearest_indices_from_coordinates_noddy(
    points: &[Vector],
    observer_coordinates: &[Vector],
    view_vectors: &[Vector],
    view_angles_deg: &[f64],
) -> Vec<i32> {
    let large_number = std::f64::MAX;
    let mut indices = Vec::new();

    for (j, observer) in observer_coordinates.iter().enumerate() {
        let mut best_distance = large_number;
        let mut index = -1;
        for (i, point) in points.iter().enumerate() {
            if point_within_angle(&point, &observer, &view_vectors[j], view_angles_deg[j]) {
                let d = distance::distance(&point, &observer);
                if d < best_distance {
                    best_distance = d;
                    index = i as i32;
                }
            }
        }
        indices.push(index);
    }

    indices
}

pub fn nearest_indices_from_indices_noddy(
    points: &[Vector],
    observer_indices: &[usize],
    view_vectors: &[Vector],
    view_angles_deg: &[f64],
) -> Vec<i32> {
    let large_number = std::f64::MAX;
    let mut indices = Vec::new();

    for (j, &observer_index) in observer_indices.iter().enumerate() {
        let mut best_distance = large_number;
        let mut index = -1;
        for (i, point) in points.iter().enumerate() {
            if i != observer_index {
                if point_within_angle(
                    &point,
                    &points[observer_index],
                    &view_vectors[j],
                    view_angles_deg[j],
                ) {
                    let d = distance::distance(&point, &points[observer_index]);
                    if d < best_distance {
                        best_distance = d;
                        index = i as i32;
                    }
                }
            }
        }
        indices.push(index);
    }

    indices
}
