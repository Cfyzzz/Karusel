import os

from openpyxl import Workbook

import tools
from model import Type, Component
from .iservise import *

ALLOWED_EXTENSIONS = {'xls', 'xlsx'}
EXPORT_FOLDER = './exports'


class ReportToExcelFileGetService(IService):
    def run(self):
        if not tools.is_valid_bd():
            # В БД нет компонентов
            return redirect(request.url)

        if not os.access(EXPORT_FOLDER, os.F_OK):
            os.makedirs(EXPORT_FOLDER)

        filename = "report.xls"
        path = os.path.join(EXPORT_FOLDER, filename)
        if os.access(path, os.F_OK):
            os.remove(path)

        self.report_to_excel(path)
        if os.access(path, os.F_OK):
            return send_file(path)
        return redirect("/")

    @staticmethod
    def report_to_excel(path):
        """ Отчет о заканчивающихся деталях в Excel-файл

        :param path: путь к файлу для выгрузки """
        workbook = Workbook()
        new_sheet = workbook.create_sheet("Отчёт для закупа")
        new_sheet.append(["", "Наименование", "№ Ящика", "Ячейка", "Кол-во", "Описание", "Корпус", "Datasheet"])
        for type_item in Type.select():
            components = Component.select().where((Component.type == type_item) &
                                                  (Component.quantity < Component.min_amount))
            if components.count() == 0:
                continue

            new_sheet.append([type_item.type])
            for component in components:
                row = [
                    "",
                    component.designation,
                    component.box,
                    component.address,
                    component.quantity,
                    component.description,
                    str(component.package) if component.package else "",
                    component.datasheet
                ]
                new_sheet.append(row)
        workbook.remove(workbook["Sheet"])
        if not workbook.worksheets:
            return
        workbook.save(filename=path)
