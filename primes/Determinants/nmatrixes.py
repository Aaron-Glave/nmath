import numpy as np
matrix = np.array([(1,2),(3,5)])
vector = np.array([5,6])
print("Matrix:", matrix, sep='\n')
print("Times vector:", vector.reshape(-1, 1), sep='\n')
print("Result:", matrix*vector, sep='\n')
print("Determinant of matrix:", np.linalg.det(matrix))