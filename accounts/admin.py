from django.contrib import admin
from .models import (
    Account,
    ConfirmationKey,
    Skill,
    AccountCompletionTask,
    Education,
    Badge,
    BadgeCriteria,
    Transaction,
    Conversation,
    Message
)


admin.site.register(Account)
admin.site.register(Skill)
admin.site.register(ConfirmationKey)
admin.site.register(AccountCompletionTask)
admin.site.register(Education)
admin.site.register(Badge)
admin.site.register(BadgeCriteria)
admin.site.register(Transaction)
admin.site.register(Conversation)
admin.site.register(Message)
