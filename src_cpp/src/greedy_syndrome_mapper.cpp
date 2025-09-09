#include "greedy_syndrome_mapper.hpp"
#include <stdexcept>
#include <algorithm>
#include <numeric>
#include <iostream> // For debugging, can be removed

#include <Eigen/Dense>

// --- Constructor ---
GreedySyndromeMapper::GreedySyndromeMapper(const std::vector<Vector>& error_patterns) {
    // Corresponds to the beginning of Python's __init__
    if (error_patterns.empty()) {
        throw std::invalid_argument("error_patterns cannot be an empty set.");
    }

    this->n = error_patterns[0].size();
    if (this->n == 0) {
        throw std::invalid_argument("Vectors in error_patterns cannot be empty.");
    }

    // Use a std::set to automatically handle duplicates and sort, similar to Python's `set(tuple(v))`
    std::set<Vector> unique_patterns(error_patterns.begin(), error_patterns.end());

    // Validate that all vectors have the same length and populate sorted_error_patterns
    for (const auto& v : unique_patterns) {
        if (v.size() != this->n) {
            throw std::invalid_argument("All vectors in error_patterns must have the same length.");
        }
        this->sorted_error_patterns.push_back(v);
    }

    // Initialize the pool of available syndromes
    generate_all_syndromes(this->n);

    // Run the main logic
    prepare_basis();
    construct_map();
}

// --- Public Methods ---
const std::map<GreedySyndromeMapper::Vector, GreedySyndromeMapper::Syndrome>& GreedySyndromeMapper::get_syndrome_map() const {
    return this->syndrome_map;
}

std::vector<std::pair<GreedySyndromeMapper::Vector, GreedySyndromeMapper::Syndrome>> GreedySyndromeMapper::get_basis_map_list() const {
    // Corresponds to Python's get_basis_map_list
    std::vector<std::pair<Vector, Syndrome>> output;
    // The std::map `basis_vectors` is already sorted by key (the dimension)
    for (const auto& pair : this->basis_vectors) {
        const Vector& basis_v = pair.second;
        auto it = this->syndrome_map.find(basis_v);
        if (it != this->syndrome_map.end()) {
            output.push_back({basis_v, it->second});
        }
    }
    return output;
}

// --- Private Methods ---

void GreedySyndromeMapper::generate_all_syndromes(int k) {
    // Corresponds to Python's `itertools.product([0, 1], repeat=n)`
    // This generates all binary vectors of length k
    for (int i = 0; i < (1 << k); ++i) {
        Vector s(k);
        bool is_zero = true;
        for (int j = 0; j < k; ++j) {
            if ((i >> j) & 1) {
                s[k - 1 - j] = 1;
                is_zero = false;
            } else {
                s[k - 1 - j] = 0;
            }
        }
        if (!is_zero) {
            this->available_syndromes.insert(s);
        }
    }
}

void GreedySyndromeMapper::prepare_basis() {
    // Corresponds to Python's _prepare_basis
    for (const auto& v : this->sorted_error_patterns) {
        // Find the first occurrence of 1 from the left
        auto it = std::find(v.begin(), v.end(), 1);
        if (it != v.end()) {
            // Python's v.index(1) gives distance from beginning.
            int first_one_pos = std::distance(v.begin(), it);
            // The dimension is counted from the right: n-1, n-2, ..., 0
            int highest_dim_index = this->n - 1 - first_one_pos;
            this->highest_dim_groups[highest_dim_index].push_back(v);
        }
    }

    // Select the first vector from each dimension group as the basis vector
    for (auto const& [dim_idx, group] : this->highest_dim_groups) {
        if (!group.empty()) {
            this->basis_vectors[dim_idx] = group[0];
        }
    }
}

void GreedySyndromeMapper::construct_map() {
    // Corresponds to Python's _construct_map
    // `basis_vectors` is a map, so it's already sorted by dimension (key)
    for (auto const& [dim_idx, basis_vector] : this->basis_vectors) {
        bool found_syndrome_for_basis = false;

        // `available_syndromes` is a set, so it's also sorted.
        for (const auto& potential_syndrome : this->available_syndromes) {
            std::map<Vector, Syndrome> syndromes_to_assign;
            bool is_valid_choice = true;

            // 1. Assign syndrome for the basis vector itself
            syndromes_to_assign[basis_vector] = potential_syndrome;

            // 2. Calculate syndromes for other vectors in the same group
            const auto& group = this->highest_dim_groups[dim_idx];
            for (const auto& other_v : group) {
                if (other_v == basis_vector) continue;

                Vector residual_vector = xor_sum(other_v, basis_vector);
                
                // The syndrome for the residual vector must already exist
                auto it = this->syndrome_map.find(residual_vector);
                if (it == this->syndrome_map.end()) {
                    is_valid_choice = false;
                    break; // This choice of potential_syndrome is invalid
                }
                
                Syndrome residual_syndrome = it->second;
                Syndrome derived_syndrome = xor_sum(potential_syndrome, residual_syndrome);
                syndromes_to_assign[other_v] = derived_syndrome;
            }

            if (!is_valid_choice) {
                continue; // Try the next potential_syndrome
            }

            // 3. Check for conflicts
            std::set<Syndrome> needed_syndromes;
            bool conflict = false;
            for(const auto& pair : syndromes_to_assign) {
                needed_syndromes.insert(pair.second);
                if (this->available_syndromes.find(pair.second) == this->available_syndromes.end()) {
                    conflict = true;
                    break;
                }
            }

            if (conflict || needed_syndromes.size() != syndromes_to_assign.size()) {
                continue; // Conflict found, try next potential_syndrome
            }

            // 4. Success! Assign and update.
            this->syndrome_map.insert(syndromes_to_assign.begin(), syndromes_to_assign.end());
            for (const auto& s : needed_syndromes) {
                this->available_syndromes.erase(s);
            }
            found_syndrome_for_basis = true;
            break; // Move to the next basis vector
        }

        if (!found_syndrome_for_basis) {
            throw std::runtime_error("Could not find a valid syndrome for a basis vector.");
        }
    }
}

GreedySyndromeMapper::Vector GreedySyndromeMapper::xor_sum(const Vector& vec1, const Vector& vec2) {
    // Assumes vec1 and vec2 have the same size
    Vector result(vec1.size());
    for (size_t i = 0; i < vec1.size(); ++i) {
        result[i] = vec1[i] ^ vec2[i];
    }
    return result;
}

Eigen::MatrixXi GreedySyndromeMapper::get_parity_check_matrix() const {
    // Corresponds to Python's get_parity_check_matrix
    std::vector<Syndrome> syndromes;
    for (const auto& pair : this->basis_vectors) {
        auto it = this->syndrome_map.find(pair.second);
        if (it != this->syndrome_map.end()) {
            syndromes.push_back(it->second);
        }
    }

    // Reverse the order of rows, matching python's `syndromes[::-1]`
    std::reverse(syndromes.begin(), syndromes.end());

    if (syndromes.empty()) {
        return Eigen::MatrixXi(0, 0);
    }

    // Find the minimum index of the first '1' across all rows
    size_t min_idx = syndromes[0].size();
    for (const auto& row : syndromes) {
        auto it = std::find(row.begin(), row.end(), 1);
        if (it != row.end()) {
            size_t idx = std::distance(row.begin(), it);
            if (idx < min_idx) {
                min_idx = idx;
            }
        }
    }

    if (min_idx >= syndromes[0].size()) { // No '1's found
        return Eigen::MatrixXi(0, 0);
    }

    // Create the matrix, performing the slice and transpose in one go.
    // The number of rows in the final matrix is the length of a sliced syndrome.
    // The number of columns is the number of syndromes.
    size_t matrix_rows = syndromes[0].size() - min_idx;
    size_t matrix_cols = syndromes.size();
    Eigen::MatrixXi matrix(matrix_rows, matrix_cols);

    for (size_t j = 0; j < matrix_cols; ++j) { // Iterate through each syndrome (column in final matrix)
        for (size_t i = 0; i < matrix_rows; ++i) { // Iterate through each element of the sliced syndrome (row in final matrix)
            matrix(i, j) = syndromes[j][i + min_idx];
        }
    }

    return matrix;
}
