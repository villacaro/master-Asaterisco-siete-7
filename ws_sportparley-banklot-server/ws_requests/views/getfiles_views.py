# -*- coding: utf-8 -*-
from ws_client.models import ClientFiles
from ws_lib.views import RESTView


class GetFiles(RESTView):

    def __init__(self):
        super(GetFiles, self).__init__()
        self.message_entrys = ['crcs']

    def request_valid(self, content, data, session=None, *args, **kwargs):
        content = super(GetFiles, self).request_valid(
            content, data, session, *args, **kwargs
        )
        crcs = self.data_object.get_entry('crcs')
        files = ClientFiles.objects.all().exclude(
            crc__in=crcs).values(
            'file',
            'location',
            'version',
            'size',
            'os')
        libs = list(files.filter(file_type='lib', status__codename='client_status_file_available'))
        client = list(files.filter(file_type='client', status__codename='client_status_file_available'))
        updater = list(files.filter(file_type='updater', status__codename='client_status_file_available'))
        docs = list(files.filter(file_type='docs', status__codename='client_status_file_available'))
        other = list(files.filter(file_type='other', status__codename='client_status_file_available'))

        content.set_message_entry("libs", libs)
        content.set_message_entry("client", client)
        content.set_message_entry("updater", updater)
        content.set_message_entry("docs", docs)
        content.set_message_entry("other", other)
        return content
