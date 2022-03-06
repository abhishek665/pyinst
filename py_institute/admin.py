from django.contrib import admin
from .models import MyUsers, Contact, UserDeviceInfo, IP

# Register your models here

admin.site.register(MyUsers)
admin.site.register(Contact)
admin.site.register(UserDeviceInfo)
admin.site.register(IP)