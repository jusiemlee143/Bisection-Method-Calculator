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

        data, root_val = bisection_method(f, a, b, tol)
        plot_function(f, a, b)

        export_to_csv(data)
        export_to_pdf(data)

        messagebox.showinfo("Success", f"Root ≈ {root_val:.5f}\nGraph and results saved in /results.")
        img = tk.PhotoImage(file="function_plot.png")
        lbl_img.config(image=img)
        lbl_img.image = img

    except Exception as e:
        messagebox.showerror("Error", str(e))

# ===== GUI SETUP =====
root = tk.Tk()
root.title("📈 Bisection Method Calculator")
root.geometry("800x600")
root.configure(bg="#E8EDF3")

# ===== Style Setup =====
style = ttk.Style()
style.configure("TLabel", font=("Segoe UI", 11))
style.configure("TButton", font=("Segoe UI", 11), padding=6)
style.configure("TEntry", padding=4)

# ===== Header =====
header = tk.Label(root, text="Bisection Method Solver", font=("Segoe UI", 18, "bold"), bg="#E8EDF3", fg="#2C3E50")
header.pack(pady=20)

# ===== Input Frame =====
frame = ttk.Frame(root, padding=20)
frame.pack(pady=10)

def add_labeled_entry(parent, text, row, default_val=""):
    ttk.Label(parent, text=text).grid(row=row, column=0, sticky="e", pady=5, padx=10)
    entry = ttk.Entry(parent, width=40)
    entry.grid(row=row, column=1, pady=5, padx=10)
    entry.insert(0, default_val)
    return entry

entry_eq = add_labeled_entry(frame, "Enter f(x):", 0, "x^3 - x - 2")
entry_a = add_labeled_entry(frame, "Lower bound (a):", 1, "1")
entry_b = add_labeled_entry(frame, "Upper bound (b):", 2, "2")
entry_tol = add_labeled_entry(frame, "Tolerance:", 3, "0.01")

# ===== Solve Button =====
btn_solve = ttk.Button(frame, text="🔍 Solve", command=run_solver)
btn_solve.grid(row=4, column=0, columnspan=2, pady=15)

# ===== Image Label =====
lbl_img = tk.Label(root, bg="#E8EDF3", bd=2, relief="groove")
lbl_img.pack(pady=10)

# ===== Ensure 'results' folder exists =====
if not os.path.exists("results"):
    os.makedirs("results")

root.mainloop()
