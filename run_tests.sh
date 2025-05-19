#!/bin/bash
set -e

echo "Building with maturin..."
maturin develop

echo "Running Rust tests..."
cargo test

echo "Running Python tests..."
cd python_examples
python test_bindings.py

echo "All tests passed!"