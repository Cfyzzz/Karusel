import tools
from model import Component, Type
from .iservise import *


class ComponentsPostService(IService):
    def run(self):
        # make new component
        if not self.request.json:
            abort(400)

        new_component, _ = tools.new_component(self.request.json)
        if new_component is None:
            abort(400)

        res = jsonify({
            'component': new_component.serialize
        })
        res.status_code = 201
        return res
