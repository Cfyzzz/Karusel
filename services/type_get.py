from model import Type, Component, Package
from .iservise import *
from peewee import DoesNotExist


class TypeGetService(IService):
    def run(self):
        type_id = self.params.get('type_id', None)
        if type_id is None:
            return abort(404)

        components = self.get_components(type_id)
        if components:
            type_component = self.get_type_by_id(type_id)
            packages = self.get_packages(type_component)
            return render_template('components.html', components=components, type_comp=type_component, packages=packages)
        return abort(404)

    @staticmethod
    def get_components(type_id: int):
        """ Получить компонеты согласно id типу

        :param type_id - идентификатор id типа
        """
        try:
            type_comp = Type.get_by_id(type_id)
            return Component.select().where(Component.type == type_comp)
        except DoesNotExist:
            return []

    @staticmethod
    def get_type_by_id(type_id: int):
        return Type.get_or_none(Type.id == type_id)

    @staticmethod
    def get_packages(type_component: Type):
        return Package.select().where(Package.type == type_component)
