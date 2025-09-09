# CMake minimum version
cmake_minimum_required(VERSION 3.10)

# Project name
project(LoopTransversalCode_CPP)

# C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Add include directories
include_directories(include)

# Add executable
add_executable(ltc_cli src/main.cpp src/greedy_syndrome_mapper.cpp)

# --- Dependencies ---
# For Eigen
target_include_directories(ltc_cli PRIVATE external/eigen-3.4.0)
