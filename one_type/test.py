from keras import backend as K

# arrayを使うので, numpyもimportします.
import numpy as np


A = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])

B = np.array([
    [9, 8, 7],
    [6, 5, 4],
    [3, 2, 1]
])


A = K.variable(A)
B = K.variable(B)

print(A)

K.get_value(A)
