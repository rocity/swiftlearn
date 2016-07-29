from django.contrib import admin
from .models import Account, ConfirmationKey, Skill, AccountCompletionTask


admin.site.register(Account)
admin.site.register(Skill)
admin.site.register(ConfirmationKey)
admin.site.register(AccountCompletionTask)