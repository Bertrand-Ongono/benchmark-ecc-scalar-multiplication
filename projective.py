# projective.py

from field import FieldOps


def is_infinity(P):
    return P is None or P[2] == 0


def from_affine(P):
    if P is None:
        return (0, 1, 0)

    x, y = P
    return (x, y, 1)


def to_affine(curve, F, P):
    if is_infinity(P):
        return None

    X, Y, Z = P

    Z_inv = F.inv(Z)
    x = F.mul(X, Z_inv)
    y = F.mul(Y, Z_inv)

    return (x, y)


def point_double(curve, F, P):
    """
    Version prévue pour a = 0.
    """
    if is_infinity(P):
        return (0, 1, 0)

    X1, Y1, Z1 = P

    if Y1 == 0:
        return (0, 1, 0)

    X1_sq = F.mul(X1, X1)
    W = F.mul(3, X1_sq)

    S = F.mul(Y1, Z1)
    B = F.mul(X1, F.mul(Y1, S))

    W_sq = F.mul(W, W)
    eight_B = F.mul(8, B)
    H = F.sub(W_sq, eight_B)

    X3 = F.mul(2, F.mul(H, S))

    four_B = F.mul(4, B)
    Y1_sq = F.mul(Y1, Y1)
    S_sq = F.mul(S, S)
    term1 = F.mul(W, F.sub(four_B, H))
    term2 = F.mul(8, F.mul(Y1_sq, S_sq))
    Y3 = F.sub(term1, term2)

    S_cu = F.mul(S_sq, S)
    Z3 = F.mul(8, S_cu)

    return (X3, Y3, Z3)


def point_add(curve, F, P, Q):
    """
    Version prévue pour a = 0.
    """
    if is_infinity(P):
        return Q
    if is_infinity(Q):
        return P

    X1, Y1, Z1 = P
    X2, Y2, Z2 = Q

    U = F.sub(F.mul(Y2, Z1), F.mul(Y1, Z2))
    V = F.sub(F.mul(X2, Z1), F.mul(X1, Z2))

    if V == 0:
        if U == 0:
            return point_double(curve, F, P)
        return (0, 1, 0)

    V2 = F.mul(V, V)
    V3 = F.mul(V2, V)
    Z1Z2 = F.mul(Z1, Z2)

    X1Z2 = F.mul(X1, Z2)
    U2 = F.mul(U, U)

    A = F.sub(F.sub(F.mul(U2, Z1Z2), V3), F.mul(2, F.mul(V2, X1Z2)))

    X3 = F.mul(V, A)

    term1 = F.mul(U, F.sub(F.mul(V2, X1Z2), A))
    term2 = F.mul(V3, F.mul(Y1, Z2))
    Y3 = F.sub(term1, term2)

    Z3 = F.mul(V3, Z1Z2)

    return (X3, Y3, Z3)


def scalar_mult(curve, k, P):
    if curve.a != 0:
        raise ValueError("La version projective actuelle supporte seulement les courbes avec a = 0.")

    F = FieldOps(curve.p)

    if k == 0 or P is None:
        return None, F.mul_count, F.inv_count

    if len(P) == 2:
        Q = from_affine(P)
    else:
        Q = P

    R = (0, 1, 0)

    while k > 0:
        if k & 1:
            R = point_add(curve, F, R, Q)
        Q = point_double(curve, F, Q)
        k >>= 1

    R_affine = to_affine(curve, F, R)
    return R_affine, F.mul_count, F.inv_count