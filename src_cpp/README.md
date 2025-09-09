# Greedy Syndrome Mapper (C++ Version)

This directory contains a C++ implementation of the Greedy Syndrome Mapper algorithm. It provides an interactive command-line interface (CLI) to calculate syndrome mappings and parity check matrices from a given set of error patterns.

## Dependencies

This project depends on **Eigen 3.4.0**. The build system expects the Eigen source files to be located in `src_cpp/external/eigen-3.4.0`.

Since dependency files are not tracked by Git, you must download and place Eigen in the correct directory before building the project.

### Dependency Setup

1.  **Create the `external` directory** (if it doesn't exist):
    ```sh
    mkdir -p src_cpp/external
    ```

2.  **Download the Eigen 3.4.0 source code archive:**
    ```sh
    curl -L -o src_cpp/external/eigen-3.4.0.tar.gz https://gitlab.com/libeigen/eigen/-/archive/3.4.0/eigen-3.4.0.tar.gz
    ```

3.  **Extract the archive** into the `external` directory:
    ```sh
    tar -xzf src_cpp/external/eigen-3.4.0.tar.gz -C src_cpp/external/
    ```

After these steps, you should have a directory structure like `src_cpp/external/eigen-3.4.0/...`. You can then proceed with the build instructions.

## How to Build

The project uses CMake for building. 

1.  **Navigate to the C++ source directory:**
    ```sh
    cd src_cpp
    ```

2.  **Configure and build the project:**
    It's recommended to create a `build` directory for the build files.
    ```sh
    cmake -S . -B build
    cmake --build build
    ```

3.  **Find the executable:**
    After a successful build, the executable `ltc_cli` will be located in the `build/` directory.

## How to Use

Run the executable from the `src_cpp` directory:

```sh
./build/ltc_cli
```

The application will start in an interactive mode:

1.  **Startup**: The program will first run and display two built-in examples.
2.  **Menu**: After the examples, you will be presented with a menu:

    ```
    ---------- Greedy Syndrome Mapper CLI ----------
    1. Run built-in examples
    2. Enter error patterns manually
    4. Exit
    --------------------------------------------
    ```

    -   **Option 1**: Reruns the built-in examples.
    -   **Option 2**: Allows you to enter your own error patterns.
        -   **Format**: Enter all patterns on a single line. Use commas (`,`) to separate patterns and spaces to separate the numbers within a pattern.
        -   **Example**: `1 0 1, 0 1 1, 1 1 1`
    -   **Option 4**: Exits the application.

