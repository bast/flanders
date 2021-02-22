#![allow(clippy::many_single_char_names)]
use crate::vector::Vector;

// rotate vector by angle_deg
fn rotate(vector: &Vector, angle_deg: f64) -> Vector {
    let angle_rad = angle_deg * std::f64::consts::PI / 180.0;

    Vector {
        x: vector.x * angle_rad.cos() - vector.y * angle_rad.sin(),
        y: vector.x * angle_rad.sin() + vector.y * angle_rad.cos(),
    }
}

// adapted after https://stackoverflow.com/a/2932601
fn ray_ray_intersection(
    a_origin: &Vector,
    a_direction: &Vector,
    b_origin: &Vector,
    b_direction: &Vector,
) -> Option<Vector> {
    let det = b_direction.x * a_direction.y - b_direction.y * a_direction.x;

    if det.abs() < f64::EPSILON {
        return None;
    }

    let dx = b_origin.x - a_origin.x;
    let dy = b_origin.y - a_origin.y;

    let u = (dy * b_direction.x - dx * b_direction.y) / det;

    Some(Vector {
        x: a_origin.x + u * a_direction.x,
        y: a_origin.y + u * a_direction.y,
    })
}

// From the observer point there is a ray with vector v.
// This function finds the intersection point u between the ray
// and a line p1-p2. If an intersection point exists, function returns true.
fn ray_and_line_intersect(p1: &Vector, p2: &Vector, observer: &Vector, v: &Vector) -> bool {
    let p1p2 = Vector {
        x: p2.x - p1.x,
        y: p2.y - p1.y,
    };

    match ray_ray_intersection(&p1, &p1p2, &observer, &v) {
        Some(intersection) => {
            // check whether intersection is not outside line bounds
            if intersection.x < p1.x.min(p2.x) {
                return false;
            }
            if intersection.x > p1.x.max(p2.x) {
                return false;
            }
            if intersection.y < p1.y.min(p2.y) {
                return false;
            }
            if intersection.y > p1.y.max(p2.y) {
                return false;
            }

            true
        }
        None => false,
    }
}

pub fn view_cone_and_line_intersect(
    p1: &Vector,
    p2: &Vector,
    observer: &Vector,
    view_vector: &Vector,
    view_angle_deg: f64,
) -> bool {
    let half_angle = 0.5 * view_angle_deg;

    let v_rotated = rotate(&view_vector, -half_angle);
    if ray_and_line_intersect(&p1, &p2, &observer, &v_rotated) {
        return true;
    }

    let v_rotated = rotate(&view_vector, half_angle);
    if ray_and_line_intersect(&p1, &p2, &observer, &v_rotated) {
        return true;
    }

    false
}
