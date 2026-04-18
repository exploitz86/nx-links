from basemodule import BaseModule


class Payloads(BaseModule):
    def __init__(self):
        self.config = [
            {
                "username": "Atmosphere-NX",
                "reponame": "Atmosphere",
                "assetPatterns": [".*fusee.*\\.bin"]
            },
            {
                "username": "Atmosphere-NX",
                "reponame": "Atmosphere",
                "prerelease": True,
                "assetPatterns": [".*fusee.*\\.bin"]
            },
            {
                "username": "Kofysh",
                "reponame": "Lockpick_RCM",
                "prerelease": True,
                "assetPatterns": [".*Lockpick_RCM\\.bin$"]
            },
            {
                "username": "suchmememanyskill",
                "reponame": "TegraExplorer",
                "prerelease": True,
                "assetPatterns": [".*TegraExplorer.*\\.bin"]
            }
        ]
        BaseModule.__init__(self)
