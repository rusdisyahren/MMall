from django.contrib import admin
from .models import *

admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(CartItem)
