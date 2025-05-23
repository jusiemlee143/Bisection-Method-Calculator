import re
import math

def convert_equation(user_input):
    """
    Converts a user-inputted equation string into a valid Python expression.

    Replaces '^' with '**', and converts 'sqrt' and '√' to 'math.sqrt'.
    Also converts 'sin', 'cos', 'tan', 'exp', 'log', and 'sqrt' to their
    corresponding Python math functions.

    Parameters
    ----------
    user_input : str
        The user-inputted equation string

    Returns
    -------
    str
        The converted equation string
    """
    # Replace ^ with **
    converted = user_input.replace("^", "**")

    # Replace 'sqrt' and '√' with 'math.sqrt'
    converted = re.sub(r"sqrt\(([^)]+)\)", r"math.sqrt(\1)", converted)
    converted = re.sub(r"√\(([^)]+)\)", r"math.sqrt(\1)", converted)

    # Replace 'sin', 'cos', 'tan', 'exp', 'log' with 'math.sin', 'math.cos', etc.
    math_funcs = ['sin', 'cos', 'tan', 'exp', 'log', 'sqrt']
    for func in math_funcs:
        converted = re.sub(rf"\b{func}\b", f"math.{func}", converted)

    return converted
