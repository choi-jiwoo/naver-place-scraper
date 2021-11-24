"""This module sends HTTP request to a server."""
from abc import ABC, abstractmethod
import requests
import json
from typing import Optional


class HttpRequest(ABC):
    """A class representing HTTP request.

    :param url: Request url.
    :type url: str

    """
    
    headers = {
        'User-Agent':
            ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/94.0.4606.81 Safari/537.36')
    }

    def __init__(self, url: str, headers: Optional[str] = None) -> None:
        self.url = url
        if headers is not None:
            self.headers = headers

    @abstractmethod
    def request(self) -> dict:
        """Sends HTTP request to a server."""
        pass


    def _convert_to_dict(self, res: requests.Response) -> dict:
        """Convert JSON response object to dictionary.

        :param res: :class:`Response` object.
        :type res: requests.Response
        :raises :class:`requests.ConnectionError`: HTTP connection failure.
        :return: Response data in dictionary.
        :rtype: dict
        """
        if res.status_code != 200:
            res.raise_for_status()

        json_data = json.loads(res.text)

        return json_data


class Get(HttpRequest):
    """Sends GET request to a server.
    """

    def __init__(self, url: str, headers: Optional[str] = None):
        super().__init__(url, headers)
        self.response = self.request()

    def request(self):
        res = requests.get(self.url, headers=self.headers)
        json_data = self._convert_to_dict(res)
        
        return json_data


class Post(HttpRequest):
    """Sends POST request to a server.

    :param payload: Payload to use in POST method, defaults to None.
    :type payload: Optional[str], optional
    """

    def __init__(self, url: str, headers: Optional[str] = None,
                 payload: Optional[str] = None) -> None:
        super().__init__(url, headers)
        self.payload = payload
        self.response = self.request()
    
    def request(self) -> dict:
        res = requests.post(self.url, headers=self.headers, json=self.payload)
        json_data = self._convert_to_dict(res)
        
        return json_data
