#pragma once
#include <vector>
#include <string>
#include <hnswlib/hnswlib.h>

struct SearchResult {
    int id;
    float score;
};

class MemoryEngine {
public:
    MemoryEngine(int dim, int max_elements);
    ~MemoryEngine();

    void addVector(int id, const std::vector<float>& embedding);
    std::vector<SearchResult> search(const std::vector<float>& query, int top_k);
    void saveIndex(const std::string& path);
    void loadIndex(const std::string& path);

private:
    int dim;
    hnswlib::L2Space* space;
    hnswlib::HierarchicalNSW<float>* index;
};