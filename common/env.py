import json
import re
from os import path
import csv


class Env():
    def __init__(self, environment):
        self.host = re.search(r".*\/\/([^\/:]+)", environment.host)[1].lower()
        with open('datafiles/{}/env.json'.format(self.host), 'r') as f:
            self.json = json.load(f)
        self.auth_server = self.json['auth_server']
        self.app_id = self.json['app_id']
        self.app_secret = self.json['app_secret']
        self.ship_to = self.json['ship_to']
        self.payments = self.json['payments']

        self.terms = []
        csv_file = 'datafiles/{}/terms.csv'.format(self.host)
        if path.exists(csv_file):
            with open(csv_file, 'r') as csvfile:
                csvreader = csv.reader(csvfile)
                next(csvreader, None)
                for row in csvreader:
                    self.terms.append(row[0])

        self.suggest_terms = []
        csv_file = 'datafiles/{}/suggest_terms.csv'.format(self.host)
        if path.exists(csv_file):
            with open(csv_file, 'r') as csvfile:
                csvreader = csv.reader(csvfile)
                next(csvreader, None)
                for row in csvreader:
                    self.suggest_terms.append(row[0])

        self.content = []
        csv_file = 'datafiles/{}/content.csv'.format(self.host)
        if path.exists(csv_file):
            with open(csv_file, 'r') as csvfile:
                csvreader = csv.reader(csvfile)
                next(csvreader, None)
                for row in csvreader:
                    self.content.append(row[0])

        self.products = []
        csv_file = 'datafiles/{}/products.csv'.format(self.host)
        if path.exists(csv_file):
            with open(csv_file, 'r') as csvfile:
                csvreader = csv.reader(csvfile)
                next(csvreader, None)
                for row in csvreader:
                    self.products.append(row)

        self.users = []
        csv_file = 'datafiles/{}/users.csv'.format(self.host)
        if path.exists(csv_file):
            with open(csv_file, 'r') as csvfile:
                csvreader = csv.reader(csvfile)
                next(csvreader, None)
                for row in csvreader:
                    self.users.append(row)

        self.apis = []
        csv_file = 'datafiles/{}/apis.csv'.format(self.host)
        if path.exists(csv_file):
            with open(csv_file, 'r') as csvfile:
                csvreader = csv.reader(csvfile)
                next(csvreader, None)
                for row in csvreader:
                    if len(row) == 1:
                        row.push('')
                    if len(row[1]) == 0:
                        name = 'unknown'
                        url = row[0].lower()
                        if "cart" in url:
                            name = 'cart'
                        elif "entitylists" in url:
                            name = 'entitylists'
                        elif "locations" in url:
                            name = 'locations'
                        elif "catalog/storefront/products" in url:
                            name = 'product'
                        elif "productsearch/suggest" in url:
                            name = 'product'
                        elif "categories/tree" in url:
                            name = 'category_tree'
                        row[1] = name
                    self.apis.append(row)
