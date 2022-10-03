import numpy as np
import testlib

a = np.array([[1,2,3],[1,2,3]], order='F')
print(testlib.mainmod(a))
