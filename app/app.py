from app.core.user import User
import app.core.const_data as data
from flask import Flask

app = Flask(__name__)

@app.route('/<string:gender>')
def hello_world(gender):
    a = User()
    if not gender in data.genders:
        return '<center><h1>This gender has not yet been invented</center></h1>'
    else:
        return '<center><h1>%s</center></h1>' % a.gender


@app.route('/')
def he():
    return 1


if __name__ == '__main__':
    app.run(host='0.0.0.0')
