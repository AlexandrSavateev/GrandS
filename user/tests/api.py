#!/usr/bin/env python3
import requests
import json
from pprint import pprint


def req(func):
    def res(*args, **kwargs):
        r = func(*args, **kwargs)
        pprint('STATUS {}'.format(r.status_code))
        if r.text:
            pprint(json.loads(r.text), width=1)
        r.raise_for_status()
        return r
    return res


phone = '+375449880970'
email = 'gegdhel@mail.ru'
password = '12345678ABC'
new_password = '12345678ABC'


def reg_client_private():
    print('reg_client_private \n')
    url = 'http://localhost:8000/api/rest-auth/registration/client/private/'
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

@req
def reg_dispatcher():
    print('reg_dispatcher \n')
    url = 'http://localhost:8000/api/rest-auth/registration/dispatcher/'
    json = {
        'phone': phone,
        'email': email,
        'password1': password,
        'password2': password
    }
    return requests.post(url=url, json=json)


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


def password_recovery_email():
    print('password_recovery_email \n')
    url = 'http://localhost:8000/api/rest-auth/password/reset/'
    json = {
        'email': 'e.dsf@jlsdkkk.dd'
    }
    r = requests.post(url=url, json=json)
    print('{} \n'.format(r.text))
    r.raise_for_status()
    return r 

@req
def password_recovery_sms():
    print('password_recovery_sms  \n')
    url = 'http://localhost:8000/api/rest-auth/send-sms/'
    json = {
        'phone': phone
    }
    r = requests.post(url=url, json=json)
    return r


def password_recovery_confirm(uid, token):
    print('password_recovery_confirm \n')
    url = 'http://localhost:8000/api/rest-auth/password/reset/confirm/'
    json = {
        'uid': uid,
        'token': token,
        'new_password1': new_password,
        'new_password2': new_password
    }
    r = requests.post(url=url, json=json)
    print('{} \n'.format(r.text))
    r.raise_for_status()
    return r 


def get_client_private(token):
    print('get_client_private \n')
    url = 'http://localhost:8000/api/rest-auth/user/client/private/'
    headers = {'Authorization': 'JWT {}'.format(token)}
    r = requests.get(url=url, headers=headers)
    print('{} \n'.format(r.text))
    r.raise_for_status()
    return r


def patch_client_private(token):
    print('patch_client_private \n')
    url = 'http://localhost:8000/api/rest-auth/user/client/private/'
    headers = {'Authorization': 'JWT {}'.format(token)}
    json = {
        'first_name': 'Evgeni',
        'last_name': 'Shudel',
        'address': {
            'city': 'Минск',
            'street': 'Тухачевского'
        },
    }
    r = requests.patch(url=url, headers=headers, json=json)
    print('{} \n'.format(r.text))
    r.raise_for_status()
    return r

@req
def patch_dispatcher(token):
    print('patch_dispatcher \n')
    url = 'http://localhost:8000/api/rest-auth/user/dispatcher/'
    headers = {'Authorization': 'JWT {}'.format(token)}
    json = {
        'email': 'avgeni@s.com',
        'last_name': 'Shudel',
        'organization': {
            'address': {
                'city': 'Минск',
                'street': 'Тухачевского'
            },
            'post_address': {
                'city': 'Минск',
                'street': 'Тухачевского'
            }
        }
    }
    r = requests.patch(url=url, headers=headers, json=json)
    return r


if __name__ == '__main__':
    r = login()
    # r = reg_client_private()
    # r = reg_dispatcher()
    token = r.json()['token']
    # password_recovery_sms()
    # patch_client_private(r.json()['token'])
    # patch_dispatcher(r.json()['token'])
    # logout = logout(login.json()['token'])
    # r = password_recovery_sms()
    # password_recovery_confirm(r.json()['uid'], r.json()['token'])
    # login = login()

