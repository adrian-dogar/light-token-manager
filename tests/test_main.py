import unittest
from unittest.mock import patch, mock_open, MagicMock
import time
import json
import os
import logging

from light_token_manager.main import LightTokenManager, unique_id

logging.basicConfig(level=logging.INFO)

class TestLightTokenManager(unittest.TestCase):

    @patch('light_token_manager.main.requests.post')
    def refreshes_token_when_expired(self, mock_post):
        mock_post.return_value.json.return_value = {
            'access_token': 'new_token',
            'expires_in': 3600
        }
        mock_post.return_value.raise_for_status = MagicMock()

        manager = LightTokenManager('http://example.com', 'client_id', 'client_secret', 'scope', 'grant_type')
        manager.expires_at = time.time() - 1  # Token expired
        token, _ = manager.get_token()

        self.assertEqual(token, 'new_token')

    @patch('light_token_manager.main.requests.post')
    def returns_existing_token_if_not_expired(self, mock_post):
        manager = LightTokenManager('http://example.com', 'client_id', 'client_secret', 'scope', 'grant_type')
        manager.token = 'existing_token'
        manager.expires_at = time.time() + 3600  # Token not expired
        token, _ = manager.get_token()

        self.assertEqual(token, 'existing_token')
        mock_post.assert_not_called()

    @patch('light_token_manager.main.os.path.exists', return_value=True)
    @patch('light_token_manager.main.open', new_callable=mock_open, read_data=json.dumps({'access_token': 'file_token', 'expires_at': time.time() + 3600}))
    def loads_token_from_file(self, mock_file, mock_exists):
        manager = LightTokenManager('http://example.com', 'client_id', 'client_secret', 'scope', 'grant_type')
        token, _ = manager.get_token()

        self.assertEqual(token, 'file_token')

    @patch('light_token_manager.main.os.path.exists', return_value=True)
    @patch('light_token_manager.main.open', new_callable=mock_open, read_data='invalid_json')
    def handles_invalid_token_file(self, mock_file, mock_exists):
        manager = LightTokenManager('http://example.com', 'client_id', 'client_secret', 'scope', 'grant_type')
        manager._load_token_from_file()

        self.assertIsNone(manager.token)
        self.assertEqual(manager.expires_at, 0)

    @patch('light_token_manager.main.requests.post')
    @patch('light_token_manager.main.open', new_callable=mock_open)
    def saves_token_to_file(self, mock_file, mock_post):
        mock_post.return_value.json.return_value = {
            'access_token': 'new_token',
            'expires_in': 3600
        }
        mock_post.return_value.raise_for_status = MagicMock()

        manager = LightTokenManager('http://example.com', 'client_id', 'client_secret', 'scope', 'grant_type')
        manager._refresh_token()

        mock_file().write.assert_called_once_with(json.dumps({'access_token': 'new_token', 'expires_at': manager.expires_at}))

    def creates_different_tokens_for_different_providers(self):
        id1 = unique_id('http://example.com', 'client_id_1', 'scope_1', 'grant_type_1')
        id2 = unique_id('http://example.com', 'client_id_2', 'scope_2', 'grant_type_2')

        self.assertNotEqual(id1, id2)

if __name__ == '__main__':
    unittest.main()