import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objs as go
import numpy as np
import sympy as sp

app = dash.Dash(
    __name__,
    external_stylesheets=[
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css"
    ]
)

app.layout = html.Div([
    dcc.Markdown(r"$\text{Runge}$ 现象观察实验", mathjax = True,style={'fontSize': '35px','text-align': 'center'}),
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
                            dcc.Markdown("滑动进行 $n$ 等分 Lagrange 插值以观察 Runge 现象",mathjax=True, style={"font-side":"30px"}),
                            dcc.Slider(2, 20, 2,
                                value=10,
                                id='runge-slider'
                                ),
                            dcc.Markdown(r"示例函数：$$f(x) = \dfrac{1}{1+ 25 x^2}$$", mathjax=True,style={"font-side":"30px"})
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
    Output('line-plot', 'figure'),
    Input('runge-slider', 'value')
)

def update_figure(n):
    x = np.linspace(-1, 1, 1000)

    # 示例函数
    y = 1 / (1 + 25 * x ** 2)
    
    x_points = np.linspace(-1, 1, n)
    y_points = 1 / (1 + 25 * x_points ** 2)
    x_lagrange = np.linspace(-1, 1, 1000)
    y_lagrange = np.zeros(1000)

    for i in range(n):
        L = 1
        for j in range(n):
            if j != i:
                L *= (x_lagrange - x_points[j]) / (x_points[i] - x_points[j])
        y_lagrange += L * y_points[i]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='原函数'))
    fig.add_trace(go.Scatter(x=x_lagrange, y=y_lagrange, mode='lines', name='Lagrange 插值'))

    return fig.to_dict()

# 运行应用
if __name__ == '__main__':
    app.run_server(debug=True)