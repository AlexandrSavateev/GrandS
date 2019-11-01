Objects:
* [<obj: Address>](#obj-address)
* [<obj: Organization>](#obj-organization)
* [<obj: ClientPrivate>](#obj-clientprivate)
* [<obj: Dispatcher>](#obj-dispatcher)
* [<obj: Driver>](#obj-driver)
* [<obj: Auto>](#obj-auto)
* [<obj: Point>](#obj-point)
* [<obj: Image>](#obj-image)
* [<obj: Technics>](#obj-technics)
* [<obj: UnitTech>](#obj-unittech)

# Используемые объекты

## Общие объекты
DATETIME FORMAT: YYYYMMDDThhmmss±hh or YYYY-MM-DDThh:mm:ss±hh

### &lt;obj: Address&gt;
```javascript
{
    id: <pint>,
    country: <str>,
    city: <str>,
    street: <srt>,
    house: <str>,
    housing: <str>,
    office: <str>,
    description: <str>,
}
```

### &lt;obj: Organization&gt;
```javascript
{
    id: <pint>,
    name: <str>,
    unp: <str>,
    address: <obj: Address>,
    post_address: <obj: Address>,
    bank: <str>,
    bank_department: <str>,
    bank_address: <str>,
    bank_bik: <str>,
    contact_org: <str>,
    iban: <str>,
    first_face: <str>,
    acting_on: <str>,
    accountant: <str>,
    contact_person: <str>,
    add_contact: <str>,
    certificate: <url>,
}
```

### <obj: ClientPrivate>
```javascript
{
    id: <pint>,
    phone: <str>,
    email: <string>,
    first_name: <str>
    last_name: <str>,
    patronymic: <str>,
    birth_date: <str(datetime)>,
    image: <url>,
    date_joined: <str(datetime)>,
    date_modified: <str(datetime)>,
    is_staff: <bool>,
    is_superuser: <bool>,
    is_active: <bool>,
    
    person_id: <str>,
    address: <obj: Address>,
}
```

### <obj: ClientLegal>
```javascript
{
    id: <pint>,
    phone: <str>,
    email: <string>,
    first_name: <str>
    last_name: <str>,
    patronymic: <str>,
    birth_date: <str(datetime)>,
    image: <url>,
    date_joined: <str(datetime)>,
    date_modified: <str(datetime)>,
    is_staff: <bool>,
    is_superuser: <bool>,
    is_active: <bool>,
    
    organization: <obj: Organization>,
}
``````

### <obj: Dispatcher>
```javascript
{
    id: <pint>,
    phone: <str>,
    email: <string>,
    first_name: <str>
    last_name: <str>,
    patronymic: <str>,
    birth_date: <datetime>,
    image: <url>,
    date_joined: <str(datetime)>,
    date_modified: <str(datetime)>,
    is_staff: <bool>,
    is_superuser: <bool>,
    is_active: <bool>,
    
    organization: <obj: Organization>,
}
``````

### <obj: Driver>
```javascript
{
    id: <pint>,
    phone: <str>,
    email: <string>,
    first_name: <str>
    last_name: <str>,
    patronymic: <str>,
    birth_date: <str(datetime)>,
    image: <url>,
    date_joined: <str(datetime)>,
    date_modified: <str(datetime)>,
    is_staff: <bool>,
    is_superuser: <bool>,
    is_active: <bool>,
    
    status: <pint>,    # 1 - готов к работе, 2 - заказ принят, 3 - приехал на место выполнения работы/место загрузки,
                       # 4 - выехал на следующую точку, 5 - работа завершена, 6 - вернулся на базу
    dispatcher: <obj: Dispatcher>,
    extra_rating: <dec>,
}
```

### &lt;obj: Auto&gt;
```javascript
{
    id: <pint>,
    category: <obj: Category>,
    driver: <obj: Driver>,
    dispatcher: <obj: Dispatcher>,
    model: <str>,
    number: <str>,
    year: <str>,  
    image: <url>
    description: <str>,
    parking_latitude: <str>,
    parking_longitude: <str>,
    parking_description: <str>,
    road_restriction: <bool>,
    relocation: <bool>,
    is_active: <bool>,
    extra_rating: <dec>,
}
```

### &lt;obj: Point&gt;
```javascript
{
    id: <pint>,
    order: <obj: Order>,
    latitude: <dec>,
    longitude: <dec>
    description: <str>,
}
```

### &lt;obj: Image&gt;
```javascript
{
    id: <pint>,
    order: <obj: Order>,
    image: <url>,
    description: <str>,
}
```

### &lt;obj: Technics&gt;
```javascript
{
    id: <pint>,
    quantity: <int>,          
    category: <obj: Category>,
    order: <obj: Order>
}
```

### &lt;obj: UnitTech&gt;
```javascript
{
    id: <pint>,
    technics: <obj: Technics>,
    auto: <obj: Auto>,
}

```
---

# API
? - необязательное поле
---
When Authorization is required: add to http header 'Authorization': 'JWT <token>'.
Token lifecycle - 24 hours.
---

### POST api/rest-auth/registration/client/private/

Регистрация клиента (физ. лицо)

### POST api/rest-auth/registration/client/legal/

Регистрация клиента (юр. лицо)

### POST api/rest-auth/registration/dispatcher/

Регистрация диспетчера

#### Request

```javascript
{
    phone: <str>,  # +375*********
    email: <str>,
    password1: <str>,
    password2: <str>
}
```

#### Response
status = 201
```javascript
{
    token: <str>,
    user: {
        id: <pint>,
        phone: <str>,
        email: <str>
    },
    sms_code: <str>
}
```
---
### POST api/rest-auth/send-sms/

Отправить смс с кодом для восстановления пароля

#### Request

```javascript
{
    phone: <str>,  # +375*********
}
```
#### Response
status = 200
```javascript
{
    token: <str>,   # for password recovery
    uid: <str>,     # for password recovery
    sms_code: <str>
}
````
---
### POST api/rest-auth/password/reset/

Отправить email для восстановления пароля

#### Request

```javascript
{
    email: <str>
}
```
#### Response
status = 200
```javascript
````
---
### POST api/rest-auth/password/reset/confirm/

Подтверждение сброса пароля

#### Request

```javascript
{
    uid: <str>,
    token: <str>,
    new_password1: <str>,
    new_password2: <str>,
    # uid and token are sent in email after calling api/rest-auth/password/reset/
    # or api/send_sms/
}
```
#### Response
status = 200
```javascript
````
---
### POST api/rest-auth/password/change/
! Authorization is required.
Изменить пароль

#### Request

```javascript
{
    new_password1: <str>,
    new_password2: <str>,
    old_password: <str>,
}
```
#### Response
status = 200
```javascript
````
---
### GET api/rest-auth/user/client/private/
! Authorization is required.

Получить данные клиента (физ.лицо)

#### Response
status = 200
```javascript
{
    <obj: ClientPrivate>
}
```

---
### PUT, PATCH api/rest-auth/user/client/private/
! Authorization is required.

Изменить данные клиента (физ.лицо)

#### Request

```javascript
{
    # from  <obj : ClientPrivate>
    ?'phone', 
    ?'email', 
    ?'first_name',
    ?'last_name', 
    ?'patronymic',
    ?'birth_date', 
    ?'person_id', 
    ?'address', 
    ?'image', 
    ?'personal_id'
}
```

#### Response
status = 200
```javascript
{
    <obj: ClientPrivate>
}
```
---
### GET api/rest-auth/user/client/legal/
! Authorization is required.

Получить данные клиента (юр.лицо)

#### Response
status = 200
```javascript
{
    <obj: ClientLegal>
}
```

---
### PUT, PATCH api/rest-auth/user/client/legal/
! Authorization is required.

Изменить данные клиента (юр.лицо)

#### Request

```javascript
{
    ?'phone', 
    ?'email', 
    ?'image',
    ?'organization': {
        # from <obj: Organization>
        ?'name',
        ?'unp', 
        ?'address': <obj: Address>,
        ?'post_address': <obj: Address>,
        ?'bank', 
        ?'bank_department',
        ?'bank_address', 
        ?'bank_bik', 
        ?'contact_org', 
        ?'iban', 
        ?'first_person', 
        ?'acting_on',
        ?'accountant', 
        ?'contact_person', 
        ?'add_contact', 
        ?'certificate'
    }
}
```

#### Response
status = 200
```javascript
{
    <obj: ClientLegal>
}
```
---
### GET api/rest-auth/user/dispatcher/
! Authorization is required.

Получить данные диспетчера

#### Response
status = 200
```javascript
{
    <obj: Dispatcher>
}
```
---
### PUT, PATCH api/rest-auth/user/dispatcher/
! Authorization is required.

Изменить данные диспетчера

#### Request

```javascript
{
    ?'phone', 
    ?'email', 
    ?'image',
    ?'organization': {
        # from <obj: Organization>
        ?'name',
        ?'unp', 
        ?'address': <obj: Address>,
        ?'post_address': <obj: Address>,
        ?'bank', 
        ?'bank_department',
        ?'bank_address', 
        ?'bank_bik', 
        ?'contact_org', 
        ?'iban', 
        ?'first_person', 
        ?'acting_on',
        ?'accountant', 
        ?'contact_person', 
        ?'add_contact', 
        ?'certificate'
    }
}
```

#### Response
status = 200
```javascript
{
    <obj: Dispatcher>
}
```

---
### POST api/rest-auth/login/

Вход пользователя (клиент, диспетчер или водитель)

#### Request

```javascript
{
    ?'phone': <str>, 
    ?'email': <str>, 
    'password',
}
```

#### Response
status = 200
```javascript
{
    <obj: Dispatcher>
}
```
---
### POST api/rest-auth/google/client/private/

Вход/регистрация клиента (физ. лицо) с помощью google

### POST api/rest-auth/google/client/legal/

Вход/регистрация клиента (юр. лицо) с помощью google

### POST api/rest-auth/google/dispatcher/

Вход/регистрация диспетчера с помощью google

### POST api/rest-auth/facebook/client/private/

Вход/регистрация клиента (физ. лицо) с помощью google

### POST api/rest-auth/facebook/client/legal/

Вход/регистрация клиента (юр. лицо) с помощью google

### POST api/rest-auth/facebook/dispatcher/

Вход/регистрация диспетчера с помощью google

#### Request

```javascript
{
    'access_token': <str>,
}
```

#### Response
status = 200
```javascript
{
    'token': <str>
}
```
---

### GET api/rest-auth/user/drivers/
! Authorization is required as a dispatcher.

Получить список водителей

#### Response
status = 200
```javascript
{
    [<obj: Driver>, ...]
}
````
---

### POST api/rest-auth/user/drivers/
! Authorization is required as a dispatcher.

Создать пользователя водитель

#### Request

```javascript
{
    is_active: <bool>,
    phone: <str>,
    email: <string>,
    first_name: <str>
    last_name: <str>,
    patronymic: <str>,
    birth_date: <str(datetime)>,
    image: <url>,
}
```

#### Response
status = 200
```javascript
{
    id: <pint>,
    is_active: <bool>,
    phone: <str>,
    email: <string>,
    first_name: <str>
    last_name: <str>,
    patronymic: <str>,
    birth_date: <str(datetime)>,
    image: <url>,
}
````
---

### GET api/rest-auth/user/drivers/<id: int>/
! Authorization is required as a dispatcher.

Получить информацию о водителе

#### Response
status = 200
```javascript
{
    <obj: Driver>
}
````
---

### PUT, PATCH, DELETE api/rest-auth/user/drivers/<id: int>/
! Authorization is required as a dispatcher.

Изменить информацию о водителе

#### Request

```javascript
{
    is_active: <bool>,
    phone: <str>,
    email: <string>,
    first_name: <str>
    last_name: <str>,
    patronymic: <str>,
    birth_date: <str(datetime)>,
    image: <url>,
}
```

#### Response
status = 200
```javascript
{
    <obj: Driver>
}
````
---

### GET api/technics/catalog/

Получить каталог техники (категория -> тип -> подтип)

#### Response
status = 200
```javascript
{
    <obj: Category>
}
````
---

### GET api/technics/autos/
! Authorization is required as a dispatcher.

Получить список техники

#### Response
status = 200
```javascript
{
    [<obj: Auto>, ...]
}
````
---

### POST api/technics/autos/
! Authorization is required as a dispatcher.

Добавить автомобиль

#### Request

```javascript
{
    <obj: Auto>
}
```

#### Response
status = 200
```javascript
{
    <obj: Auto>
}
````
---

### GET api/technics/autos/<id: int>/
! Authorization is required as a dispatcher.

Получить информацию об автомобиле

#### Response
status = 200
```javascript
{
    <obj: Auto>
}
````
---

### PUT, PATCH, DELETE api/technics/autos/<id: int>/
! Authorization is required as a dispatcher.

Изменить информацию об автомобиле

#### Request

```javascript
{
    <obj: Auto>
}
```

#### Response
status = 200
```javascript
{
    <obj: Auto>
}
````
---

### GET api/orders/
! Authorization is required as a client.

Получить список заказов

#### Response
status = 200
```javascript
{
    count: <int>,
    next: <url>,
    previous: <url>,
    results: [<obj: Order>, ...]
}
````
---

### POST api/orders/
! Authorization is required as a client.

Добавить заказ

#### Request
```javascript
{
    started_at: <str(datetime)>,
    ended_at: <str(datetime)>,
    ?description: <str>,
    ?is_closed: <bool>
}
```

#### Response
status = 200
```javascript
{
    id: <pint>,
    started_at: <str(datetime)>,
    ended_at: <str(datetime)>,
    description: <str>,
    is_closed: <bool>
}
````
---

### POST api/orders/search/
! Authorization is required as a client or dispatcher.

Получить список заказов, используя фильтр и условия сортировки.

#### Request
```javascript
{
    ?filter: {
        is_confirm: <bool>,
        is_complete: <bool>,
        is_paid: <bool>,
        is_closed: <bool>,
    },
    ?sort: ["-created_at", "price", ...]
    # sort: list of order object fields; 
    # "-" means descend
}
```

#### Response
status = 200
```javascript
{
    count: <int>,
    next: <url>,
    previous: <url>,
    results: [
        #{
            id: <pint>,
            started_at: <str(datetime)>,
            ended_at: <str(datetime)>,
            description: <str>,
            is_closed: <bool>б
            points: [<obj: Point>, ...],
            technics: [<obj: Technics>, ...], 
            images: [<obj: Images>, ...], 
        }, 
        ...
    ]
}
````
---

### GET api/orders/<id: int>/
! Authorization is required as a client.

Получить информацию о заказе

#### Response
status = 200
```javascript
{
    <obj: Order>
}
````
---

### PUT, PATCH, DELETE api/orders/<id: int>/
! Authorization is required as a client.

Изменить информацию о заказе

#### Request

```javascript
{
    started_at: <str(datetime)>,
    ended_at: <str(datetime)>,
    ?description: <str>,
    ?is_closed: <bool>
}
```

#### Response
status = 200
```javascript
{
    id: <pint>,
    started_at: <str(datetime)>,
    ended_at: <str(datetime)>,
    description: <str>,
    is_closed: <bool>б
    points: [<obj: Point>, ...],
    technics: [<obj: Technics>, ...], 
    images: [<obj: Images>, ...], 
}
````
---

### POST api/orders/points/
! Authorization is required as a client.

Добавить точку/точки заказа.

#### Request
```javascript
{
    order: <pint>, 
    latitude: <dec>, 
    longitude: <dec>,
    ?description: <str>,
}

OR

[
    {
        order: <pint>, 
        latitude: <dec>, 
        longitude: <dec>,
        ?description: <str>,
    },
    ...
]
```

#### Response
status = 200
```javascript
{
    id: <pint>,
    order: <pint>, 
    latitude: <dec>, 
    longitude: <dec>,
    description: <str>,
}

OR

[
    {
        id: <pint>,
        order: <pint>, 
        latitude: <dec>, 
        longitude: <dec>,
        ?description: <str>,
    },
    ...
]
````
---

### POST api/orders/technics/
! Authorization is required as a client.

Добавить тип техники и количество к заказу.

#### Request
```javascript
{
    order: <pint>, 
    category: <pint>, 
    quantity: <pint>,
}

OR

[
    {
        order: <pint>, 
        category: <pint>, 
        quantity: <pint>,
    },
    ...
]
```

#### Response
status = 200
```javascript
{
    id: <pint>,
    order: <pint>, 
    category: <pint>, 
    quantity: <pint>,
}

OR

[
    {
        id: <pint>,
        order: <pint>, 
        category: <pint>, 
        quantity: <pint>,
    },
    ...
]
````
---

### POST api/orders/images/
! Authorization is required as a client.

Добавить изображение/изображения к заказу.

#### Request
```javascript
{
    order: <pint>, 
    description: <str>, 
    image: <file>,
}

OR

[
    {
        order: <pint>, 
        description: <str>, 
        image: <file>,
    },
    ...
]
```

#### Response
status = 200
```javascript
{
    id: <pint>,
    order: <pint>, 
    description: <str>, 
    image: <url>,
}

OR

[
    {
        id: <pint>,
        order: <pint>, 
        description: <str>, 
        image: <url>,
    },
    ...
]
````
