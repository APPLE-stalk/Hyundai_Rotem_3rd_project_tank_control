from flask import Flask, request, jsonify
from controller.pid_controller import PIDController

# flask 앱
app = Flask(__name__)
model = YOLO('yolov8n.pt')
pid = PIDController()

speed_data = []
target_speed = 0.0

# tank_val_ms = 0.0
tank_val_kh = 0.0

@app.route('/info', methods=['POST'])
def info():
    # global tank_val_ms
    global tank_val_kh
    print("sss")
    
    data = request.get_json(force=True)
    if not data:
        return jsonify({"error": "No JSON received"}), 400

    # print("📨 /info data received:", data)
    
    # tank_val_ms = data['playerSpeed']
    tank_val_kh = data['playerSpeed']*3.6
    speed_data.append(tank_val_kh)
    
    # print("📨 /info data received:", data['time'])
    # print('tank_speed: {0:.2f} m/s'.format(data['playerSpeed']))
    # print('tank_speed: {0:.2f} km/h'.format(data['playerSpeed']*3.6))

    # Auto-pause after 15 seconds
    #if data.get("time", 0) > 15:
    #    return jsonify({"status": "success", "control": "pause"})
    # Auto-reset after 15 seconds
    #if data.get("time", 0) > 15:
    #    return jsonify({"stsaatus": "success", "control": "reset"})
    return jsonify({"status": "success", "control": ""})

@app.route('/get_move', methods=['GET'])
def get_move():
    # global move_command
    # if move_command:
    #     command = move_command.pop(0)
    #     print(f"🚗 Move Command: {command}")
    #     return jsonify(command)
    # else:
    #     return jsonify({"move": "STOP", "weight": 1.0})

    # global tank_val_ms
    # global tank_val_kh
    
    # global error_pre_val_kh
    # global val_error_kh
    # global target_val_kh
    # global dt
    # global speed_data
    # kd_val = 0.0

    # target_val_kh = 60 # 0.08
    # kp_val = 0.18
    
    # target_val_kh = 50 # 0.08
    # kp_val = 0.152
    
    # target_val_kh = 40 # 0.08
    # kp_val = 0.0915
    
    # target_val_kh = 30 # 0.08
    # kp_val = 0.0699
    
    # target_val_kh = 20 # 0.08
    # kp_val = 0.068
    
    # target_val_kh = 10 
    # kp_val = 0.068
    
    # speed_data.append(tank_val_kh)

    # val_error_kh = target_val_kh-tank_val_kh
    
    # d_error_val_kh = (val_error_kh - error_pre_val_kh)/dt
    
    # control = val_error_kh*kp_val + d_error_val_kh*kd_val
    control = pid.compute(target_speed, tank_val_kh)
    
    
    # print('controller output: {0}'.format(control))
    return jsonify({"move": "W", "weight": control})