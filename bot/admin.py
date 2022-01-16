from django.contrib import admin
from django.db.models import QuerySet

from bot.models import Bot


@admin.register(Bot)
class BotAdmin(admin.ModelAdmin):
    change_form_template = 'admin/change_bot_form.html'
    actions = ['reset_webhook']

    @admin.action(description="Re set webhook")
    def reset_webhook(self, request, queryset: QuerySet[Bot]):
        for bot in queryset:
            bot.set_webhook()
        self.message_user(request, "Webhook reset successfully")
