import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objs as go
import numpy as np
import sympy as sp
from algo.lagrange_concrete import lagrange_polynomial_concrete as lpc

# 初始化应用
app = dash.Dash(
    __name__,
    external_stylesheets=[
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css",
        "https://cdn.jsdelivr.net/npm/katex@0.16.0/dist/katex.min.css"
    ],
    external_scripts=[
        "https://cdn.jsdelivr.net/npm/katex@0.16.0/dist/katex.min.js",
        "https://cdn.jsdelivr.net/npm/katex@0.16.0/dist/contrib/auto-render.min.js"
    ]
)
# 初始布局
app.layout = html.Div([
    dcc.Markdown(r"$\text{Lagrange}$ 插值的 Python 实现", mathjax = True,style={'fontSize': '35px','text-align': 'center'}),
    html.Div(
        className="container mt-4",
        children=[
            html.Div(
                className="row",
                children=[
                    # 左侧输入栏
                    html.Div(
                        className="col-6",
                        children=[
                            dcc.Markdown("输入点 (格式: $x_1$ $x_2$ $\cdots$):",mathjax = True ,className="form-label"),
                            dcc.Input(id='x-values', type='text', placeholder="例如: 1 2 3", className="form-control"),
                            dcc.Markdown("输入函数值 (格式: $y_1$ $y_2$ $\cdots$):", mathjax=True , className="form-label mt-3"),
                            dcc.Input(id='y-values', type='text', placeholder="例如: 2 4 6", className="form-control"),
                            html.Button("更新图像", id='update-button', n_clicks=0, className="btn btn-primary mt-3"),
                            html.Div(id='polynomial-display', className="mt-4", style={'fontSize': '20px'})
                        ]
                    ),
                    # 右侧图像栏
                    html.Div(
                        className="col-6",
                        children=[
                            dcc.Graph(id='line-plot'),
                        ]
                    )
                ]
            )
        ]
    )
])



@app.callback(
    [Output('line-plot', 'figure'),
     Output('polynomial-display', 'children')],
    [Input('update-button', 'n_clicks')],
    [State('x-values', 'value'), State('y-values', 'value')]
)
def update_graph(n_clicks, x_values, y_values):
    if not x_values or not y_values:
        return {}, "请提供有效输入"

    try:
        # 转换输入数据
        x_values = list(map(float, x_values.split(' ')))
        y_values = list(map(float, y_values.split(' ')))
        if len(x_values) != len(y_values):
            return {}, "x 和 y 的数量必须相同"

        # 计算 Lagrange 插值
        x = sp.Symbol('x')
        lagrange_poly = lpc(X=x_values, FX=y_values)

        poly_latex = sp.latex(lagrange_poly)

        # 绘制折线图
        x_interp = np.linspace(min(x_values), max(x_values), 500).tolist()  # 转换为 Python 列表
        y_interp = [float(lagrange_poly.evalf(subs={x: xi})) for xi in x_interp]  # 转换为标准 Python 数字类型

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_values, y=y_values, mode='markers+lines', name='输入点'))
        fig.add_trace(go.Scatter(x=x_interp, y=y_interp, mode='lines', name='插值曲线'))
        fig.update_layout(title="Lagrange 插值", xaxis_title="x", yaxis_title="y")

        # 返回字典格式的图像和 LaTeX 公式
        return fig.to_dict(), dcc.Markdown(f"插值多项式:\n$$\n{poly_latex}\n$$\n",mathjax=True )

    except Exception as e:
        return {}, f"发生错误: {str(e)}"

# 运行应用
if __name__ == '__main__':
    app.run_server(debug=True)
