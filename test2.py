from skfem import *
import numpy as np
from supermeshing import intersect


if 0:
    m1 = MeshTet().refined(1)
    m2 = MeshHex.init_tensor(
        np.linspace(1, 1.5, 3),
        np.linspace(0, 1, 3),
        np.linspace(0, 1, 4),
    )
    e1 = ElementTetP1()
    e2 = ElementHex1()

    p1, t1, facets1 = m1.trace(lambda x: x[0] == 1)
    p1 = p1[1:]  # projection to (y, z)
    #m1t = MeshTri(p1, t1)
    m1t = MeshTri(p1, t1)

    p2, t2, facets2 = m2.trace(lambda x: np.isclose(x[0], 1))
    p2 = p2[1:]  # projection to (y, z)
    #m2t = MeshQuad(p2, t2)
    m2t = MeshQuad(p2, t2)

else:
    m1 = MeshTri().refined(3)
    m2 = MeshQuad.init_tensor(
        np.linspace(1, 1.5, 5),
        np.linspace(0, 1, 6),
    ).refined()
    e1 = ElementTriP1()
    e2 = ElementQuad1()

    ax = m1.draw()
    m2.draw(ax=ax).show()

    p1, t1, facets1 = m1.trace(lambda x: x[0] == 1)
    p1 = p1[1:]  # projection to (y, z)
    #m1t = MeshTri(p1, t1)
    m1t = MeshLine(p1, t1)

    p2, t2, facets2 = m2.trace(lambda x: x[0] == 1)
    p2 = p2[1:]  # projection to (y, z)
    #m2t = MeshQuad(p2, t2)
    m2t = MeshLine(p2, t2)

# intersect
p12, t12, orig1, orig2 = intersect(p1, t1, p2, t2)

#m12 = MeshTri(p12, t12)
m12 = MeshLine(p12, t12)

map1t = MappingAffine(m1t)
map2t = MappingAffine(m2t)
map1 = MappingAffine(m1)
map2 = MappingAffine(m2)
map12 = MappingAffine(m12)


basis1 = Basis(m1, e1)
basis2 = Basis(m2, e2)

fbasis0 = FacetBasis(m1, e1)

fbasis1 = FacetBasis(m1,
                     e1,
                     mapping=map1,
                     quadrature=(map1t.invF(map12.F(fbasis0.quadrature[0]),
                                            tind=orig1),
                                 fbasis0.quadrature[1]),
                     facets=facets1[orig1])


fbasis2 = FacetBasis(m2,
                     e2,
                     mapping=map2,
                     quadrature=(map2t.invF(map12.F(fbasis0.quadrature[0]),
                                            tind=orig2),
                                 fbasis0.quadrature[1]),
                     facets=facets2[orig2])


@BilinearForm
def mass(u, v, w):
    return u * v


from skfem.models import laplace, unit_load

K1 = laplace.assemble(basis1)
K2 = laplace.assemble(basis2)
P1 = mass.assemble(fbasis1)
P2 = mass.assemble(fbasis1, fbasis2)
f1 = unit_load.assemble(basis1)
f2 = unit_load.assemble(basis2)


K, ix = block([[K1, None, P1],
               [None, K2, -P2],
               [P1.T, -P2.T, None]])
f = np.concatenate((f1, f2, 0*f1))

D1 = basis1.get_dofs(lambda x: np.isclose(x[0], 0)).all()
D2 = basis2.get_dofs(lambda x: np.isclose(x[0], 1.5)).all() + ix[0]
D3 = basis1.complement_dofs(basis1.get_dofs(lambda x: np.isclose(x[0],1)).all()) + ix[1]

y = solve(*condense(K, f, D=np.concatenate((D1, D2, D3))))


if m1.dim() > 2:
    m1.save('out1.vtk', point_data={'u': y[:basis1.N]})
    m2.save('out2.vtk', point_data={'u': y[basis1.N:(basis1.N + basis2.N)]})
    ax = m1t.draw(linewidth=2, color='red')
    m2t.draw(ax=ax, linewidth=2, color='blue')
    m12.draw(ax=ax).show()
else:
    y1, y2, _ = np.split(y, ix)
    vmin, vmax = np.min(y), np.max(y)
    ax = m1.plot(y1, vmin=vmin, vmax=vmax)
    m2.plot(y2, vmin=vmin, vmax=vmax, ax=ax).show()

