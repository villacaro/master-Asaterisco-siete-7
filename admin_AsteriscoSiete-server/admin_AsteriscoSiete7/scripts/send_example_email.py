# -*- coding: utf-8 -*-

from django.core.mail import mail_admins


def run(*args):
    """
         >> python manage.py runscript send_example_email
    """
    print("Enviando mensaje de ejemplo.")
    mail_admins(subject="Ejemplo.", message="Dont worry!")
    print("Mensaje enviado.")
