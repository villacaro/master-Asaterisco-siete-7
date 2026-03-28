
from admin_historic.models import TaquillaSessions, TaquillaSessionsDetail, UsersProcesses
from django.utils.timezone import now
from ws_lib.json import JSONObject


class TaquillaSessionDetailManager(object):

    def __init__(self, session=None):
        self._session = session
        if session:
            self._user = session.user
        else:
            self._user = None
        self.sessiondetail = None
        self._style_class = "error"
        self._error = False
        self._error_message = None
        self._callback = False
        self._callback_message = None
        self._callback_object = JSONObject()
        self._callback_json = {
            'callback': None
        }

    @property
    def session(self):
        return self._session

    @session.setter
    def session(self, value):
        self._session = value

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, value):
        self._user = value

    @property
    def style_class(self):
        return self._style_class

    @style_class.setter
    def style_class(self, value):
        self._style_class = value

    @property
    def error(self):
        return self._error

    @error.setter
    def error(self, value):
        self._error = value

    @property
    def error_message(self):
        return self._error_message

    @error_message.setter
    def error_message(self, value):
        self._error_message = value
        self.error = True

    @property
    def callback(self):
        return self._callback

    @callback.setter
    def callback(self, value):
        self._callback = value

    @property
    def callback_message(self):
        return self._callback_message

    @callback_message.setter
    def callback_message(self, value):
        self._callback_message = value
        self.callback = True

    @property
    def callback_object(self):
        return self._callback_object

    @callback_object.setter
    def callback_object(self, value):
        self._callback_object = value

    @property
    def callback_json(self):
        return self._callback_json

    @callback_json.setter
    def callback_json(self, value):
        self._callback_json = value

    def get_callback_entry(self, key):
        return self.callback_object.get_entry(key)

    def set_callback_entry(self, key, value):
        return self.callback_object.set_entry(key, value)

    def load(self, codename):
        self.sessiondetail = TaquillaSessionsDetail(
            session_id=self.session.pk,
            userprocess=UsersProcesses.get_userprocess_by_codename(
                codename=codename
            ),
            enrro=self.error
        )

    def save(self):
        try:
            if self.error is True:
                self.callback_object.set_entry(
                    "error_message", self.error_message
                )
                self.callback_json["callback"] = self.callback_object.json
            if self.callback is True:
                self.callback_object.set_entry(
                    "callback_message", self.callback_message
                )
                self.callback_json["callback"] = self.callback_object.json
            if self.error is True or self.callback is True:
                self.callback_object.set_entry("class", self.style_class)
                self.sessiondetail.detail = self.callback_json
            if self.sessiondetail:
                self.sessiondetail.enrro = self.error
                self.sessiondetail.save()
        except Exception:
            raise

    def new(self, user, ip):
        self.user = user

        TaquillaSessions.objects.filter(
            user_id=user.pk, enddate=None
        ).update(
            enddate=now()
        )

        self.session = TaquillaSessions.objects.create(
            startdate=now(), user_id=user.pk, ip=ip
        )
