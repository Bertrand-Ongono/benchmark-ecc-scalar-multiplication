# affine.py

from field import FieldOps


def point_add(curve, F, P, Q):
    if P is None:
        return Q
    if Q is None:
        return P

    x1, y1 = P
    x2, y2 = Q

    if x1 == x2 and (y1 + y2) % curve.p == 0:
        return None

    if P == Q:
        return point_double(curve, F, P)

    num = F.sub(y2, y1)
    den = F.sub(x2, x1)
    lam = F.mul(num, F.inv(den))

    x3 = F.sub(F.sub(F.mul(lam, lam), x1), x2)
    y3 = F.sub(F.mul(lam, F.sub(x1, x3)), y1)

    return (x3, y3)


def point_double(curve, F, P):
    if P is None:
        return None

    x, y = P

    if y == 0:
        return None

    num = F.add(F.mul(3, F.mul(x, x)), curve.a)
    den = F.mul(2, y)
    lam = F.mul(num, F.inv(den))

    x3 = F.sub(F.mul(lam, lam), F.mul(2, x))
    y3 = F.sub(F.mul(lam, F.sub(x, x3)), y)

    return (x3, y3)


def scalar_mult(curve, k, P):
    F = FieldOps(curve.p)

    R = None
    Q = P

    while k > 0:
        if k & 1:
            R = point_add(curve, F, R, Q)
        Q = point_double(curve, F, Q)
        k >>= 1

    return R, F.mul_count, F.inv_count