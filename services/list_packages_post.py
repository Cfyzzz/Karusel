from peewee import DoesNotExist

from model import Package, Component, Type
from tools import is_valid_input_str
from .iservise import *


class ListPackagesPostService(IService):
    def run(self):
        action = self.request.form.get('action')
        package_id = self.request.form.get('typeId')

        if action == "edit":
            try:
                package = Package.get_by_id(package_id)
            except DoesNotExist:
                flash("Что-то пошло не так. Корпус не найден")
                return redirect(request.url)
            new_name = self.request.form.get('typeRename')
            if not is_valid_input_str(new_name, 16):
                flash("Вы ввели некорректное имя корпуса")
                return redirect(request.url)

            new_package = Package.get_or_none(package=new_name)
            if new_package:
                flash("Такой корпус уже существует. Введите другое название корпуса")
                return redirect(request.url)

            package.package = new_name
            package.save()
            return redirect(request.url)
        elif action == "delete":
            try:
                package = Package.get_by_id(package_id)
            except DoesNotExist:
                flash("Что-то пошло не так. Корпус не найден")
                return redirect(request.url)
            Component.delete().where(Component.package == package).execute()
            Package.delete_by_id(package_id)
            flash(f"Корпус \"{package.package}\" удалён")
            return redirect(request.url)
        elif action == "append":
            package_name = self.request.form.get('typeName')
            type_name = self.request.form.get('typeType')
            the_type = Type.get_or_none(type=type_name)

            if the_type is None:
                flash("Ошибка. Тип не распознан")
                return redirect(request.url)

            if not is_valid_input_str(package_name, 16):
                flash("Вы ввели некорректное имя корпуса")
                return redirect(request.url)

            new_package = Package.get_or_none(package=package_name, type=the_type)
            if new_package:
                flash("Такой корпус уже существует. Введите другое название корпуса")
                return redirect(request.url)
            new_package = Package.create(package=package_name, type=the_type)
            new_package.save()
        return redirect(request.url)