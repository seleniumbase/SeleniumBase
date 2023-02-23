#!/usr/bin/env python3
import json
import os
from selenium.webdriver.chromium.options import ChromiumOptions


class ChromeOptions(ChromiumOptions):
    _session = None
    _user_data_dir = None

    @property
    def user_data_dir(self):
        return self._user_data_dir

    @user_data_dir.setter
    def user_data_dir(self, path):
        """Sets the browser profile folder to use. Creates one if missing."""
        abs_path = os.path.abspath(path)
        self._user_data_dir = os.path.normpath(abs_path)

    @staticmethod
    def _undot_key(key, value):
        """Turn a (dotted key, value) into a proper nested dict."""
        if "." in key:
            key, rest = key.split(".", 1)
            value = ChromeOptions._undot_key(rest, value)
        return {key: value}

    @staticmethod
    def _merge_nested(a, b):
        """Merges b into a, overwriting duplicate leaf values using b."""
        for key in b:
            if key in a:
                if isinstance(a[key], dict) and isinstance(b[key], dict):
                    ChromeOptions._merge_nested(a[key], b[key])
                    continue
            a[key] = b[key]
        return a

    def handle_prefs(self, user_data_dir):
        prefs = self.experimental_options.get("prefs")
        if prefs:
            user_data_dir = user_data_dir or self._user_data_dir
            default_path = os.path.join(user_data_dir, "Default")
            os.makedirs(default_path, exist_ok=True)
            undot_prefs = {}
            for key, value in prefs.items():
                undot_prefs = self._merge_nested(
                    undot_prefs, self._undot_key(key, value)
                )
            prefs_file = os.path.join(default_path, "Preferences")
            try:
                if os.path.exists(prefs_file):
                    with open(
                        prefs_file, encoding="utf-8", mode="r", errors="ignore"
                    ) as f:
                        undot_prefs = self._merge_nested(
                            json.load(f), undot_prefs
                        )
            except Exception:
                pass
            try:
                with open(prefs_file, encoding="utf-8", mode="w") as f:
                    json.dump(undot_prefs, f)
            except Exception:
                pass
            # Remove experimental_options to avoid errors
            del self._experimental_options["prefs"]
        exclude_switches = self.experimental_options.get("excludeSwitches")
        if exclude_switches is not None:
            del self._experimental_options["excludeSwitches"]
        use_auto_ext = self.experimental_options.get("useAutomationExtension")
        if use_auto_ext is not None:
            del self._experimental_options["useAutomationExtension"]

    @classmethod
    def from_options(cls, options):
        o = cls()
        o.__dict__.update(options.__dict__)
        return o
