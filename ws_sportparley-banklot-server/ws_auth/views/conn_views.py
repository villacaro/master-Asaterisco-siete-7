# -*- coding: utf-8 -*-

from ws_client.models import ClientIPAddress, ClientVersion
from ws_lib.views import RESTView


class Connection(RESTView):

    def __init__(self):
        super(Connection, self).__init__()
        self.message_entrys = ["version", "os"]

    def request_valid(self, content, data, session=None, *args, **kwargs):
        content = super(Connection, self).request_valid(
            content, data, session, *args, **kwargs
        )

        if not content.error:
            version = ClientVersion.get_version()

            if not version:
                content.error_message = "No existe ClientVersion object de status \"Activo\""
            else:
                if version.check_version(self.data_object.get_entry("version")):
                    conn_address = ClientIPAddress.get_default_ip_by_ip_type(1)
                    auth_address = ClientIPAddress.get_default_ip_by_ip_type(3)
                    content.set_message_entry(
                        "conn_address", conn_address.ip_address
                    )
                    content.set_message_entry(
                        "auth_address", auth_address.ip_address
                    )
                    content.set_message_entry(
                        "protocol", auth_address.protocol
                    )
                    content.set_message_entry(
                        "update", 0
                    )
                else:
                    autoupdate_address = ClientIPAddress.get_default_ip_by_ip_type(2)
                    content.set_message_entry(
                        "autoupdate_address", autoupdate_address.ip_address
                    )
                    content.set_message_entry(
                        "protocol", autoupdate_address.protocol
                    )
                    content.set_message_entry(
                        "update", 1
                    )
        return content
