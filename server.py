from flask import *

import model


DEBUG = True
SECRET_KEY = 'ssshhhh'

app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/components', methods=['GET', 'POST'])
def components():
    if request.method == 'GET':
        ...
    elif request.method == 'POST':
        ...


@app.route('/components/<string:type>/<string:designation>', methods=['GET'])
@app.route('/components/push', methods=['PUT'])
@app.route('/components/pop', methods=['DELETE'])
def component():
    ...


@app.route('/import', method=['POST'])
def from_excel():
    ...


@app.route('/export', method=['GET'])
def to_excel():
    ...


if __name__ == '__main__':
    app.run()


# ref: https://medium.com/@prabhath_kiran/simple-rest-api-using-flask-and-peewee-3d75c7bff515
# ref: https://habr.com/ru/post/483202/
