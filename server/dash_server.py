from dash import Dash, dcc, html
from dash.dependencies import Output, Input, State
import plotly.graph_objs as go
from utils.config import SHARED

def create_dash_app():
    app = Dash(__name__)
    shared = SHARED

    # 초기 PID 값 설정
    shared['pid'] = {'kp': 0.07, 'ki': 0.0, 'kd': 0.0}

    app.layout = html.Div([
        html.H4("실시간 속도 시각화"),
        dcc.Graph(id='live-graph'),
        dcc.Interval(id='interval', interval=500, n_intervals=0),

        html.Div([
            html.Label("타겟 속도 (0~70 km/h)"),
            dcc.Slider(
                id='target-speed-slider',
                min=0,
                max=70,
                step=1,
                value=0,
                marks={i: f"{i} km/h" for i in range(0, 71, 10)}
            )
        ], style={'margin-top': '20px'}),

        html.Div(id='target-speed-display', style={'margin-top': '10px', 'font-weight': 'bold'}),

        html.H4("PID 파라미터 조정 (Kp, Ki, Kd)"),
        html.Div([
            html.Label("Kp:"),
            dcc.Input(id='input-kp', type='number', value=0.0515, step=0.0001),
            html.Label("Ki:"),
            dcc.Input(id='input-ki', type='number', value=0.0, step=0.0001),
            html.Label("Kd:"),
            dcc.Input(id='input-kd', type='number', value=0.0, step=0.0001),
        ], style={'margin-top': '10px', 'margin-bottom': '10px'}),

        html.Div(id='pid-display', style={'font-weight': 'bold'})
    ])

    @app.callback(
        Output('live-graph', 'figure'),
        Input('interval', 'n_intervals')
    )
    def update_graph(n):
        data = shared['speed_data'][-100:]
        return {
            'data': [go.Scatter(y=data, mode='lines+markers')],
            'layout': go.Layout(yaxis=dict(range=[0, 80]))
        }

    @app.callback(
        Output('target-speed-display', 'children'),
        Input('target-speed-slider', 'value')
    )
    def update_target_speed_display(val):
        shared['tank_tar_val_kh'] = val
        return f"현재 타겟 속도: {val} km/h"

    @app.callback(
        Output('pid-display', 'children'),
        Input('input-kp', 'value'),
        Input('input-ki', 'value'),
        Input('input-kd', 'value')
    )
    def update_pid_values(kp, ki, kd):
        shared['pid']['kp'] = kp
        shared['pid']['ki'] = ki
        shared['pid']['kd'] = kd
        return f"PID 값 - Kp: {kp}, Ki: {ki}, Kd: {kd}"

    return app
