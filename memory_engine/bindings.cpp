#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "engine.h"

namespace py = pybind11;

PYBIND11_MODULE(memory_engine, m) {
    m.doc() = "MemoryOS C++ vector search engine";

    py::class_<SearchResult>(m, "SearchResult")
        .def_readonly("id", &SearchResult::id)
        .def_readonly("score", &SearchResult::score);

    py::class_<MemoryEngine>(m, "MemoryEngine")
        .def(py::init<int, int>(), py::arg("dim"), py::arg("max_elements"))
        .def("add_vector", &MemoryEngine::addVector)
        .def("search", &MemoryEngine::search)
        .def("save_index", &MemoryEngine::saveIndex)
        .def("load_index", &MemoryEngine::loadIndex);
}