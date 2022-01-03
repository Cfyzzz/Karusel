import re
from os import path

import pandas as pd
from openpyxl import Workbook

from model import Component, Type, Package, drop_all_tables, create_tables, peewee

column_names = {"Наименование": "designation", "№ Ящика": "box", "Ячейка": "address", "Кол-во": "quantity",
                "Описание": "description", "Корпус": "package", "Datasheet": "datasheet"}


class InsufficientException(Exception):
    """ Недостаточное количество деталей """

    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return f"InsufficientException, {self.message}"
        return "InsufficientException has been raised"


def decrement_element(component: Component, number: int):
    """ Списать со склада элемент
    В случае недостаточного количества на складе выкидывается исключение InsufficientException

     :param component: списываемый элемент
     :param number: списываемое количество"""

    validate_component(component)
    validate_number(number)
    if component.quantity >= number:
        component.quantity -= number
        component.save()
    else:
        raise InsufficientException(
            f"{component.description} {component.type} {component.package} на складе всего {component.quantity}, списываете {number}")


def increment_element(component: Component, number: int):
    """ Добавить на склад элемент

         :param component: добавляемый элемент
         :param number: добавляемое количество"""
    validate_component(component)
    validate_number(number)
    component.quantity += number
    component.save()


def import_from_excel(excel_file, append=True):
    """ Импортировать данные из excel-файла

    :param excel_file: путь к Excel-файлу для импорта
    :param append: True (по умолчанию) - добавлять новые или заменять существующие записи;
    False - удалить теущие данные по базе и построить новую"""
    validate_file(excel_file)
    xl = pd.ExcelFile(excel_file)

    if xl.sheet_names and not append:
        drop_tables()

    # Processing sheets
    for sheet_name in xl.sheet_names:
        type, _ = Type.get_or_create(type=sheet_name)
        df = xl.parse(sheet_name)

        for idx, row in df.iterrows():
            data_component = {'type': type}
            for column_xl, column_bd in column_names.items():
                if column_xl in row:
                    data_component[column_bd] = row[column_xl]

            prepare_data_component(data_component)
            quantity = data_component.pop("quantity", 0)
            component, _ = Component.get_or_create(**data_component)
            component.quantity += quantity
            component.save()


def export_to_excel(path):
    """ Экспортировать базу в Excel-файл

    :param path: путь к файлу для выгрузки """
    workbook = Workbook()
    for type_item in Type.select():
        new_sheet = workbook.create_sheet(type_item.type)
        new_sheet.append(["", "Корпус", "Наименование", "№ Ящика", "Ячейка", "Кол-во", "Описание", "Datasheet"])
        for component in Component.select().where(Component.type == type_item):
            row = [
                "",
                str(component.package) if component.package else "",
                component.designation,
                component.box,
                component.address,
                component.quantity,
                component.description,
                component.datasheet
            ]
            new_sheet.append(row)

    workbook.remove(workbook["Sheet"])
    workbook.save(filename=path)


def validate_component(component):
    """ Проверка компонента, что он существует в базе """
    if not component:
        raise Exception("Нет такого компонента")


def validate_number(number):
    """ Проверка положительного числа """
    if type(number) is not int or number >= 0:
        raise Exception("Это не положительное целое число")


def validate_file(file):
    """ Проверка существования файла """
    if not path.exists(file):
        raise FileExistsError


def prepare_data_component(data):
    """ Подготовка компонента к записи в базу """
    if "description" in data:
        data["description"] = "" if str(data["description"]) == "nan" else data["description"]

    if "address" in data:
        data["address"] = "" if str(data["address"]) == "nan" else data["address"]

    if "quantity" in data:
        data["quantity"] = data["quantity"] if data["quantity"].__class__ is int else 0

    if "package" in data:
        package, _ = Package.get_or_create(package=data["package"])
        data["package"] = package


def union_metric_format(value: str) -> str:
    """ Приведение обозначений номинала к единому формату """
    reg = r'[+-]?\d+\.?\d*|[unpkM]?'
    arr = re.findall(reg, value)
    if not arr or arr[0] == '':
        return value

    val = arr[0]
    liter = arr[1]

    if liter == "u":
        koef = 1000000
    elif liter == "n":
        koef = 1000
    elif liter == "k":
        koef = 1000
    elif liter == "M":
        koef = 1000000
    else:
        koef = 1

    return str(float(val) * koef)


def drop_tables():
    """ Создание новой базы данных """
    drop_all_tables()
    create_tables()


def new_component(json_component: dict):
    """ Создаёт новый компонет или перезаписывает существующий

    :param json_component - словарь с полями компонента
    :return component, created - компонент и флаг о создании нового в базе
    """
    if 'type' not in json_component:
        return None, None
    type, _ = Type.get_or_create(type=json_component['type'])
    json_component['type'] = type
    prepare_data_component(json_component)
    component, created = Component.get_or_create(**json_component)
    component.save()
    return component, created


def is_valid_bd() -> bool:
    """ Проверка на существование БД

    :return True - если существует БД и заполнена, False - иначе
    """
    quantity = Component.select(peewee.fn.COUNT(Component.id))
    return quantity > 0


# ref: https://www.knowledgehut.com/blog/programming/how-to-work-with-excel-using-python
# ref: https://coderoad.ru/53640958/%D0%9E%D0%B1%D1%8A%D0%B5%D0%B4%D0%B8%D0%BD%D0%B5%D0%BD%D0%B8%D0%B5-%D0%BD%D0%B5%D0%BE%D0%B1%D1%8F%D0%B7%D0%B0%D1%82%D0%B5%D0%BB%D1%8C%D0%BD%D1%8B%D1%85-%D1%84%D0%B8%D0%BB%D1%8C%D1%82%D1%80%D0%BE%D0%B2-%D0%BF%D0%B5%D1%80%D0%B5%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D1%85-%D0%B7%D0%B0%D0%BF%D1%80%D0%BE%D1%81%D0%BE%D0%B2-%D0%B2-Peewee
