import os
import traceback

from werkzeug.exceptions import RequestEntityTooLarge

import tools
from .iservise import *


ALLOWED_EXTENSIONS = {'xls', 'xlsx'}
EXPORT_FOLDER = './exports'


class ExportToExcelFileGetService(IService):
    def run(self):
        if not tools.is_valid_bd():
            # В БД нет компонентов
            return redirect(request.url)

        if not os.access(EXPORT_FOLDER, os.F_OK):
            os.makedirs(EXPORT_FOLDER)

        filename = "excel_file.xls"
        path = os.path.join(EXPORT_FOLDER, filename)
        if os.access(path, os.F_OK):
            os.remove(path)

        tools.export_to_excel(path)
        if os.access(path, os.F_OK):
            return send_file(path)
        return redirect(request.url)
