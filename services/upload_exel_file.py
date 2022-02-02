import os
import traceback

from werkzeug.exceptions import RequestEntityTooLarge

import tools
from .iservise import *


ALLOWED_EXTENSIONS = {'xls', 'xlsx'}
UPLOAD_FOLDER = './uploads'


class UploadExcelFileService(IService):
    def __init__(self, the_request, the_config):
        super().__init__(the_request)
        self.config = the_config
        self.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit 16 Mb

    def run(self):
        file = self.request.files['file']
        if not os.access(UPLOAD_FOLDER, os.F_OK):
            os.makedirs(UPLOAD_FOLDER)

        try:
            if file and self.allowed_file(file.filename):
                filename = "excel_file"
                path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(path)
                tools.import_from_excel(path, append=False)
                flash("База данных загружена")
                return redirect(request.url)
        except RequestEntityTooLarge:
            # Превышен допустимый размер файла
            traceback.format_exc()
        # Что-то пошло не так...
        return redirect(request.url)

    @staticmethod
    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
