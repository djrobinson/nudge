from quart import Quart

app = Quart(__name__)


@app.route('/')
async def index():
    return '<h1>Howdy</h1>'


@app.route('/up')
async def up():
    return 'Up'


if __name__ == "__main__":
    app.run(host='localhost', port=8080)
