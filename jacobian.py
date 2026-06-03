# jacobian.py

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
    Z_inv2 = F.mul(Z_inv, Z_inv)
    Z_inv3 = F.mul(Z_inv2, Z_inv)

    x = F.mul(X, Z_inv2)
    y = F.mul(Y, Z_inv3)

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

    Y1_sq = F.mul(Y1, Y1)
    S = F.mul(4, F.mul(X1, Y1_sq))
    M = F.mul(3, F.mul(X1, X1))
    X3 = F.sub(F.mul(M, M), F.mul(2, S))

    Y1_4 = F.mul(Y1_sq, Y1_sq)
    Y3 = F.sub(F.mul(M, F.sub(S, X3)), F.mul(8, Y1_4))

    Z3 = F.mul(2, F.mul(Y1, Z1))

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

    Z1_sq = F.mul(Z1, Z1)
    Z2_sq = F.mul(Z2, Z2)

    U1 = F.mul(X1, Z2_sq)
    U2 = F.mul(X2, Z1_sq)

    Z1_cu = F.mul(Z1_sq, Z1)
    Z2_cu = F.mul(Z2_sq, Z2)

    S1 = F.mul(Y1, Z2_cu)
    S2 = F.mul(Y2, Z1_cu)

    if U1 == U2:
        if S1 != S2:
            return (0, 1, 0)
        return point_double(curve, F, P)

    H = F.sub(U2, U1)
    R = F.sub(S2, S1)

    H_sq = F.mul(H, H)
    H_cu = F.mul(H_sq, H)
    U1_H_sq = F.mul(U1, H_sq)

    X3 = F.sub(F.sub(F.mul(R, R), H_cu), F.mul(2, U1_H_sq))
    Y3 = F.sub(F.mul(R, F.sub(U1_H_sq, X3)), F.mul(S1, H_cu))
    Z3 = F.mul(H, F.mul(Z1, Z2))

    return (X3, Y3, Z3)


def scalar_mult(curve, k, P):
    if curve.a != 0:
        raise ValueError("La version Jacobi actuelle supporte seulement les courbes avec a = 0.")

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