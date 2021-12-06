from model import Component, Type, Package
from peewee import DoesNotExist
import pandas as pd


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


def get_rows(**filter) -> list[Component]:
    """ Получить записи по фильтру

    :param filter: фильтр для запроса"""
    try:
        return Component.select().where(**filter)
    except DoesNotExist:
        return []


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
        raise InsufficientException(f"{component.description} {component.type} {component.package} на складе всего {component.quantity}, списываете {number}")


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
    xl = pd.read_excel(io=excel_file, engine='openpyxl')
    if xl.sheet_names and not append:
        drop_all_tables()

    # Processing sheets
    for sheet_name in xl.sheet_names:
        type = Type.get_or_create(type=sheet_name.lower())
        df1 = xl.parse(sheet_name)
        df1.head()


def export_to_excel(path):
    """ Экспортировать базу в Excel-файл

    :param path: путь к файлу для выгрузки """
    ...


def validate_component(component):
    """ Проверка компонента, что он существует в базе """
    pass


def validate_number(number):
    """ Проверка положительного числа """
    pass


def validate_file(file):
    """ Проверка существования файла """
    ...


def drop_all_tables():
    """ Уничтожение всех таблиц """
    ...