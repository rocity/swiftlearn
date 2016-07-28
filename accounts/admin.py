from django.contrib import admin
from .models import Account, ConfirmationKey


admin.site.register(Account)
admin.site.register(ConfirmationKey)