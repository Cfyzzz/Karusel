from flask import *

import settings
from services import *


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
def type_component(type_id):
    if request.method == 'GET':
        service = TypeGetService(request, type_id=type_id)
        return service.run()

    elif request.method == 'POST':
        service = TypePostService(request)
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


@app.route('/types', methods=['GET', 'POST'])
def list_types():
    if request.method == 'GET':
        service = ListTypesGetService(request)
        return service.run()
    if request.method == 'POST':
        service = ListTypesPostService(request)
        return service.run()


@app.route('/packages', methods=['GET', 'POST'])
def list_packages():
    if request.method == 'GET':
        service = ListPackagesGetService(request)
        return service.run()
    if request.method == 'POST':
        service = ListPackagesPostService(request)
        return service.run()


if __name__ == '__main__':
    app.run(host=settings.HOST, port=settings.PORT, debug=settings.DEBUG)
