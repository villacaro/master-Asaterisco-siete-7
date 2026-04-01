# -*- coding: utf-8 -*-
from admin_asterisco7.settings import CACHES_CONF_TIME
from admin_historic import auditoria
from admin_historic.models import choices_apps
from django.core.cache import cache
from django.db import models
from jsonfield import JSONField


class Menu(models.Model):

    """Define los campos correspondientes al modelo de un menu en base de datos.

    Definicion de campo:
        name: nombre del menu
        codename: codigo del nombre del menu, generalmente es el mismo codename del url
        url: url como tal de menu en cuetion
        icon: icono del menu
        content_type: tipo de contenido, o propiamente tipo de nivel, posibles valores
            1:'Nivel 1: Titulo o seccion del menu'
            2:'Nivel 2: de Submenu o subtitulo'
            3:'Nivel 3: de enlace'
        orden: entero que indica el orden de presedencia en el cual se imprime el menu
        is_view: este campo indica si el menu es de vista, por ejemplo si se puede ver en el menu.
        is_public: este campo indica si es un link de origen publico, como por ejemplo el login.
        is_is_global: este campo indica que la vista es global, osea para todos los usuarios
                    sin necesidad de definirla en permisos, pero si debe haber un usuario
                    autentificado.
        created_at y updated_at: registros de creacion y actualizacion.

    """

    name = models.CharField(
        max_length=160,
        null=True,
        blank=True,
        verbose_name='Titulo '
    )
    codename = models.CharField(
        max_length=160,
        verbose_name='Codigo ',
        db_index=True,
    )
    url = models.CharField(
        max_length=160,
        null=True,
        blank=True,
        verbose_name='Url ',
        db_index=True,
    )
    menu_suc = models.ForeignKey(
        'admin_permisologia.Menu',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )
    icon = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name='Icono '
    )

    choices_conten_types = (
        (1, 'Titulo princial.'),
        (2, 'Subtitulo.'),
        (3, 'Enlace.'),
    )

    content_type = models.IntegerField(
        choices=choices_conten_types,
        null=True,
        blank=True,
        verbose_name='Nivel '
    )

    orden = models.IntegerField(
        default=0,
        verbose_name='Orden '
    )
    is_view = models.BooleanField(
        default=False,
        verbose_name='Visible '
    )
    is_public = models.BooleanField(
        default=False,
        verbose_name='PÃºblico '
    )
    is_global = models.BooleanField(
        default=False,
        verbose_name='Global ',
        help_text='Enlace privado, pero global'
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
        db_tablespace = 'ts_comer'
        verbose_name = 'Menu (url)'
        verbose_name_plural = 'Menus (enlaces)'
        unique_together = ('codename', 'url')
        ordering = ['orden', ]

    def __str__(self):
        """
        Retorna el nombre del menu
        """
        if self.menu_suc is None:
            return self.name
        else:
            if self.menu_suc.menu_suc is None:
                return '{0} | {1}'.format(
                    self.menu_suc.name,
                    self.name
                )
            else:
                return '{0} | {1} | {2}'.format(
                    self.menu_suc.menu_suc.name,
                    self.menu_suc.name,
                    self.name
                )

    def save(self, *args, **kwargs):
        super(Menu, self).save(*args, **kwargs)

    def get_json(self):
        """Retorna un json.
        Retorna el menu en formato json
        """
        return {
            'id': self.pk,
            'codename': self.codename,
            'name': self.name,
            'type': self.content_type,
            'orden': self.orden,
            'url': self.url,
            'icon': self.icon,
            'suc': self.menu_suc.pk if self.menu_suc is not None else 0,
            'nodos': []
        }

    @staticmethod
    def get_search(url):
        """Retorna una url.

        Retorna el menu dado un url, si no encuentra coincidencias por el menu,
        intenta buscar por su codename.
        """
        from django.urls import resolve
        resolve_name = resolve(url).url_name
        menu = cache.get(
            'menu_{0}'.format(resolve_name)
        )
        if not menu:
            menu = cache.get(
                'menu_{0}'.format(url)
            )

        if not menu:
            try:
                menu = Menu.objects.only(
                    'is_public', 'is_global').get(
                    codename=resolve_name)
                cache.set(
                    'menu_{0}'.format(resolve_name),
                    menu,
                    CACHES_CONF_TIME['registros_db']['menu']
                )
            except Exception:
                menu = Menu.objects.only('is_public', 'is_global').get(url=url)
                cache.set(
                    'menu_{0}'.format(url),
                    menu,
                    CACHES_CONF_TIME['registros_db']['menu']
                )
        return menu

    @staticmethod
    def register(
        name=None, codename='', url=None, menu_suc=None,
        icon=None, content_type=3, orden=0, is_view=False,
        is_public=False, is_global=False
    ):

        return Menu.objects.update_or_create(
            codename=codename, url=url,
            defaults={
                'name': name,
                'menu_suc': menu_suc,
                'icon': icon,
                'content_type': content_type,
                'orden': orden,
                'is_view': is_view,
                'is_public': is_public,
                'is_global': is_global,
            }
        )[0]


class Permissions(models.Model):

    """Definicion de los posibles Permisos.

    Estructura en db:
        name: nombre del permiso

        codename: codigo reservado para permisos en particular

        content_type: Este tipo de codigo referencia a las app instaladas

        menu: posibles enlaces hacia en menu de un permiso, por ejempplo crear operadora
            tiene el menu completo con los 3 enlaces
            de titulo, de submenu y el enlace como tal.

        profiles: son los perfiles de usuarios para los que estara disponible el permiso

        created_at y updated_at: registros de creacion y actualizacion.
    """

    name = models.CharField(
        max_length=160,
        unique=True,
        verbose_name='Nombre '
    )
    codename = models.CharField(
        max_length=160,
        unique=True,
        verbose_name='Codigo ',
        editable=False)

    content_type = models.CharField(
        max_length=50,
        choices=choices_apps,
        verbose_name='App '
    )

    menu = models.ManyToManyField(
        Menu,
        verbose_name='Vistas asociadas '
    )
    profiles = models.ManyToManyField(
        'admin_users.UserProfile',
        verbose_name='Perfiles asociados '
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
        db_tablespace = 'ts_comer'
        verbose_name = 'Permiso'
        verbose_name_plural = 'Permisos'
        ordering = ['content_type', 'name']

    def __str__(self):
        """
        Retorna el nombre del permiso concatenado con la app en custion y el nombre del modelo
        """
        return self.get_content_type_display() + ' | ' + self.name

    def save(self, *args, **kwargs):
        super(Permissions, self).save(*args, **kwargs)

    @staticmethod
    def register(name, codename, content_type, menus, profiles):
        from admin_users.models import UserProfile
        permiso = Permissions.objects.update_or_create(
            codename=codename,
            defaults={
                'name': name,
                'content_type': content_type,
            }
        )[0]

        """agrega los menus al permiso"""
        for menu in menus:
            if not permiso.menu.filter(pk=menu.pk).exists():
                permiso.menu.add(menu)

        """agrega los profiles al permiso"""

        """Agregando profiles"""
        for profile in profiles:
            permiso.profiles.add(UserProfile.objects.get(codename=profile))

        """Eliminando profiles desasociado"""
        for profile in permiso.profiles.values_list('codename', flat=True):
            if profile not in profiles:
                permiso.profiles.remove(
                    UserProfile.objects.get(
                        codename=profile
                    )
                )

        return permiso


class Groups(models.Model):

    """Definicion de Grupos.

    Los grupos, son perfiles precargados con varios permisos asociados a uno o muchos usuarios.

    Estructura en DB:
        name: nombre del grupo
        codename: codigo en texto, para manejar los grupos por un key
        permissions: permisos asociados al grupo, estos pueden ser varios
        created_at y updated_at: registros de creacion y actualizacion.
    """

    name = models.CharField(
        verbose_name='Nombre del grupo (*)',
        unique=True,
        max_length=160
    )
    codename = models.CharField(
        verbose_name='Codename (*)',
        max_length=160,
        unique=True,
        editable=False
    )
    permissions = models.ManyToManyField(
        Permissions,
        verbose_name='Permisos asociados (*)'
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
        db_tablespace = 'ts_comer'
        verbose_name = 'Grupo'
        verbose_name_plural = 'Grupos'
        ordering = ['name', ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.codename = self.name.lower().replace(' ', '_')
        super(Groups, self).save(*args, **kwargs)
        cache.clear()

    # @models.permalink (eliminado en Django 3.1)
    def get_absolute_url(self):
        from django.urls import reverse, NoReverseMatch
        try:
            return reverse('admin_permisologia_groups_detail', kwargs={'pk': self.pk})
        except NoReverseMatch:
            return '/admin/'

    @staticmethod
    def register(name, codename, permissions):
        # Metodo inulitizado, por reglas de negocio no se
        # registraran grupos por defecto
        return
        """
        try:
            grupo = Groups.objects.get(name=name)
        except Groups.DoesNotExist:
            grupo = Groups.objects.create(name=name)
            # agrega los permisos al grupo
            for permiso in permissions:
                if not grupo.permissions.filter(pk=permiso.pk).exists():
                    grupo.permissions.add(permiso)
        """


class PermissionsSales(models.Model):

    """Permisos de ventas
    Definicion: Tabla que almacena las restricciones de ventas por juego de
    algun ente de la comercializacion

    Estructura en db:

    """

    deporte = models.ForeignKey(
        'admin_juego.TipoProducto',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )

    grupo = models.ForeignKey(
        'admin_juego.GruposSorteo',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )

    modalidad = models.ForeignKey(
        'admin_juego.ModalidadJuego',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )

    comercializadora = models.ForeignKey(
        'admin_finanzas.Comercializadora',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )

    breaking = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        editable=False,
    )

    audit_exclude = ('breaking',)

    class Meta:
        db_tablespace = 'ts_comer'
        verbose_name = 'Permiso Venta'
        verbose_name_plural = 'Permisos ventas'

    def __str__(self):
        if self.modalidad:
            return 'Restriccion de {0} | {1} | {2} para {3}'.format(
                self.deporte, self.grupo, self.modalidad, self.comercializadora)
        elif self.grupo:
            return 'Restriccion de {0} | {1} para {2}'.format(
                self.deporte, self.grupo, self.comercializadora)
        elif self.deporte:
            return 'Restriccion de {0} para {1}'.format(
                self.deporte, self.comercializadora)
        return ''

    def save(self, *args, **kwargs):
        super(PermissionsSales, self).save(*args, **kwargs)
        cache.delete('permissionssales_{0}_{1}_{2}_{3}'.format(
            self.comercializadora_id,
            self.deporte_id,
            self.grupo_id,
            self.modalidad_id,
        ))

    def delete(self):
        cache.delete('permissionssales_{0}_{1}_{2}_{3}'.format(
            self.comercializadora_id,
            self.deporte_id,
            self.grupo_id,
            self.modalidad_id,
        ))
        super(PermissionsSales, self).delete()

    def get_ref_related_historic(self):
        """
        Retorna una relacion de referencia, hacia el modelo donde se crea,
        pertenece la instancia actual
        """
        return '{0}.{1}.{2}'.format(
            self.comercializadora.get_object().__module__.split('.')[0],
            self.comercializadora.get_object().__class__.__name__.lower(),
            self.comercializadora.get_object_id()
        )


class PermissionsSalesRestrictions(models.Model):

    """Permisos de ventas
    Definicion: Tabla que almacena las restricciones de ventas por modalidad
    algun ente de la comercializacion

    Estructura en db:

    """
    comercializadora = models.ForeignKey(
        'admin_finanzas.Comercializadora',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )

    deporte = models.ForeignKey(
        'admin_juego.TipoProducto',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )

    restrictions = JSONField(
        null=True,
        blank=True,
        verbose_name='Restricciones'
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
        db_tablespace = 'ts_comer'
        verbose_name = 'Permiso Venta (Restricciones)'
        verbose_name_plural = 'Permisos ventas (Restricciones)'

    def __str__(self):
        return 'Restriccion en {0} para {1}'.format(self.deporte, self.comercializadora)

    def save(self, *args, **kwargs):
        super(PermissionsSalesRestrictions, self).save(*args, **kwargs)
        cache.delete('permissionssalesrestrictions_{0}_{1}'.format(
            self.comercializadora_id, self.deporte_id))

    def delete(self):
        cache.delete('permissionssalesrestrictions_{0}_{1}'.format(
            self.comercializadora_id, self.deporte_id,))
        super(PermissionsSalesRestrictions, self).delete()

    def get_ref_related_historic(self):
        """
        Retorna una relacion de referencia, hacia el modelo donde se crea,
        pertenece la instancia actual
        """
        return '{0}.{1}.{2}'.format(
            self.comercializadora.get_object().__module__.split('.')[0],
            self.comercializadora.get_object().__class__.__name__.lower(),
            self.comercializadora.get_object_id()
        )


"""
# =============================================================
# =============================================================
# ====================Modelos auditados========================
"""
auditoria.register(Groups, PermissionsSales, PermissionsSalesRestrictions)
