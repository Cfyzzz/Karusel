from flask import *


class IService:
    def __init__(self, the_request: Request, **params):
        self.request = the_request
        self.params = params

    def run(self):
        abort(404)
