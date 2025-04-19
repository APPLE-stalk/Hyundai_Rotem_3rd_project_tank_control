SHARED = {
    'pre_playerPos': {
        'x':0,
        # 'y':0,
        'z':0
    },
    
    'del_playerPos_x': [],
    'del_playerPos_z': [],
    
    
    "tank_cur_val_ms": 0.0,
    
    "tank_cur_val_kh": 0.0,
    "tank_tar_val_kh": 0.0,
    
    "speed_data": [],
    
    "pid": {
        "kp": 0.5,#0.1525,#0.0515,
        "ki": 0.0,
        "kd": 0.05,#0.18#0.0
    }
}

# # PID 제어기 기본 파라미터
# PID_CONFIG = {
#     'kp': 0.07,
#     'ki': 0.0,
#     'kd': 0.0,
#     'dt': 1.0
# }

# # YOLO 모델 설정
# YOLO_CONFIG = {
#     'model_path': 'yolov8n.pt',
#     'target_classes': {
#         0: "person",
#         2: "car",
#         7: "truck",
#         15: "rock"
#     }
# }

# # 서버 설정
# SERVER_CONFIG = {
#     'flask_port': 5050,
#     'dash_port': 8050
# }

# # 속도 그래프 설정
# GRAPH_CONFIG = {
#     'max_speed': 80,
#     'max_points': 100
# }
