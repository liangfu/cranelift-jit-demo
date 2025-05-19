#!/usr/bin/env python3
"""
Stress test for the cranelift_jit_demo Python bindings.
This script exercises various features of the toy language
and the Python bindings to ensure they work correctly.
"""

import sys
import os
import time

# Add the parent directory to sys.path to find the module when running directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    import cranelift_jit_demo
except ImportError:
    print("cranelift_jit_demo module not found. Run 'maturin develop' first.")
    sys.exit(1)

def run_benchmark(name, code, iterations=10):
    """Run a benchmark for the given code."""
    print(f"Running benchmark: {name}")
    
    jit = cranelift_jit_demo.JitCompiler()
    
    # Compile the code first
    start_time = time.time()
    func_id = jit.compile(code)
    compile_time = time.time() - start_time
    print(f"  Compile time: {compile_time:.6f} seconds")
    
    # Run the code multiple times
    total_time = 0
    for i in range(iterations):
        start_time = time.time()
        result = jit.execute(func_id)
        total_time += time.time() - start_time
    
    avg_time = total_time / iterations
    print(f"  Average execution time: {avg_time:.6f} seconds")
    print(f"  Result: {result}")
    print()
    
    return result

# Test 1: Recursive Fibonacci
recursive_fibonacci = """
function fibonacci(n) {
    if (n < 2) {
        return n;
    }
    return fibonacci(n-1) + fibonacci(n-2);
}

function main() {
    return fibonacci(15);
}
"""

# Test 2: Iterative Fibonacci
iterative_fibonacci = """
function fibonacci(n) {
    if (n == 0) {
        return 0;
    }
    
    let prev = 0;
    let curr = 1;
    let n = n - 1;
    
    while (n != 0) {
        let next = curr + prev;
        prev = curr;
        curr = next;
        n = n - 1;
    }
    
    return curr;
}

function main() {
    return fibonacci(30);
}
"""

# Test 3: Nested conditional logic
nested_conditionals = """
function test(a, b, c) {
    if (a > 0) {
        if (b > 0) {
            if (c > 0) {
                return 1;
            } else {
                return 2;
            }
        } else {
            if (c > 0) {
                return 3;
            } else {
                return 4;
            }
        }
    } else {
        if (b > 0) {
            if (c > 0) {
                return 5;
            } else {
                return 6;
            }
        } else {
            if (c > 0) {
                return 7;
            } else {
                return 8;
            }
        }
    }
}

function main() {
    let sum = 0;
    
    // Test all combinations of a, b, c being positive or negative
    let a = 1;
    while (a >= -1) {
        let b = 1;
        while (b >= -1) {
            let c = 1;
            while (c >= -1) {
                sum = sum + test(a, b, c);
                c = c - 2;
            }
            b = b - 2;
        }
        a = a - 2;
    }
    
    return sum;
}
"""

if __name__ == "__main__":
    print("=== Cranelift JIT Demo Python Bindings Stress Test ===\n")
    
    # Run the benchmarks
    fib_rec_result = run_benchmark("Recursive Fibonacci (n=15)", recursive_fibonacci)
    assert fib_rec_result == 610, f"Expected 610, got {fib_rec_result}"
    
    fib_iter_result = run_benchmark("Iterative Fibonacci (n=30)", iterative_fibonacci)
    assert fib_iter_result == 832040, f"Expected 832040, got {fib_iter_result}"
    
    conditionals_result = run_benchmark("Nested Conditionals", nested_conditionals)
    assert conditionals_result == 36, f"Expected 36, got {conditionals_result}"
    
    print("All stress tests passed successfully!")