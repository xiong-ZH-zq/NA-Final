from functools import reduce    # 简化列表运算
from copy import deepcopy


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

    def func(x: float) -> float:
        """插值基函数
        
        :param x: 插值基函数的自变量取值
        """

        product_number = [x - point for point in points]
        numerator = reduce(lambda x, y: x * y, product_number)

        return numerator / denominator

    return func

def lagrange_polynomial(X:list[float], FX: list[float]) -> callable:
    """根据自变量取值和相应函数值进行 Lagrange 插值. （仅考虑互异节点）
    
    :param X: 列表，自变量取值数组
    :param FX: 列表，自变量取值对应函数值数组
    """

    # 先检查二者是否长度一致，且排除重节点情形
    if len(set(X)) != len(set(FX)) and len(X) != len(set(X)):
        raise Exception("请保证自变量取值和函数值等长，且不出现重节点情形.")
    

    # 若一致，则考虑 Lagrange 插值
    def func(y: float):
        """Lagrange 插值函数
        
        :param y: 自变量取值
        """

        result = 0

        for index, x in enumerate(X):
            l = basis_polynomial(nodes = X,node = x)
            result += FX[index] * l(y)
        
        return result
    
    return func


if __name__ == "__main__":
    # 测试用例 1：输入参数不等长
    # lagrange_polynomial([1],[1,2])

    # 测试用例 2：重节点排除
    # lagrange_polynomial([1,1],[1,2])

    # 测试用例 3: 《数值计算方法》习题 2 T2.1(1)
    X = [-1, 0, 0.5, 1]
    FX = [-3, -0.5, 0, 1]
    f = lagrange_polynomial(X, FX) # 插值函数
    print("插值多项式在插值点的取值：")
    for x in X:
        print(f"f({x}) 的取值为：{f(x)}")

    test = [-0.5, 1.5, 2]   # 对应的正确函数值为 -1.25 3.25 7.5

    for t in test:
        print("插值多项式在任意点的取值：")
        print(f"f({t}) 的取值为：{f(t)}")
    print("-" * 20 + "测试用例 3 结束" + "-" * 20)

    # 测试用例 4: 《数值计算方法》习题 2 T2.1(2)
    X = [-1, 0, 0.5, 1]
    FX = [-1.5, 0, 0, 0.5]
    f = lagrange_polynomial(X, FX) # 插值函数
    print("插值多项式在插值点的取值：")
    for x in X:
        print(f"f({x}) 的取值为：{f(x)}")

    test = [-0.5, 1.5, 2]   # 对应的正确函数值为 -0.25 2.25 6.0

    for t in test:
        print("插值多项式在任意点的取值：")
        print(f"f({t}) 的取值为：{f(t)}")

    print("-" * 20 + "测试用例 4 结束" + "-" * 20)