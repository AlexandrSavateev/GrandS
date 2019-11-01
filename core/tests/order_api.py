#!/usr/bin/env python3
import requests
import json
from pprint import pprint
from datetime import datetime, timedelta


def req(func):
    def res(*args, **kwargs):
        print('\n*** ' + func.__name__.upper() + ' ***\n')
        r = func(*args, **kwargs)
        pprint('STATUS {}'.format(r.status_code))
        if r.text:
            pprint(json.loads(r.text))
        r.raise_for_status()
        return r
    return res


phone = '+375449880970'
email = 'eshudel@mail.ru'
password = '12345678ABC'
new_password = '12345678ABC'


@req
def login():
    url = 'http://localhost:8000/api/rest-auth/login/'
    json = {
        'phone': phone,
        'password': password
    }
    return requests.post(url=url, json=json)

@req
def create_order(token):
    url = 'http://localhost:8000/api/orders/'
    headers = {'Authorization': 'JWT {}'.format(token)}
    json = {
        'started_at': (datetime.now() + timedelta(hours=3)).strftime("%Y-%m-%dT%H:%M:%S"),
        'ended_at': (datetime.now() + timedelta(hours=5)).strftime("%Y-%m-%dT%H:%M:%S")
    }
    return requests.post(url=url, headers=headers, json=json)

@req
def get_order(token):
    url = 'http://localhost:8000/api/orders/1/'
    headers = {'Authorization': 'JWT {}'.format(token)}
    return requests.get(url=url, headers=headers)


@req
def get_all_orders(token):
    url = 'http://localhost:8000/api/orders/'
    headers = {'Authorization': 'JWT {}'.format(token)}
    return requests.get(url=url, headers=headers)


@req
def get_orders(token):
    url = 'http://localhost:8000/api/orders/search/'
    headers = {'Authorization': 'JWT {}'.format(token)}
    json = {
        'filter': {
            'is_confirm': False,
            'is_closed': False,
            # 'id': 2,
        },
        'sort': ['-price', 'is_confirm', 'is_closed', 'abc', '-is_confirm']
    }
    return requests.post(url=url, headers=headers, json=json)


@req
def update_order(token):
    url = 'http://localhost:8000/api/orders/1/'
    headers = {'Authorization': 'JWT {}'.format(token)}
    json = {
        'is_closed': True,
    }
    return requests.patch(url=url, headers=headers, json=json)


@req
def create_point(token, order_id):
    url = 'http://localhost:8000/api/orders/' + str(order_id) + '/points/'
    headers = {'Authorization': 'JWT {}'.format(token)}
    p = {
        'latitude': 0.000002,
        'longitude': 0.000001,
    }
    points = [p for _ in range(2)]
    return requests.post(url=url, headers=headers, json=points)


@req
def create_tech(token, order_id):
    url = 'http://localhost:8000/api/orders/' + str(order_id) + '/technics/'
    headers = {'Authorization': 'JWT {}'.format(token)}
    p = {
        # 'category': 3,
        # 'subtypes': [1],
        'tech_type': 1,
    }
    return requests.post(url=url, headers=headers, json=p)


@req
def order_confirm(token, order_id):
    url = 'http://localhost:8000/api/orders/' + str(order_id) + '/confirm/'
    headers = {'Authorization': 'JWT {}'.format(token)}
    return requests.post(url=url, headers=headers)


if __name__ == '__main__':
    # r = login()
    # token = r.json()['token']
    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyLCJ1c2VybmFtZSI6IiszNzU0NDk4ODA5NzAiLCJleHAiOjE1NDQzMDcwOTYsImVtYWlsIjoiZ2VnZGhlbEBtYWlsLnJ1IiwicGhvbmUiOiIrMzc1NDQ5ODgwOTcwIn0.CfM_RV885pj1sCOflcYMO9jYys78oLe5QQhd7B102kk"
    # create_order(token)
    # create_point(token, 3)
    # update_order(token)
    # get_order(token)
    # create_tech(token, 3)
    # get_orders(token)
    order_confirm(token, 3)
