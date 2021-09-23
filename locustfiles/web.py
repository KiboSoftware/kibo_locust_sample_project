from locust import HttpUser, task, between, tag
from locust import events
import randomp
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


class Web(HttpUser):
    wait_time = between(.3, 5)

    @events.init.add_listener
    def on_locust_init(environment, **kwargs):
        environment.env = Env(environment)

    @ task(10)
    def anon_user_browse(self):
        self.reset_cookies()
        self.homepage()
        for x in range(3):
            self.suggest()
        self.search()
        self.product_detail()

    @ task(5)
    def anon_user_abandon(self):
        self.reset_cookies()
        self.homepage()
        for x in range(3):
            self.suggest()
        self.search()
        self.product_detail()
        self.add_to_cart()

    @ task(5)
    def login_user_abandon(self):
        self.reset_cookies()
        self.login_in()
        self.homepage()
        for x in range(3):
            self.suggest()
        self.search()
        self.product_detail()
        self.add_to_cart()

    @ task(1)
    def login_user_checkout(self):
        self.reset_cookies()
        self.login_in()
        self.homepage()
        for x in range(3):
            self.suggest()
        self.search()
        self.product_detail()
        self.add_to_cart()
        self.checkout()

    def reset_cookies(self):
        self.client.cookies.clear()

    def homepage(self):
        self.client.get("/",
                        name="HOMEPAGE",
                        proxies=proxies)

    def login_in(self):
        user = self.random_user()
        log_in = {
            "email": user[0],
            "password": user[1]
        }
        self.client.post(
            '/user/login',
            json=log_in,
            name="LOGIN",
            proxies=proxies)

    def suggest(self, term=None):
        if term is None:
            term = self.random_suggest()
        self.client.get(
            '/api/commerce/catalog/storefront/productsearch/suggest?groups=pages,categories&pageSize=9&query={}'.format(
                term),
            name="SUGGEST",
            proxies=proxies)

    def content(self, url=None):
        if url is None:
            url = self.random_content()
        self.client.get(url,
                        name="CONTENT",
                        proxies=proxies)

    def product_detail(self, product=None):
        if product is None:
            product = self.random_product()
        self.client.get(
            '/p/{}'.format(product['productCode']),
            name="PRODUCT_DETAIL",
            proxies=proxies)

    def search(self, term=None):
        if term is None:
            term = self.random_term()
        self.client.get(
            '/search?query={}'.format(term),
            name="SEARCH",
            proxies=proxies)

    def add_to_cart(self, product=None):
        if product is None:
            product = self.random_product()
        cart_item = {
            "product": product,
            "quantity": 1,
            "fulfillmentMethod": "Ship"
        }
        self.client.post('/api/commerce/carts/current/items/',
                         json=cart_item,
                         name="ADD_TO_CART",
                         proxies=proxies)

    def checkout(self):
        fulfillment_info = copy.deepcopy(self.random_ship_to())
        payment = copy.deepcopy(self.random_payment())
        payment['newBillingInfo']['billingContact']['email'] = str(
            random.randint(1, 1000000))+'@test.com'

        resp = self.client.post(
            "/cart/checkout",
            name="CHECKOUT_FROM_CART",
            proxies=proxies)

        url = resp.history[0].headers['location']
        order_id = url.split('/')[-1]
        api_base = '/api/commerce/orders/' + order_id
        self.client.put(
            api_base+'/fulfillmentinfo',
            name="CHECKOUT_SET_ADDRESS",
            json=fulfillment_info,
            proxies=proxies)

        resp = self.client.get(
            api_base+'/shipments/methods',
            proxies=proxies,
            name="CHECKOUT_GET_SHIPPING")
        shipping_method_code = resp.json()[0]['shippingMethodCode']
        fulfillment_info['shippingMethodCode'] = shipping_method_code
        self.client.put(api_base+'/fulfillmentinfo',
                        name="CHECKOUT_SET_SHIPPING",
                        json=fulfillment_info,
                        proxies=proxies)
        total = self.client.get(api_base,
                                name="CHECKOUT_GET_TOTAL",
                                proxies=proxies,).json()['total']
        payment['amount'] = total
        self.client.post(api_base+'/payments/actions',
                         name="CHECKOUT_6",
                         proxies=proxies,
                         json=payment)
        self.client.post(api_base+'/actions',
                         name="CHECKOUT_SUBMIT",
                         proxies=proxies,
                         json={'actionName': 'SubmitOrder'})
        self.client.get(url + '/confirmation',
                        proxies=proxies,
                        name="CHECKOUT_CONFIRMATION")

    def random_product(self):
        line = random.choice(self.environment.env.products)
        return {
            "productCode": line[0],
            "options": []
        }

    def random_content(self):
        return random.choice(self.environment.env.content)

    def random_term(self):
        return random.choice(self.environment.env.terms)

    def random_suggest(self):
        return random.choice(self.environment.env.suggest_terms)

    def random_ship_to(self):
        return random.choice(self.environment.env.ship_to)

    def random_payment(self):
        return random.choice(self.environment.env.payments)

    def random_user(self):
        return random.choice(self.environment.env.users)
