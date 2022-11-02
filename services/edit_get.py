from peewee import DoesNotExist

from model import Component, Package
from .iservise import *


class EditGetService(IService):
    def run(self):
        component_id = self.request.args.get('id', None)
        if component_id is None or not component_id.isdigit():
            return abort(404)

        component: Component = self.get_component(int(component_id))
        if component is None:
            return abort(404)

        component_package = component.package
        component_package_package = Package.package.null
        if component_package:
            component_package_package = component_package.package
        packages = [component.package]
        packages.extend(Package.select().where(Package.package != component_package_package))
        return render_template('append.html',
                               types=[component.type],
                               packages=packages,
                               component=component
                               )

    @staticmethod
    def get_component(component_id: int) -> [Component, None]:
        """ Получить компонет согласно его id

        :param component_id - идентификатор id типа
        :return Component - компонент с id равным component_id или None
        """
        try:
            return Component.get_by_id(component_id)
        except DoesNotExist:
            return
