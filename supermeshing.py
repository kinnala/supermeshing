import numpy as np

import supermeshing_fortran


def intersect(p1, t1, p2, t2):

    p1 = np.asfortranarray(p1)
    t1 = np.asfortranarray(t1 + 1)
    p2 = np.asfortranarray(p2)
    t2 = np.asfortranarray(t2 + 1)

    out = supermeshing_fortran.intersect(p1, t1, p2, t2)

    # split the output

    # remove extra zeros
    dim = p1.shape[0]
    nvert = dim + 1
    k = int(out[0, -1] - 1)
    out = out[:, :k]

    # triangle vertices
    P1 = out[:dim, ::(dim + 1)]
    P2 = out[:dim, 1::(dim + 1)]
    if dim > 1:
        P3 = out[:dim, 2::(dim + 1)]
        if dim > 2:
            P4 = out[:dim, 3::(dim + 1)]

    # original triangle indices
    T1 = out[dim, ::(dim + 1)].astype(np.int64)
    T2 = out[dim + 1, ::(dim + 1)].astype(np.int64)

    if dim == 1:
        p = np.hstack((P1, P2))
    elif dim == 2:
        p = np.hstack((P1, P2, P3))
    elif dim == 3:
        p = np.hstack((P1, P2, P3, P4))

    t = np.arange(nvert * P1.shape[1], dtype=np.int64).reshape((nvert, -1))

    return p, t, T1 - 1, T2 - 1
