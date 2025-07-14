import os
import subprocess
import sys

import numpy as np
import pytest

# Add the parent directory to the Python path BEFORE importing the module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from greedy_syndrome_mapper import GreedySyndromeMapper

def test_empty_error_patterns():
    with pytest.raises(ValueError):
        GreedySyndromeMapper([])

def test_inconsistent_length_error_patterns():
    T = [[1,0,0], [0,1], [0,0,1]]
    with pytest.raises(ValueError):
        GreedySyndromeMapper(T)

def test_basic_mapping_n3():
    n = 3
    T = [list(v) for v in [
        [1,0,0], [0,1,0], [0,0,1]
    ]]
    mapper = GreedySyndromeMapper(T)
    # Should have three syndromes
    assert len(mapper.syndrome_map) == n
    # Syndromes should be unique
    syndromes = list(mapper.syndrome_map.values())
    assert len(set(syndromes)) == n
    # Basis map format should be correct
    basis_map = mapper.get_basis_map_list()
    assert all(isinstance(b, list) and isinstance(s, list) for b, s in basis_map)

def test_parity_check_matrix_shape_and_type():
    #n = 3
    T = [list(v) for v in [
        [1,0,0], [0,1,0], [0,0,1]
    ]]
    mapper = GreedySyndromeMapper(T)
    matrix = mapper.get_parity_check_matrix()
    assert isinstance(matrix, np.ndarray)
    # The number of rows should be n <-- it's wrong!
    # The number of rows can only know after mapping!!!
    #assert matrix.shape[0] == n <-- it's wrong!

def test_full_nonzero_vectors_n3():
    #n = 3
    T = [list(v) for v in [
        [1,0,0], [0,1,0], [0,0,1], [1,1,0], [1,0,1], [0,1,1], [1,1,1]
    ]]
    mapper = GreedySyndromeMapper(T)
    # Syndrome mapping should have 7 entries
    assert len(mapper.syndrome_map) == 7
    # Check parity matrix shape
    # The number of rows can only know after mapping!!!
    #matrix = mapper.get_parity_check_matrix()
    #assert matrix.shape[1] == 7 <-- it's wrong!

def test_basis_vector_selection():
    n = 4
    T = [
        [1,0,0,0],
        [0,1,0,0],
        [0,0,1,0],
        [0,0,0,1],
        [1,1,0,0]
    ]
    mapper = GreedySyndromeMapper(T)
    # Should have 4 basis vectors
    assert len(mapper._basis_vectors) == n

#def test_runtime_error_on_unsolvable():
    # Construct a theoretically unmappable case
    T = [[1,0,0], [1,0,0], [1,0,0]]
    #with pytest.raises(RuntimeError): #XXXX basis should be contained in T!!! and i've just using set to make error patterns unique
    #    GreedySyndromeMapper(T) #XXXX

def test_edge_case_n1():
    T = [[1]]
    mapper = GreedySyndromeMapper(T)
    assert len(mapper.syndrome_map) == 1
    matrix = mapper.get_parity_check_matrix()
    assert matrix.shape == (1,1)

def test_get_basis_map_list_output():
    T = [[1,0,0], [0,1,0], [0,0,1]]
    mapper = GreedySyndromeMapper(T)
    basis_map = mapper.get_basis_map_list()
    assert isinstance(basis_map, list)
    for item in basis_map:
        assert isinstance(item, list)
        assert len(item) == 2
        assert all(isinstance(x, list) for x in item)

def test_get_parity_check_matrix_empty():
    # This test checks the behavior with a single error pattern.
    T = [[1,0,0]]
    mapper = GreedySyndromeMapper(T)
    matrix = mapper.get_parity_check_matrix()
    assert isinstance(matrix, np.ndarray)
    # For a single syndrome, the matrix shape should be (1,1)
    assert matrix.shape == (1,1)

# Advanced: Test if __main__ examples run correctly (optional)
def test_main_examples():
    script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'greedy_syndrome_mapper.py'))
    result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
    out = result.stdout
    assert "Full syndrome mapping" in out or "[Example 2]" in out
