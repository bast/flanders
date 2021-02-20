use crate::vector::Vector;

#[inline]
pub fn distance(p1: &Vector, p2: &Vector) -> f64 {
    let dx = p2.x - p1.x;
    let dy = p2.y - p1.y;

    (dx * dx + dy * dy).sqrt()
}
