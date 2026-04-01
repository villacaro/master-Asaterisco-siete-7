from django.urls import reverse

# obtenemos el render que queremos adulterar
old_reverse = reverse


def new_reverse(self, lookup_view, **kwargs):
    url = old_reverse(lookup_view, **kwargs)
    if url:
        if self.info_user:
            from admin_principal.middleware import check_url, ignore_links
            if ignore_links(url) is False:
                if check_url(url=url,
                             object_user=self.object_user,
                             object_session=self.object_session,
                             object_comercializadora=self.object_comercializadora):
                    # hay permisos
                    pass
                else:
                    from admin_asterisco7.settings import PAGE_404_URL
                    url = PAGE_404_URL
    return url
