#ifndef GREEDY_SYNDROME_MAPPER_HPP
#define GREEDY_SYNDROME_MAPPER_HPP

#include <vector>
#include <map>
#include <set>
#include <string>
#include <utility> // For std::pair
#include <Eigen/Dense>

class GreedySyndromeMapper {
public:
    // Type aliases for clarity, making the code easier to read.
    using Vector = std::vector<int>;
    using Syndrome = std::vector<int>;

    /**
     * @brief Constructor that takes error patterns and runs the mapping algorithm.
     * @param error_patterns A vector of vectors representing the error patterns.
     */
    GreedySyndromeMapper(const std::vector<Vector>& error_patterns);

    /**
     * @brief Returns the full mapping of error patterns to syndromes.
     */
    const std::map<Vector, Syndrome>& get_syndrome_map() const;

    /**
     * @brief Returns the mapping for only the basis vectors.
     */
    std::vector<std::pair<Vector, Syndrome>> get_basis_map_list() const;

    /**
     * @brief Generates the parity check matrix using basis syndromes.
     * @return An Eigen::MatrixXi representing the parity check matrix.
     */
    Eigen::MatrixXi get_parity_check_matrix() const;

private:
    int n; // Dimension of the vectors
    std::vector<Vector> sorted_error_patterns;
    std::map<int, Vector> basis_vectors; // Map from dimension index to basis vector
    std::map<int, std::vector<Vector>> highest_dim_groups; // Groups vectors by their highest dimension
    std::set<Syndrome> available_syndromes;
    std::map<Vector, Syndrome> syndrome_map;

    /**
     * @brief Identifies basis vectors and groups patterns by highest dimension.
     *        Corresponds to Python's _prepare_basis.
     */
    void prepare_basis();

    /**
     * @brief The core greedy algorithm to build the syndrome map.
     *        Corresponds to Python's _construct_map.
     */
    void construct_map();

    /**
     * @brief Generates all non-zero binary vectors of length k.
     *        Used to initialize the pool of available syndromes.
     */
    void generate_all_syndromes(int k);

    /**
     * @brief Calculates the bitwise XOR sum of a list of vectors.
     *        Corresponds to Python's _xor_sum.
     */
    static Vector xor_sum(const Vector& vec1, const Vector& vec2);
};

#endif // GREEDY_SYNDROME_MAPPER_HPP
