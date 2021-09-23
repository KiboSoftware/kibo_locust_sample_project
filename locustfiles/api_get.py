from locust import HttpUser, task, between, tag
from locust import events
import random
import copy
import re
import json
import uuid
import csv
from datetime import datetime, timedelta
import logging
from common import Auth, Env
proxies = {
    #    "http": "http://localhost:8866",
    # "https": "http://localhost:8866"
}
logger = logging.getLogger(__name__)


class SearchApi(HttpUser):
    wait_time = between(.3, 5)

    @events.init.add_listener
    def on_locust_init(environment, **kwargs):
        environment.env = Env(environment)
        environment.auth = Auth(environment.env)

    @ task(10)
    def get_api(self):
        api = self.random_api()
        self.client.get(
            api[0],
            name=api[1],
            proxies=proxies)

    def random_api(self):
        return random.choice(self.environment.env.apis)


# https://t29864-s49542.stg1.mozu.com
