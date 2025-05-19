#!/usr/bin/env python3
import unittest
import sys
import os

# Add the parent directory to sys.path to find the module when running tests directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    import cranelift_jit_demo
except ImportError:
    print("cranelift_jit_demo module not found. Run 'maturin develop' first.")
    sys.exit(1)


class TestCraneliftBindings(unittest.TestCase):
    def setUp(self):
        self.jit = cranelift_jit_demo.JitCompiler()
        
    def test_simple_function(self):
        """Test a simple function that returns a constant."""
        code = """
        function main() {
            return 42
        }
        """
        result = self.jit.run(code)
        self.assertEqual(result, 42)
        
    def test_arithmetic(self):
        """Test basic arithmetic operations."""
        code = """
        function main() {
            let a = 10
            let b = 5
            return a + b * 2
        }
        """
        result = self.jit.run(code)
        self.assertEqual(result, 20)
        
    def test_if_statement(self):
        """Test if statement functionality."""
        code = """
        function main() {
            let x = 10
            if (x > 5) {
                return 1
            } else {
                return 0
            }
        }
        """
        result = self.jit.run(code)
        self.assertEqual(result, 1)
        
    def test_recursive_function(self):
        """Test recursive function calls (factorial)."""
        code = """
        function factorial(n) {
            if (n <= 1) {
                return 1
            }
            return n * factorial(n - 1)
        }
        
        function main() {
            return factorial(5)
        }
        """
        result = self.jit.run(code)
        self.assertEqual(result, 120)
        
    def test_compile_and_execute(self):
        """Test separate compile and execute functionality."""
        code = """
        function main() {
            return 42
        }
        """
        func_id = self.jit.compile(code)
        self.assertIsInstance(func_id, str)
        result = self.jit.execute(func_id)
        self.assertEqual(result, 42)
        
    def test_syntax_error(self):
        """Test handling of syntax errors."""
        code = """
        function main() {
            return 42
        """  # Missing closing brace
        with self.assertRaises(Exception) as context:
            self.jit.run(code)
        self.assertTrue("Syntax error" in str(context.exception))


if __name__ == "__main__":
    unittest.main()