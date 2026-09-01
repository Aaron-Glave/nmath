from typing import List
# Function for finding the determinant of a matrix.
def get_det(mat: List[List[int]], n: int):
  
    # Base case: if the matrix is 1x1
    if n == 1:
        return mat[0][0]
    
    # Base case for 2x2 matrix
    if n == 2:
        return mat[0][0] * mat[1][1] - \
               mat[0][1] * mat[1][0]
    
    # Recursive case for larger matrices
    res = 0
    for col in range(n):
      
        # Create a submatrix by removing the first 
        # row and the current column
        sub = [[0] * (n - 1) for _ in range(n - 1)]
        for i in range(1, n):
            subcol = 0
            for j in range(n):
              
                # Skip the current column
                if j == col:
                    continue
                
                # Fill the submatrix
                sub[i - 1][subcol] = mat[i][j]
                subcol += 1
        
        # Cofactor expansion
        sign = 1 if col % 2 == 0 else -1
        res += sign * mat[0][col] * get_det(sub, n - 1)
    
    return res

if __name__ == '__main__': # Driver program to test the above function
    _mat = [[1, 0, 2, -1],
           [3, 0, 0, 5],
           [2, 1, 4, -3],
           [1, 0, 5, 0]]
    print(get_det(_mat, len(_mat)))
