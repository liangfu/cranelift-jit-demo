# Cranelift JIT Demo - Python Bindings

This directory contains examples of using the Cranelift JIT Demo from Python.

## Installation

To install the Python bindings:

```bash
# Development installation
maturin develop

# Or build a wheel
maturin build
pip install target/wheels/cranelift_jit_demo-*.whl
```

## Example Usage

```python
import cranelift_jit_demo

# Create a new JIT compiler instance
jit = cranelift_jit_demo.JitCompiler()

# Example code in the toy language
code = """
function fibonacci(n) {
    if (n < 2) {
        return n;
    }
    return fibonacci(n-1) + fibonacci(n-2);
}

function main() {
    return fibonacci(10);
}
"""

# Run the code
result = jit.run(code)
print(f"Result: {result}")
```

## API Reference

### `JitCompiler`

- `__init__()`: Create a new JIT compiler instance
- `run(code: str) -> int`: Compile and execute the given code
- `compile(code: str) -> str`: Compile the given code and return a function ID
- `execute(function_id: str) -> int`: Execute a previously compiled function by ID