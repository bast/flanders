//! Flanders: Fast 2D nearest neighbor search with an angle.

mod distance;
mod intersections;
mod tree;
mod vector;
mod view;

pub use crate::tree::build_tree;
pub use crate::vector::Vector;
pub use crate::view::nearest_index_from_coordinates_noddy;
pub use crate::view::nearest_index_from_index_noddy;
