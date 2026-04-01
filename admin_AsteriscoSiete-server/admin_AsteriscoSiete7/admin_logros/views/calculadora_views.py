from admin_lib.util_views import MyViewBase
from admin_logros.forms import CalculadoraForm
from django.views.generic import FormView


class CalculadoraView(MyViewBase, FormView):
    template_name = "admin_logros/calculadora/calculadora_form.html"
    form_class = CalculadoraForm
