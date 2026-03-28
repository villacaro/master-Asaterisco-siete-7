# -*- coding: utf-8 -*-

from ws_lib.views import RESTView


class ChangePassword(RESTView):
    process_db = 'process_passwdchanged'

    def __init__(self):
        super(ChangePassword, self).__init__()
        self.entrys = ['message', 'session']
        self.message_entrys = ['password_old', 'password_new']

    def request_valid(self, content, data, session, *args, **kwargs):
        content = super(ChangePassword, self).request_valid(
            content, data, session, *args, **kwargs
        )

        if not content.error:
            user = session.user
            passwd = user.check_password(
                self.data_object.get_entry('password_old')
            )
            if passwd:
                user.set_password(
                    self.data_object.get_entry('password_new')
                )
                user.save()
            else:
                content.error = True
                content.error_message = 'Credencial anterior incorrecta.'

        return content
