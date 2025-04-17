# 속도제어기

from flask import Flask, request, jsonify
from dash import Dash, dcc, html
from dash.dependencies import Output, Input
import threading
import plotly.graph_objs as go


# import os
# import torch
from ultralytics import YOLO


# python speed_controller.py

# flask 앱
app = Flask(__name__)
model = YOLO('yolov8n.pt')

# 경도 코딩
tank_val_ms = 0.0
tank_val_kh = 0.0

target_val_kh = 0.0
error_pre_val_kh = 0.0
val_error_kh = 0.0

speed_data = []

dt = 1.0

# dash 앱
dash_app = Dash(__name__)
# Dash 레이아웃 구성: 실시간 그래프와 타겟 속도 슬라이더 추가
dash_app.layout = html.Div([
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

# 그래프 업데이트 콜백 함수
@dash_app.callback(
    Output('live-graph', 'figure'),
    Input('interval', 'n_intervals')
)
def update_graph(n):
    # speed_data의 복사본 생성
    data = speed_data.copy()
    max_points = 100
    data_len = len(data)
    
    if data_len <= max_points:
        x_start = 0
    else:
        x_start = data_len - max_points

    x_range = [x_start, data_len]
    y_range = [0, 80]  # 고정 y축 (필요에 따라 조정)

    return {
        'data': [go.Scatter(y=data, mode='lines+markers')],
        'layout': go.Layout(
            xaxis=dict(range=x_range, title='데이터 포인트'),
            yaxis=dict(range=y_range, title='Speed'),
            title='실시간 속도 시각화'
        )
    }


# 슬라이더 변경 시 타겟 속도를 업데이트하는 콜백 함수
@dash_app.callback(
    Output('target-speed-display', 'children'),
    Input('target-speed-slider', 'value')
)
def update_target_speed_display(value):
    global target_val_kh   # target_speed 대신 target_val_kh 사용
    target_val_kh = value  # 전역 변수 덮어쓰기
    return f"현재 타겟 속도: {value} km/h"

   
    
## 스레드 함수    
def run_flask():
    app.run(port=5050, debug=False, use_reloader=False)

def run_dash():
    dash_app.run(port=8050, debug=False, use_reloader=False)



# Move commands with weights (11+ variations)
move_command = [
    {"move": "W", "weight": 1.0}
    # 'move':['W' or 'A' or 'S' or 'D'], 'weight': [weight]
    # 'move': ["STOP"]
]

# Action commands with weights (15+ variations)
action_command = [
    # {"turret": "Q", "weight": 1.0}
    # "turret": ["Q" or "E" or "R" or "F"], "weight":[weight]
    # "turret": ["FIRE"]
]

@app.route('/detect', methods=['POST'])
def detect():
    # image = request.files.get('image')
    # if not image:
    #     return jsonify({"error": "No image received"}), 400
    data = request.get_json(force=True)
    print("📨📨📨📨📨📨📨📨📨📨📨📨📨📨📨📨📨📨📨📨📨📨📨📨📨📨📨📨📨📨 /info data received:", data)

    # image_path = 'temp_image.jpg'
    # image.save(image_path)

    # results = model(image_path)
    # detections = results[0].boxes.data.cpu().numpy()

    # target_classes = {0: "person", 2: "car", 7: "truck", 15: "rock"}
    # filtered_results = []
    # for box in detections:
    #     class_id = int(box[5])
    #     if class_id in target_classes:
    #         filtered_results.append({
    #             'className': target_classes[class_id],
    #             'bbox': [float(coord) for coord in box[:4]],
    #             'confidence': float(box[4])
    #         })

    # return jsonify(filtered_results)
    return jsonify({'hi':'hh'})

@app.route('/info', methods=['POST'])
def info():
    global tank_val_ms
    global tank_val_kh
    data = request.get_json(force=True)
    if not data:
        return jsonify({"error": "No JSON received"}), 400

    # print("📨 /info data received:", data)
    
    tank_val_ms = data['playerSpeed']
    tank_val_kh = data['playerSpeed']*3.6
    
    print("📨 /info data received:", data['time'])
    print('tank_speed: {0:.2f} m/s'.format(data['playerSpeed']))
    print('tank_speed: {0:.2f} km/h'.format(data['playerSpeed']*3.6))

    # Auto-pause after 15 seconds
    #if data.get("time", 0) > 15:
    #    return jsonify({"status": "success", "control": "pause"})
    # Auto-reset after 15 seconds
    #if data.get("time", 0) > 15:
    #    return jsonify({"stsaatus": "success", "control": "reset"})
    return jsonify({"status": "success", "control": ""})

@app.route('/update_position', methods=['POST'])
def update_position():
    data = request.get_json()
    if not data or "position" not in data:
        return jsonify({"status": "ERROR", "message": "Missing position data"}), 400

    try:
        x, y, z = map(float, data["position"].split(","))
        current_position = (int(x), int(z))
        print(f"📍 Position updated: {current_position}")
        return jsonify({"status": "OK", "current_position": current_position})
    except Exception as e:
        return jsonify({"status": "ERROR", "message": str(e)}), 400



    

@app.route('/get_action', methods=['GET'])
def get_action():
    global action_command
    if action_command:
        command = action_command.pop(0)
        print(f"🔫 Action Command: {command}")
        return jsonify(command)
    else:
        #return jsonify({"turret": "", "weight": 0.0})
        return jsonify({"hh":'hi'})

@app.route('/update_bullet', methods=['POST'])
def update_bullet():
    data = request.get_json()
    if not data:
        return jsonify({"status": "ERROR", "message": "Invalid request data"}), 400

    print(f"💥 Bullet Impact at X={data.get('x')}, Y={data.get('y')}, Z={data.get('z')}, Target={data.get('hit')}")
    return jsonify({"status": "OK", "message": "Bullet impact data received"})

@app.route('/set_destination', methods=['POST'])
def set_destination():
    data = request.get_json()
    if not data or "destination" not in data:
        return jsonify({"status": "ERROR", "message": "Missing destination data"}), 400

    try:
        x, y, z = map(float, data["destination"].split(","))
        print(f"🎯 Destination set to: x={x}, y={y}, z={z}")
        return jsonify({"status": "OK", "destination": {"x": x, "y": y, "z": z}})
    except Exception as e:
        return jsonify({"status": "ERROR", "message": f"Invalid format: {str(e)}"}), 400

@app.route('/update_obstacle', methods=['POST'])
def update_obstacle():
    data = request.get_json()
    if not data:
        return jsonify({'status': 'error', 'message': 'No data received'}), 400

    print("🪨 Obstacle Data:", data)
    return jsonify({'status': 'success', 'message': 'Obstacle data received'})

#Endpoint called when the episode starts
@app.route('/init', methods=['GET'])
def init():
    config = {
        "startMode": "start",  # Options: "start" or "pause"
        "blStartX": 60,  #Blue Start Position
        "blStartY": 10,
        "blStartZ": 27.23,
        "rdStartawX": 59, #Red Start Position
        "rdStartY": 10,
        "rdStartZ": 280
    }
    print("🛠️ Initialization config sent via /init:", config)
    return jsonify(config)

@app.route('/start', methods=['GET'])
def start():
    print("🚀 /start command received")
    return jsonify({"control": ""})
@app.route('/get_move', methods=['GET'])
def get_move():
    # global move_command
    # if move_command:
    #     command = move_command.pop(0)
    #     print(f"🚗 Move Command: {command}")
    #     return jsonify(command)
    # else:
    #     return jsonify({"move": "STOP", "weight": 1.0})

    global tank_val_ms
    global tank_val_kh
    
    global error_pre_val_kh
    global val_error_kh
    global target_val_kh
    global dt
    global speed_data
    kd_val = 0.0

    # target_val_kh = 60 # 0.08
    # kp_val = 0.18
    
    # target_val_kh = 50 # 0.08
    # kp_val = 0.152
    
    # target_val_kh = 40 # 0.08
    # kp_val = 0.0915
    
    # target_val_kh = 30 # 0.08
    kp_val = 0.0699
    
    # target_val_kh = 20 # 0.08
    # kp_val = 0.068
    
    # target_val_kh = 10 
    # kp_val = 0.068
    
    speed_data.append(tank_val_kh)

    val_error_kh = target_val_kh-tank_val_kh
    
    d_error_val_kh = (val_error_kh - error_pre_val_kh)/dt
    
    control = val_error_kh*kp_val + d_error_val_kh*kd_val
    
    
    print('controller output: {0}'.format(control))
    return jsonify({"move": "W", "weight": control})
   
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5050)
if __name__ == '__main__':
    t1 = threading.Thread(target=run_flask)
    t2 = threading.Thread(target=run_dash)

    t1.start()
    t2.start()

    t1.join()
    t2.join()