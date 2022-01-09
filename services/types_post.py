import requests

import tools
from .iservise import *


class TypesPostService(IService):
    def run(self):
        url_pop = tools.get_base_url() + "/components/pop"
        payload_pop = {'id': self.request.form.get('componentId'), 'quantity': self.request.form.get('num')}
        headers = {'Content-Type': 'application/json'}
        requests.put(url_pop, headers=headers, data=json.dumps(payload_pop, indent=4))
        return redirect(request.url)
