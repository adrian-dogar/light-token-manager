import json
import os.path
import time
from threading import Lock

import requests


class LightTokenManager:
    def __init__(self, token_url, client_id, client_secret, scope, grant_type, local_storage='tokens.json'):
        self.token_url = token_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.scope = scope
        self.grant_type = grant_type
        self.local_storage = local_storage
        self.token = None
        self.expires_at = 0
        self.lock = Lock()

    def get_token(self):
        with self.lock:
            self._load_token_from_file()
            if self.token is None or self.expires_at - 60 < time.time():
                self._refresh_token()
            return self.token

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

    def _refresh_token(self):
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'scope': self.scope,
            'grant_type': self.grant_type,
        }
        response = requests.post(self.token_url, data=data)
        response.raise_for_status()
        token_data = response.json()
        self.token = token_data['access_token']
        self.expires_at = time.time() + token_data['expires_in']
        self._save_token_to_file()

    def _save_token_to_file(self):
        with open(self.local_storage, 'w') as file:
            json.dump({'access_token': self.token, 'expires_at': self.expires_at}, file)