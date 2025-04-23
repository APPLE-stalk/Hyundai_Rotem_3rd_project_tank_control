from server.flask_server import app as flask_app
from server.dash_server import create_dash_app
from server.thread_manager import run_multithread
<<<<<<< HEAD
=======
from utils.config import SHARED

>>>>>>> kd

def run_flask():
    flask_app.run(port=5050, debug=False, use_reloader=False)

def run_dash():
    create_dash_app().run(port=8050, debug=False, use_reloader=False)

if __name__ == '__main__':
<<<<<<< HEAD
    run_multithread(run_flask, run_dash)      
    
    
=======
    run_multithread(run_flask, run_dash)
>>>>>>> kd
