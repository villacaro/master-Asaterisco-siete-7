# -*- coding: utf-8 -*-
from admin_banklotsports.settings import FORMAT_STR_DATETIME
from admin_juego.models import EventNotification
# from admin_lib.util_json import JsonDumps
from admin_lib.util_views import MyViewBase
from django.contrib import messages
from django.utils.timezone import now
from django.views.generic import ListView


# Eventos en redis
# from admin_banklotsports.settings import redis_event, FORMAT_STR_DATETIME


class EventNotificationView(MyViewBase):
    model = EventNotification


class EventNotificationListView(EventNotificationView, ListView):

    def get_queryset_filter(self):
        self.get_object_sistema_logros()
        if self.object_sistema_logros.pk == self.object_sistema_juego.pk:
            querryset = EventNotification.objects.filter(
                sistema=self.object_sistema_juego.pk
            )
        else:
            querryset = EventNotification.objects.filter(
                sistema__in=[self.object_sistema_juego.pk, self.object_sistema_logros.pk]
            )
        return querryset

    def get_queryset(self):
        querryset = self.get_queryset_filter()
        return querryset.filter(in_production=False).order_by("data_origin")

    def get(self, request, *args, **kwargs):
        self.object_list = self.model.objects.none()
        context = self.get_context_data()
        context["actualizaciones"] = self.get_queryset().count()
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        if request.POST.get("detalle") == '':
            self.object_list = self.get_queryset()
            context = self.get_context_data()
            context["actualizaciones"] = self.get_queryset().count()
            return self.render_to_response(context)
        else:

            pks = request.POST.getlist("objetos")
            if len(pks) == 0:
                for pk in self.get_queryset():
                    pks.append(pk.pk)
            # objs_para_redis = {}
            # objs_para_redis["0"] = { "hora": None, "data": [] }
            date_production = now()

            def get_date_production_old(querryset):
                querryset = querryset.filter(in_production=True).order_by("-date_production")

                if querryset.exists():
                    return querryset[0].date_production.strftime(FORMAT_STR_DATETIME)

                return None

            old_date = get_date_production_old(self.get_queryset_filter())
            if old_date:
                if date_production.strftime(FORMAT_STR_DATETIME) == old_date:
                    messages.warning(
                        request,
                        "No se pueden poner en producción nuevas actualizaciones "
                        "con menos de 1 minuto de diferencia, debe esperar dicho "
                        "tiempo para realizar esta acción."
                    )

                    return EventNotificationListView.get(self, request, *args, **kwargs)
            else:
                pass

            # continua el proceso normal, en caso de no estar lanzando producciones
            # en el mismo minuto

            for pk in pks:
                try:
                    obj = self.get_queryset_filter().get(
                        pk=pk,
                        in_production=False,
                    )

                    obj.in_production = True
                    obj.date_production = date_production

                    obj.save(
                        update_fields=["in_production", "date_production"]
                    )

                except EventNotification.DoesNotExist:
                    pass

            if pks:
                messages.info(
                    request,
                    "{0} actualizacion(es) enviada(s) con éxito".format(len(pks))
                )

            """
            if len( objs_para_redis ) or len(objs_para_redis["0"]["data"]):
                if not len( objs_para_redis["0"]["data"] ):
                    del objs_para_redis["0"]
                # enviando datos a redis,
                # q son capturados en nodejs y los envia a las taquillas
                redis_event.publish(
                    "notificacion_games",
                    JsonDumps(  objs_para_redis  )
                )
            """
            return EventNotificationListView.get(self, request, *args, **kwargs)
