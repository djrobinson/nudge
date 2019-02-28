# manage.py
from dotenv import load_dotenv
load_dotenv()

import os

from quart import Quart, websocket, render_template, jsonify

app_settings = os.getenv(
    'APP_SETTINGS',
    'project.server.config.DevelopmentConfig'
)
app = Quart(
    __name__,
    template_folder='./client/templates',
    static_folder='./client/static'
)
is_debug = True
print("Configuring App")
app.config.from_object(app_settings)

from server.api.views import main_blueprint
app.register_blueprint(main_blueprint)

@app.websocket('/ws')
async def ws():
    while True:
        data = await websocket.receive()
        await websocket.send(f"echo {data}")


@app.route('/', methods=['GET'])
def home():
    return jsonify({'hello': 'index'})


def run_web_app():
    app.run(debug=is_debug)


if __name__ == '__main__':
    run_web_app()

