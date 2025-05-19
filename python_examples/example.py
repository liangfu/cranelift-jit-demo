import cranelift_jit_demo

def main():
    # Create a new JIT compiler instance
    jit = cranelift_jit_demo.JitCompiler()
    
    # First define the fibonacci function
    fib_code = """fn fibonacci(n) -> (result) {
    if n < 2 {
        result = n
    } else {
        result = fibonacci(n - 1) + fibonacci(n - 2)
    }
}
"""
    
    # Then define a main function that calls fibonacci
    main_code = """fn main() -> (result) {
    result = fibonacci(10)
}
"""
    
    # First compile and the fibonacci function
    try:
        fib_ptr = jit.compile(fib_code)
        print(f"Compiled fibonacci: {fib_ptr}")
    except Exception as e:
        print(f"Error compiling fibonacci: {e}")
        return
    
    # Then compile the main function
    try:
        main_ptr = jit.compile(main_code)
        print(f"Compiled main: {main_ptr}")
    except Exception as e:
        print(f"Error compiling main: {e}")
        return
    
    # Execute the main function
    try:
        result = jit.execute(main_ptr)
        print(f"Result from main function: {result}")
    except Exception as e:
        print(f"Error executing main: {e}")

if __name__ == "__main__":
    main()