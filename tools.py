import copy, os

def vectors_bin(n): 
    vectors = []
    for i in range(2**n):
        vector = [int(x) for x in bin(i)[2:].zfill(n)]
        vectors.append(vector)
    return vectors

def index_v(v):
    return [len(v)-1-i for i in range(len(v)) if v[i] == 1]

'''
dir_path_1 = os.path.dirname(os.path.realpath(__file__))
path_1 = dir_path_1 + '/parity_print.txt'
f = open(path_1,'w') 
'''

def gltc_bin(T):
    """
    Constructs a syndrome map for a given set of error patterns T using a greedy algorithm.
    This corresponds to the "Greedy construction" (Section 3.3) in the thesis.
    The function aims to find an injective mapping (a syndrome) for each basis vector
    that satisfies the partial homomorphism property.
    """
    n = len(T[0]) 

    highest_dim = {} 
    for v in T:
        i = n - 1 - v.index(1)
        if i not in highest_dim:
            highest_dim[i] = [v]
        else:
            highest_dim[i].append(v)

    # Initialize the structure to hold the mapping from basis vectors to their syndromes.
    # map_basis[i] will store [basis_vector, syndrome_vector].
    # The first vector in highest_dim[i] is chosen to represent that dimension's basis.
    map_basis = [[highest_dim[i][0],highest_dim[i][0]] for i in range(n)] 
    binary_vectors = vectors_bin(n) 
    del binary_vectors[0]
    del binary_vectors[0]

    # This is the pool of available syndromes. We will pick from this list.
    syn_compliment_temp_0 = copy.deepcopy(binary_vectors)

    # Iterate through each dimension to assign a syndrome to its basis vector.
    # This is the inductive step of the greedy algorithm.
    for i in range(1, n): 
        try_and_error = [] 
        repeat = True 
        # This loop performs the "greedy" choice. It tries syndromes one by one
        # until it finds one that doesn't violate the homomorphism property for T.
        while repeat:
            repeat = False
            syn_compliment_temp = [x for x in syn_compliment_temp_0 if x not in try_and_error] 
            # Greedily pick the smallest available vector as the syndrome for the current basis vector.
            # This corresponds to the "min(W)" step in the thesis.
            map_basis[i][1] = syn_compliment_temp[0] 
            temp = syn_compliment_temp[0] 
            del syn_compliment_temp[0] 
            # Check for conflicts. If other vectors in T share the same highest dimension,
            # their syndromes are determined by this new assignment. We must check if this causes
            # a syndrome collision (violating injectivity).
            if len(highest_dim[i]) > 1: 
                for j in range(1, len(highest_dim[i])): 
                    # Calculate the syndrome of the non-basis vector based on the homomorphism property:
                    # s(t) = s(sum(b_i)) = sum(s(b_i)), where b_i are basis vectors.
                    sum = [0] * n
                    subscript = index_v(highest_dim[i][j]) 
                    for k in range(len(subscript)): 
                        sum = [(sum[l] + map_basis[subscript[k]][1][l])%2 for l in range(n)] 
                    # If the calculated syndrome is not available (i.e., already taken), our greedy choice was wrong.
                    if sum in syn_compliment_temp: 
                        syn_compliment_temp.remove(sum) 
                    else:              
                        # The chosen syndrome `temp` is invalid. Add it to the list of failed attempts. 
                        try_and_error.append(temp)                   
                        print('wrong syndrome',map_basis[i][0],'-->',temp)
                        repeat = True 
                        # Trigger a retry with the next available syndrome.
                        break   
        # Update the pool of available syndromes for the next iteration.         
        syn_compliment_temp = try_and_error + syn_compliment_temp 
        syn_compliment_temp_0 = copy.deepcopy(syn_compliment_temp) 
    return map_basis                    
