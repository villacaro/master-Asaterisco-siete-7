# -*- coding: utf-8 -*-

from io import StringIO

import pdfkit
import xhtml2pdf.pisa as pisa
from admin_asterisco7.settings import DEBUG, PROJECT_PATH
from django.contrib import messages
from django.core.cache import cache
from django.core.mail import send_mail
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import Context
from django.template.loader import get_template
from django.utils.timezone import now

"""
Mantener esta variable en true mientras se hacen pruebas con pdfs,
de lo contrario debera ser False
"""
PRINT_DEBUG = DEBUG


def PdfView(request, *args, **kwargs):
    """
    Vista generica para la impresion de pdf
    """
    if PRINT_DEBUG:
        var_cache = None
    else:
        var_cache = cache.get(kwargs.get('cache_key') + '-xhtml2pdf')
    if var_cache is not None:
        # en caso de ya existir el pdf generado se retorna de una vez
        return HttpResponse(var_cache, content_type='application/pdf')
    else:
        # aqui se procesa el pdf en su primer request

        def render_to_pdf(template_src, context_dict):
            """
            Genera un pdf dado un html con xhtml2pdf (pisa)
            """
            template = get_template(template_src)
            context = Context(context_dict)
            html = template.render(context)
            result = StringIO()
            pdf = pisa.pisaDocument(StringIO('{0}'.format(html)), result)
            if not pdf.err:
                xhtml2pdf_generate = result.getvalue()
                if not PRINT_DEBUG:
                    # guarda la nueva cache
                    cache.set(kwargs.get('cache_key') + '-xhtml2pdf', xhtml2pdf_generate, 60 * 60)
                    # elimina la cache anterior
                    cache.delete(kwargs.get('cache_key'))
                return HttpResponse(xhtml2pdf_generate, content_type='application/pdf')
            else:
                # en caso de error el pdf nunca se genera
                import cgi
                return HttpResponse('Han ocurrido algunos errores <pre>%s</pre>' % cgi.escape(html))

        var_cache = cache.get(kwargs.get('cache_key'))
        if var_cache is not None:
            # Si existe la data en cache se genera el pdf
            data = {
                'fecha': now(),
                'reporte': var_cache,
                'sistema': kwargs.get('object_sistema_juego'),
                'usuario': kwargs.get('object_user'),
                'comercializadora': kwargs.get('object_comercializadora'),
            }

            # ==============================================================================#
            #                               Example
            # ==============================================================================#
            """
            data['blog_entries'] = []
            for i in range(1,10):
                data['blog_entries'].append({
                    'id': i,
                    'title':'Playing with pisa 3.0.16 and dJango Template Engine',
                    'body':'This is a simple example..'
                    })
            return render_to_pdf('admin_lib/util_print/example-table.html', data)

            # ==============================================================================#
            # ==============================================================================#
            """
            return render_to_pdf(
                var_cache['template_name'],
                data
            )
        else:
            # En caso de no existir se envia un mensaje de error 404
            # pag no encontrada
            raise Http404


def CsvView(request, *args, **kwargs):
    """
       Vista generica para la impresion de csv

       Formato para los filtros de cadena
       ["Multibanca:","Multibanca1","Banca:","Banca1","Distribuidores:","Todos","Agencia:","Todos"]

       Formato para los titulos
       [{'text': 'Fecha'}, {'text': 'Dia de la semana'}]

       Para el cuerpo
       [{'pertenece':
            [{'html': True, 'class': '  link-red', 'val': '2015-04-28'},
            {'html': True, 'class': '  link-red', 'val': 'Martes'},
            {'html': False, 'class': 'text-align-right ', 'val': Decimal('0.00')}
        ]}

        Para el footer
        ['Total', ' ', 0, 0, 0, 0, 0, 0]

    """

    if PRINT_DEBUG:
        var_cache = None
    else:
        var_cache = cache.get(kwargs.get('cache_key') + '-csv')
    if var_cache is not None:
        return HttpResponse(var_cache, content_type='text/csv')
    else:
        import re

        def clean_string(cadena):
            if '</a>' in cadena:
                match = re.search(r'(<a.*>).*(</a>)', cadena)
                cadena = cadena.replace(match.group(1), '')
                cadena = cadena.replace(match.group(2), '')

            elif '</span>' in cadena:
                match = re.search(r'(<span.*>).*(</span>)', cadena)
                cadena = cadena.replace(match.group(1), '')
                cadena = cadena.replace(match.group(2), '')

            elif '</p>' in cadena:
                match = re.search(r'(<p.*>).*(</p>)', cadena)
                cadena = cadena.replace(match.group(1), '')
                cadena = cadena.replace(match.group(2), '')

            return cadena

        def render_to_xls(context):
            import xlwt
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename={0}.xls'.format(
                context['reporte']['titulo']
            )

            wb = xlwt.Workbook()
            writer = wb.add_sheet('Hoja1')

            # Style bold Cabecera
            font_style = xlwt.XFStyle()
            font_style.font.bold = True

            font_style_color = xlwt.XFStyle()
            font_style_color.font.bold = True
            pattern = xlwt.Pattern()
            pattern.pattern = xlwt.Pattern.SOLID_PATTERN
            pattern.pattern_fore_colour = xlwt.Style.colour_map['gray25']
            font_style_color.pattern = pattern

            writer.write(0, 0, context['reporte']['titulo'], font_style)
            writer.write(1, 0, 'Comercializadora:', font_style)
            writer.write(1, 1, context['reporte']['comercializador'])
            if context['reporte'].get("agrupado"):
                writer.write(2, 0, 'Agrupado:', font_style)
                writer.write(2, 1, context['reporte']['agrupado'])

            fechas = context['reporte']['fecha'].split("/")
            if len(fechas) == 1:
                writer.write(3, 0, 'Dia', font_style)
                writer.write(3, 1, fechas[0])
            elif len(fechas) == 2:
                writer.write(3, 0, 'Desde:', font_style)
                writer.write(3, 1, fechas[0])
                writer.write(3, 2, 'Hasta:', font_style)
                writer.write(3, 3, fechas[1])

            # Filtros Cadena
            row_num = 5
            if context['reporte'].get('filters_cadena'):
                col_num = 0
                for item in context['reporte']['filters_cadena']:
                    if col_num % 2 == 0:
                        writer.write(row_num, col_num, item, font_style)
                    else:
                        writer.write(row_num, col_num, item)
                    col_num += 1
                row_num += 2

            # Titulos
            col_num = 0
            for item in context['reporte']['titles']:
                writer.write(row_num, col_num, item['text'], font_style_color)
                writer.col(col_num).width = 4000
                col_num += 1

            # Cuerpo
            row_num += 1
            for item in context['reporte']['content']:
                col_num = 0
                for val in item['pertenece']:

                    if val:
                        if '</a>' in str(val['val']) or '</span>' in str(val['val']) or '</p>' in str(val['val']):
                            value = clean_string(val['val'])
                        else:
                            value = val['val']
                    else:
                        value = val

                    writer.write(row_num, col_num, value)
                    col_num += 1
                row_num += 1

            col_num = 0
            for item in context['reporte']['footer']:
                writer.write(row_num, col_num, item, font_style_color)
                col_num += 1

            wb.save(response)
            return response

        def render_to_csv(context):
            import csv
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="{0}.csv"'.format(
                context['reporte']['titulo']
            )

            writer = csv.writer(response, delimiter=';')

            # Cabecera
            writer.writerow([context['reporte']['titulo']])
            writer.writerow(['Fecha:', context['reporte']['fecha']])
            writer.writerow([''])

            # Titulos
            row = []
            for item in context['reporte']['titles']:
                row.append(item['text'])
            writer.writerow(row)

            # Cuerpo
            for item in context['reporte']['content']:
                row = []
                for val in item['pertenece']:
                    if '</a>' in str(val['val']) or '</span>' in str(val['val']):
                        row.append(clean_string(val['val']))
                    else:
                        row.append(val['val'])
                writer.writerow(row)

            # Footer
            row = []
            for item in context['reporte']['footer']:
                row.append(item)
            writer.writerow(row)
            return response

        var_cache = cache.get(kwargs.get('cache_key'))
        if var_cache is not None:
            # Si existe la data en cache se genera el pdf
            data = {
                'fecha': now(),
                'reporte': var_cache,
                'sistema': kwargs.get('object_sistema_juego'),
                'usuario': kwargs.get('object_user'),
                'comercializadora': kwargs.get('object_comercializadora'),
            }
            return render_to_xls(
                data
            )
        else:
            raise Http404


def EmailView(request, *args, **kwargs):

    if PRINT_DEBUG:
        var_cache = None
    else:
        var_cache = cache.get(kwargs.get('cache_key') + '-email')
    # if var_cache is not None:
        # raise Http404
        # return HttpResponse(var_cache, content_type='text/csv')
    # else:

    def render_to_email(template_src, context_dict, to_email):
        template = get_template(template_src)
        context = Context(context_dict)
        html = template.render(context)

        send_mail(
            'Detalle de comercializadora',
            'Here is the message.',
            '',
            [to_email],
            fail_silently=False,
            html_message=html
        )

    var_cache = cache.get(kwargs.get('cache_key'))
    if var_cache is not None:
        data = {
            'fecha': now(),
            'usuario': kwargs.get('object_user'),
            'comercializadora': kwargs.get('object_comercializadora'),
            'reporte': var_cache,
        }
        render_to_email(
            var_cache['template_name'],
            data,
            var_cache['email']
        )

        messages.success(
            request,
            "¡Enhorabuena! Correo enviado con exito a la direccion {0}".format(
                var_cache['email']
            )
        )
        return HttpResponseRedirect(var_cache['reverse'])
    else:
        raise Http404


def PdfKitView(request, *args, **kwargs):
    """
    Vista generica para la impresion de pdf
    """
    if PRINT_DEBUG:
        var_cache = None
    else:
        var_cache = cache.get(kwargs.get('cache_key') + '-pdfkit')
    if var_cache is not None:
        # en caso de ya existir el pdf generado se retorna de una vez
        return HttpResponse(var_cache, content_type='application/pdf')
    else:
        # aqui se procesa el pdf en su primer request

        def render_to_pdf(template_src, context_dict):
            """
            Genera un pdf dado un html con pdfkit
            """
            template = get_template(template_src)
            context = Context(context_dict)
            html = template.render(context)

            options = {
                'page-size': 'A4',
                'encoding': "UTF-8",
            }

            css = 'admin_asterisco7/static/css/style.css'
            pdf = pdfkit.from_string(html, False, css=css, options=options)
            if not PRINT_DEBUG:
                cache.set(kwargs.get('cache_key') + '-pdfkit', pdf, 60 * 60)
                cache.delete(kwargs.get('cache_key'))
            return HttpResponse(pdf, content_type='application/pdf')

        var_cache = cache.get(kwargs.get('cache_key'))
        if var_cache is not None:
            # Si existe la data en cache se genera el pdf
            data = {
                'fecha': now(),
                'reporte': var_cache,
                'sistema': kwargs.get('object_sistema_juego'),
                'usuario': kwargs.get('object_user'),
                'comercializadora': kwargs.get('object_comercializadora'),
                'path': PROJECT_PATH,
            }
            return render_to_pdf(
                var_cache['template_name'],
                data
            )
        else:
            raise Http404
