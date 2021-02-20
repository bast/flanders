use crate::vector::Vector;

// rotate vector by angle_deg
pub fn rotate(vector: &Vector, angle_deg: f64) -> Vector {
    let angle_rad = angle_deg * std::f64::consts::PI / 180.0;

    Vector {
        x: vector.x * angle_rad.cos() - vector.y * angle_rad.sin(),
        y: vector.x * angle_rad.sin() + vector.y * angle_rad.cos(),
    }
}

// return line-line intersection coefficients using homogeneous coordinates
fn get_intersection(u1: &(f64, f64, f64), u2: &(f64, f64, f64)) -> (f64, f64, f64) {
    let a = u1.1 * u2.2 - u2.1 * u1.2;
    let b = u1.2 * u2.0 - u2.2 * u1.0;
    let c = u1.0 * u2.1 - u2.0 * u1.1;

    (a, b, c)
}

#[inline]
fn sgn(x: f64) -> i32 {
    if x < 0.0 {
        return -1;
    } else if x > 0.0 {
        return 1;
    } else {
        return 0;
    }
}

// find (a, b, c) in ax + bx + c = 0 from two points on that line
fn line_coeffs_from_two_points(p1: &Vector, p2: &Vector) -> (f64, f64, f64) {
    let a = p1.y - p2.y;
    let b = p2.x - p1.x;
    let c = (p1.x - p2.x) * p1.y + (p2.y - p1.y) * p1.x;

    (a, b, c)
}

// From the observer point there is a ray with vector v.
// This function finds the intersection point u between the ray
// and a line p1-p2. If an intersection point exists, function returns true.
fn intersection_point_exists(p1: &Vector, p2: &Vector, observer: &Vector, v: &Vector) -> bool {
    const TINY: f64 = 1.0e-20;

    let r2 = observer.add(&v);

    let ray = line_coeffs_from_two_points(&observer, &r2);
    let line = line_coeffs_from_two_points(&p1, &p2);

    let (a, b, c) = get_intersection(&line, &ray);

    if c.abs() < TINY {
        return false;
    }

    let u = Vector { x: a / c, y: b / c };

    // check whether intersection is in the direction of the ray
    if sgn(u.x - observer.x) != sgn(v.x) {
        return false;
    }
    if sgn(u.y - observer.y) != sgn(v.y) {
        return false;
    }

    // check whether intersection is not outside line bounds
    // FIXME check this code - when porting to Rust I didn't understand this anymore and converted
    // in the blind
    let min_loc = p1.x.min(p2.x);
    let max_loc = p1.x.max(p2.x);
    if (max_loc - min_loc).abs() > TINY {
        if (u.x.min(min_loc) - u.x).abs() > TINY {
            return false;
        }
        if (u.x.max(max_loc) - u.x).abs() > TINY {
            return false;
        }
    }
    let min_loc = p1.y.min(p2.y);
    let max_loc = p1.y.max(p2.y);
    if (max_loc - min_loc).abs() > TINY {
        if (u.y.min(min_loc) - u.y).abs() > TINY {
            return false;
        }
        if (u.y.max(max_loc) - u.y).abs() > TINY {
            return false;
        }
    }

    // intersection point exists
    true
}

// Computes number of intersection of two rays starting from view_origin
// intersecting with line between p1 and p2.
// Returns 0, 1, or 2.
fn get_num_intersections(
    p1: &Vector,
    p2: &Vector,
    observer: &Vector,
    view_vector: &Vector,
    view_angle_deg: f64,
) -> i32 {
    let mut n = 0;

    let v_rotated = rotate(&view_vector, -view_angle_deg / 2.0);
    if intersection_point_exists(&p1, &p2, &observer, &v_rotated) {
        n += 1;
    }

    let v_rotated = rotate(&view_vector, view_angle_deg / 2.0);
    if intersection_point_exists(&p1, &p2, &observer, &v_rotated) {
        n += 1;
    }

    n
}
