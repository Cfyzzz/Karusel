from flask import *

import settings
import tools
import model

DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = settings.SECRET_KEY


@app.route('/components', methods=['GET', 'POST'])
def components():
    if request.method == 'GET':
        query = tools.get_rows(request.args)
        data = [item.serialize for item in query]
        if data:
            res = jsonify({
                'components': data
            })
            res.status_code = 200
        else:
            # if no results are found.
            output = {
                "error": "No results found. Check url again",
                "url": request.url,
            }
            res = jsonify(output)
            res.status_code = 404
        return res

    elif request.method == 'POST':
        # make new component
        if not request.json:
            abort(400)

        new_component, _ = tools.new_component(request.json)
        if new_component is None:
            abort(400)

        res = jsonify({
            'component': new_component.serialize
        })
        res.status_code = 201
        return res


@app.route('/components/push', methods=['PUT'])
def component_push():
    if request.method == 'PUT':
        if not request.json:
            abort(400)

        if 'box' not in request.json or 'address' not in request.json:
            abort(400)

        _, created = tools.append_component(request.json)
        res = jsonify({})
        res.status_code = 201 if created else 204
        return res


@app.route('/components/pop', methods=['DELETE', 'PUT'])
def component_pop():
    if request.method == 'PUT':
        if not request.json:
            abort(400)

        result = tools.decrement_component(request.json)
        if result is None:
            abort(400)

        res = jsonify({})
        res.status_code = 204
        return res

    elif request.method == 'DELETE':
        if tools.delete_component(request.json):
            res = jsonify({})
            res.status_code = 204
        else:
            res = jsonify({
                "Error": "The requested resource is no longer available at the "
                         "server or incorrect parameters provided."
            })
            res.status_code = 410
        return res

# @app.route('/import', method=['POST'])
# def from_excel():
#     ...
#
#
# @app.route('/export', method=['GET'])
# def to_excel():
#     ...


if __name__ == '__main__':
    app.run(host=settings.DATABASE['host'], port=settings.DATABASE['port'], debug=DEBUG)
    # app.run()

# ref: https://medium.com/@prabhath_kiran/simple-rest-api-using-flask-and-peewee-3d75c7bff515
# ref: https://habr.com/ru/post/483202/
# ref: https://ru.stackoverflow.com/questions/779534/%D0%9F%D0%B5%D1%80%D0%B5%D0%B4%D0%B0%D1%87%D0%B0-%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D1%85-%D0%BC%D0%B5%D0%B6%D0%B4%D1%83-%D0%B2%D1%8C%D1%8E%D1%88%D0%BA%D0%B0%D0%BC%D0%B8-python-flask
