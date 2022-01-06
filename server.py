from flask import *

import settings
from services import *


DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = settings.SECRET_KEY


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/stock')
def stock():
    service = StockGetService(request)
    return service.run()


@app.route('/type/<int:type_id>')
def types(type_id):
    service = TypesGetService(request, type_id=type_id)
    return service.run()


@app.route('/components', methods=['GET', 'POST'])
def components():
    if request.method == 'GET':
        service = ComponentsGetService(request)
        return service.run()

    elif request.method == 'POST':
        service = ComponentsPostService(request)
        return service.run()


@app.route('/components/push', methods=['PUT'])
def component_push():
    if request.method == 'PUT':
        service = ComponentsPushPutService(request)
        return service.run()


@app.route('/components/pop', methods=['DELETE', 'PUT'])
def component_pop():
    if request.method == 'PUT':
        service = ComponentsPopPutService(request)
        return service.run()

    elif request.method == 'DELETE':
        service = ComponentsPopDeleteService(request)
        return service.run()


@app.route('/import', methods=['GET', 'POST'])
def from_excel():
    if request.method == 'POST':
        service = UploadExcelFileService(request, app.config)
        return service.run()
    return '''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form action="" method=post enctype=multipart/form-data>
          <p><input type=file name=file>
             <input type=submit value=Upload>
        </form>
        '''


@app.route('/export', methods=['GET'])
def to_excel():
    if request.method == 'GET':
        service = ExportToExcelFileGetService(request)
        return service.run()


if __name__ == '__main__':
    app.run(host=settings.DATABASE['host'], port=settings.DATABASE['port'], debug=DEBUG)
    # app.run()

# ref: https://medium.com/@prabhath_kiran/simple-rest-api-using-flask-and-peewee-3d75c7bff515
# ref: https://habr.com/ru/post/483202/
# ref: https://ru.stackoverflow.com/questions/779534/%D0%9F%D0%B5%D1%80%D0%B5%D0%B4%D0%B0%D1%87%D0%B0-%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D1%85-%D0%BC%D0%B5%D0%B6%D0%B4%D1%83-%D0%B2%D1%8C%D1%8E%D1%88%D0%BA%D0%B0%D0%BC%D0%B8-python-flask
# https://flask-russian-docs.readthedocs.io/ru/latest/patterns/fileuploads.html
# https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3-ru
