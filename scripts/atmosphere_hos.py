from basemodule import BaseModule
import re


class AtmosphereHos(BaseModule):
    def __init__(self):
        self.output_section = "cfws"
        self.config = [
            {
                "username": "Atmosphere-NX",
                "reponame": "Atmosphere"
            }
        ]
        BaseModule.__init__(self)

    def handle_module(self):
        release = self.get_latest_release(0)
        if release is None:
            return

        body = release.body or ""
        match = re.search(
            r"support was added for ([0-9]+(?:\.[0-9]+){1,3})\.",
            body,
            re.IGNORECASE
        )
        if match:
            self.out["Atmosphere_Supported_HOS"] = match.group(1)
        else:
            self.out["Atmosphere_Supported_HOS"] = "Unknown"
