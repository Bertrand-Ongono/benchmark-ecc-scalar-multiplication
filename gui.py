# gui.py

import tkinter as tk
from tkinter import messagebox
import time

from curve import EllipticCurve, get_secp256k1
from affine import scalar_mult as scalar_affine
from jacobian import scalar_mult as scalar_jacobian
from projective import scalar_mult as scalar_projective
from montgomery import scalar_mult as scalar_montgomery
from benchmark import run_benchmark


def run_calculation():
    try:
        k = int(entry_k.get())

        method = method_var.get()

        if mode_var.get() == "secp":
            curve = get_secp256k1()
            G = curve.G

        else:
            p = int(entry_p.get())
            a = int(entry_a.get())
            b = int(entry_b.get())
            Gx = int(entry_Gx.get())
            Gy = int(entry_Gy.get())

            curve = EllipticCurve(p, a, b, (Gx, Gy))

            if not curve.is_non_singular():
                messagebox.showerror("Erreur", "Courbe singulière")
                return

            if not curve.is_on_curve((Gx, Gy)):
                messagebox.showerror("Erreur", "Le point G n'est pas sur la courbe")
                return

            G = (Gx, Gy)

        start = time.perf_counter()

        if method == "affine":
            Q, mul, inv = scalar_affine(curve, k, G)

        elif method == "jacobi":
            if curve.a != 0:
                messagebox.showerror(
                    "Erreur",
                    "La méthode Jacobi actuelle supporte seulement les courbes avec a = 0."
                )
                return
            Q, mul, inv = scalar_jacobian(curve, k, G)

        elif method == "projective":
            if curve.a != 0:
                messagebox.showerror(
                    "Erreur",
                    "La méthode Projective actuelle supporte seulement les courbes avec a = 0."
                )
                return
            Q, mul, inv = scalar_projective(curve, k, G)

        elif method == "montgomery":
            Q, mul, inv = scalar_montgomery(curve, k, G)

        else:
            messagebox.showerror("Erreur", "Méthode invalide")
            return

        end = time.perf_counter()

        result_text.set(
            f"Résultat Q = {Q}\n"
            f"Multiplications = {mul}\n"
            f"Inversions = {inv}\n"
            f"Temps = {end - start:.6f} s"
        )

    except Exception as e:
        messagebox.showerror("Erreur", str(e))


def run_benchmark_gui():
    run_benchmark()


def toggle_mode():
    if mode_var.get() == "secp":
        for widget in custom_fields:
            widget.config(state="disabled")
    else:
        for widget in custom_fields:
            widget.config(state="normal")


# --- Fenêtre principale ---
root = tk.Tk()
root.title("ECC Benchmark GUI")

# Mode
mode_var = tk.StringVar(value="secp")

tk.Label(root, text="Mode").grid(row=0, column=0)

tk.Radiobutton(
    root,
    text="secp256k1",
    variable=mode_var,
    value="secp",
    command=toggle_mode
).grid(row=0, column=1)

tk.Radiobutton(
    root,
    text="Courbe personnalisée",
    variable=mode_var,
    value="custom",
    command=toggle_mode
).grid(row=0, column=2)

# Champs courbe personnalisée
tk.Label(root, text="p").grid(row=1, column=0)
entry_p = tk.Entry(root)
entry_p.grid(row=1, column=1)

tk.Label(root, text="a").grid(row=2, column=0)
entry_a = tk.Entry(root)
entry_a.grid(row=2, column=1)

tk.Label(root, text="b").grid(row=3, column=0)
entry_b = tk.Entry(root)
entry_b.grid(row=3, column=1)

tk.Label(root, text="Gx").grid(row=4, column=0)
entry_Gx = tk.Entry(root)
entry_Gx.grid(row=4, column=1)

tk.Label(root, text="Gy").grid(row=5, column=0)
entry_Gy = tk.Entry(root)
entry_Gy.grid(row=5, column=1)

custom_fields = [entry_p, entry_a, entry_b, entry_Gx, entry_Gy]

# Scalaire
tk.Label(root, text="k").grid(row=6, column=0)
entry_k = tk.Entry(root)
entry_k.grid(row=6, column=1)

# Méthode
method_var = tk.StringVar(value="affine")

tk.Label(root, text="Méthode").grid(row=7, column=0)

tk.Radiobutton(
    root,
    text="Affine",
    variable=method_var,
    value="affine"
).grid(row=7, column=1)

tk.Radiobutton(
    root,
    text="Jacobi",
    variable=method_var,
    value="jacobi"
).grid(row=7, column=2)

tk.Radiobutton(
    root,
    text="Projectif",
    variable=method_var,
    value="projective"
).grid(row=7, column=3)

tk.Radiobutton(
    root,
    text="Montgomery",
    variable=method_var,
    value="montgomery"
).grid(row=7, column=4)

# Boutons
tk.Button(
    root,
    text="Calculer",
    command=run_calculation
).grid(row=8, column=0, columnspan=2)

tk.Button(
    root,
    text="Benchmark",
    command=run_benchmark_gui
).grid(row=8, column=2, columnspan=3)

# Résultat
result_text = tk.StringVar()
tk.Label(
    root,
    textvariable=result_text,
    justify="left"
).grid(row=9, column=0, columnspan=5)

# Initialisation
toggle_mode()

# Lancer
root.mainloop()