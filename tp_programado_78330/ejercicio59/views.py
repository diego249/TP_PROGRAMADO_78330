from django.shortcuts import render
from .forms import ParametersForm
from django.views import generic
import numpy as np

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

        matriz = [[''] * 29 for f in range(1)]
        reloj = 0

        while reloj <= fin:
            if reloj <= relojFin and reloj >= relojInicio:
                matriz[-1][0] = 0
                matriz[-1][1] = 0
                matriz[-1][2] = 0
                matriz[-1][3] = 0
                matriz[-1][4] = 0
                matriz[-1][5] = 0
                matriz[-1][6] = 0
                matriz[-1][7] = 0
                matriz[-1][8] = 0
                matriz[-1][9] = 0
                matriz[-1][10] = 0
                matriz[-1][11] = 0
                matriz[-1][12] = 0
                matriz[-1][13] = 0
                matriz[-1][14] = 0
                matriz[-1][15] = 0
                matriz[-1][16] = 0
                matriz[-1][17] = 0
                matriz[-1][18] = 0
                matriz[-1][19] = 0
                matriz[-1][20] = 0
                matriz[-1][21] = 0
                matriz[-1][22] = 0
                matriz[-1][23] = 0
                matriz[-1][24] = 0
                matriz[-1][25] = 0
                matriz[-1][26] = 0
                matriz[-1][27] = 0
                matriz[-1][28] = 0
                reloj += 1
                vector_temporal = [''] * len(matriz[0])
                matriz = np.vstack([matriz, vector_temporal])


        return render(self.request, self.template_name, {"matrizResultado": matriz, "vectorEntrada": [fin, relojInicio, relojFin]
        })
