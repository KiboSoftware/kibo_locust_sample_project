from datetime import datetime, timedelta
import requests


class Auth():
    def __init__(self, env):
        self.app_id = env.app_id
        self.app_secret = env.app_secret
        self.auth_server = env.auth_server
        self.token = None
        self.access_token = None
        self.token_exp = datetime.now()

    def get_token(self):
        if datetime.now() >= self.token_exp:
            resp = requests.post(
                '{}/api/platform/applications/authtickets/oauth'.format(
                    self.auth_server),
                data={
                    "client_id": self.app_id,
                    "client_secret": self.app_secret,
                    "grant_type": "client"
                })
            if (resp.status_code > 399):
                raise RuntimeError(resp.text)
            self.token = resp.json()
            self.token_exp = datetime.now(
            ) + timedelta(seconds=self.token["expires_in"])
            self.access_token = self.token['access_token']
        return self.access_token
