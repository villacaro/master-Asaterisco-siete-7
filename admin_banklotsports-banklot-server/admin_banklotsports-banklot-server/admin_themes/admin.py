from django.contrib import admin

from .forms import ThemeForm
from .models import Color, Company, Theme


# Register your models here.
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name',)


@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'description',)
    form = ThemeForm


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('pk', 'theme', 'color', 'color_type',)
