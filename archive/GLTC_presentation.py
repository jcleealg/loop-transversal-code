from tools import gltc_bin
import numpy as np

T_given_0 = [[0,0,0,0,0,1],[0,0,0,0,1,0],[0,0,0,0,1,1],[0,0,0,1,0,0],
[0,0,0,1,1,0],[0,0,1,0,0,0],[0,0,1,0,0,1],[0,1,0,0,0,0],[0,1,0,0,1,0],[1,0,0,0,0,0],[1,0,0,1,0,0]]

T_given_1 = [[0,0,0,0,0,1],[0,0,0,0,1,0],[0,0,0,0,1,1],[0,0,0,1,0,0],
[0,0,0,1,1,0],[0,0,1,0,0,0],[0,0,1,1,0,0],[0,1,0,0,0,0],[0,1,1,0,0,0],[1,0,0,0,0,0],[1,1,0,0,0,0]]

#This is the classical error pattern of (7,4) Hamming code as an example.
#T_given_1 = [[0,0,0,0,0,0,1],[0,0,0,0,0,1,0],[0,0,0,0,1,0,0],[0,0,0,1,0,0,0],[0,0,1,0,0,0,0],[0,1,0,0,0,0,0],[1,0,0,0,0,0,0]]

print('-----------------')
map = gltc_bin(T_given_1)
H = []
for x in map:
    H.append(x[1])
    print(x)
print('-----------------')
H = H[::-1]
first_nonzero = [next((i for i, v in enumerate(row) if v != 0), len(row)) for row in H]
min_idx = min(first_nonzero)
H_trimmed = [row[min_idx:] for row in H]
H_trimmed = np.array(H_trimmed)
H_T = H_trimmed.T.tolist()
print("Parity check matrix constructed from the given error pattern set:")
for row in H_T:
    print(' '.join(str(x) for x in row))
