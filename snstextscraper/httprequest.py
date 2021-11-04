import requests
import json
from fake_useragent import UserAgent
from typing import Optional


class HttpRequest:

    def __init__(self, url: str, type: str = 'get',
                 payload: Optional[str] = None) -> None:
        self.url = url
        self.type = type
        self.payload = payload
        self.data = self.request_json()

    def request_json(self) -> dict:
        ua = UserAgent()
        headers = {
            'User-Agent': ua.chrome,
        }

        if self.type == 'get':
            res = requests.get(self.url, headers=headers)
        elif self.type == 'post':
            res = requests.post(self.url,
                                headers=headers,
                                json=self.payload)

        if res.status_code != 200:
            res.raise_for_status()

        json_data = json.loads(res.text)

        return json_data
