import os
import math
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image, ImageTk
from fpdf import FPDF
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox

# === UTILS ===
def convert_equation(equation: str) -> str:
    return equation.replace("^", "**").strip()

def build_function(eq_str):
    return lambda x: eval(eq_str, {"x": x, "math": math, "__builtins__": None})

def plot_function(f, a, b, filename='function_plot.png'):
    x_vals = [a + i * (b - a) / 1000 for i in range(1001)]
    y_vals = [f(x) for x in x_vals]

    plt.figure(figsize=(10, 4))
    plt.axhline(0, color='gray', linestyle='--')
    plt.plot(x_vals, y_vals, color='blue')
    plt.title("Function Graph")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

def bisection_method(f, a, b, tol=0.01):
    if f(a) * f(b) >= 0:
        raise ValueError("Interval does not bracket a root.")

    data = []
    while (b - a) / 2 > tol:
        c = (a + b) / 2
        fc = f(c)
        data.append((a, b, c, fc))

        if fc == 0:
            break
        elif f(a) * fc < 0:
            b = c
        else:
            a = c

    return data, c

def export_to_csv(data, path='results/bisection_results.csv'):
    df = pd.DataFrame(data, columns=['a', 'b', 'c', 'f(c)'])
    df.to_csv(path, index=False)

def export_to_pdf(data, path='results/bisection_results.pdf'):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, "Bisection Method Results", ln=True)
    pdf.cell(0, 10, "", ln=True)

    for i, row in enumerate(data, start=1):
        a, b, c, fc = row
        pdf.cell(0, 10, f"Iter {i}: a={a:.5f}, b={b:.5f}, c={c:.5f}, f(c)={fc:.5f}", ln=True)

    pdf.output(path)

# === GUI LOGIC ===
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

        Messagebox.ok(
            f"Root ≈ {root_val:.5f}\nGraph and results saved in /results.",
            title="Success",
            alert=True
        )

        # Load and resize image using Pillow
        img = Image.open("function_plot.png")
        try:
            resample = Image.Resampling.LANCZOS
        except AttributeError:
            resample = Image.ANTIALIAS  # backward compatibility

        img = img.resize((750, 300), resample)
        photo = ImageTk.PhotoImage(img)

        # Clear previous image and display new one
        canvas.delete("all")
        canvas.create_image(0, 0, anchor="nw", image=photo)
        canvas.image = photo

        # Update scroll region to match the image's size
        canvas.config(scrollregion=canvas.bbox("all"))

    except Exception as e:
        Messagebox.show_error(str(e), title="Error")

# === GUI SETUP ===
root = ttk.Window(themename="superhero")
root.title("📈 Bisection Method Calculator")

# Allow window resizing and remove the fixed size
root.geometry("900x700")
root.resizable(True, True)

# Create a main frame to center the content
main_frame = ttk.Frame(root)
main_frame.pack(fill="both", expand=True)

ttk.Label(
    main_frame,
    text="Bisection Method Solver",
    font=("Segoe UI", 20, "bold"),
    bootstyle="primary"
).pack(pady=25)

frame = ttk.Frame(main_frame, padding=20)
frame.pack()

def add_labeled_entry(parent, text, row, default_val=""):
    ttk.Label(parent, text=text).grid(row=row, column=0, sticky="e", pady=8, padx=10)
    entry = ttk.Entry(parent, width=40)
    entry.grid(row=row, column=1, pady=8, padx=10)
    entry.insert(0, default_val)
    return entry

entry_eq = add_labeled_entry(frame, "Enter f(x):", 0, "x^3 - x - 2")
entry_a = add_labeled_entry(frame, "Lower bound (a):", 1, "1")
entry_b = add_labeled_entry(frame, "Upper bound (b):", 2, "2")
entry_tol = add_labeled_entry(frame, "Tolerance:", 3, "0.01")

ttk.Button(
    frame,
    text="🔍 Solve",
    command=run_solver,
    bootstyle="success"
).grid(row=4, column=0, columnspan=2, pady=20)

# Graph display area
frame_img = ttk.Labelframe(main_frame, text="📊 Function Plot", padding=10, bootstyle="info")
frame_img.pack(pady=10, padx=20, fill="x")

# Create canvas for image and add scrollbars
canvas_frame = ttk.Frame(frame_img)
canvas_frame.pack(fill="both", expand=True)

canvas = ttk.Canvas(canvas_frame)
canvas.pack(side="left", fill="both", expand=True)

# Add horizontal and vertical scrollbars to the canvas
h_scroll = ttk.Scrollbar(canvas_frame, orient="horizontal", command=canvas.xview)
h_scroll.pack(side="bottom", fill="x")
v_scroll = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
v_scroll.pack(side="right", fill="y")

canvas.configure(xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)

# Ensure the 'results' folder exists
if not os.path.exists("results"):
    os.makedirs("results")

root.mainloop()
