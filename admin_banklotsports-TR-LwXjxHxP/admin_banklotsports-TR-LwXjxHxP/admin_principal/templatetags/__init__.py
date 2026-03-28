# -*- coding: utf-8 -*-

from django.template.defaulttags import URLNode

# obtenemos el render que queremos adulterar
old_render = URLNode.render


def new_render(self, context):
    """
    Sobrescribiendo el url tags de django para poder agregar
    codigo a la funcion del render.
    """
    # ejecutamos el render adulterado y procedemos a escribir
    # seguidamente el codigo que necesitamos
    url = old_render(self, context)
    if not url and self.asvar:
        url = context[self.asvar]

    if url:
        if 'info_user' in context:
            from admin_principal.middleware import check_url, ignore_links
            if ignore_links(url) is False:
                if check_url(url=url,
                             object_user=context['info_user']['user'],
                             object_session=context['info_user']['session'],
                             object_comercializadora=context['info_user']['comercializadora']):
                    # hay permisos
                    pass
                else:
                    from admin_banklotsports.settings import PAGE_404_URL
                    url = PAGE_404_URL
    if self.asvar:
        context[self.asvar] = url
        return ''
    else:
        return url

# reemplazamos el render original por el que acabamos de definir


URLNode.render = new_render
