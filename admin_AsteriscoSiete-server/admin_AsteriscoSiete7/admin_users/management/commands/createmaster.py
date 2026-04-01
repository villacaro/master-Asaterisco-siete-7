# -*- coding: utf-8 -*-
import getpass
import sys
from optparse import make_option

from admin_status.models import Status, StatusDetail
from admin_users.models import UserProfile, Users
from django.contrib.auth.management import get_default_username
from django.core import exceptions
from django.core.management.base import BaseCommand
from django.utils.encoding import force_str
from django.utils.six.moves import input
from django.utils.text import capfirst


class Command(BaseCommand):

    UserModel = Users

    def __init__(self, *args, **kwargs):
        # Options are defined in an __init__ method to support swapping out
        # custom user models in tests.
        super(Command, self).__init__(*args, **kwargs)

        self.option_list = BaseCommand.option_list + (
            make_option(
                '--%s' % self.UserModel.USERNAME_FIELD,
                dest=self.UserModel.USERNAME_FIELD,
                default=None,
                help='Especifique el nombre de usuario master a crear.'
            ),
        )

    option_list = BaseCommand.option_list
    help = 'Proceso para crear un usuario master activo.'
    args = '--user=ebar0n'

    def execute(self, *args, **options):
        self.stdin = options.get('stdin', sys.stdin)  # Used for testing
        return super(Command, self).execute(*args, **options)

    def handle(self, *args, **options):

        username = options.get(self.UserModel.USERNAME_FIELD, None)
        password = None

        default_username = get_default_username()
        try:

            while username is None:
                input_msg = 'Ingrese el nombre de usuario'
                if default_username:
                    input_msg = '%s (si deja el usuario en blanco se usara "%s")' % (
                        input_msg, default_username)

                raw_value = input(force_str('%s: ' % input_msg))

                if default_username and raw_value == '':
                    raw_value = default_username

                try:
                    self.UserModel.objects.get(user=raw_value)
                except self.UserModel.DoesNotExist:
                    username = raw_value
                else:
                    self.stderr.write('Error: El usuario %s ya existe.' %
                                      raw_value)
                    username = None

            user_data = {}
            for field_name in self.UserModel.REQUIRED_FIELDS:
                field = self.UserModel._meta.get_field(field_name)
                user_data[field_name] = options.get(field_name, None)
                while user_data[field_name] is None:
                    raw_value = input(force_str('%s: ' % capfirst(field.verbose_name)))
                    try:
                        user_data[field_name] = field.clean(raw_value, None)
                    except exceptions.ValidationError as e:
                        self.stderr.write('Error: %s' % '; '.join(e.messages))
                        user_data[field_name] = None

                    if field.unique:
                        try:
                            kwargs = {}
                            kwargs[field_name] = raw_value
                            self.UserModel.objects.get(**kwargs)
                        except self.UserModel.DoesNotExist:
                            pass
                        else:
                            self.stderr.write('Error: El valor %s ya existe.' %
                                              raw_value)
                            user_data[field_name] = None

            # Get a password
            while password is None:
                if not password:
                    password = getpass.getpass(
                        force_str('Ingrese la contraseña: ')
                    )
                    password2 = getpass.getpass(
                        force_str('Ingrese nuevamente la contraseña: ')
                    )
                    if password != password2:
                        self.stderr.write('Error: las contraseñas no coinciden.')
                        password = None
                        continue
                if password.strip() == '':
                    self.stderr.write('Error: La contraseña es obligatoria.')
                    password = None
                    continue

        except KeyboardInterrupt:
            self.stderr.write('\n\nOperación cancelada.')
            sys.exit(1)

        if username:
            user_create = self.UserModel()
            user_create.user = username
            user_create.superuser = True
            user_create.profile = UserProfile.objects.get(codename='userprofile_master')
            self.stdout.write('{0}'.format(user_create.user))
            self.stdout.write('{0}'.format(user_create.profile))
            # asignando contraseña
            user_create.set_password(password)

            user_create.save()
            # asignando estatus
            StatusDetail.objects.create(
                status=Status.objects.get(codename='status_activo'),
                user=user_create
            )
            self.stdout.write('Master creado con exito.')
