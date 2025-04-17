from flask import Flask, request, jsonify
from controller.pid_controller import PIDController
from utils.config import SHARED

# flask 앱
app = Flask(__name__)
pid = PIDController()
shared = SHARED



@app.route('/info', methods=['POST'])
def info():
    data = request.get_json(force=True)
    shared['tank_cur_val_ms'] = data['playerSpeed']
    shared['tank_cur_val_kh'] = data['playerSpeed']*3.6
    
    if not data:
        return jsonify({"error": "No JSON received"}), 400

    # print("📨 /info data received:", data)
    
    # tank_val_ms = data['playerSpeed']
    # tank_val_kh = data['playerSpeed']*3.6
    # speed_data.append(tank_val_kh)
    
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
    print('uuuuuuuu', shared['tank_tar_val_kh'])
    control = pid.compute(shared['tank_tar_val_kh'], shared['tank_cur_val_kh'])
    
    if control > 0:
        return jsonify({"move": "W", "weight": control})
    elif control < 0:
        return jsonify({"move": "S", "weight": -control})
    else:
        return jsonify({"move": "STOP"})
    # 

    # # print('controller output: {0}'.format(control))
    # return jsonify({"move": "W", "weight": control})


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