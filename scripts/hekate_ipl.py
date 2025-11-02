from basemodule import BaseModule


class HekateIpl(BaseModule):
    def __init__(self):
        BaseModule.__init__(self)

    def handle_module(self):
        self.out["hekate_ipl.ini"] = "https://raw.githubusercontent.com/exploitz86/nx-links/master/resources/hekate_ipl.ini"