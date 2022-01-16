from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from telebot.apihelper import delete_webhook, set_webhook


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-id']


class Bot(BaseModel):
    token = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=120)
    username = models.CharField(max_length=120)

    def __str__(self):
        return self.username

    def set_webhook(self):
        set_webhook(self.token, f"{settings.HOST}/bot/{self.token}/")

    def clean(self):
        try:
            self.set_webhook()
        except:
            raise ValidationError("Could not set webhook. Please check params")


class User(BaseModel):
    bots = models.ManyToManyField(Bot)
    tgid = models.BigIntegerField(unique=True)
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120, null=True, blank=True)
    username = models.CharField(max_length=120, null=True, blank=True)


# @receiver(pre_save, sender=Bot)
# def pre_save_bot(sender, instance: Bot, *args, **kwargs):
#     bot = TeleBot(instance.token)
#     me = bot.get_me()
#     instance.name = me.first_name
#     instance.username = me.username
#     del bot

@receiver(post_delete, sender=Bot)
def delete_bot(sender, instance: Bot, *args, **kwargs):
    delete_webhook(instance.token, drop_pending_updates=True)
