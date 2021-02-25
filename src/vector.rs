#[derive(Debug, Clone, Copy)]
pub struct Vector {
    pub x: f64,
    pub y: f64,
}

impl Vector {
    pub fn length(&self) -> f64 {
        (self.x * self.x + self.y * self.y).sqrt()
    }
    pub fn scale(&self, factor: f64) -> Vector {
        Vector {
            x: factor * self.x,
            y: factor * self.y,
        }
    }
}

pub fn tuples_to_vectors(tuples: &[(f64, f64)]) -> Vec<Vector> {
    tuples.iter().map(|t| Vector { x: t.0, y: t.1 }).collect()
}
