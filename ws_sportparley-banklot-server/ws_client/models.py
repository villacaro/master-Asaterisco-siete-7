# -*- coding: utf-8 -*-
import os
import zlib

from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models
from ws_sportparley.settings import CACHES_CONF_TIME

from .lib import BasicClass


# Create your models here.
class ClientStatus(models.Model, BasicClass):
    '''
    Table ws_client_clientstatus (Status de cliente)
    Attributes:
        status: Nombre del status.
        codename: Codename del status.
        content_type: Tipo de status.
        created_at: Registro de creación.
        updated_at: Registro de actualización.
    Example:
        status: Estandar
        codename: client_status_ip_default
        content_type: 1
    '''
    status = models.CharField(
        max_length=140,
        verbose_name='Estado'
    )
    codename = models.CharField(
        unique=True,
        max_length=140,
        verbose_name='Codename',
        default='client_status_',
        db_index=True,
    )
    CONTENT_TYPE_CHOICES = (
        (1, 'IP'),
        (2, 'Versiones'),
        (3, 'Archivos'),
    )
    content_type = models.IntegerField(
        choices=CONTENT_TYPE_CHOICES,
        verbose_name='Tipo de status'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        editable=False,
    )

    class Meta:
        app_label = 'ws_client'
        db_tablespace = 'ts_comer'
        verbose_name = 'Estado de cliente'
        verbose_name_plural = 'Estados de cliente'

    def __str__(self):
        return self.status

    def equals_by_codename(self, codename):
        '''
        Verifica si los codename son iguales por un codename específico.
        '''
        if self.codename == codename:
            return True
        return False

    @staticmethod
    def get_status_by_codename(codename):
        '''
        Retorna el status por un codename específico.
        '''
        try:
            return ClientStatus.objects.get(codename=codename)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_status_list_by_content_type(content_type):
        '''
        Retorna la lista de status por un content_type específico.
        '''
        try:
            status_list = ClientStatus.objects.filter(content_type=content_type)
            return status_list.values_list('id', 'status')
        except ObjectDoesNotExist:
            return None


class ClientIPAddress(models.Model, BasicClass):
    '''
    Table ws_client_ipaddress (Direcciones de IP del cliente)
    Attributes:
        ip_address: Dirección IP.
        ip_type: Tipo de IPAddress.
        protocol: Protocolo de la dirección.
        status: Status del IPAddress.
        created_at: Registro de creación.
        updated_at: Registro de actualización.
    Example:
        ip_address: 127.0.0.1
        ip_type: 1 - Connection
        protocol: 1 - HTTP
        status: 2 - client_status_ip_active
    '''
    ip_address = models.CharField(
        max_length=140,
        verbose_name='Dirección IP'
    )
    TYPE_CHOICES = (
        (1, 'Connection'),
        (2, 'Auto Update'),
        (3, 'Auth'),
        (4, 'Get Data'),
    )
    ip_type = models.IntegerField(
        choices=TYPE_CHOICES,
        verbose_name='Tipo de IP'
    )
    CHOICES_PROTOCOL = (
        (1, 'HTTP'),
        (2, 'HTTPS'),
    )
    protocol = models.IntegerField(
        choices=CHOICES_PROTOCOL,
        verbose_name='Protocolo'
    )
    status = models.ForeignKey(
        'ClientStatus'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        editable=False
    )

    class Meta:
        unique_together = [('ip_address', 'ip_type'), ('ip_type', 'status')]
        app_label = 'ws_client'
        db_tablespace = 'ts_comer'
        verbose_name = 'Dirección IP'
        verbose_name_plural = 'Direcciones IP'

    def __str__(self):
        return self.ip_address

    def save(self, *args, **kwargs):
        key = '{0}_{1}_{2}'.format('ClientIPAddress', 'client_status_ip_default', self.ip_type)
        cache.delete(key)
        super(ClientIPAddress, self).save(*args, **kwargs)

    @staticmethod
    def get_default_ip_by_ip_type(ip_type):
        '''
        Retorna la IP por defecto por un ip_type específico.
        '''
        key = '{0}_{1}_{2}'.format('ClientIPAddress', 'client_status_ip_default', ip_type)
        clientip = cache.get(key)
        if not clientip:
            try:
                clientip = ClientIPAddress.objects.only('ip_address', 'protocol').get(
                    ip_type=ip_type,
                    status__codename='client_status_ip_default'
                )
                cache.set(
                    key,
                    clientip,
                    CACHES_CONF_TIME['registros_db']['ClientIPAddress']
                )
            except Exception:
                raise Exception(
                    'No existe ClientIPAddress objects de status \"Default\" y de tipo \"{0}\"'.format(
                        ip_type
                    )
                )
        return clientip


class ClientVersion(models.Model, BasicClass):
    '''
    Table ws_client_clientversion (Versiones del cliente)
    Attributes:
        version: Versión del cliente.
        status: Status de la versión.
        created_at: Registro de creación.
        updated_at: Registro de actualización.
    Example:
        version: 1.0.0
        status: client_status_vs_active
    '''
    version = models.CharField(
        max_length=140,
        verbose_name='Versión',
        unique=True
    )
    status = models.ForeignKey(
        'ClientStatus'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        editable=False
    )

    name_cache = '{0}_{1}'.format('ClientVersion', 'client_status_vs_active')

    class Meta:
        unique_together = [('version', 'status')]
        app_label = 'ws_client'
        db_tablespace = 'ts_comer'
        verbose_name = 'Versión de cliente'
        verbose_name_plural = 'Versiones de cliente'

    def __str__(self):
        return self.version

    def save(self, *args, **kwargs):
        cache.delete(self.name_cache)
        super(ClientVersion, self).save(*args, **kwargs)

    def check_version(self, version):
        '''
        Verifica la versión actual dada una versión específica.
        '''
        if str(version) == str(self):
            return True
        return False

    def set_status_by_status_codename(self, status_codename):
        '''
        Asigna un status nuevo a la versión por un status_codename específico.
        '''
        self.status = ClientStatus.get_status_by_codename(status_codename)
        if self.status is not None:
            self.save()
        else:
            raise Exception('No existe el {0} Object por codename: {1}'.format(
                'ClientStatus',
                status_codename
            )
            )

    def clean(self):
        '''
        1. Asigna un status a los archivos de la versión específica.
        '''
        version = self.get_version()
        status = 'client_status_file_unavailable'
        if not version:  # Si no hay version disponible utiliza la que va a editar
            version = self.version
            status = 'client_status_file_available'
        ClientFiles.set_files_status(version, status)

    @staticmethod
    def get_version():
        '''
        Retorna la versión actual del cliente.
        '''
        clienvs = cache.get(ClientVersion.name_cache)
        if not clienvs:
            try:
                clienvs = ClientVersion.objects.only('pk', 'version').get(
                    status__codename='client_status_vs_active'
                )
                cache.set(
                    ClientVersion.name_cache,
                    clienvs,
                    CACHES_CONF_TIME['registros_db']['ClientVersion']
                )
            except Exception:
                return None
        return clienvs


def get_image_path(instance, name):
    return os.path.join('download/%s/' % str(instance.file_type), name)


class ClientFiles(models.Model, BasicClass):
    '''
    Table ws_client_clientfiles (Archivos del cliente)
    Attributes:
        name: Nombre del archivo.
        status: Status del archivo.
        location: Ubicación del archivo.
        client_version: Versión del cliente.
        version: Versión del archivo.
        size: Tamaño en bytes del archivo.
        file_type: Tipo de archivo.
        os: Sistema operativo que ejecuta el archivo.
        crc: CRC o identificador único del archivo.
        download_url: URL de descarga del archivo.
        created_at: Registro de creación.
        updated_at: Registro de actualización.
    Example:
        name: sportparley.jar
        status: client_status_file_available
        location: /
        client_version: 1 - 1.0.0
        version: None
        size: 1000
        file_type: client
        os: ALL
        crc: 1234567890
        download_url: /download/client/
    '''
    status = models.ForeignKey(
        'ClientStatus'
    )
    location = models.CharField(
        max_length=140,
        verbose_name='Ubicación'
    )
    client_version = models.ForeignKey(
        'ClientVersion',
        null=True,
        blank=True
    )
    version = models.CharField(
        max_length=140,
        verbose_name='Versión',
        null=True,
        blank=True
    )
    size = models.IntegerField(
        verbose_name='Tamaño',
        help_text='En bytes, ejemplo: 1000'
    )
    FILE_TYPES_CHOICES = (
        ('client', 'Cliente'),
        ('updater', 'Actualizador'),
        ('lib', 'Librería'),
        ('docs', 'Documentación'),
        ('other', 'Otro'),
    )
    file_type = models.CharField(
        max_length=140,
        verbose_name='Tipo',
        choices=FILE_TYPES_CHOICES
    )
    OS_TYPES = (
        ('ALL', 'All'),
        ('WIN32', 'Windows'),
        ('LINUX', 'Linux'),
        ('MACOS', 'Mac OS'),
    )
    os = models.CharField(
        max_length=140,
        verbose_name='Sistema operativo',
        choices=OS_TYPES
    )
    crc = models.CharField(
        max_length=140,
        verbose_name='Hash CRC',
        default='0',
        editable=False
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        editable=False
    )
    file = models.FileField(
        upload_to=get_image_path
    )

    class Meta:
        unique_together = ('file', 'client_version',)
        app_label = 'ws_client'
        db_tablespace = 'ts_comer'
        verbose_name = 'Archivo de cliente'
        verbose_name_plural = 'Archivos de cliente'

    def __str__(self):
        return self.file.name

    def as_json(self):
        '''
        Retorna el objecto de ClientFiles en formato JSON.
        '''
        return dict(
            location=self.location,
            version=self.version,
            crc=self.crc,
        )

    def set_status(self, status_codename):
        '''
        Asigna un status a un archivo de cliente dado un status_codename específico.
        '''
        self.status = ClientStatus.get_status_by_codename(status_codename)
        self.save()

    def getcrc(self, excludeLine='', includeLine=''):
        try:
            fd = self.file  # open('{0}{1}'.format(self.download_url, self.name), 'rb')
        except IOError:
            print('Unable to open the file in readmode: {0}'.format(self.file.name))
            return
        eachLine = fd.readline()
        prev = None
        while eachLine:
            if excludeLine and eachLine.startswith(excludeLine):
                continue
            if not prev:
                prev = zlib.crc32(eachLine)
            else:
                prev = zlib.crc32(eachLine, prev)
            eachLine = fd.readline()
        fd.close()
        return prev

    def clean(self):
        client_version = ClientVersion.get_version()
        if client_version:
            if (
                self.client_version is not None and
                str(client_version) != '{0}'.format(self.client_version)
            ):
                raise ValidationError(
                    ('La versión actual del cliente es la \"%s\"' % (client_version))
                )

    @staticmethod
    def get_client_file_by_version(version):
        return (ClientFiles.objects.filter(version=version, file_type='client') |
                ClientFiles.objects.filter(client_version__version=version, file_type='client'))

    @staticmethod
    def getClientFilesByOS(os):
        return (ClientFiles.objects.filter(os='ALL', status__codename='client_status_file_available') |
                ClientFiles.objects.filter(os=os, status__codename='client_status_file_available'))

    @staticmethod
    def set_files_status(version, status):
        client_file = ClientFiles.get_client_file_by_version(version)
        if client_file:
            client_file = client_file[0]
            client_file.set_status(status)
