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

# m1 = MeshTet()
# m2 = MeshTet.init_tensor(np.linspace(0, 1, 2),
#                          np.linspace(0, 1, 2),
#                          np.linspace(0, 1, 3))

m12 = MeshTri(*intersect(*m1, *m2))

if m1.dim() == 2:
    axs = plt.subplots(1, 3)
else:
    axs = plt.subplots(1, 3, subplot_kw=dict(projection='3d'))
m1.draw(ax=axs[1][0], color='red')
m2.draw(ax=axs[1][1], color='blue')
m12.draw(ax=axs[1][2], color='black').show()
