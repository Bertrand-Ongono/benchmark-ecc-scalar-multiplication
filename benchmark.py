# benchmark.py

import random
import time

from curve import get_secp256k1
from affine import scalar_mult as scalar_affine
from jacobian import scalar_mult as scalar_jacobian
from projective import scalar_mult as scalar_projective
from montgomery import scalar_mult as scalar_montgomery


def benchmark_method(name, scalar_func, curve, scalars):
    total_time = 0.0
    total_mul = 0
    total_inv = 0
    results = []

    for k in scalars:
        start = time.perf_counter()
        Q, mul_count, inv_count = scalar_func(curve, k, curve.G)
        end = time.perf_counter()

        total_time += (end - start)
        total_mul += mul_count
        total_inv += inv_count
        results.append(Q)

    avg_time = total_time / len(scalars)
    avg_mul = total_mul / len(scalars)
    avg_inv = total_inv / len(scalars)

    return {
        "name": name,
        "avg_time": avg_time,
        "avg_mul": avg_mul,
        "avg_inv": avg_inv,
        "results": results,
    }


def generate_scalars(count, bits=256, seed=42):
    random.seed(seed)
    scalars = []

    for _ in range(count):
        k = random.getrandbits(bits)
        if k == 0:
            k = 1
        scalars.append(k)

    return scalars


def verify_all_results(reference_results, other_results):
    for i in range(len(reference_results)):
        if reference_results[i] != other_results[i]:
            return False
    return True


def safe_ratio(a, b):
    if b == 0:
        return float("inf")
    return a / b


def print_method_block(data):
    print(f"Méthode : {data['name'].upper()}")
    print(f"Temps moyen           : {data['avg_time']:.6f} s")
    print(f"Multiplications moy.  : {data['avg_mul']:.2f}")
    print(f"Inversions moy.       : {data['avg_inv']:.2f}")
    print()


def print_report(
    affine_data,
    jacobian_data,
    projective_data,
    montgomery_data,
    scalars_count,
    curve_name
):
    print("=== BENCHMARK ECC ===")
    print(f"Courbe testée : {curve_name}")
    print(f"Nombre de scalaires testés : {scalars_count}")
    print("Taille des scalaires : 256 bits")
    print()

    print_method_block(affine_data)
    print_method_block(jacobian_data)
    print_method_block(projective_data)
    print_method_block(montgomery_data)

    same_jac = verify_all_results(affine_data["results"], jacobian_data["results"])
    same_proj = verify_all_results(affine_data["results"], projective_data["results"])
    same_mont = verify_all_results(affine_data["results"], montgomery_data["results"])

    print("Vérification des résultats :")
    print("Résultats identiques affine / jacobi     ?", same_jac)
    print("Résultats identiques affine / projectif  ?", same_proj)
    print("Résultats identiques affine / montgomery ?", same_mont)
    print()

    fastest = min(
        [affine_data, jacobian_data, projective_data, montgomery_data],
        key=lambda x: x["avg_time"]
    )

    print(f"Méthode la plus rapide sur cette machine : {fastest['name']}")
    print()

    ratio_aff_vs_jac = safe_ratio(affine_data["avg_time"], jacobian_data["avg_time"])
    ratio_aff_vs_proj = safe_ratio(affine_data["avg_time"], projective_data["avg_time"])
    ratio_proj_vs_jac = safe_ratio(projective_data["avg_time"], jacobian_data["avg_time"])
    ratio_aff_vs_mont = safe_ratio(affine_data["avg_time"], montgomery_data["avg_time"])
    ratio_mont_vs_jac = safe_ratio(montgomery_data["avg_time"], jacobian_data["avg_time"])

    print("Ratios de temps :")
    print(f"- Affine / Jacobi      : {ratio_aff_vs_jac:.2f}x")
    print(f"- Affine / Projectif   : {ratio_aff_vs_proj:.2f}x")
    print(f"- Projectif / Jacobi   : {ratio_proj_vs_jac:.2f}x")
    print(f"- Affine / Montgomery  : {ratio_aff_vs_mont:.2f}x")
    print(f"- Montgomery / Jacobi  : {ratio_mont_vs_jac:.2f}x")
    print()

    print("Analyse :")
    print("- L'affine utilise moins de multiplications, mais un grand nombre d'inversions.")
    print("- Les coordonnées projectives et de Jacobi évitent presque toutes les inversions intermédiaires.")
    print("- Jacobi demande plus de multiplications que l'affine, mais reste souvent plus rapide.")
    print("- Le projectif standard améliore aussi les performances par rapport à l'affine.")
    print("- La Montgomery ladder effectue une addition et un doublement à chaque bit du scalaire.")
    print("- Dans ce projet, Montgomery est implémentée en coordonnées affines complètes (x, y).")
    print("- Elle est donc plus régulière que double-and-add, mais elle conserve beaucoup d'inversions.")
    print("- Pour les smart cards, Jacobi reste le meilleur choix en performance brute.")
    print("- Une ladder régulière en coordonnées projectives ou jacobiennes serait un meilleur choix sécurité/performance.")


def run_benchmark():
    curve = get_secp256k1()
    scalars_count = 50
    scalars = generate_scalars(count=scalars_count, bits=256, seed=42)

    affine_data = benchmark_method(
        name="Affine",
        scalar_func=scalar_affine,
        curve=curve,
        scalars=scalars
    )

    jacobian_data = benchmark_method(
        name="Jacobi",
        scalar_func=scalar_jacobian,
        curve=curve,
        scalars=scalars
    )

    projective_data = benchmark_method(
        name="Projectif",
        scalar_func=scalar_projective,
        curve=curve,
        scalars=scalars
    )

    montgomery_data = benchmark_method(
        name="Montgomery ladder",
        scalar_func=scalar_montgomery,
        curve=curve,
        scalars=scalars
    )

    print_report(
        affine_data=affine_data,
        jacobian_data=jacobian_data,
        projective_data=projective_data,
        montgomery_data=montgomery_data,
        scalars_count=scalars_count,
        curve_name=curve.name
    )


if __name__ == "__main__":
    run_benchmark()