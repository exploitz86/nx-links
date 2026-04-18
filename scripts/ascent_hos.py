from basemodule import BaseModule
import re


class AscentHos(BaseModule):
    def __init__(self):
        self.output_section = "cfws"
        self.config = [
            {
                "username": "exploitz86",
                "reponame": "Ascent"
            }
        ]
        BaseModule.__init__(self)

    def handle_module(self):
        release = self.get_latest_release(0)
        if release is None:
            return

        body = release.body or ""
        match = re.search(
            r"^\s*Latest supported HOS:\s*([0-9]+(?:\.[0-9]+){1,3})\s*$",
            body,
            re.MULTILINE | re.IGNORECASE
        )
        if match:
            self.out["Ascent_Supported_HOS"] = match.group(1)
