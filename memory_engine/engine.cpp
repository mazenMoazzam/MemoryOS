#include "engine.h"
#include <stdexcept>
#include <algorithm>

MemoryEngine::MemoryEngine(int dim, int max_elements) : dim(dim) {
    space = new hnswlib::L2Space(dim);
    index = new hnswlib::HierarchicalNSW<float>(space, max_elements);
}

MemoryEngine::~MemoryEngine() {
    delete index;
    delete space;
}

void MemoryEngine::addVector(int id, const std::vector<float>& embedding) {
    if ((int)embedding.size() != dim) {
        throw std::invalid_argument("Embedding dimension mismatch");
    }
    index->addPoint(embedding.data(), id);
}

std::vector<SearchResult> MemoryEngine::search(const std::vector<float>& query, int top_k) {
    if ((int)query.size() != dim) {
        throw std::invalid_argument("Query dimension mismatch");
    }

    auto results = index->searchKnn(query.data(), top_k);
    std::vector<SearchResult> output;

    while (!results.empty()) {
        auto [score, id] = results.top();
        output.push_back({(int)id, score});
        results.pop();
    }

    std::sort(output.begin(), output.end(), [](const SearchResult& a, const SearchResult& b) {
        return a.score < b.score;
    });

    return output;
}

void MemoryEngine::saveIndex(const std::string& path) {
    index->saveIndex(path);
}

void MemoryEngine::loadIndex(const std::string& path) {
    delete index;
    index = new hnswlib::HierarchicalNSW<float>(space, path);
}