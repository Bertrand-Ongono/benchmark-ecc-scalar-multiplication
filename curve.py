# curve.py


class EllipticCurve:
    def __init__(self, p, a, b, G=None, name="Courbe personnalisée"):
        self.p = p
        self.a = a
        self.b = b
        self.G = G
        self.name = name

    def is_non_singular(self):
        """
        Vérifie que 4a^3 + 27b^2 != 0 mod p
        """
        left = (4 * pow(self.a, 3, self.p) + 27 * pow(self.b, 2, self.p)) % self.p
        return left != 0

    def is_on_curve(self, P):
        """
        Vérifie qu'un point affine P = (x, y) appartient à la courbe.
        """
        if P is None:
            return True

        x, y = P
        left = (y * y) % self.p
        right = (x * x * x + self.a * x + self.b) % self.p
        return left == right


def get_secp256k1():
    p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
    a = 0
    b = 7
    G = (
        55066263022277343669578718895168534326250603453777594175500187360389116729240,
        32670510020758816978083085130507043184471273380659243275938904335757337460388
    )

    return EllipticCurve(
        p=p,
        a=a,
        b=b,
        G=G,
        name="secp256k1"
    )