from src.app import createApp
import os
from dotenv import load_dotenv, find_dotenv

from src.config.extension import socketio

load_dotenv(find_dotenv())

port = os.getenv('FLASK_PORT')
env_name = os.getenv('FLASK_ENV')

if env_name == "development":
    debug = True
else:
    debug = False

app = createApp()

if __name__ == '__main__':
    # run app
    # app.run(debug=debug, host='0.0.0.0', port=port)
    socketio.run(app, debug=debug, host='0.0.0.0', port=port, allow_unsafe_werkzeug=True)
