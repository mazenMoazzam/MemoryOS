cmake_minimum_required(VERSION 3.15)
project(memory_engine)

set(CMAKE_CXX_STANDARD 17)

find_package(pybind11 REQUIRED)

include_directories(
    /Users/mazenmoazzam/Desktop/memoryOS/hnswlib
    /Users/mazenmoazzam/Library/Python/3.9/lib/python/site-packages/pybind11/include
)

pybind11_add_module(memory_engine
    engine.cpp
    bindings.cpp
)