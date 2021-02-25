use pyo3::prelude::*;
use pyo3::wrap_pyfunction;

use crate::tree::*;

#[pymodule]
fn flanders(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add("__version__", env!("CARGO_PKG_VERSION"))?;

    m.add_function(wrap_pyfunction!(build_search_tree, m)?)?;
    m.add_function(wrap_pyfunction!(nearest_indices_from_coordinates, m)?)?;
    m.add_function(wrap_pyfunction!(nearest_indices_from_indices, m)?)?;

    Ok(())
}
