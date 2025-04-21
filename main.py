import tkinter as tk
from tkinter import ttk, messagebox
from equation_utils import convert_equation
from bisection import build_function, plot_function, bisection_method, export_to_csv, export_to_pdf
import os

def run_solver():
    user_eq = entry_eq.get()
    a_val = entry_a.get()
    b_val = entry_b.get()
    tol_val = entry_tol.get()

    try:
        eq = convert_equation(user_eq)
        f = build_function(eq)
        a, b, tol = float(a_val), float(b_val), float(tol_val)

        data, root = bisection_method(f, a, b, tol)
        plot_function(f, a, b)

        export_to_csv(data)
        export_to_pdf(data)

        messagebox.showinfo("Success", f"Root ≈ {root:.5f}\nGraph and results saved in /results.")
        img = tk.PhotoImage(file="function_plot.png")
        lbl_img.config(image=img)
        lbl_img.image = img

    except Exception as e:
        messagebox.showerror("Error", str(e))

# ===== GUI SETUP =====
root = tk.Tk()
root.title("Bisection Method Solver")
root.geometry("700x500")
root.configure(bg="#F0F4FA")

frame = tk.Frame(root, bg="#F0F4FA", padx=20, pady=20)
frame.pack(pady=20)

tk.Label(frame, text="Enter f(x):", bg="#F0F4FA").grid(row=0, column=0, sticky="e")
entry_eq = ttk.Entry(frame, width=40)
entry_eq.grid(row=0, column=1, pady=5)
entry_eq.insert(0, "x^3 - x - 2")

tk.Label(frame, text="Lower bound (a):", bg="#F0F4FA").grid(row=1, column=0, sticky="e")
entry_a = ttk.Entry(frame)
entry_a.grid(row=1, column=1, pady=5)
entry_a.insert(0, "1")

tk.Label(frame, text="Upper bound (b):", bg="#F0F4FA").grid(row=2, column=0, sticky="e")
entry_b = ttk.Entry(frame)
entry_b.grid(row=2, column=1, pady=5)
entry_b.insert(0, "2")

tk.Label(frame, text="Tolerance:", bg="#F0F4FA").grid(row=3, column=0, sticky="e")
entry_tol = ttk.Entry(frame)
entry_tol.grid(row=3, column=1, pady=5)
entry_tol.insert(0, "0.01")

btn_solve = ttk.Button(frame, text="Solve", command=run_solver)
btn_solve.grid(row=4, column=0, columnspan=2, pady=15)

lbl_img = tk.Label(root, bg="#F0F4FA")
lbl_img.pack()

if not os.path.exists("results"):
    os.makedirs("results")

root.mainloop()