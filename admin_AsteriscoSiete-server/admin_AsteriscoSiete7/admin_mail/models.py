# -*- coding: utf-8 -*-

from django.urls import reverse
from django.db import models


class MessageAdjunt(models.Model):
    """Message: Mensajes

    Campos definidos:
            adjunt(FileField): documento o archivo digital, que se adjunta en mensajes

    """
    adjunt = models.FileField(upload_to='message_adjunt')

    class Meta:
        verbose_name = ('Adjunto de un mensaje')
        verbose_name_plural = ('Adjuntos de un mensaje')

    def __str__(self):
        return self.adjunt.name.replace('message_adjunt/', '')


class Message(models.Model):
    """Message: Mensajes

    Campos definidos:

        subject(CharField): Asunto del mensaje

        body(TextField): Cuerpo del mensaje, esto esta en texto plano o html preferiblemente

        adjunts(ManyToManyField): archivos adjuntos del mensaje

        from_comercializadora(ForeignKey): Comercializadora que lo envia

        priority(CharField): Prioridad del mensaje

        date_production(datetime): Fecha y hora de envio

        send_at: Fecha y hora de envio del mensaje.

    Dichas notificaciones de envian en los modulos respectivos, dependiendo de su tipo
    """

    PRIORITY_HIGH = '0'
    PRIORITY_MEDIUM = '1'
    PRIORITY_LOW = '2'

    PRIORITIES = [
        [PRIORITY_HIGH, 'Alta'],
        [PRIORITY_MEDIUM, 'Media'],
        [PRIORITY_LOW, 'Baja'],
    ]

    subject = models.CharField(
        max_length=100,
        verbose_name='Asunto',
        help_text='Introduzca el asusto del mensaje'
    )
    body = models.TextField(
        verbose_name='Mensaje',
        help_text='Introduzca el texto a enviar',
        blank=True,
    )
    adjunts = models.ManyToManyField(
        MessageAdjunt,
        related_name='message_adjunts',
        editable=False,
    )
    from_comercializadora = models.ForeignKey(
        'admin_finanzas.Comercializadora',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )
    priority = models.CharField(
        max_length=1,
        choices=PRIORITIES,
        default=PRIORITY_MEDIUM,
        verbose_name='Prioridad',
        help_text='Seleccione la priodidad que desea con la que se envie el mensaje'
    )
    send_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )

    class Meta:
        verbose_name = ('Mensaje')
        verbose_name_plural = ('Mensajes')

    def __str__(self):
        return '{0}'.format(self.subject)


class MessageSend(models.Model):
    """Message: Mensajes

    Campos definidos:

        message(ForeignKey): Mensaje enviado

        to_comercializadora(ManyToManyField): Comercializadoras a las que se
            envia el mensaje

        options(CharField): Configuracion de envio


    """

    SEND_SIMPLE = '1'
    SEND_MASIVO = '2'
    SEND_TAQUILLAS = '3'

    SEND_OPTIONS = [
        (SEND_SIMPLE, 'Simple'),
        (SEND_MASIVO, 'Masivo'),
        (SEND_TAQUILLAS, 'Taquillas'),
    ]

    message = models.ForeignKey(
        'admin_mail.Message',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )
    to_comercializadora = models.ManyToManyField(
        'admin_finanzas.Comercializadora',
    )
    options = models.CharField(
        max_length=1,
        choices=SEND_OPTIONS,
        default=SEND_SIMPLE,
    )

    class Meta:
        verbose_name = ('Mensaje enviados')
        verbose_name_plural = ('Mensajes enviados')


class MessageComer(models.Model):
    """Message: Mensajes

        Campos definidos:

    """

    TRAY_GROUP_RECEIVED = '1'
    TRAY_GROUP_SENT = '2'
    TRAY_GROUP_ARCHIVED = '3'
    TRAY_GROUP_RECYCLE = '4'

    TRAY_GROUP = (
        (TRAY_GROUP_RECEIVED, 'Recibidos'),
        (TRAY_GROUP_SENT, 'Enviados'),
        (TRAY_GROUP_ARCHIVED, 'Archivados'),
        (TRAY_GROUP_RECYCLE, 'Papelera'),
    )

    comercializadora = models.ForeignKey(
        'admin_finanzas.Comercializadora',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )
    message = models.ForeignKey(
        'admin_mail.Message',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )
    read = models.BooleanField(
        default=False,
    )
    tray_group = models.CharField(
        max_length=1,
        choices=TRAY_GROUP,
        default=TRAY_GROUP_RECEIVED,
    )

    class Meta:
        verbose_name = ('Mensaje')
        verbose_name_plural = ('Mensajes')
        ordering = ['-message__send_at']

    def __str__(self):
        return '{0}'.format(self.message)

    def get_tray_diff_archived(self):
        return self.tray_group != self.TRAY_GROUP_ARCHIVED

    def get_ulr_list(self):
        if self.tray_group == self.TRAY_GROUP_SENT:
            url_name = 'admin_mail_message_list'
        else:
            url_name = 'admin_mail_message_list_{0}'.format(
                self.get_tray_group_display().lower()
            )
        return reverse(url_name)
