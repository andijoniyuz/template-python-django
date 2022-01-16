from typing import Callable

from telebot import TeleBot, types, apihelper
from telebot.handler_backends import StateContext

apihelper.API_URL = "http://localhost:8088/bot{0}/{1}"

class State:
    def __init__(self):
        self._states = {}
        self.bot_id = None

    def id(self, chat_id):
        return ":".join([self.bot_id, str(chat_id)])

    def add_state(self, chat_id, state):
        """
        Add a state.
        :param chat_id:
        :param state: new state
        """
        if self.id in self._states:

            self._states[chat_id]['state'] = state
        else:
            self._states[chat_id] = {'state': state, 'data': {}}

    def current_state(self, chat_id):
        """Current state"""
        chat_id = self.id(chat_id)
        if chat_id in self._states:
            return self._states[chat_id]['state']
        else:
            return False

    def delete_state(self, chat_id):
        """Delete a state"""
        return self._states.pop(chat_id)

    def _get_data(self, chat_id):
        chat_id = self.id(chat_id)
        return self._states[chat_id]['data']

    def set(self, chat_id, new_state):
        """
        Set a new state for a user.
        :param chat_id:
        :param new_state: new_state of a user
        """
        chat_id = self.id(chat_id)
        self.add_state(chat_id, new_state)

    def _add_data(self, chat_id, key, value):
        chat_id = self.id(chat_id)
        result = self._states[chat_id]['data'][key] = value
        return result

    def finish(self, chat_id):
        """
        Finish(delete) state of a user.
        :param chat_id:
        """
        chat_id = self.id(chat_id)
        self.delete_state(chat_id)

    def retrieve_data(self, chat_id):
        """
        Save input text.

        Usage:
        with state.retrieve_data(message.chat.id) as data:
            data['name'] = message.text

        Also, at the end of your 'Form' you can get the name:
        data['name']
        """
        chat_id = self.id(chat_id)
        return StateContext(self, chat_id)


class MyBot(TeleBot):
    def __init__(
            self, parse_mode=None, threaded=True, skip_pending=False, num_threads=2,
            next_step_backend=None, reply_backend=None, exception_handler=None, last_update_id=0,
            suppress_middleware_excepions=False
    ):
        self._token = None
        super(MyBot, self).__init__(token=InvalidToken(), parse_mode=parse_mode, threaded=threaded,
                                    skip_pending=skip_pending, num_threads=num_threads,
                                    next_step_backend=next_step_backend, reply_backend=reply_backend,
                                    exception_handler=exception_handler, last_update_id=last_update_id,
                                    suppress_middleware_excepions=suppress_middleware_excepions)
        self.current_states = State()

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, value):
        self._token = value
        if not isinstance(self._token, InvalidToken):
            self.current_states.bot_id = self.id

    @property
    def id(self):
        if not isinstance(self.token, InvalidToken):
            return self.token.split(":")[0]
        return

    def register_next_step_handler(
            self, message: types.Message, callback: Callable, *args, **kwargs) -> None:
        _id = ":".join([self.id, str(message.chat.id)])
        self.register_next_step_handler_by_chat_id(_id, callback, *args, **kwargs)

    def _notify_next_handlers(self, new_messages):
        for i, message in enumerate(new_messages):
            need_pop = False
            handler_group_id = ":".join([self.token.split(":")[0], str(message.chat.id)])
            handlers = self.next_step_backend.get_handlers(handler_group_id)
            if handlers:
                for handler in handlers:
                    need_pop = True
                    self._exec_task(handler["callback"], message, *handler["args"], **handler["kwargs"])
            if need_pop:
                new_messages.pop(i)  # removing message that was detected with next_step_handler

    def process_new_updates(self, updates):
        if isinstance(self.token, InvalidToken):
            raise ValueError("Token is not valid. You need to change Bot instance token to valid one")
        super(MyBot, self).process_new_updates(updates)


class InvalidToken:
    pass
