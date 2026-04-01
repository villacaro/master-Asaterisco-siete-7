# -*- coding: utf-8 -*-
import errno
import os

from django import forms
from django.conf import settings

from .models import Theme


class ThemeForm(forms.ModelForm):

    class Meta:
        model = Theme
        fields = [
            'name',
            'codename',
            'description',
            'screenshoot'
        ]

    def makedir(self, path):
        try:
            os.makedirs(path)
        except OSError as exc:
            if exc.errno == errno.EEXIST:
                pass
            else:
                raise

    def save(self, commit=True, *args, **kwargs):
        super(ThemeForm, self).save(commit=False, *args, **kwargs)

        codename = self.cleaned_data.get('codename')
        template_dir = "/admin_principal/templates/themes/{0}/".format(codename)
        static_url = "/admin_asterisco7/static/themes/{0}/".format(codename)
        media_url = "/admin_asterisco7/media/themes/{0}/".format(codename)

        base_dir = getattr(settings, 'BASE_DIR', None)

        template_dir_path = "{0}{1}".format(base_dir, template_dir)
        static_url_path = "{0}{1}".format(base_dir, static_url)
        media_url_path = "{0}{1}".format(base_dir, media_url)

        self.makedir(template_dir_path)
        self.makedir(static_url_path)
        self.makedir(media_url_path)

        # Asigna las url y template_dir con el codename
        self.instance.template_dir = template_dir
        self.instance.static_url = static_url
        self.instance.media_url = media_url

        return self.instance
