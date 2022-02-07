from model import Package
from .iservise import *


class ListPackagesGetService(IService):
    def run(self):
        packages = self.get_all_packages()
        return render_template('packages.html', packages=packages)

    @staticmethod
    def get_all_packages():
        """ Получить все корпуса компонентов

        :return Список корпусов компонентов """
        return Package.select()
