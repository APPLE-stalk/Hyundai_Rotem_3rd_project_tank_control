from dash import Dash, dcc, html
from dash.dependencies import Output, Input
import plotly.graph_objs as go
from utils.config import SHARED




def create_dash_app():
    # dash 앱
    app = Dash(__name__)
    shared = SHARED
    
    # Dash 레이아웃 구성: 실시간 그래프와 타겟 속도 슬라이더 추가
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

        # 슬라이더로 지정한 타겟 속도를 표시할 영역
        html.Div(id='target-speed-display', style={'margin-top': '10px', 'font-weight': 'bold'})
    ])
    
    @app.callback(
    Output('live-graph', 'figure'),
    Input('interval', 'n_intervals')
        )
    # 그래프 업데이트 콜백 함수
    def update_graph(n):
        # speed_data의 복사본 생성
        data = shared['speed_data'][-100:]
        return {
            'data': [go.Scatter(y=data, mode='lines')],
            'layout': go.Layout(yaxis=dict(range=[0, 80]))
        }
    @app.callback(
        Output('target-speed-display', 'children'),
        Input('target-speed-slider', 'value')
        )
    def update_target_speed_display(val):
        shared['tank_tar_val_kh'] = val
        return f"현재 타겟 속도: {val} km/h"

    return app