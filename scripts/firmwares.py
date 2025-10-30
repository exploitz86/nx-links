""" 
import internetarchive as ia
import re
from basemodule import BaseModule
import urllib.parse

class Firmwares(BaseModule):
    def __init__(self):
        self.collections = [
            {"title": "nintendo-switch-global-firmwares", "prefix": ""},
            {"title": "nintendo-switch-china-firmwares",
                "prefix": "[China Firmware] "}
        ]
        self.url = "https://archive.org/download/"
        BaseModule.__init__(self)

    def sort_firmwares(self, file):
        match = re.match(r"Firmware ([\d\.]+).*\.zip", file["name"])
        res = 0
        if match:
            ver = match[1].split(".")
            for i in range(len(ver)):
                res += (100**(len(ver) - 1 - i)) * int(ver[i])
        else:
            res = 0
        return res

    def handle_module(self):
        for collection in self.collections:
            item = ia.get_item(collection["title"])
            #files = sorted(item.files, key=lambda d: d.get("mtime", "0"), reverse=True)
            files = sorted(item.files, key=self.sort_firmwares, reverse=True)
            for file in files:
                match = re.match(r"(Firmware.+)\.zip", file["name"])
                if match:
                    download = self.url + \
                        collection["title"] + "/" + file['name']
                    self.out[collection["prefix"] + match[1]
                             ] = urllib.parse.quote(download, safe=":/")
"""

from basemodule import BaseModule
from github import Github, GithubException
import re

class Firmwares(BaseModule):
    def __init__(self):
        self.repo_owner = "THZoria"
        self.repo_name = "NX_Firmware"
        self.limit = 10  # Increased limit since GitHub releases are more reliable
        BaseModule.__init__(self)

    def sort_firmware_versions(self, release):
        """Sort firmware releases by version number (newest first)"""
        # Extract version from tag_name or name (e.g., "v18.1.0" -> "18.1.0")
        version_match = re.search(r'(\d+)\.(\d+)\.(\d+)', release.tag_name or release.name)
        if version_match:
            major, minor, patch = map(int, version_match.groups())
            # Create sortable version number (higher = newer)
            return (major * 10000) + (minor * 100) + patch
        return 0

    def handle_module(self):
        try:
            # Use GitHub API to get releases (use token from basemodule args)
            from basemodule import args
            gh = Github(args.githubToken)
            repo = gh.get_repo(f"{self.repo_owner}/{self.repo_name}")
            
            # Get all releases and sort by version
            releases = list(repo.get_releases())
            releases.sort(key=self.sort_firmware_versions, reverse=True)
            
            # Limit to recent releases
            recent_releases = releases[:self.limit] if len(releases) > self.limit else releases
            
            for release in recent_releases:
                # Look for Firmware.*.zip files in release assets
                for asset in release.get_assets():
                    if re.match(r"Firmware.*\.zip", asset.name):
                        # Extract firmware version/name from filename
                        firmware_match = re.match(r"(Firmware.*)\.zip", asset.name)
                        if firmware_match:
                            firmware_name = firmware_match.group(1)
                            # Add to output with GitHub download link
                            self.out[f"[GitHub] {firmware_name}"] = asset.browser_download_url
                            
        except GithubException as e:
            print(f"GitHub API error fetching firmwares from {self.repo_owner}/{self.repo_name}: {e}")
            # Fallback: continue without firmware data rather than crash
        except Exception as e:
            print(f"Error fetching firmwares from GitHub: {e}")
            # Fallback: continue without firmware data rather than crash