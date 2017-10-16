from django.contrib import admin

# Register your models here
from .models import IkeaItem
from .models import Customer

admin.site.register(IkeaItem)
admin.site.register(Customer)
