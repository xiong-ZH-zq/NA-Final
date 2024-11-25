# 计算出差商表
def differential_quotient(f: dict, points: list[float]) -> list[list[float]]:
    """计算牛顿差商表
    
    :param f: 字典，保存插值节点的映射值.
    :param points: 浮点数组，插值节点.
    :return result: 差商表
    """

    # 结果的差商表
    result = [[]]

    # 零阶差商的取值
    for point in points:
        result[0].append(f[point])

    l = len(points)
    
    # 一般而言，所需的差商最高为 len(points) 阶
    for i in range(1,l):
        # i 为当前计算的差商阶数
        result.append([])
        
        for j in range(l-i):
            # j 为当前计算的差商在差商表中的序号

            # 利用递推公式计算
            result[i].append((result[i-1][j+1] - result[i-1][j]) / (points[i + j] - points[j]))
        
    return result

def newton_interpolation(X:list[float], FX: list[float]) -> callable:
    """Newton 插值法
    
    :param X: 浮点数组，插值节点横坐标
    :param FX: 浮点数组，插值节点横坐标对应函数值
    :return func: 函数，Newton 插值多项式函数
    """
    
    f = dict(zip(X,FX))
    l = len(X)

    differentials = differential_quotient(f=f,points=X)

    def func(x: float):
        # 插值函数，利用秦九韶算法计算多项式值

        result = differentials[0][0]
        term = 1.0

        for i in range(1,l):
            term *= x - X[i-1]
            result += term * differentials[i][0]

        return result
    
    return func

if __name__ == "__main__":

    # 测试用例 1: 《数值计算方法》习题 2 T2.1(1)

    X = [-1, 0, 0.5, 1]
    FX = [-3, -0.5, 0, 1]
    f = newton_interpolation(X, FX) # 插值函数
    print("插值多项式在插值点的取值：")
    for x in X:
        print(f"f({x}) 的取值为：{f(x)}")

    test = [-0.5, 1.5, 2]   # 对应的正确函数值为 -1.25 3.25 7.5

    for t in test:
        print("插值多项式在任意点的取值：")
        print(f"f({t}) 的取值为：{f(t)}")
    print("-" * 20 + "测试用例 3 结束" + "-" * 20)

    # 测试用例 2: 《数值计算方法》习题 2 T2.1(2)

    X = [-1, 0, 0.5, 1]
    FX = [-1.5, 0, 0, 0.5]
    f = newton_interpolation(X, FX) # 插值函数
    print("插值多项式在插值点的取值：")
    for x in X:
        print(f"f({x}) 的取值为：{f(x)}")

    test = [-0.5, 1.5, 2]   # 对应的正确函数值为 -0.25 2.25 6.0

    for t in test:
        print("插值多项式在任意点的取值：")
        print(f"f({t}) 的取值为：{f(t)}")

    print("-" * 20 + "测试用例 4 结束" + "-" * 20)