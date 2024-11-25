"""
:name: Gauss.py
:description: Use Gauss elimination to solve a system of linear equations
"""

class Vector():
    def __init__(self, values: list[float]):
        self.values = values
    
    def __add__(self, other):
        return Vector([self.values[i] + other.values[i] for i in range(len(self.values))])
    
    def __sub__(self, other):
        return Vector([self.values[i] - other.values[i] for i in range(len(self.values))])
    
    def __mul__(self, factor):
        """乘法重载，包括数乘和内积"""
        if type(factor) == Vector:
            return sum([self.values[i] * factor.values[i] for i in range(len(self.values))])
        elif type(factor) == float or type(factor) == int:
            return Vector([self.values[i] * factor for i in range(len(self.values))])
    
    def norm(self) -> float:
        """向量的模（范数）"""
        return sum([value ** 2 for value in self.values]) ** 0.5


class Matrix():
    def __init__(self, values: list[Vector]):
        self.values = values
    
    def echelon_form(self):
        """矩阵阶梯化"""
        for i in range(len(self.values)):
            for j in range(i+1, len(self.values)):
                factor = self.values[j].values[i] / self.values[i].values[i]
                self.values[j] = self.values[j] - self.values[i] * factor
        return self
    
    def rank(self):
        """矩阵的秩"""
        return len([row for row in self.echelon_form().values if row.norm() != 0])

if __name__ == "__main__":
    matrix = Matrix([Vector([2, 1, -1]), Vector([-3, -1, 2]), Vector([-2, 1, 3])])
    matrix = matrix.echelon_form()
    for row in matrix.values:
        print(row.values)
    
    print(matrix.rank())