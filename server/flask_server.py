from flask import Flask, request, jsonify
from controller.pid_controller import PIDController
from utils.config import SHARED
from models.yolo_model import ObjectDetector
import numpy as np
# flask 앱
app = Flask(__name__)
vel_pid = PIDController()
shared = SHARED

detector = ObjectDetector()


@app.route('/info', methods=['POST'])
def info():
    data = request.get_json(force=True)
    
    # print("📨 /info data received:", data['time'])
    
    # 경도 추가 25_04_20 -> 2차원 헤딩 정보로 전후진 구분 기능 추가하기
    # print('x: ', data['playerPos']['x'])
    # print('y: ', data['playerPos']['y'])
    # print('z: ', data['playerPos']['z'])
    
    
    # 위치 delta 구하기, [현재 위치 - 이전 위치]
    del_playerPos_x = data['playerPos']['x'] - shared['pre_playerPos']['x']
    del_playerPos_z = data['playerPos']['z'] - shared['pre_playerPos']['z']
    
    
    # 전후진 구분 알고리즘 개발 용 시각화 리스트, 리스트는 알고리즘 동작에는 필요 없음
    shared['del_playerPos']['x'].append(del_playerPos_x)
    shared['del_playerPos']['z'].append(del_playerPos_z)
    
    
    # 이동 벡터
    v_move = np.array([del_playerPos_x, del_playerPos_z]) 
    

    # 월드 좌표계 기준의 전차의 yaw(deg -> 라디안)
    yaw_deg = data['playerBodyX']
    yaw_rad = np.deg2rad(90 - yaw_deg)

    # 월드 좌표계 기준의 전차의 yaw(deg -> 라디안)의 벡터화
    v_forward = np.array([np.cos(yaw_rad), np.sin(yaw_rad)])  

    # 방향 판단
    moving_direction = np.sign(np.dot(v_forward, v_move)) # 두 벡터 내적 이용, +1: 전진, -1: 후진
    
    
    # 알고리즘 말단부, 최신 정보로 업데이트
    shared['pre_playerPos']['x'] = data['playerPos']['x']
    shared['pre_playerPos']['z'] = data['playerPos']['z']

    
    shared['tank_cur_vel_ms'] = data['playerSpeed']*moving_direction # 전후진 고려
    shared['tank_cur_vel_kh'] = data['playerSpeed']*3.6*moving_direction # 전후진 고려
    shared['vel_data'].append(shared['tank_cur_vel_kh'])
    
    if not data:
        return jsonify({"error": "No JSON received"}), 400

    

    # Auto-pause live-graphafter 15 seconds
    #if data.get("time", 0) > 15:
    #    return jsonify({"status": "success", "control": "pause"})
    # Auto-reset after 15 seconds
    #if data.get("time", 0) > 15:
    #    return jsonify({"stsaatus": "success", "control": "reset"})
    return jsonify({"status": "success", "control": ""})

@app.route('/get_move', methods=['GET'])
def get_move():
    vel_pid.update_gains(
    kp=shared['vel_pid']['kp'],
    ki=shared['vel_pid']['ki'],
    kd=shared['vel_pid']['kd'],
    dt=shared['vel_pid']['dt'] # dt는 고정값이라 업데이트 생략
    )
    
    # global move_command
    # if move_command:
    #     command = move_command.pop(0)
    #     print(f"🚗 Move Command: {command}")
    #     return jsonify(command)
    # else:
    #     return jsonify({"move": "STOP", "weight": 1.0})
    
    # 속도 제어기(PID)
    control = vel_pid.compute(shared['tank_tar_vel_kh'], shared['tank_cur_vel_kh'])
    
    print('control: ', control)
    print('p', vel_pid.kp)
    print('d', vel_pid.kd)
    print(shared['tank_tar_vel_kh'])
    if control > 0:
        return {"move": "W", "weight": control}
    
    else:
        return {"move": "S", "weight": (-1)*control}
    



@app.route('/get_action', methods=['GET'])
def get_action():
    # global action_command
    # if 1:
        #command = action_command.pop(0)
        # print(f"🔫 Action Command: {command}")
    #     return jsonify(0)
    # else:
        #return jsonify({"turret": "", "weight": 0.0})
        # return jsonify({"hh":'hi'})
    return jsonify({"hh":'hi'})
    
@app.route('/start', methods=['GET'])
def start():
    # print("🚀 /start command received")
    # return jsonify({"control": ""})
    return jsonify({"hh":'hi'})

@app.route('/update_position', methods=['POST'])
def update_position():
    # data = request.get_json()
    # if not data or "position" not in data:
    #     return jsonify({"status": "ERROR", "message": "Missing position data"}), 400

    # try:
    #     x, y, z = map(float, data["position"].split(","))
    #     current_position = (int(x), int(z))
    #     # print(f"📍 Position updated: {current_position}")
    #     return jsonify({"status": "OK", "current_position": current_position})
    # except Exception as e:
    #     return jsonify({"status": "ERROR", "message": str(e)}), 400
    return jsonify({"hh":'hi'})

@app.route('/detect', methods=['POST'])
def detect():
    print("📨📨📨📨📨📨📨📨📨📨📨📨📨📨📨📨📨📨📨📨📨📨📨📨📨📨📨📨📨📨" )
    image = request.files.get('image')
    if not image:
        return jsonify({"error": "No image received"}), 400

    image_path = 'temp_image.jpg'
    image.save(image_path)

    results = detector.detect(image_path)
    return jsonify(results)


    
