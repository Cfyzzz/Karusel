import tools
from .iservise import *


class SettingsGetService(IService):
    def run(self):
        protocol, host, port = tools.get_url_karusel().split(":")
        parts = host.split(".")
        for idx in range(len(parts)):
            for _ in range(3 - len(parts[idx])):
                parts[idx] += "0" + parts[idx]
        host = ".".join(parts)
        return render_template('settings.html', host=f"{protocol}:{host}", port=port)
