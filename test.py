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

m1 = MeshTet()
m2 = MeshTet.init_tensor(np.linspace(0, 1, 2),
                         np.linspace(0, 1, 2),
                         np.linspace(0, 1, 3))

p1 = np.asfortranarray(m1.p)
t1 = np.asfortranarray(m1.t + 1)
p2 = np.asfortranarray(m2.p)
t2 = np.asfortranarray(m2.t + 1)

out = np.real(testlib.mainmod(p1, t1, p2, t2))

# split the output

# remove extra zeros
dim = m1.p.shape[0]
nvert = dim + 1
k = int(out[0, -1] - 1)
out = out[:, :k]

# triangle vertices
P1 = out[:dim, ::(dim + 1)]
P2 = out[:dim, 1::(dim + 1)]
P3 = out[:dim, 2::(dim + 1)]
if dim > 2:
    P4 = out[:dim, 3::(dim + 1)]

# original triangle indices
T1 = out[dim, ::(dim + 1)].astype(np.int64)
T2 = out[dim + 1, ::(dim + 1)].astype(np.int64)

p = np.hstack((P1, P2, P3))
if dim > 2:
    p = np.hstack((P1, P2, P3, P4))

if dim == 2:
    m12 = MeshTri(p, np.arange(nvert * P1.shape[1]).reshape((nvert, -1)))
elif dim == 3:
    m12 = MeshTet(p, np.arange(nvert * P1.shape[1]).reshape((nvert, -1)))

print(out)

if dim == 2:
    axs = plt.subplots(1, 3)
elif dim == 3:
    axs = plt.subplots(1, 3, subplot_kw=dict(projection='3d'))
m1.draw(ax=axs[1][0], color='red')
m2.draw(ax=axs[1][1], color='blue')
m12.draw(ax=axs[1][2], color='black').show()
#ax.plot(out[0], out[1], 'bo')
