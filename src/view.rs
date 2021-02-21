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

pub fn nearest_index_from_coordinates_noddy(
    points: &[Vector],
    observer: &Vector,
    view_vector: &Vector,
    view_angle_deg: f64,
) -> i32 {
    let large_number = std::f64::MAX;
    let mut best_distance = large_number;
    let mut index = -1;

    for (i, point) in points.iter().enumerate() {
        if point_within_angle(&point, &observer, &view_vector, view_angle_deg) {
            let d = distance::distance(&point, &observer);
            if d < best_distance {
                best_distance = d;
                index = i as i32;
            }
        }
    }

    index
}

pub fn nearest_index_from_index_noddy(
    points: &[Vector],
    observer_index: usize,
    view_vector: &Vector,
    view_angle_deg: f64,
) -> i32 {
    let large_number = std::f64::MAX;
    let mut best_distance = large_number;
    let mut index = -1;

    for (i, point) in points.iter().enumerate() {
        if i != observer_index
            && point_within_angle(
                &point,
                &points[observer_index],
                &view_vector,
                view_angle_deg,
            )
        {
            let d = distance::distance(&point, &points[observer_index]);
            if d < best_distance {
                best_distance = d;
                index = i as i32;
            }
        }
    }

    index
}
