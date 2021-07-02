from django.shortcuts import render
from .forms import ParametersForm
from django.views import generic

# Create your views here.
def index(request):
    return render(request, "index.html")

class simulacion(generic.FormView):
    form_class = ParametersForm
    template_name = 'ejercicio59.html'

    def form_valid(self, form):
        # parametros de entrada por form
        fin = form.cleaned_data['fin']
        relojFin = form.cleaned_data['min_fin']
        relojInicio = form.cleaned_data['min_inicio']

        return render(self.request, self.template_name, {
                                                         "vectorEntrada": [fin, relojInicio, relojFin]
        })
