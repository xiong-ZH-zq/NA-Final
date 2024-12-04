"""
:name: Gauss.py
:description: Use Gauss elimination to solve a system of linear equations
"""

import decimal
import sys

def read_matrix_from_file(filename):
    """
    Read matrix from a text file.
    
    Args:
        filename (str): Path to the input matrix file
    
    Returns:
        list: 2D list representing the matrix
    """
    try:
        with open(filename, 'r') as file:
            matrix = []
            for line in file:
                # Split line and convert to Decimal, handling potential whitespace
                row = [decimal.Decimal(x.strip()) for x in line.split()]
                matrix.append(row)
        return matrix
    except FileNotFoundError:
        print(f"Error: File {filename} not found.")
        sys.exit(1)
    except decimal.InvalidOperation:
        print("Error: Invalid number in matrix file.")
        sys.exit(1)

def gauss_elimination(matrix):

    # Set precision for decimal calculations and rounding method
    decimal.getcontext().prec = 50  # Increased precision
    decimal.getcontext().rounding = decimal.ROUND_HALF_UP  # Symmetric rounding

    n = len(matrix)

    # Forward elimination
    for i in range(n):
        # Find pivot
        max_element = abs(matrix[i][i])
        max_row = i
        for k in range(i + 1, n):
            if abs(matrix[k][i]) > max_element:
                max_element = abs(matrix[k][i])
                max_row = k

        # Swap maximum row with current row
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]

        # Make all rows below this one 0 in current column
        for k in range(i + 1, n):
            c = -matrix[k][i] / matrix[i][i]
            for j in range(i, n + 1):
                if i == j:
                    matrix[k][j] = decimal.Decimal('0')
                else:
                    matrix[k][j] += c * matrix[i][j]

    # Back substitution
    x = [decimal.Decimal('0')] * n
    for i in range(n - 1, -1, -1):
        x[i] = matrix[i][n] / matrix[i][i]
        for k in range(i - 1, -1, -1):
            matrix[k][n] -= matrix[k][i] * x[i]

    # Round solutions to the nearest whole number if very close
    def round_if_close(value, tolerance=decimal.Decimal('1E-10')):
        # Check if the value is very close to its rounded version
        rounded = value.quantize(decimal.Decimal('1'), rounding=decimal.ROUND_HALF_UP)
        return rounded if abs(value - rounded) < tolerance else value

    return [round_if_close(sol) for sol in x]

def main(filename):
    """
    Main function to read matrix and solve the system of linear equations.
    """

    matrix = read_matrix_from_file(filename)
    solutions = gauss_elimination(matrix)

    # 求解方程组并打印结果
    print("Solutions:")
    for i, solution in enumerate(solutions, 1):
        print(f"x{i} = {solution}")

if __name__ == "__main__":
    main('./assets/matrix.txt')
    
