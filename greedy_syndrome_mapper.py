import itertools
from collections import defaultdict
import numpy as np

class GreedySyndromeMapper:
    """
    GreedySyndromeMapper constructs a syndrome mapping for a given set of error patterns using a greedy algorithm.
    This class encapsulates the algorithm's state and logic for better efficiency, readability, and maintainability.
    Corresponds to "Greedy construction" (Section 3.3) in the referenced paper.
    """
    def __init__(self, error_patterns: list[tuple[int]] | list[list[int]]) -> None:
        if not error_patterns:
            raise ValueError("error_patterns cannot be an empty set.")
        n = len(error_patterns[0])
        self.n = n  # Store the dimension for later use
        if not all(len(v) == n for v in error_patterns):
            raise ValueError("All vectors in error_patterns must have the same length.")

        self.sorted_error_patterns = [tuple(v) for v in sorted(error_patterns)] # Use sorted error_patterns as dictionary keys
        self._basis_vectors = {}  # Store the basis vector for each dimension
        self._highest_dim_groups = defaultdict(list) # Group error_patterns's vectors by their highest dimension

        # Use set for O(1) lookup and removal, greatly improving efficiency
        all_vectors = (tuple(v) for v in itertools.product([0, 1], repeat=self.n))
        self.available_syndromes = set(all_vectors)
        self.available_syndromes.remove(tuple([0] * self.n)) # Remove zero vector

        self.syndrome_map = {} # Final mapping result: {vector: syndrome}

        self._prepare_basis()
        self._construct_map()

    def _prepare_basis(self):
        """
        Determine basis vectors and group by highest dimension in T.
        """
        for v in self.sorted_error_patterns:
            try:
                # Find the leftmost '1', which is the highest dimension
                highest_dim_index = self.n - 1 - v.index(1) # Counting from right to left
                self._highest_dim_groups[highest_dim_index].append(v)
            except ValueError: # Skip zero vector
                continue

        # Select the first vector from each dimension as the basis
        for i in range(self.n):
            if i in self._highest_dim_groups:
                self._basis_vectors[i] = self._highest_dim_groups[i][0]

    @staticmethod
    def _xor_sum(vectors) -> tuple[int] | None:
        if not vectors:
            return None
        arr = np.array(vectors, dtype=np.uint8)
        return tuple(int(x) for x in np.bitwise_xor.reduce(arr))

    def _construct_map(self):
        """
        Execute the greedy algorithm to construct the syndrome mapping.
        """
        # Process basis vectors in order of their dimensions
        for i in sorted(self._basis_vectors.keys()):
            basis_vector = self._basis_vectors[i]

            # Start with the smallest available syndrome
            # sorted() ensures the greedy choice strategy
            for potential_syndrome in sorted(list(self.available_syndromes)):
                
                # Initialize a dictionary to hold the syndromes to assign
                syndromes_to_assign = {}
                is_valid_choice = True
                
                # 1. Basis vector's syndrome
                syndromes_to_assign[basis_vector] = potential_syndrome

                # 2. Other vectors in the same group (calculated via homomorphic properties)
                other_vectors_in_group = [v for v in self._highest_dim_groups[i] if v != basis_vector]
                
                for other_v in other_vectors_in_group:
                    # s(v) = s(basis) + s(v - basis)
                    # In GF(2) ，v - basis = v + basis (XOR)
                    residual_vector = self._xor_sum([other_v, basis_vector])
                    # self-subordinate is required here.
                    # The syndrome of the residual vector should have been assigned in previous steps

                    if residual_vector not in self.syndrome_map:
                        # This situation should not occur in theory, since we process in dimension order
                        is_valid_choice = False
                        break
                    
                    residual_syndrome = self.syndrome_map[residual_vector]
                    derived_syndrome = self._xor_sum([potential_syndrome, residual_syndrome])
                    
                    syndromes_to_assign[other_v] = derived_syndrome
                
                if not is_valid_choice:
                    continue

                # Check if all syndromes to be assigned are available and non-conflicting
                needed_syndromes = set(syndromes_to_assign.values())
                if len(needed_syndromes) == len(syndromes_to_assign) and needed_syndromes.issubset(self.available_syndromes):
                    # Selection successful! Update the mapping and remove from the available pool
                    self.syndrome_map.update(syndromes_to_assign)
                    self.available_syndromes -= needed_syndromes
                    break # Success, break out of potential_syndrome loop and process next basis
            else:
                # If the for loop ends normally (not broken), it means no suitable syndrome was found
                raise RuntimeError(f"Could not find a valid syndrome for basis vector {basis_vector}.")

    def get_basis_map_list(self) -> list[list[list[int]]]:
        """
        Return the mapping of basis vectors in the original code format.
        """
        output = []
        for i in sorted(self._basis_vectors.keys()):
            basis_v = self._basis_vectors[i]
            syndrome = self.syndrome_map.get(basis_v, None) # Use .get to avoid errors
            if syndrome is not None:
                output.append([list(basis_v), list(syndrome)])
        return output

# --- Example ---
if __name__ == '__main__':
    # Generate all nonzero binary vectors of length n=3 as T
    n = 3
    T = [list(v) for v in itertools.product([0, 1], repeat=n) if any(v)]
    try:
        mapper = GreedySyndromeMapper(T)
        print("Full syndrome mapping (vector -> syndrome):")
        for vector, syndrome in sorted(mapper.syndrome_map.items()):
            print(f"  {vector} -> {syndrome}")

        print("\nBasis mapping in original format:")
        basis_map = mapper.get_basis_map_list()
        for basis_v, syndrome_v in basis_map:
            print(f"  {basis_v} -> {syndrome_v}")

    except (ValueError, RuntimeError) as e:
        print(f"Error: {e}")

    # Second example: n=7, T is all unit basis vectors
    n2 = 7
    T2 = [[int(i == j) for i in range(n2)] for j in range(n2)]
    try:
        mapper2 = GreedySyndromeMapper(T2)
        print("\n[Example 2] Syndrome mapping for all basis vectors (n=7):")
        for vector, syndrome in sorted(mapper2.syndrome_map.items()):
            print(f"  {vector} -> {syndrome}")
        print("\n[Example 2] Basis mapping in original format:")
        basis_map2 = mapper2.get_basis_map_list()
        for basis_v, syndrome_v in basis_map2:
            print(f"  {basis_v} -> {syndrome_v}")
    except (ValueError, RuntimeError) as e:
        print(f"[Example 2] Error: {e}")