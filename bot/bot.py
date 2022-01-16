import logging
import telebot
from telebot.custom_filters import StateFilter

from .telebot_override import MyBot

telebot.logger.setLevel(logging.ERROR)

bot = MyBot(parse_mode='HTML', )
bot.add_custom_filter(StateFilter(bot))
