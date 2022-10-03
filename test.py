import numpy as np
import matplotlib.pyplot as plt
import testlib
from skfem import *


m1 = MeshTri.init_tensor(np.linspace(0, 1, 3),
                         np.linspace(0, 1, 4))
m2 = MeshTri.init_sqsymmetric().refined(1)

# m1 = MeshQuad.init_tensor(np.linspace(0, 1, 3),
#                           np.linspace(0, 1, 4))
# m2 = MeshQuad().refined(2)

m1 = MeshQuad.init_tensor(np.linspace(0, 1, 3),
                          np.linspace(0, 1, 4))
m2 = MeshTri().refined(2)

m1 = MeshTet().refined(2)
m2 = MeshTet.init_tensor(np.linspace(0, 1, 3),
                         np.linspace(0, 1, 4),
                         np.linspace(0, 1, 5))

p1 = np.asfortranarray(m1.p)
t1 = np.asfortranarray(m1.t + 1)
p2 = np.asfortranarray(m2.p)
t2 = np.asfortranarray(m2.t + 1)

out = np.real(testlib.mainmod(p1, t1, p2, t2))

# split the output

# remove extra zeros
out = out[:, :int(out[0, -1] - 1)]

# triangle vertices
P1 = out[:3, ::3]
P2 = out[:3, 1::3]
P3 = out[:3, 2::3]

# original triangle indices
T1 = out[2, ::3].astype(np.int64)
T2 = out[3, ::3].astype(np.int64)

p = np.hstack((P1, P2, P3))

m12 = MeshTri(p, np.arange(3 * P1.shape[1]).reshape(3, -3))

print(out)

m1.draw(color='red')
m2.draw(color='blue')
m12.draw(color='black').show()
#ax.plot(out[0], out[1], 'bo')
