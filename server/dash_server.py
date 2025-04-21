from dash import Dash, dcc, html
from dash.dependencies import Output, Input, State
import plotly.graph_objs as go
from utils.config import SHARED
import numpy as np



def create_dash_app():
    app = Dash(__name__)
    shared = SHARED

    # 초기 PID 값 설정

    # shared['pid'] = {'kp': 0.5, 'ki': 0.0, 'kd': 0.05, 'dt': 0.2}

    app.layout = html.Div([
        html.H4("실시간 속도 시각화"),
        dcc.Graph(id='live-graph'),
        dcc.Interval(id='interval', interval=500, n_intervals=0),

        html.Div([
            html.Label("타겟 속도 (-30~70 km/h)"),
            dcc.Slider(
                id='target-speed-slider',
                min=-30,
                max=70,
                step=1,
                value=0,
                marks={i: f"{i} km/h" for i in range(-30, 71, 10)}
            )
        ], style={'margin-top': '20px'}),

        html.Div(id='target-speed-display', style={'margin-top': '10px', 'font-weight': 'bold'}),

        html.H4("PID 파라미터 조정 (Kp, Ki, Kd)"),
        html.Div([
            html.Label("Kp:"),
            dcc.Input(id='input-kp', type='number', value=shared['vel_pid']['kp'], step=0.0001),
            html.Label("Ki:"),
            dcc.Input(id='input-ki', type='number', value=shared['vel_pid']['ki'], step=0.0001),
            html.Label("Kd:"),
            dcc.Input(id='input-kd', type='number', value=shared['vel_pid']['kd'], step=0.0001),
        ], style={'margin-top': '10px', 'margin-bottom': '10px'}),
        
        html.Div(id='pid-display', style={'font-weight': 'bold'}),

        html.H4("전차 위치 변화량 (ΔX, ΔZ)", style={'margin-top': '40px'}),
        dcc.Graph(id='delta-pos-graph'),

        # html.Div(id='pid-display', style={'font-weight': 'bold'})
        
        # 경도 추가 25_04_21 steer 관련
        html.H4("현재 각도 (deg)", style={'margin-top': '40px'}),
        dcc.Graph(id='steer-gauge'),
        
        html.H4("타겟 각도 조절 (deg)"),
        dcc.Slider(
            id='target-angle-slider',
            min=-180, max=180, step=1, value=0,
            marks={
                -180: '-180°',
                -90: '-90°',
                0: '0°',
                90: '90°',
                180: '180°'
                # 0: '0°',
                # 90: '90°',
                # 180: '180°',
                # 270: '270°',
                # 360: '360°'
            }
        ),
        html.Div(id='target-angle-display', style={'font-weight': 'bold', 'margin-top': '10px'}),

        html.H4("Yaw PID 파라미터 조정 (Kp, Ki, Kd)", style={'margin-top': '30px'}),
        html.Div([
            html.Label("Kp:"), dcc.Input(id='steer-kp', type='number', value=shared['steer_pid']['kp'], step=0.0001),
            html.Label("Ki:"), dcc.Input(id='steer-ki', type='number', value=shared['steer_pid']['ki'], step=0.0001),
            html.Label("Kd:"), dcc.Input(id='steer-kd', type='number', value=shared['steer_pid']['kd'], step=0.0001),
        ], style={'margin-top': '10px', 'margin-bottom': '10px'}),
        html.Div(id='steer-pid-display', style={'font-weight': 'bold'}),
        
    ])

    @app.callback(
        Output('live-graph', 'figure'),
        Input('interval', 'n_intervals')
    )
    def update_graph(n):
        data = shared['vel_data'][-100:]
        
        return {
            'data': [go.Scatter(y=data, mode='lines+markers')],
            'layout': go.Layout(
                xaxis=dict(
                    range=[max(0, len(data) - 100), len(data)],
                    dtick=10,  # x축 눈금 간격
                    title='시간 (포인트)'
                ),
                yaxis=dict(
                    range=[-40, 80],
                    dtick=10,  # y축 눈금 간격
                    title='속도 (km/h)'
                ),
                title='실시간 속도 시각화'
            )
        }

    # 경도 추가 25_04_19
    # 축에 평행한 상태에서 1km/h에서 전후진 시 request 시간별 변위 시각화, 측정 용도
    @app.callback(
        Output('delta-pos-graph', 'figure'),
        Input('interval', 'n_intervals')
    )
    def update_delta_graph(n):
        del_x_data = shared.get('del_playerPos', {}).get('x', [])[-100:]
        del_z_data = shared.get('del_playerPos', {}).get('z', [])[-100:]
        return {
            'data': [
                go.Scatter(y=del_x_data, mode='lines', name='ΔX', line=dict(dash='dot')),
                go.Scatter(y=del_z_data, mode='lines', name='ΔZ', line=dict(dash='dash'))
            ],
            'layout': go.Layout(
                xaxis=dict(title='시간 (포인트)', dtick=10, range=[max(0, len(del_x_data) - 100), len(del_x_data)]),
                # yaxis=dict(title='좌표 변화량', dtick=1),
                title='전차 위치 변화량 (ΔX, ΔZ)',
                legend=dict(orientation='h')
            )
    }
    
    @app.callback(
        Output('target-speed-display', 'children'),
        Input('target-speed-slider', 'value')
    )
    def update_target_speed_display(val):
        shared['tank_tar_vel_kh'] = val
        return f"현재 타겟 속도: {val} km/h"

    @app.callback(
        Output('pid-display', 'children'),
        Input('input-kp', 'value'),
        Input('input-ki', 'value'),
        Input('input-kd', 'value')
    )
    def update_pid_values(kp, ki, kd):
        shared['vel_pid']['kp'] = kp
        shared['vel_pid']['ki'] = ki
        shared['vel_pid']['kd'] = kd
        return f"PID 값 - Kp: {kp}, Ki: {ki}, Kd: {kd}"
    
    
    # 경도 추가 25_04_21_steer 관련
    @app.callback(
        Output('steer-gauge', 'figure'),
        Input('interval', 'n_intervals')
    )
    def update_steer_gauge(n):
        angle = shared.get('tank_cur_yaw_deg', 0)
        
        # 파란 점: 현재 angle 방향으로 r=0~1까지 49개 점
        r_values_blue = np.linspace(0, 0.98, 49)
        theta_values_blue = [angle] * len(r_values_blue)
        blue_dots = go.Scatterpolar(
            r=r_values_blue,
            theta=theta_values_blue,
            mode='markers',
            marker=dict(size=3, color='blue'),
            name='angle path'
        )
        # 빨간 점: r=1 위치에 하나만 찍기
        red_tip = go.Scatterpolar(
            r=[1],
            theta=[angle],
            mode='markers',
            marker=dict(size=10, color='red'),
            name='current direction'
        )

        return {
        'data': [blue_dots, red_tip],
        'layout': go.Layout(
            polar=dict(
                radialaxis=dict(visible=False),
                angularaxis=dict(
                    direction='clockwise',
                    rotation=90,
                    tickmode='array',
                    tickvals=[0, 90, 180, 270],
                    ticktext=['0°', '90°', '180°', '270°']
                )
            ),
            showlegend=False,
            title='현재 전차 각도 (나침반)'
        )
    }
        
    @app.callback(
        Output('target-angle-display', 'children'),
        Input('target-angle-slider', 'value')
    )
    def update_target_angle_display(angle):
        shared['tank_tar_yaw_deg'] = angle
        return f"현재 타겟 각도: {shared['tank_tar_yaw_deg']}°"


    @app.callback(
        Output('steer-pid-display', 'children'),
        Input('steer-kp', 'value'),
        Input('steer-ki', 'value'),
        Input('steer-kd', 'value')
    )
    def update_yaw_pid(kp, ki, kd):
        shared['steer_pid']['kp'] = kp
        shared['steer_pid']['ki'] = ki
        shared['steer_pid']['kd'] = kd
        return f"steer PID 값 - Kp: {kp}, Ki: {ki}, Kd: {kd}"

    return app
