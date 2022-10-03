import numpy as np
import matplotlib.pyplot as plt
import testlib
from skfem import *


m1 = MeshTri.init_tensor(np.linspace(0, 1, 3),
                         np.linspace(0, 1, 4))
m2 = MeshTri.init_sqsymmetric().refined(1)

p1 = np.asfortranarray(m1.p)
t1 = np.asfortranarray(m1.t + 1)
p2 = np.asfortranarray(m2.p)
t2 = np.asfortranarray(m2.t + 1)

out = np.real(testlib.mainmod(p1, t1, p2, t2))

out = out[:, :int(out[1, -1] - 1)]

P1 = out[:, ::3]
P2 = out[:, 1::3]
P3 = out[:, 2::3]

p = np.hstack((P1, P2, P3))

m12 = MeshTri(p, np.arange(3 * P1.shape[1]).reshape(3, -3))

print(out)

m1.draw(color='red')
m2.draw(color='blue')
m12.draw(color='black').show()
#ax.plot(out[0], out[1], 'bo')
