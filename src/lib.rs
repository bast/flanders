//! Flanders: Fast 2D nearest neighbor search with an angle.

mod distance;
mod intersections;
mod python;
mod tree;
mod vector;
mod view;

pub use crate::tree::build_search_tree;

pub use crate::tree::nearest_indices_from_coordinates;
pub use crate::tree::nearest_indices_from_indices;

pub use crate::view::nearest_indices_from_coordinates_noddy;
pub use crate::view::nearest_indices_from_indices_noddy;
