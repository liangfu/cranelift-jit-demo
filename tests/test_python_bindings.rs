#[cfg(test)]
mod tests {
    use cranelift_jit_demo::python::JitCompiler;
    use pyo3::prelude::*;
    use pyo3::types::PyDict;

    #[test]
    fn test_jit_compiler_creation() {
        Python::with_gil(|py| {
            let jit_compiler = JitCompiler::new().expect("Failed to create JitCompiler");
            assert!(jit_compiler.jit.is_initialized());
        });
    }

    #[test]
    fn test_simple_compilation() {
        Python::with_gil(|py| {
            let mut jit_compiler = JitCompiler::new().expect("Failed to create JitCompiler");
            
            let code = r#"
                function main() {
                    return 42
                }
            "#;
            
            let result = jit_compiler.run(code).expect("Failed to run code");
            assert_eq!(result, 42);
        });
    }

    #[test]
    fn test_compile_and_execute() {
        Python::with_gil(|py| {
            let mut jit_compiler = JitCompiler::new().expect("Failed to create JitCompiler");
            
            let code = r#"
                function main() {
                    return 42
                }
            "#;
            
            let func_id = jit_compiler.compile(code).expect("Failed to compile code");
            assert!(!func_id.is_empty());
            
            let result = jit_compiler.execute(&func_id).expect("Failed to execute function");
            assert_eq!(result, 42);
        });
    }

    #[test]
    fn test_python_module() {
        Python::with_gil(|py| {
            let module = PyModule::new(py, "cranelift_jit_test").unwrap();
            
            // Add the JitCompiler class to the module
            module.add_class::<JitCompiler>().unwrap();
            
            // Create a Python execution environment
            let locals = PyDict::new(py);
            locals.set_item("JitCompiler", module.getattr("JitCompiler").unwrap()).unwrap();
            
            // Execute Python code that uses our module
            let code = r#"
                jit = JitCompiler()
                code = """
                function main() {
                    return 42
                }
                """
                result = jit.run(code)
                assert result == 42
            "#;
            
            py.run(code, None, Some(locals)).unwrap();
        });
    }
}