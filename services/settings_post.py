import tools
from .iservise import *


class SettingsPostService(IService):
    def run(self):
        host = self.request.form.get('host')
        port = self.request.form.get('port')
        tools.set_url_karusel(f"http://{host}:{port}")
        return redirect(self.request.url)
