# 속도제어기





# import os
# import torch



# python speed_controller.py


# 경도 코딩
tank_val_ms = 0.0
tank_val_kh = 0.0

target_val_kh = 0.0
error_pre_val_kh = 0.0
val_error_kh = 0.0


dt = 1.0






# 슬라이더 변경 시 타겟 속도를 업데이트하는 콜백 함수
@dash_app.callback(
    Output('target-speed-display', 'children'),
    Input('target-speed-slider', 'value')
)
def update_target_speed_display(value):
    global target_val_kh   # target_speed 대신 target_val_kh 사용
    target_val_kh = value  # 전역 변수 덮어쓰기
    return f"현재 타겟 속도: {value} km/h"

   
    


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



