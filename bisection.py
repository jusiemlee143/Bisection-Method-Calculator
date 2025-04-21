import math
import matplotlib.pyplot as plt
import pandas as pd
from fpdf import FPDF

def build_function(eq_str):
    return lambda x: eval(eq_str, {"x": x, "math": math, "__builtins__": None})

def plot_function(f, a, b, filename='function_plot.png'):
    x_vals = [a + i * (b - a) / 1000 for i in range(1001)]
    y_vals = [f(x) for x in x_vals]
    plt.figure(figsize=(6, 4))
    plt.axhline(0, color='gray', linestyle='--')
    plt.plot(x_vals, y_vals)
    plt.title("Function Graph")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.grid(True)
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

        if fc == 0: break
        elif f(a) * fc < 0: b = c
        else: a = c

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