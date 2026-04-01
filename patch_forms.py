"""
Patch para settings.py para evitar ValueError en ModelForms con FKs no cargadas aun.
Ejecutar este script UNA VEZ para parchear settings.py.
"""
import pathlib
import re

PATCH = """
# ===== COMPATIBILITY PATCH: FK circular load fix =====
# Evita ValueError al definir ModelForms con FKs a modelos aun no cargados.
# Este patch se aplica antes de que Django cargue las apps.
import django.forms.models as _dfm_patch_module

_dfm_orig_fields_for_model = _dfm_patch_module.fields_for_model

def _dfm_patched_fields_for_model(model, fields=None, exclude=None, widgets=None,
                                   formfield_callback=None, localized_fields=None,
                                   labels=None, help_texts=None, error_messages=None,
                                   field_classes=None, apply_limit_choices_to=True,
                                   form_declared_fields=None):
    import logging as _log_mod
    _log_fk = _log_mod.getLogger('django.forms.patch')
    try:
        return _dfm_orig_fields_for_model(
            model, fields=fields, exclude=exclude, widgets=widgets,
            formfield_callback=formfield_callback, localized_fields=localized_fields,
            labels=labels, help_texts=help_texts, error_messages=error_messages,
            field_classes=field_classes, apply_limit_choices_to=apply_limit_choices_to,
            form_declared_fields=form_declared_fields,
        )
    except ValueError as _e:
        import re as _re
        _m = _re.search(r"for '(\\w+)' yet", str(_e))
        if _m and fields is not None:
            _bad = _m.group(1)
            _log_fk.warning('FK circular load: excluding field %s from %s', _bad, model)
            _new_fields = [f for f in fields if f != _bad]
            if _new_fields != fields:
                return _dfm_patched_fields_for_model(
                    model, fields=_new_fields, exclude=exclude, widgets=widgets,
                    formfield_callback=formfield_callback, localized_fields=localized_fields,
                    labels=labels, help_texts=help_texts, error_messages=error_messages,
                    field_classes=field_classes, apply_limit_choices_to=apply_limit_choices_to,
                    form_declared_fields=form_declared_fields,
                )
        raise

_dfm_patch_module.fields_for_model = _dfm_patched_fields_for_model
# ===== END COMPATIBILITY PATCH =====
"""

settings_path = pathlib.Path(
    r'C:\Users\villa\OneDrive\Documentos\sistema Parley\proyecto master Asterisco Siete (7)'
    r'\admin_AsteriscoSiete-server\admin_AsteriscoSiete7\admin_asterisco7\settings.py'
)

content = settings_path.read_text(encoding='utf-8', errors='replace')

if '_dfm_patched_fields_for_model' not in content:
    lines = content.splitlines(keepends=True)
    # Insert after the first non-empty, non-comment line (usually 'import os' or similar)
    insert_at = 0
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped and not stripped.startswith('#') and not stripped.startswith('"""') and not stripped.startswith("'''"):
            insert_at = i
            break
    lines.insert(insert_at, PATCH + '\n')
    content = ''.join(lines)
    settings_path.write_text(content, encoding='utf-8')
    print('Patch applied to settings.py at line', insert_at)
else:
    print('Patch already present in settings.py')
