"""This module sends HTTP request to a server."""
import requests
import json
from typing import Optional


class HttpRequest:
    """A class representing HTTP request.

    :param url: Request url.
    :type url: str
    :param type: Request method. Either 'get or 'post', defaults to 'get'.
    :type type: str, optional
    :param payload: Payload to use in POST method, defaults to None.
    :type payload: Optional[str], optional
    """

    headers = {
        'User-Agent':
            ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
             'AppleWebKit/537.36 (KHTML, like Gecko) '
             'Chrome/94.0.4606.81 Safari/537.36')
    }

    def __init__(self, url: str, type: str = 'get',
                 payload: Optional[str] = None) -> None:
        self.url = url
        self.type = type
        self.payload = payload
        self.data = self.request_json()

    def request_json(self) -> dict:
        """Sends HTTP request to a server .

        :return: Response data.
        :rtype: dict
        """
        if self.type == 'get':
            res = requests.get(self.url, headers=HttpRequest.headers)
        elif self.type == 'post':
            res = requests.post(self.url,
                                headers=HttpRequest.headers,
                                json=self.payload)

        if res.status_code != 200:
            res.raise_for_status()

        json_data = json.loads(res.text)

        return json_data
