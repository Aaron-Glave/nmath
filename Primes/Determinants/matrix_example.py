import numpy as np
from typing import List
import manual_determinant

if __name__ == '__main__':
    ma_a = [
    [-1 ,2 , 3,  4],
    [1 ,17 ,4,  2],
    [5 ,7,9,12],
    [4,3,2,1]
    ]

    ma = np.array(ma_a)
    print("What is the determinant of")
    for line in ma_a:
        print(line)
    print("?")
    print("According to numpy it is", np.linalg.det(ma))
    print("According to manual_determinant it is", manual_determinant.get_det(ma_a, 4), end="\n\n")
    print("Calculate that by hand now.",
    "Remember to calculate a determinant you take the a number,", "[let's call it n] in the top row, cross out its row and column", "and calculate the determinant of the smaller remaining matrix.",
    "Going to the left as you look across the top you alternate", "from adding and subtracting n times the smaller determinant.", sep="\n")
