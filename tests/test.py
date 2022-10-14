import numpy as np
import matplotlib.pyplot as plt
from supermeshing import intersect
from skfem import *


m1 = MeshTri.init_tensor(np.linspace(0, 1, 3),
                         np.linspace(0, 1, 4))
m2 = MeshTri.init_sqsymmetric().refined(1)

# m1 = MeshQuad.init_tensor(np.linspace(0, 1, 3),
#                           np.linspace(0, 1, 4))
# m2 = MeshQuad().refined(2)

# m1 = MeshQuad.init_tensor(np.linspace(0, 1, 3),
#                           np.linspace(0, 1, 4))
# m2 = MeshTri().refined(2)

m1 = MeshTet()
m2 = MeshTet.init_tensor(np.linspace(0, 1, 2),
                         np.linspace(0, 1, 2),
                         np.linspace(0, 1, 3))

# m1 = MeshTri.init_tensor(np.linspace(0, 1, 40),
#                          np.linspace(0, 1, 38))
# m2 = MeshTri.init_sqsymmetric().refined(3)

p, t, t1, t2 = intersect(*m1, *m2)
m12 = MeshTri(p, t)

e1 = ElementTriP1()

map12 = MappingAffine(m12)
map1 = MappingAffine(m1)
map2 = MappingAffine(m2)

basis0 = Basis(m1, e1)
basis1 = Basis(m1,
               e1,
               mapping=map1,
               quadrature=(map1.invF(map12.F(basis0.quadrature[0]),
                                     tind=t1), basis0.quadrature[1]),
               elements=t1)

basis2 = Basis(m2,
               e1,
               mapping=map2,
               quadrature=(map2.invF(map12.F(basis0.quadrature[0]),
                                     tind=t2), basis0.quadrature[1]),
               elements=t2)
basis3 = Basis(m2, e1)

y1 = basis0.project(lambda x: np.sin(x[0]*5))

@BilinearForm
def mass(u, v, w):
    return u * v

P = mass.assemble(basis1, basis2)
M = mass.assemble(basis2)

y2 = solve(M, P.dot(y1))

basis0.plot(y1)
basis3.plot(y2).show()

#basis2 = Basis(m2, ElementTriP1(), mapping=map2)


if m1.dim() == 2:
    axs = plt.subplots(1, 3)
else:
    axs = plt.subplots(1, 3, subplot_kw=dict(projection='3d'))
m1.draw(ax=axs[1][0], color='red')
m2.draw(ax=axs[1][1], color='blue')
m12.draw(ax=axs[1][2], color='black').show()
