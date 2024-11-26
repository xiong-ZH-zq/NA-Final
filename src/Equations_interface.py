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
    dcc.Markdown(r"线性方程组求解 （$\text{Gauss}$ 消元法）", mathjax = True,style={'fontSize': '35px','text-align': 'center'}),
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
                            dcc.Markdown("""输入增广矩阵以计算，空格分隔，回车换行，若输入方阵则视为齐次线性方程组.""",mathjax=True, style={"font-side":"30px"}),
                            dcc.Textarea(
                                placeholder="""输入矩阵，示例：\n1 2\n3 4""",
                                value='',
                                style={'width': '100%', 'height': 200},
                                id='matrix-input'
                            ),
                            html.Button("求解上述方程", id='update-button', n_clicks=0, className="btn btn-primary mt-3")
                        ]
                    ),
                    # 右侧图像栏
                    html.Div(
                        className="col-6",
                        children=[
                            html.Div(id='matrix-display', className="mt-4", style={'fontSize': '20px'}),
                        ]
                    ),

                    html.Div(id='solution-display', className="mt-4", style={'fontSize': '20px'})
                ]
            )
        ]
    )
])

def list_to_latex_matrix(lst):
    matrix_str = "\\begin{pmatrix}\n"
    for row in lst:
        matrix_str += " & ".join(map(str, row)) + " \\\\\n"
    matrix_str += "\\end{pmatrix}"
    return matrix_str

@app.callback(
    Output('matrix-display', 'children'),
    Input('matrix-input', 'value')
)

def update_display(matrix:str):
    try:
        matrix = list_to_latex_matrix([[float(j) for j in i.split()] for i in matrix.split('\n')])
        return dcc.Markdown(f"输入矩阵为：\n\n$${matrix}$$",mathjax=True)
    except:
        return "请提供有效输入"

@app.callback(
    Output('solution-display', 'children'),
    [Input('update-button', 'n_clicks'),
    State('matrix-input', 'value')]
)
def update_solution(n_clicks,matrix:str):
    if n_clicks == 0:
        return "点击按钮求解"
    try:
        matrix = [[float(j) for j in i.split()] for i in matrix.split('\n')]
        A = sp.Matrix(matrix)
        if A.rank() == A.shape[0]:
            return dcc.Markdown(f"方程组有唯一解",mathjax = True)
        elif A.rank() < A.shape[0]:
            return "方程组有无穷解"
        else:
            return "方程组无解"
    except Exception as e:
        return f"请提供有效输入 {e}"



if __name__ == '__main__':
    app.run_server(debug=True)