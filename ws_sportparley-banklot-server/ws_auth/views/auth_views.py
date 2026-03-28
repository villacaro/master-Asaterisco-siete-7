# -*- coding: utf-8 -*-
from datetime import timedelta

import rsa
from admin_banklotsports.settings import FORMAT_STR_DATETIME_SECONDS
from django.utils.timezone import now
from ws_client.models import ClientIPAddress
from ws_lib.crypto import CryptoRSA
from ws_lib.views import RESTView


class Auth(RESTView):

    def __init__(self):
        super(Auth, self).__init__()
        self.message_entrys = ['ins', 'client_id', 'client_srl', 'user', 'password', 'key']

    def get_content_data(self):
        # Edito la estructura a la que necesite
        content = super(Auth, self).get_content_data()
        content.set_message_entry(
            'date',
            now().strftime(FORMAT_STR_DATETIME_SECONDS)
        )
        return content

    def request_valid(self, content, data, session, *args, **kwargs):
        content = super(Auth, self).request_valid(
            content, data, session, *args, **kwargs
        )

        if not content.error:
            if (self.data_object.get_entry('user') == session.user.user and
                    session.user.check_password(self.data_object.get_entry('password'))):

                success = False
                user_status = session.user.get_status().codename
                serial = session.user.taquilla.serial
                ins = int(self.data_object.get_entry('ins'))
                install = 0
                if user_status == 'status_activo':
                    success = True
                elif user_status in ['status_instalacion', 'status_reinstalacion']:
                    if ins == 0:
                        install = 1
                    else:
                        install = 2
                elif user_status == 'status_bloqueado':
                    content.error_message = 'Usuario bloqueado, ' + \
                                            'contacte con soporte técnico'
                    content.error = True
                    session = self.process_session_detail(
                        session=session,
                        process='process_auth',
                        error_message=content.error_message
                    )
                    return content
                elif user_status == 'status_eliminado':
                    content.error_message = 'El usuario introducido no existe, o fue eliminado'
                    content.error = True
                    session = self.process_session_detail(
                        session=session,
                        process='process_auth',
                        error_message=content.error_message
                    )
                    return content

                if install == 1:
                    callback_message = 'Necesita reinstalación'
                    session = self.process_session_detail(
                        session=session,
                        process='process_auth',
                        style_class='danger',
                        callback_message=callback_message
                    )
                    content.set_message_entry('ins', 1)
                    content.set_message_entry('alert', callback_message)
                    session.session.enddate = now()
                    session.session.save(update_fields=['enddate', 'updated_at'])
                elif install == 2:
                    taquilla_status_detail = session.user.get_taquilla_status_details()
                    taquilla_status_detail.close_status_to(
                        'status_activo'
                    )
                    success = True
                    session.user.taquilla.update_serial(
                        self.data_object.get_entry('client_srl')
                    )
                    serial = self.data_object.get_entry('client_srl')
                    session = self.process_session_detail(
                        session=session,
                        process='auth_reinstallation',
                        style_class='success',
                        callback_message='Reinstalación realizada con éxito'
                    )

                if install == 0 and serial != self.data_object.get_entry('client_srl'):
                    content.error = True
                    content.error_message = 'No puede hacer esta acción'
                    session = self.process_session_detail(
                        session=session,
                        process='process_auth',
                        callback_message=content.error_message
                    )
                    return content

                if success:
                    getdata_address = ClientIPAddress.get_default_ip_by_ip_type(4)
                    content.set_message_entry(
                        'getdata_address', getdata_address.ip_address
                    )
                    content.set_message_entry(
                        'protocol', getdata_address.protocol
                    )
                    content.set_message_entry(
                        'ins', 0
                    )

                    # Si no existe RSA o, ya tiene 3 meses de caducidad
                    if not session.user.keys_date or now() > (session.user.keys_date + timedelta(days=90)):
                        (pub, priv) = CryptoRSA.newkeys()
                        session.user.pub_key = pub.save_pkcs1().decode('utf-8')
                        session.user.priv_key = priv.save_pkcs1().decode('utf-8')
                        session.user.keys_date = now()
                        session.user.save(update_fields=['priv_key', 'pub_key', 'keys_date'])
                    else:
                        # Generando clave RSA
                        pub = rsa.PublicKey.load_pkcs1((session.user.pub_key).encode())

                    content.set_message_entry(
                        'key', '{0} {1}'.format(pub.n, pub.e)
                    )

                    pub_key_str = self.data_object.get_entry('key').split(' ')
                    pub_key = rsa.PublicKey(n=pub_key_str[0], e=pub_key_str[1])

                    session.user.pub_key_client = pub_key.save_pkcs1().decode('utf-8')
                    session.user.save(update_fields=['pub_key_client'])

                    # Temporalmente se pone none para que no genere una firma en la peticion actual
                    session.user.pub_key_client = None

                    session = self.process_session_detail(
                        session=session,
                        process='process_login',
                    )
                    content.set_entry('session', session.session.pk)

            else:
                callback_message = 'Credenciales incorrectas'
                session = self.process_session_detail(
                    session=session,
                    process='process_auth',
                    style_class='danger',
                    callback_message=callback_message
                )
                content.set_message_entry('error', 1)
                content.set_message_entry('error_message', callback_message)
                session.session.enddate = now()
                session.session.save(update_fields=['enddate', 'updated_at'])

        return content
