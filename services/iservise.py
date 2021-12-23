from flask import *


class IService:
    def __init__(self, the_request: Request):
        self.request = the_request

    def run(self):
        abort(404)
