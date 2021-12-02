"""This module sends HTTP request to a server."""
from abc import ABC, abstractmethod
import requests
import json
from typing import Optional


class HttpRequest(ABC):
    """A class representing HTTP request.
    """
# 
    def __init__(self, url: str, headers: Optional[str] = None) -> None:
        self.url = url
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

    :param url: Request url.
    :type url: str
    :param headers: HTTP request headers, defaults to None.
    :type headers: Optional[str], optional
    """

    def __init__(self, url: str, headers: Optional[str] = None):
        super().__init__(url, headers)

    def request(self) -> dict:
        res = requests.get(self.url, headers=self.headers)
        json_data = self._convert_to_dict(res)
        
        return json_data


class Post(HttpRequest):
    """Sends POST request to a server.

    :param url: Request url.
    :type url: str
    :param headers: HTTP request headers, defaults to None.
    :type headers: Optional[str], optional
    :param payload: Payload to use in POST method, defaults to None.
    :type payload: Optional[str], optional
    """

    def __init__(self, url: str, payload: dict,
                 headers: Optional[str] = None) -> None:
        super().__init__(url, headers)
        self.payload = payload
    
    def request(self) -> dict:
        res = requests.post(self.url, headers=self.headers, json=self.payload)
        json_data = self._convert_to_dict(res)
        
        return json_data
