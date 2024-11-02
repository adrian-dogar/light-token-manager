import json
import os.path
import time
from threading import Lock
import hashlib
import requests

class LightTokenManager:
    def __init__(self, token_url, client_id, client_secret, scope, grant_type, local_storage=None):
        self.token_url = token_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.scope = scope
        self.grant_type = grant_type
        self.token = None
        self.expires_at = 0
        self.lock = Lock()
        self.local_storage = local_storage if local_storage else f"{self.unique_id()}_token.json"

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

    def get_token(self):
        with self.lock:
            self._load_token_from_file()
            if self.token is None or self.expires_at - 60 < time.time():
                self._refresh_token()
            return self.token

    def unique_id(self):
        unique_string = f"{self.token_url}::{self.client_id}::{self.scope}::{self.grant_type}"
        return hashlib.sha256(unique_string.encode()).hexdigest()[:16]
