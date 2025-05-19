import cranelift_jit_demo

def main():
    # Create a new JIT compiler instance
    jit = cranelift_jit_demo.JitCompiler()
    
    # A very simple example following the exact format expected by the parser
    code = """fn add(a, b) -> (c) {
    c = a + b
}
"""
    
    try:
        # Compile the code
        ptr = jit.compile(code)
        print(f"Compiled to: {ptr}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()