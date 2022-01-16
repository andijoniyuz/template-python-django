from telebot import types

from .models import Bot, User


def get_user(user: types.User, bot: Bot):
    u = User.objects.filter(tgid=user.id).first()
    if not u:
        u = User.objects.create(
            tgid=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username
        )
    if not u.bots.filter(id=bot.id).exists():
        u.bots.add(bot)
    return u


def get_bot(token: str):
    return Bot.objects.get(token=token)
