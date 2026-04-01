# -*- coding: utf-8 -*-
import string
from random import choice

from admin_banklotsports.settings import CACHES_CONF_TIME
from admin_historic import auditoria
from admin_principal.security import Security
from django import template
from django.contrib.auth.models import AbstractBaseUser
from django.core.cache import cache
from django.db import models
from django.utils.timezone import now

register = template.Library()


class UsersManager(models.Manager):
    """Manager de usuarios

    Esta clase maneja las operaciones basicas de los usuarios, como verificar la password,
    logearse etc.
    """

    def login(self, username, request, id_comercializadora=None):
        """
        Procesa el login, para x usuario con autenticiacion verificada
        """

        user = Users.objects.get(user=username)

        try:
            """
            obtiene la ultima fecha de logea de la ultima session iniciada
            """
            user.last_login = user.sessions_set.all().order_by(
                "-created_at")[0].created_at
            """
            en el save automaticamente se cierrar todas las sessiones iniciadas
            """
            user.save(update_fields=['last_login'])
        except Exception:
            """
            Cierro todas las sessiones abiertas
            """
            user.clear_session()

        """
        Ahora creamos la variable de session
        """
        var_session = Security()
        """
        Creo la session
        """
        from admin_historic.models import Sessions
        session = Sessions.objects.create(
            user=user,
            ip=var_session.get_ip(request),
            user_agent=request.META.get("HTTP_USER_AGENT", ""),
        )
        """
        # Inicia una nueva sesión
        """
        user.new_process_in_session(codename="process_login")
        session.enddate = now()
        session.save(update_fields=["enddate"])
        """
        #obtengo el id de la comercializadora asociado
        """
        id_comercializadora = user.get_comercializadora(
            id_comercializadora=id_comercializadora)
        if id_comercializadora:
            user.comercializadora_session = id_comercializadora
            id_comercializadora_pk = id_comercializadora.pk
            user.save(
                clear_session=False,
                update_fields=["comercializadora_session"]
            )
        else:
            id_comercializadora_pk = id_comercializadora

        id_sistema_juego = user.get_sistema_juego(id_comercializadora_pk)
        if id_sistema_juego is None:
            id_sistema_juego = 0
        else:
            id_sistema_juego = id_sistema_juego.pk

        var_session.set_conf(
            request=request,
            id_sesion=session.pk,
            id_usuario=user.pk,
            id_comercializadora=id_comercializadora_pk,
            id_sistema_juego=id_sistema_juego
        )

        """
        #guarda la cookie generada para una posterior verificacion
        """

        session.cookie = var_session.texto
        session.enddate = None
        session.save(update_fields=["cookie", "enddate"])

        cache.set(
            'sessions_expire_{0}'.format(session.pk),
            True,
            CACHES_CONF_TIME['registros_db']['session_expire']
        )

    def authenticate(self, username, password):
        """
        Este este metodo dados una credenciales se verifica que ambas coincidan,
        para asi devolver el usuario que intenta iniciar session.

        Provicionalmente, mientras se migra de metodo de encriptacion,
        hay una validacion que al notar que la contraseña es incorrecta,
        se va a una segunda verificcion con la contraseña anterior,
        se der correcta dicha contraseña con este key, se procede a crear
        el nuevo token. Este ultimo proceso con el tiempo se debe eliminar.
        """
        try:
            user = Users.objects.select_related('profile').get(user=username)
            if user.check_password(password):
                return user
            else:
                None
        except Users.DoesNotExist:
            return None


class UserProfile(models.Model):
    """UserProfile: Perfiles de usuario

    Esta tabla posee la definicion basica de los distintos usuarios posibles ha aver,

    Campos definidos:
        nombre(string): nombre del perfil de usuario, por ejemplo: Operadora

        codename(string): codigo en minusculas del perfil de usuario

        content_type(entero): indica el tipo de nivel, por ejemplo los usuarios de nivel uno
        pueden crear usuarios de niveles sucesores

        created_at y updated_at: registros de creacion y actualizacion.
    """

    nombre = models.CharField(
        max_length=160
    )
    codename = models.CharField(
        max_length=160,
        unique=True,
        db_index=True,
    )
    content_type = models.IntegerField(
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        editable=False,
    )

    def __str__(self):
        """
        Funcion invocada por python cuando se le hace un str al objeto,
        por defecto se devuelve el nombre de la instancia, ya que es lo mas representativo
        """
        return self.nombre

    class Meta:
        db_tablespace = "ts_comer"
        verbose_name = ('Tipo de usuario')
        verbose_name_plural = ('Tipos de usuarios')
        ordering = ["content_type", ]

    def save(self, *args, **kwargs):
        super(UserProfile, self).save(*args, **kwargs)
        self.cache_clear()

    def cache_clear(self):
        cache.delete(
            '{0}_{1}'.format('user_type', self.codename)
        )
        cache.delete(
            '{0}_{1}'.format('user_type', self.pk)
        )

    def get_verbose_name(self):
        return self._meta.verbose_name

    def get_nombre(self):
        return self.nombre

    def get_codename(self):
        return self.codename

    def get_content_type(self):
        return self.content_type

    @models.permalink
    def get_absolute_url(self):
        return ('user_profile_detail', (), {'pk': self.pk})

    @staticmethod
    def get_profile_by_codename(codename):
        profile = cache.get('{0}_{1}'.format('user_type', codename))
        if not profile:
            profile = UserProfile.objects.get(codename=codename)
            cache.set(
                '{0}_{1}'.format('user_type', codename),
                profile,
                CACHES_CONF_TIME['registros_db']['user_type']
            )
        return profile

    @staticmethod
    def get_userprofile_by_pk(pk):
        profile = cache.get('{0}_{1}'.format('user_type', pk))
        if not profile:
            profile = UserProfile.objects.get(pk=pk)
            cache.set(
                '{0}_{1}'.format('user_type', pk),
                profile,
                CACHES_CONF_TIME['registros_db']['user_type']
            )
        return profile


class Users(AbstractBaseUser):

    """Los Users, o usuarios

    Clase que define las propiedades de los posibles usuarios a representar, dicha clase
    hereda de la
    clase abstracta base de los usuarios de Djando, dicha clase posee ciertas funciones
    o codigo
    reutilizable asi como el manejo del password con un buen algoritmo de encriptacion.

    Campos definidos en la clase abstacta
        password: es el password
        last_login: fecha en la que se realizo el ultimo login

    Campos definidos:
        user: campo unico que identifica al usuario, es el unico campo que tiene por defecto la
        asignacion de un indice en db

        profile: clave foranea que vincula un usuario a un unico perfin de usuario.

        etiqueta: posible titulo de tipo de usuario personalizado.

        email: correo electronico, este campo es opcional y a su vez unico.

        token: campo reservado para posibles token generados por el sistema para recuperaciones
        de cuenta.

        token_time: indicador que sirve para validar el momento en el que se genero un token

        user_ref: clave forarea con el usuario creador.

        superuser: booleano que indica si el user en cuestion es super usuario en su perfil
        correspondiente, no se le asignaran permisos de manera explicita.

        comercializadora: posee todas las comercializadoras a las cuales esta afiliado
        (debe tener una por defecto).

        groups: distintos grupos a los que pertenece el usuario

        user_permissions: distintos permisos individuales que posee el usuario

        created_at y updated_at: registros de creacion y actualizacion.
    """

    user = models.CharField(
        max_length=100,
        db_index=True,
        unique=True,
        verbose_name='Nombre de usuario (*)',
        help_text="Ingrese el nombre de usuario"
    )

    profile = models.ForeignKey(
        'UserProfile',
        verbose_name="Perfil de usuario (*)",
        help_text="Seleccione el perfil de usuario"

    )
    etiqueta = models.CharField(
        max_length=200,
        verbose_name='Etiqueta ',
        null=True,
        blank=True
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        null=True,
        blank=True,
        verbose_name='Correo electronico ',
        help_text="Ingrese el correo electronico"
    )

    token = models.CharField(
        max_length=200,
        null=True,
        editable=False
    )
    token_time = models.DateTimeField(
        editable=False,
        null=True
    )

    user_ref = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='Usuario creador',
    )
    superuser = models.BooleanField(
        default=False,
        verbose_name='Superusuario',
    )

    comercializadora = models.ManyToManyField(
        "admin_finanzas.Comercializadora",
        blank=False,
        verbose_name='Comercializadora',
    )

    comercializadora_session = models.ForeignKey(
        "admin_finanzas.Comercializadora",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        editable=False,
        related_name="comercializadora_session"
    )

    groups = models.ManyToManyField(
        "admin_permisologia.Groups",
        verbose_name='Grupos de usuario',
        blank=True,
        help_text="Seleccione los grupos disponibles",
        related_name="user_set",
        related_query_name="user"
    )

    user_permissions = models.ManyToManyField(
        "admin_permisologia.Permissions",
        verbose_name="Permisos de usuario",
        blank=True,
        help_text="Seleccione los permisos para el usuario.",
        related_name="user_set",
        related_query_name="user"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        editable=False,
    )

    objects = UsersManager()

    USERNAME_FIELD = 'user'
    REQUIRED_FIELDS = ['email']
    audit_exclude = ('token', 'token_time', 'last_login', 'comercializadora_session', 'updated_at')

    class Meta:
        db_tablespace = "ts_comer"
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        ordering = ["user", ]

    def __str__(self):
        return self.user

    @models.permalink
    def get_absolute_url(self):
        return ('admin_users_users_detail', (), {'pk': self.pk})

    def save(self, clear_session=True, *args, **kwargs):
        """
        Al momento de guardar informacion de un usuario
        por defecto la bandera de clear_session indica que
        se debe cerrar la session abierta de este user en
        caso de tener alguna iniciada.
        """
        super(Users, self).save(*args, **kwargs)
        if clear_session:
            self.clear_session()

        self.cache_clear()

    def cache_clear(self, clear_permisos=False):
        cache.delete('{0}_{1}'.format('user_status', self.pk))
        cache.delete('{0}_{1}'.format('user_count_comer', self.pk))

        if clear_permisos:
            for comercializadora in self.comercializadora.all():
                cache.delete(
                    "menu_{0}_{1}".format(
                        self.pk,
                        self.get_profile_codename_by_comercializadora(
                            comercializadora
                        )
                    )
                )
                cache.delete(
                    "menu_permission_{0}_{1}".format(
                        self.pk,
                        self.get_profile_codename_by_comercializadora(
                            comercializadora
                        )
                    )
                )

    def get_superuser_display(self):
        """
        Retorna en texto si es o no super usuario
        """
        return "Si" if self.superuser else "No"

    def get_etiqueta(self):
        """
        Retorna la etiqueta del usuario o en su defecto una cadena vacia
        """
        if self.etiqueta:
            return self.etiqueta
        else:
            return ""

    def get_email(self):
        """
        Retorna el email del usuario o en su defecto una cadena vacia
        """
        if self.email is not None:
            return self.email
        else:
            return ""

    def get_user(self):
        """
        Retorna el user, invoca al metodo padre que realiza la misma tarea, basandose en el campo
        USERNAME_FIELD
        """
        return self.get_username()

    def get_token(self, is_save=True, token_len=48):
        """
        Genera un token de tamaño 6, comprendido por letras y numeros
        """
        chars = string.ascii_letters + string.digits
        while True:
            token = ''.join(choice(chars) for i in range(token_len))
            try:
                Users.objects.get(token=token)
            except Users.DoesNotExist:
                if is_save:
                    self.token = token
                    self.token_time = now()
                    self.save(update_fields=["token", "token_time"])
                break
        return token

    def get_status(self):
        """
        Devuelve el estatus actual del usuario
        """
        status = cache.get(
            '{0}_{1}'.format('user_status', self.pk)
        )
        if not status:
            from admin_status.models import StatusDetail
            try:
                status = self.statusdetail_set.select_related(
                    'status').get(enddate=None).status
            except StatusDetail.DoesNotExist:
                """
                si existe alguna clase de error al consultar el status
                anulados todos los anteriores si los  hay, y procedemos
                a generar un status nuevo
                """
                from admin_status.models import Status
                status = Status.get_status_by_codename(codename='status_bloqueado')
                StatusDetail.objects.create(
                    status=status,
                    user=self
                )
            cache.set(
                '{0}_{1}'.format('user_status', self.pk),
                status,
                CACHES_CONF_TIME['registros_db']['user']
            )

        return status

    def get_comercializadora_is_multiple(self):
        """
        Retorna true en caso de que el usuario tenga mas de una comercializadora asociada
        """
        is_multiple = cache.get('{0}_{1}'.format('user_count_comer', self.pk))
        if not is_multiple:
            is_multiple = self.comercializadora.all().count() > 1
            cache.set(
                '{0}_{1}'.format('user_count_comer', self.pk),
                is_multiple,
                CACHES_CONF_TIME['registros_db']['user']
            )
        return is_multiple

    def get_comercializadora(self, id_comercializadora=None):
        """
        Retorna una comercializadora, en caso de no indicar cual,
        se devolvera una por defecto.
        """
        if not id_comercializadora:
            if self.profile.codename == "userprofile_master":
                return 0
            else:
                if self.comercializadora_session:
                    return self.comercializadora_session
                else:
                    return self.comercializadora.all()[0]
        else:
            return self.comercializadora.get(pk=id_comercializadora)

    def get_sistema_juego(self, id_comercializadora):
        """
        Retorna el id de sistema de juego asociado a la comercializadora recibida.
        """
        if id_comercializadora is None or id_comercializadora == 0:
            return None
        else:
            sistemajuego = cache.get(
                'sistemajuego_{0}'.format(id_comercializadora))
            if not sistemajuego:
                comer = self.comercializadora.get(pk=id_comercializadora)
                from admin_juego.models import SistemaJuego
                sistemajuego = SistemaJuego.objects.get_sistema_juego_by_comercializadora(
                    comer)
            return sistemajuego

    def get_session(self):
        """
        Retorno la session actual, asociada al usuario
        """
        try:
            return self.sessions_set.get(enddate=None)
        except Exception:
            sessions = self.sessions_set.filter(enddate=None)
            if sessions.exists():
                session = sessions[0]
                for obj in sessions[1:]:
                    obj.enddate = now()
                    obj.save(update_fields=['enddate'])
                return session
            else:
                return None

    def logout(self, activo=True):
        """
        Creamos el detalle se session correspondiente y procedemos a cerrar la session
        """
        if self.get_session() is not None:
            if activo:
                self.new_process_in_session(codename="process_logout")
            else:
                self.new_process_in_session(codename="process_expiresession")
            self.clear_session()

            return True
        else:
            return False

    def new_process_in_session(self, codename):
        """
        Creamos un nuevo proceso en detalle de session
        """
        session = self.get_session()
        if session:
            return session.new_process_session(codename=codename)
        else:
            return None

    def clear_session(self):
        """
        Elimino todas las secciones abiertas
        """
        self.sessions_set.filter(enddate=None).update(enddate=now())

    def get_profile_codename_by_comercializadora(self, comercializadora):
        """
        Devuelve el codename del profile asociado a la comercializadora,
        en caso de no existir de devuelve el del usuarios
        """
        if comercializadora is not None:
            return comercializadora.get_type_codename()
        else:
            return self.profile.codename

    def get_query_set_groups(self, comercializadora):
        """
        Devuelte el querry_set de los grupos a los cuales tiene acceso el
        usuario con dicha comercializadora
        """
        profile_codename = self.get_profile_codename_by_comercializadora(
            comercializadora)

        from admin_permisologia.models import Groups
        if self.superuser is True:
            querry_set = Groups.objects.filter(
                permissions__profiles__codename=profile_codename
            ).distinct()
        else:
            querry_set = self.groups.all()

        return querry_set

    def get_query_set_permissions(self, comercializadora):
        """
        Devuelte el querry_set de permisos disponibles para el usuario
        """
        profile_codename = self.get_profile_codename_by_comercializadora(
            comercializadora)

        from admin_permisologia.models import Permissions

        if self.superuser is True:
            querry_set = Permissions.objects.filter(
                profiles__codename=profile_codename)
        else:
            querry_set = self.user_permissions.all()
            """
            obteniendo permisos por grupos asociados
            """
            for grupo in self.groups.all():
                querry_set |= grupo.permissions.filter(
                    profiles__codename=profile_codename)

        return querry_set.distinct()

    def get_check_permission(self, session_pk, comercializadora, menu):
        """
        Verifica el que el usuario tenga permisos de ver el url en cuestion
        """
        profile_codename = self.get_profile_codename_by_comercializadora(
            comercializadora)

        """
        #Verifica si los permisos estan en cache
        """
        enlaces = cache.get("menu_permission_{0}_{1}".format(
            self.pk, profile_codename))

        if enlaces is None:
            enlaces = {}

            if self.superuser is True:
                from admin_permisologia.models import Permissions
                for permisos in Permissions.objects.all():
                    if permisos.profiles.filter(codename=profile_codename).exists():
                        for permiso in permisos.menu.all():
                            json_menu = permiso.get_json()
                            enlaces["{0}".format(
                                json_menu.get("id"))] = json_menu
            else:
                """
                obteniendo permisos individuales asociados
                """
                for permisos in self.user_permissions.all():
                    if permisos.profiles.filter(codename=profile_codename).exists():
                        for permiso in permisos.menu.all():
                            json_menu = permiso.get_json()
                            enlaces["{0}".format(
                                json_menu.get("id"))] = json_menu

                """
                obteniendo permisos por grupos asociados
                """
                for grupo in self.groups.all():
                    for permisos in grupo.permissions.all():
                        if permisos.profiles.filter(codename=profile_codename).exists():
                            for permiso in permisos.menu.all():
                                json_menu = permiso.get_json()
                                enlaces["{0}".format(
                                    json_menu.get("id"))] = json_menu
            cache.set(
                "menu_permission_{0}_{1}".format(self.pk, profile_codename),
                enlaces,
                CACHES_CONF_TIME['registros_db']['menu_permisos']
            )
        """
        por ultimo se verifica si el menu asociado lo tiene disponible el user
        """
        if "{0}".format(menu.pk) in enlaces:
            return True
        else:
            return False

    def get_permissions(self, session_pk, comercializadora):
        """
        Verifica los permisos asociado al usuario con la comercializadora respectiva
        """
        profile_codename = self.get_profile_codename_by_comercializadora(
            comercializadora)

        """
        Verifica si el menu consultado ya esta e cache
        """
        enlaces = cache.get("menu_{0}_{1}".format(self.pk, profile_codename))

        if enlaces is None:
            enlaces_nivel_1 = {}
            enlaces_nivel_2 = {}
            enlaces_nivel_3 = {}

            if self.superuser is True:
                """
                si es super usuario tiene acceso a todos los permisos compatibles
                """
                from admin_permisologia.models import Permissions
                for permisos in Permissions.objects.all().prefetch_related('profiles'):
                    if permisos.profiles.filter(codename=profile_codename).exists():
                        for permiso in permisos.menu.filter(is_view=True):
                            json_menu = permiso.get_json()
                            if json_menu.get("type") == 1:
                                enlaces_nivel_1["{0}".format(
                                    json_menu.get("id"))] = json_menu
                            elif json_menu.get("type") == 2:
                                enlaces_nivel_2["{0}".format(
                                    json_menu.get("id"))] = json_menu
                            elif json_menu.get("type") == 3:
                                enlaces_nivel_3["{0}".format(
                                    json_menu.get("id"))] = json_menu
            else:
                """
                obteniendo permisos individuales asociados
                """
                for permisos in self.user_permissions.all():
                    if permisos.profiles.filter(codename=profile_codename).exists():
                        for permiso in permisos.menu.filter(is_view=True):
                            json_menu = permiso.get_json()
                            if json_menu.get("type") == 1:
                                enlaces_nivel_1["{0}".format(
                                    json_menu.get("id"))] = json_menu
                            elif json_menu.get("type") == 2:
                                enlaces_nivel_2["{0}".format(
                                    json_menu.get("id"))] = json_menu
                            elif json_menu.get("type") == 3:
                                enlaces_nivel_3["{0}".format(
                                    json_menu.get("id"))] = json_menu
                """
                obteniendo permisos por grupos asociados
                """
                for grupo in self.groups.all():
                    for permisos in grupo.permissions.all():
                        if permisos.profiles.filter(codename=profile_codename).exists():
                            for permiso in permisos.menu.filter(is_view=True):
                                json_menu = permiso.get_json()
                                if json_menu.get("type") == 1:
                                    enlaces_nivel_1[
                                        "{0}".format(json_menu.get("id"))
                                    ] = json_menu
                                elif json_menu.get("type") == 2:
                                    enlaces_nivel_2[
                                        "{0}".format(json_menu.get("id"))
                                    ] = json_menu
                                elif json_menu.get("type") == 3:
                                    enlaces_nivel_3[
                                        "{0}".format(json_menu.get("id"))
                                    ] = json_menu
            """
            agrupando los distintos niveles
            """
            for key3 in enlaces_nivel_3:
                obj = enlaces_nivel_3["{0}".format(key3)]
                enlaces_nivel_2["{0}".format(obj.get("suc"))][
                    "nodos"].append(obj)

            for key2 in enlaces_nivel_2:
                obj = enlaces_nivel_2["{0}".format(key2)]
                enlaces_nivel_1["{0}".format(obj.get("suc"))][
                    "nodos"].append(obj)

            enlaces = []
            for key1 in enlaces_nivel_1:
                enlaces.append(enlaces_nivel_1["{0}".format(key1)])

            """
            ordenando los niveles
            """
            def orden(obj):
                return obj.get("orden")
            enlaces.sort(key=orden)
            for enlace2 in enlaces:
                enlace2["nodos"].sort(key=orden)
                for enlace3 in enlace2["nodos"]:
                    enlace3["nodos"].sort(key=orden)

            cache.set(
                "menu_{0}_{1}".format(self.pk, profile_codename),
                enlaces,
                CACHES_CONF_TIME['registros_db']['menu_permisos']
            )
        return enlaces

    def get_user_comercializadoras(self):
        """
        Retorna las comercializadoras que estan asociadas al usuario
        """
        from admin_status.models import Status
        status_eliminado = Status.get_status_by_codename('status_eliminado').pk
        comercializadoras_user = self.comercializadora.all()\
            .exclude(bloque__status_id=status_eliminado)\
            .exclude(banca__status_id=status_eliminado)\
            .exclude(distribuidor__status_id=status_eliminado)\
            .exclude(agencia__status_id=status_eliminado)

        return comercializadoras_user

    def get_query_comercializadoras_level(self, profile=None):
        """
        Obtiene todas las comercializadoras del mismo nivel del usuario.

        Ejemplo: Usuario 'user1' es de tipo 'userprofile_operadora'
        se retornaran las comercializadoras asociadas a el de tipo Operadora

        Si el parametro profile, no es necesario consultar el objecto del usuario
        """

        if profile is None:
            profile = self.profile.codename
        kwargs = {}
        if profile == 'userprofile_master':
            return []
        elif profile == 'userprofile_operadora':
            kwargs['operadora__isnull'] = False
        elif profile == 'userprofile_bloque':
            kwargs['bloque__isnull'] = False
        elif profile == 'userprofile_banca':
            kwargs['banca__isnull'] = False
        elif profile == 'userprofile_distribuidor':
            kwargs['distribuidor__isnull'] = False
        elif profile == 'userprofile_agencia':
            kwargs['agencia__isnull'] = False

        from admin_status.models import Status
        status_eliminado = Status.get_status_by_codename('status_eliminado').pk
        comercializadoras = self.comercializadora.filter(**kwargs)\
            .exclude(bloque__status_id=status_eliminado)\
            .exclude(banca__status_id=status_eliminado)\
            .exclude(distribuidor__status_id=status_eliminado)\
            .exclude(agencia__status_id=status_eliminado)
        return comercializadoras


"""
#=============================================================
#=============================================================
#====================Modelos auditados========================
"""

auditoria.register(Users,)
"""
#=============================================================
#=============================================================
"""
