use crate::jit::JIT;
use pyo3::exceptions::{PyRuntimeError, PySyntaxError};
use pyo3::prelude::*;

/// JIT Compiler for the Cranelift toy language
#[pyclass]
pub struct JitCompiler {
    pub jit: JIT,
}

#[pymethods]
impl JitCompiler {
    /// Create a new JIT compiler instance
    #[new]
    pub fn new() -> PyResult<Self> {
        Ok(Self { jit: JIT::default() })
    }

    /// Compile and execute code
    #[pyo3(text_signature = "($self, code)")]
    pub fn run(&mut self, code: &str) -> PyResult<i64> {
        // Compile the code
        let code_ptr = match self.jit.compile(code) {
            Ok(ptr) => ptr,
            Err(err) => return Err(PySyntaxError::new_err(format!("Compilation error: {}", err))),
        };
        
        // Execute the compiled code
        // We need to transmute the pointer to a function and call it
        let code_fn = unsafe { std::mem::transmute::<_, fn() -> i64>(code_ptr) };
        let result = code_fn();
        Ok(result)
    }

    /// Compile code but do not execute it
    #[pyo3(text_signature = "($self, code)")]
    pub fn compile(&mut self, code: &str) -> PyResult<String> {
        match self.jit.compile(code) {
            Ok(ptr) => Ok(format!("{:p}", ptr)),
            Err(err) => Err(PyRuntimeError::new_err(format!("Compilation error: {}", err))),
        }
    }

    /// Execute a previously compiled function by pointer
    #[pyo3(text_signature = "($self, function_id)")]
    pub fn execute(&mut self, function_id: &str) -> PyResult<i64> {
        // Parse the pointer from string
        let ptr = match function_id.trim().strip_prefix("0x") {
            Some(hex) => {
                match usize::from_str_radix(hex, 16) {
                    Ok(addr) => addr,
                    Err(_) => return Err(PyRuntimeError::new_err("Invalid function pointer format")),
                }
            },
            None => return Err(PyRuntimeError::new_err("Invalid function pointer format")),
        };

        // Convert pointer to function and call it
        let code_fn = unsafe { std::mem::transmute::<_, fn() -> i64>(ptr) };
        let result = code_fn();
        Ok(result)
    }
}