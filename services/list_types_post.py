from peewee import DoesNotExist

from tools import get_base_url, is_valid_input_str
from model import Type
from .iservise import *


class ListTypesPostService(IService):
    def run(self):
        action = self.request.form.get('action')
        type_id = self.request.form.get('typeId')

        if action == "edit":
            try:
                type_component = Type.get_by_id(type_id)
                new_name = self.request.form.get('typeRename')
                type_component.type = new_name
                type_component.save()
            except DoesNotExist:
                flash("Что-то пошло не так. Тип не найден")
                return redirect(request.url)
            return redirect(request.url)
        elif action == "delete":
            try:
                type_component = Type.get_by_id(type_id)
            except DoesNotExist:
                flash("Что-то пошло не так. Тип не найден")
                return redirect(request.url)
            flash(f"Тип \"{type_component.type}\" удалён")
            Type.delete_by_id(type_id)
            return redirect(request.url)
        elif action == "append":
            type_name = self.request.form.get('typeName')

            if not is_valid_input_str(type_name, 64):
                flash("Вы ввели некорректное имя типа")
                return redirect(request.url)

            new_type = Type.get_or_none(type=type_name)
            if new_type:
                flash("Такой тип уже существует. Введите другое название типа")
                return redirect(request.url)
            new_type = Type.create(type=type_name)
            new_type.save()
        return redirect(request.url)
