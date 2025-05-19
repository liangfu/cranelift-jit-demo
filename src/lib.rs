pub mod frontend;
pub mod jit;
pub mod python;

use pyo3::prelude::*;

/// Python module for Cranelift JIT
#[pymodule]
fn cranelift_jit_demo(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<python::JitCompiler>()?;
    Ok(())
}
