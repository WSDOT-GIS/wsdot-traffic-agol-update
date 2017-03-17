"""Tests for arcgisext
"""
from __future__ import (
    unicode_literals, print_function, division, absolute_import)

import unittest
from os.path import exists
from datetime import datetime
import json
from arcgisext import TokenManager

_LOGIN_JSON_PATH = "login-info.json"


class TestArcGisExt(unittest.TestCase):
    """
    """
    def test_token(self):
        if not exists(_LOGIN_JSON_PATH):
            raise FileNotFoundError(_LOGIN_JSON_PATH)
        with open(_LOGIN_JSON_PATH) as json_file:
            login_info = json.load(json_file)
            username = login_info["username"]
            password = login_info["password"]
        token_manager = TokenManager(
            username, password, 60, "https://wsdot.maps.arcgis.com")
        self.assertGreaterEqual(
            token_manager._expires, datetime.now(),
            "Token expiration should be later than the current time.")
        self.assertTrue(isinstance(token_manager._token, str))


if __name__ == '__main__':
    unittest.main()
