from django.contrib import admin
from .models import (Address, User, ClientLegal, ClientPrivate, Organization, Dispatcher, Driver)


admin.site.register(User)
admin.site.register(Address)
admin.site.register(ClientLegal)
admin.site.register(ClientPrivate)
admin.site.register(Organization)
admin.site.register(Dispatcher)
admin.site.register(Driver)
