from model import Type, Package
from .iservise import *


class AppendGetService(IService):
    def run(self):
        types = Type.select()
        packages = Package.select()
        return render_template('append.html', types=types, packages=packages)
