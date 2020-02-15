import os
import sys
from os.path import join, isdir
import subprocess
import requests
from constants import OUTPUT_DIR, URL_EXTENSION_API, CMD_LIST_EXTENSIONS, CMD_VSCODE_VERSION, EXTENSION_PATTERN


class VSCodeExtensions:
    def __init__(self):
        self._list_extensions = []

    @property
    def _is_vscode_installed(self):
        _is_vscode_installed_cache_var_name = '_is_vscode_installed_cache'
        if hasattr(self, _is_vscode_installed_cache_var_name):
            return getattr(self, _is_vscode_installed_cache_var_name)
        try:
            _ = subprocess.check_output(CMD_VSCODE_VERSION)
            setattr(self, _is_vscode_installed_cache_var_name, True)
            return True
        except subprocess.CalledProcessError:
            setattr(self, _is_vscode_installed_cache_var_name, False)
            return False

    def get_list_installed_extensions(self, from_cache=False):
        if not self._is_vscode_installed:
            print("[!] VSCode is NOT installed on system.", file=sys.stdou)
            return []
        if from_cache and self._list_extensions:
            return self._list_extensions
        result = subprocess.check_output(CMD_LIST_EXTENSIONS)
        self._list_extensions = result.strip().decode().split('\n')
        return self._list_extensions
