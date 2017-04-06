"""Supplements to the arcgis package.
"""

from __future__ import (
    unicode_literals, print_function, division, absolute_import)

import json
import re
from time import sleep
from datetime import datetime
import requests

_DEFAULT_ROOT_URI = "https://www.arcgis.com/sharing/rest/"


class JobFailureError(Exception):
    """Thrown when a job on a GIS server has failed.
    """

    def __init__(self, status_response):
        """Creates new instance.
        """
        self.status_response = status_response
        super().__init__()


class TokenError(Exception):
    """An error that occurs while requesting a token.
    """
    def __init__(self, info: dict):
        self.error_info = info
        super().__init__()


class TokenManager(object):
    """Class that manages tokens.
    """

    def _request_token(self):
        """Requests a new token
        """
        response = requests.post(
            "%s/generateToken" % self.root_uri.rstrip("/"), {
                "username": self.username,
                "password": self.password,
                "expiration": '60',
                "referer": 'https://wsdot.maps.arcgis.com',
                "f": 'json'
            })

        token_info = response.json()
        if "error" in token_info:
            raise TokenError(token_info["error"])
        self._token = token_info["token"]
        self._expires = datetime.fromtimestamp(token_info["expires"] / 1000)

    def __init__(self, username, password, referrer, expiration=60,
                 root_uri=_DEFAULT_ROOT_URI):
        """Initializes the class and requests a token.
        """
        self.username = username
        self.password = password
        self.expiration = expiration
        self.referrer = referrer
        self.root_uri = root_uri
        self._token = None
        self._request_token()

    @property
    def token(self):
        """Returns the token, first making a request for a new token if the
        current one has expired.
        """
        if not self._token or self._expires <= datetime.now():
            self._request_token()
        return self._token


def export(item_id: str, root_uri: str,
           token_manager: TokenManager,
           result_item_id: str=None,
           export_format: str="Feature Collection",
           overwrite: bool=True,
           sleep_interval_in_seconds: int=2):
    """
    See http://resources.arcgis.com/en/help/arcgis-rest-api/index.html#/Export_Item/02r30000008s000000/
    """

    token = token_manager.token

    username = token_manager.username

    def get_status(item_id: str, job_id: str):
        """Checks on the status of a job.
        """
        url = "%s/content/users/%s/items/%s/status/" % (
            root_uri, username, item_id)
        data = {
            "token": token,
            "jobType": "export",
            "jobId": job_id,
            "f": "json"
        }
        status_request = requests.post(url, data=data)
        return status_request.json()

    data = {
        "itemId": item_id,
        "exportFormat": export_format,
        "resultItemId": result_item_id,
        "overwrite": overwrite,
        "f": "json",
        "token": token
    }

    export_request = requests.post(
        "%s/content/users/%s/export" % (root_uri, username), data=data)
    export_response = export_request.json()

    # response
    # type              The type of the resulting item.
    # size              The size of the resulting item.
    # jobId             The job ID of the export job.
    # exportItemId      The ID of the result item of the export.
    # serviceItemId     The ID of the service item that was exported.
    # exportFormat      The format of the export.

    item_id = export_response["exportItemId"]
    job_id = export_response["jobId"]

    # Continually check on status until job has completed.
    status = "processing"
    done_re = re.compile("^((?:failed)|(?:completed))$", re.IGNORECASE)
    while not done_re.match(status):
        status_response = get_status(item_id, job_id)
        print(status_response)
        status = status_response["status"]
        match = done_re.match(status)
        if match:
            if re.match("failed", status, re.IGNORECASE):
                raise JobFailureError(status_response)
            elif re.match("completed", status, re.IGNORECASE):
                break
        sleep(sleep_interval_in_seconds)

    return True
