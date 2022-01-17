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


@app.route('/append', methods=['GET', 'POST'])
def append():
    if request.method == 'GET':
        service = AppendGetService(request)
        return service.run()
    if request.method == 'POST':
        service = AppendPostService(request)
        return service.run()


@app.route('/type/<int:type_id>', methods=['GET', 'POST'])
def types(type_id):
    if request.method == 'GET':
        service = TypesGetService(request, type_id=type_id)
        return service.run()

    elif request.method == 'POST':
        service = TypesPostService(request)
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


@app.route('/components/pop', methods=['DELETE', 'PUT', 'GET'])
def component_pop():
    if request.method in ['PUT', 'GET']:
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
# https://coderoad.ru/42601478/Flask-%D0%B2%D1%8B%D0%B7%D0%BE%D0%B2-%D1%84%D1%83%D0%BD%D0%BA%D1%86%D0%B8%D0%B8-python-%D0%BD%D0%B0-%D0%BA%D0%BD%D0%BE%D0%BF%D0%BA%D0%B5-OnClick-%D1%81%D0%BE%D0%B1%D1%8B%D1%82%D0%B8%D0%B5
