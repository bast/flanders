use std::num::ParseFloatError;
use std::str::FromStr;

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
    pub fn add(&self, v: &Vector) -> Vector {
        Vector {
            x: self.x + v.x,
            y: self.y + v.y,
        }
    }
}

impl FromStr for Vector {
    type Err = ParseFloatError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let coords: Vec<&str> = s.split_whitespace().collect();

        let x = coords[0].parse()?;
        let y = coords[1].parse()?;

        Ok(Vector { x, y })
    }
}
