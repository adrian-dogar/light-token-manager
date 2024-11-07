import json
import yaml
import os.path
import time
from threading import Lock
import hashlib
import requests

class LightTokenManager:
    def __init__(self, token_url, client_id=None, client_secret=None, scope=None, grant_type=None, local_storage=None, payload_format="form", body=None):
        self.token_url = token_url
        self.token = None
        self.expires_at = 0
        self.body = body if body else {}
        if client_id:
            self.body['client_id'] = client_id
        if client_secret:
            self.body['client_secret'] = client_secret
        if scope:
            self.body['scope'] = scope
        if grant_type:
            self.body['grant_type'] = grant_type

        self.lock = Lock()
        self.local_storage = local_storage if local_storage else f"{self.unique_id()}_token.json"
        self.payload_format = payload_format

    def _load_token_from_file(self):
        if os.path.exists(self.local_storage):
            with open(self.local_storage, 'r') as file:
                try:
                    data = json.load(file)
                    self.token = data['access_token']
                    self.expires_at = data['expires_at']
                except (json.JSONDecodeError, KeyError):
                    self.token = None
                    self.expires_at = 0

    def _save_token_to_file(self):
        with open(self.local_storage, 'w') as file:
            data  = {'access_token': self.token, 'expires_at': self.expires_at}
            json.dump(data, file)

    def _refresh_token(self):
        if self.payload_format == "form":
            self._refresh_token_form()
        elif self.payload_format == "json":
            self._refresh_token_json()
        elif self.payload_format == "yaml":
            self._refresh_token_yaml()
        else:
            raise ValueError("Invalid payload format")

    def _refresh_token_form(self):
        response = requests.post(self.token_url, data=self.body)
        response.raise_for_status()
        token_data = response.json()
        self.token = token_data['access_token']
        self.expires_at = time.time() + token_data['expires_in']
        self._save_token_to_file()

    def _refresh_token_json(self):
        response = requests.post(
            self.token_url,
            headers={'Content-Type': 'application/json'},
            data=json.dumps(self.body)
        )
        response.raise_for_status()
        token_data = response.json()
        self.token = token_data['access_token']
        self.expires_at = time.time() + token_data['expires_in']
        self._save_token_to_file()

    def _refresh_token_yaml(self):
        response = requests.post(
            self.token_url,
            headers={'Content-Type': 'application/yaml'},
            data=yaml.safe_dump(self.body)
        )
        response.raise_for_status()
        token_data = response.json()
        self.token = token_data['access_token']
        self.expires_at = time.time() + token_data['expires_in']
        self._save_token_to_file()

    def get_token(self):
        with self.lock:
            self._load_token_from_file()
            if self.token is None or self.expires_at - 60 < time.time():
                self._refresh_token()
            return self.token

    def unique_id(self):
        unique_string = f"{self.token_url}::{json.dumps(self.body)}"
        return hashlib.sha256(unique_string.encode()).hexdigest()[:16]
