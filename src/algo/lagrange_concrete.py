from sympy import *
from functools import reduce    # 简化列表运算
from copy import deepcopy

_x = Symbol('x')

def basis_polynomial(nodes: list[float], node: float) -> callable:
    """构造插值基函数（仅考虑互异节点的情形）

    :param nodes: 列表，插值节点数组
    :param node: 浮点数，取值为 1 的节点数
    :return func: 函数，插值基函数

    node 需要在 points 当中.
    """

    # 移除插值节点当中和 l_i 指标相同的 x_i 防止除零错误
    points = list(deepcopy(nodes))
    points.remove(node)

    # 计算分母
    product_number = [node - point for point in points]
    denominator = reduce(lambda x, y: x * y, product_number)

    def func(x):
        """插值基函数
        
        :param x: 插值基函数的自变量取值
        """

        product_number = [x - point for point in points]
        numerator = reduce(lambda x, y: x * y, product_number)

        return numerator / denominator

    return func

def lagrange_polynomial_concrete(X:list[float], FX: list[float]) -> callable:
    """根据自变量取值和相应函数值进行 Lagrange 插值. （仅考虑互异节点）
    与之前的函数有所不同的是，本函数返回的是具体的多项式表达式
    
    :param X: 列表，自变量取值数组
    :param FX: 列表，自变量取值对应函数值数组
    """

    # 先检查二者是否长度一致，且排除重节点情形
    if len(set(X)) != len(set(FX)) and len(X) != len(set(X)):
        raise Exception("请保证自变量取值和函数值等长，且不出现重节点情形.")

    result = 0

    for index, x in enumerate(X):
        l = basis_polynomial(nodes = X,node = x)
        result += FX[index] * l(_x)

    # 返回简化后的多项式  
    return simplify(collect(result,_x,evaluate = True))

if __name__ == "__main__":

    # 测试用例，可输出幂形式的多项式

    X = [-1, 0, 0.5, 1]
    FX = [-3, -0.5, 0, 1]
    f = lagrange_polynomial_concrete(X, FX) # 插值函数
    print(f)