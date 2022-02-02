import requests
from peewee import DoesNotExist

import tools
from model import Component, Type
from .iservise import *


class ListTypesPostService(IService):
    def run(self):
        try:
            type_component = Type.get_by_id(self.request.form.get('typeId'))
        except DoesNotExist:
            flash("Что-то пошло не так. Компонент не найден")
            return redirect(request.url)
        url_edit = tools.get_base_url() + "/types/" + type_component.type
        return redirect(url_edit)
