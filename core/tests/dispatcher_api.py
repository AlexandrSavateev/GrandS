#!/usr/bin/env python3
import requests
from pprint import pprint


phone = '+375449876548'
email = 'eshudel@mail.ru'
password = 'sambukubudesh'
new_password = 'sambukubudesh'


def reg_dispatcher():
    print('reg_dispatcher \n')
    url = 'http://localhost:8000/api/rest-auth/registration/dispatcher/'
    json = {
        'phone': phone,
        'email': email,
        'password1': password,
        'password2': password
    }
    r = requests.post(url=url, json=json)
    print('{} \n'.format(r.text))
    r.raise_for_status()
    return r


def login():
    print('Login \n')
    url = 'http://localhost:8000/api/rest-auth/login/'
    json = {
        'phone': phone,
        'password': password
    }
    r = requests.post(url=url, json=json)
    print('{} \n'.format(r.text))
    r.raise_for_status()
    return r


def logout(token):
    print('Logout \n')
    url = 'http://localhost:8000/api/rest-auth/logout/'
    headers = {'Authorization': 'JWT {}'.format(token)}
    r = requests.post(url=url, headers=headers)
    print('{} \n'.format(r.text))
    r.raise_for_status()
    return r

def get_options(token):
    print('Get options \n')
    url = 'http://localhost:8000/api/technics/autos/'
    headers = {'Authorization': 'JWT {}'.format(token)}
    r = requests.options(url=url, headers=headers)
    print('{} \n'.format(r.text))
    r.raise_for_status()
    return r


def get_autos(token):
    print('Get list of Autos \n')
    url = 'http://localhost:8000/api/technics/autos/'
    headers = {'Authorization': 'JWT {}'.format(token)}
    r = requests.get(url=url, headers=headers)
    print('{} \n'.format(r.text))
    r.raise_for_status()
    return r


def get_auto(token, id):
    print('Get Auto by id \n')
    url = 'http://localhost:8000/api/technics/autos/' + str(id) + '/'
    headers = {'Authorization': 'JWT {}'.format(token)}
    r = requests.get(url=url, headers=headers)
    print('{} \n'.format(r.text))
    r.raise_for_status()
    return r


def create_auto(token):
    print('Create Auto \n')
    url = 'http://localhost:8000/api/technics/autos/'
    headers = {'Authorization': 'JWT {}'.format(token)}
    json = {
        'category': 3,
        'model': 'ЗИЛ',
        'number': '1245 KK-6',
        'parking_latitude': 0.000001,
        'parking_longitude': 0.000001
    }
    r = requests.post(url=url, headers=headers, json=json)
    print('{} \n'.format(r.text))
    r.raise_for_status()
    return r


def update_auto(token, id):
    print('Update Auto \n')
    url = 'http://localhost:8000/api/technics/autos/' + str(id) + '/'
    headers = {'Authorization': 'JWT {}'.format(token)}
    json = {
        # 'category': 3,
        'model': 'ЗИЛ2',
        'number': '1245 KK-6',
        'parking_latitude': 0.000002,
        'parking_longitude': 0.000002
    }
    r = requests.put(url=url, headers=headers, json=json)
    print('{} \n'.format(r.text))
    r.raise_for_status()
    return r


def get_drivers(token):
    print('Get Drivers \n')
    url = 'http://localhost:8000/api/technics/drivers/'
    headers = {'Authorization': 'JWT {}'.format(token)}
    r = requests.get(url=url, headers=headers)
    print('{} \n'.format(r.text))
    r.raise_for_status()
    return r


def get_driver(token, id):
    print('Get Driver by id \n')
    url = 'http://localhost:8000/api/technics/drivers/' + str(id) + '/'
    headers = {'Authorization': 'JWT {}'.format(token)}
    r = requests.get(url=url, headers=headers)
    print('{} \n'.format(r.text))
    r.raise_for_status()
    return r


def create_driver(token):
    print('Create Driver \n')
    url = 'http://localhost:8000/api/technics/drivers/'
    headers = {'Authorization': 'JWT {}'.format(token)}
    json = {
        'phone': '+375449886550',
        'first_name': 'Alex',
        'last_name': 'Gavrilov',
        # 'status': 5
    }
    r = requests.post(url=url, headers=headers, json=json)
    print('{} \n'.format(r.text))
    r.raise_for_status()
    return r


def update_driver(token, id):
    print('Update Driver \n')
    url = 'http://localhost:8000/api/technics/drivers/' + str(id) + '/'
    headers = {'Authorization': 'JWT {}'.format(token)}
    json = {
        'phone': '+375449885485',
        'first_name': 'Саша',
        'last_name': 'Афанасьев',
        'status': 5
    }
    r = requests.patch(url=url, headers=headers, json=json)
    print('{} \n'.format(r.text))
    r.raise_for_status()
    return r


if __name__ == '__main__':
    r = login()
    token = r.json()['token']
    # logout = logout(r.json()['token'])
    # r = reg_dispatcher()
    # autos = get_autos(r.json()['token'])
    # auto = update_auto(r.json()['token'], 4)
    # auto = get_auto(r.json()['token'], 2)
    # auto = create_driver(r.json()['token'])
    # drivers = get_drivers(r.json()['token'])
    # create_autos= create_auto(r.json()['token'])
    # get_options(r.json()['token'])
    update_driver(token, 5)
    get_driver(token, 5)
