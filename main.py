# main.py

from curve import EllipticCurve, get_secp256k1
from affine import scalar_mult as scalar_affine
from jacobian import scalar_mult as scalar_jacobian
from projective import scalar_mult as scalar_projective
from montgomery import scalar_mult as scalar_montgomery
from benchmark import run_benchmark


def read_int(prompt):
    while True:
        value = input(prompt).strip()
        try:
            return int(value)
        except ValueError:
            print("Valeur invalide. Entre un entier.")


def read_point():
    print("Entre les coordonnées du point G :")
    x = read_int("Gx = ")
    y = read_int("Gy = ")
    return (x, y)


def print_result(method_name, Q, mul_count, inv_count):
    print()
    print(f"=== RÉSULTAT : {method_name.upper()} ===")
    print("Point résultat Q =", Q)
    print("Multiplications :", mul_count)
    print("Inversions      :", inv_count)
    print()


def run_single_test_secp256k1():
    curve = get_secp256k1()
    k = read_int("Entre le scalaire k = ")

    print()
    print(f"Courbe : {curve.name}")
    print("1. Affine")
    print("2. Jacobi")
    print("3. Projectif")
    print("4. Montgomery ladder")
    choice = input("Choix méthode : ").strip()

    if choice == "1":
        Q, mul_count, inv_count = scalar_affine(curve, k, curve.G)
        print_result("Affine", Q, mul_count, inv_count)

    elif choice == "2":
        Q, mul_count, inv_count = scalar_jacobian(curve, k, curve.G)
        print_result("Jacobi", Q, mul_count, inv_count)

    elif choice == "3":
        Q, mul_count, inv_count = scalar_projective(curve, k, curve.G)
        print_result("Projectif", Q, mul_count, inv_count)

    elif choice == "4":
        Q, mul_count, inv_count = scalar_montgomery(curve, k, curve.G)
        print_result("Montgomery ladder", Q, mul_count, inv_count)

    else:
        print("Choix invalide.")


def run_custom_curve_affine():
    print()
    print("=== COURBE PERSONNALISÉE ===")
    p = read_int("p = ")
    a = read_int("a = ")
    b = read_int("b = ")
    G = read_point()
    k = read_int("k = ")

    curve = EllipticCurve(p=p, a=a, b=b, G=G, name="Courbe personnalisée")

    print()
    print("Vérification de la courbe...")

    if not curve.is_non_singular():
        print("Erreur : la courbe est singulière.")
        return

    if not curve.is_on_curve(G):
        print("Erreur : le point G n'appartient pas à la courbe.")
        return

    print()
    print("Méthode disponible pour courbe personnalisée :")
    print("1. Affine")
    print("2. Montgomery ladder")
    choice = input("Choix méthode : ").strip()

    if choice == "1":
        Q, mul_count, inv_count = scalar_affine(curve, k, G)
        print_result("Affine (courbe personnalisée)", Q, mul_count, inv_count)

    elif choice == "2":
        Q, mul_count, inv_count = scalar_montgomery(curve, k, G)
        print_result("Montgomery ladder (courbe personnalisée)", Q, mul_count, inv_count)

    else:
        print("Choix invalide.")

    print("Note :")
    print("- Les versions Jacobi et Projectif de ce projet sont actuellement prévues pour a = 0.")
    print("- La Montgomery ladder ajoutée ici utilise aussi les coordonnées affines.")


def show_menu():
    print("=== PROJET ECC - MENU ===")
    print("1. Test simple sur secp256k1")
    print("2. Benchmark complet sur secp256k1")
    print("3. Tester une courbe personnalisée")
    print("4. Quitter")


def main():
    while True:
        show_menu()
        choice = input("Ton choix : ").strip()

        if choice == "1":
            run_single_test_secp256k1()

        elif choice == "2":
            print()
            run_benchmark()
            print()

        elif choice == "3":
            run_custom_curve_affine()

        elif choice == "4":
            print("Au revoir.")
            break

        else:
            print("Choix invalide.")
            print()


if __name__ == "__main__":
    main()