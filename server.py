from model import Component, Type, Package
from peewee import DoesNotExist


def get_row(**filter) -> list[Component]:
    """ Получить записи по фильтру

    :param filter: фильтр для запроса"""
    try:
        return Component.select().where(**filter)
    except DoesNotExist:
        return []
    except Exception as ex:
        raise ex


def decrement_element(element, number):
    """ Списать со склада элемент

     :param element: списываемый элемент
     :param number: списываемое количество"""
    ...


def increment_element(element, number):
    """ Добавить на склад элемент

         :param element: добавляемый элемент
         :param number: добавляемое количество"""
    ...


def import_from_excel(excel_file, append=True):
    """ Импортировать данные из excel-файла

    :param excel_file: Excel-файл для импорта
    :param append: True (по умолчанию) - добавлять новые или заменять существующие записи;
    False - удалить теущие данные по базе и построить новую"""
    ...


def export_to_excel(path):
    """ Экспортировать базу в Excel-файл

    :param path: путь к файлу для выгрузки """
    ...
