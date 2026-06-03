# montgomery.py

from field import FieldOps


def is_infinity(P):
    return P is None


def point_add(curve, F, P, Q):
    """
    Addition de deux points en coordonnées affines.

    Cette fonction est volontairement proche de affine.py,
    mais elle est utilisée ici dans la Montgomery ladder.
    """
    if P is None:
        return Q

    if Q is None:
        return P

    x1, y1 = P
    x2, y2 = Q

    # P + (-P) = O
    if x1 == x2 and (y1 + y2) % curve.p == 0:
        return None

    # P + P = 2P
    if P == Q:
        return point_double(curve, F, P)

    num = F.sub(y2, y1)
    den = F.sub(x2, x1)

    lam = F.mul(num, F.inv(den))

    x3 = F.sub(F.sub(F.mul(lam, lam), x1), x2)
    y3 = F.sub(F.mul(lam, F.sub(x1, x3)), y1)

    return (x3, y3)


def point_double(curve, F, P):
    """
    Doublement d'un point en coordonnées affines.

    Formule générale pour une courbe de Weierstrass :
        y^2 = x^3 + ax + b
    """
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
    """
    Montgomery ladder pour calculer Q = kP.

    Contrairement au double-and-add classique, cette méthode effectue
    une addition et un doublement à chaque bit du scalaire.

    R0 = O
    R1 = P

    Pour chaque bit de k :
        si bit = 0 :
            R1 = R0 + R1
            R0 = 2R0
        si bit = 1 :
            R0 = R0 + R1
            R1 = 2R1

    Remarque :
    Ici, on utilise une Montgomery ladder sur points affines.
    Ce n'est pas une implémentation x-only optimisée comme Curve25519,
    car secp256k1 est une courbe de Weierstrass.
    """
    F = FieldOps(curve.p)

    if k == 0 or P is None:
        return None, F.mul_count, F.inv_count

    R0 = None
    R1 = P

    bits = bin(k)[2:]

    for bit in bits:
        if bit == "0":
            R1 = point_add(curve, F, R0, R1)
            R0 = point_double(curve, F, R0)
        else:
            R0 = point_add(curve, F, R0, R1)
            R1 = point_double(curve, F, R1)

    return R0, F.mul_count, F.inv_count