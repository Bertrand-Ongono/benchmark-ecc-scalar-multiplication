from curve import get_secp256k1
from affine import scalar_mult as scalar_affine
from montgomery import scalar_mult as scalar_montgomery


curve = get_secp256k1()
G = curve.G

k = 123456789

Q_affine, mul_affine, inv_affine = scalar_affine(curve, k, G)
Q_montgomery, mul_montgomery, inv_montgomery = scalar_montgomery(curve, k, G)

print("Q affine      =", Q_affine)
print("Q Montgomery =", Q_montgomery)
print()

print("Résultats identiques ?", Q_affine == Q_montgomery)
print()

print("Affine :")
print("Multiplications =", mul_affine)
print("Inversions      =", inv_affine)
print()

print("Montgomery ladder :")
print("Multiplications =", mul_montgomery)
print("Inversions      =", inv_montgomery)