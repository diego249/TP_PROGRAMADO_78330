from django.shortcuts import render
from .forms import ParametersForm
from django.views import generic
import numpy as np
from . import clases

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
        proxima_llegada = 0
        eventos = ["Inicialización", "Llegada Cliente", "Fin Asignacion", "Fin Entrega Pedido", "Fin Turno", "Fin Impresion", "Fin Cobro"]
        evento = ''
        init = True
        llegada_cliente = False
        asignacion_cliente = False
        pedido_cliente = False
        fin_turno_cliente = False
        impresion_cliente = False
        cobro_cliente = False
        id_cliente = 0
        clientes = []

        bandera = False

        min1 = 100000
        min2 = 0

        #servidores
        estados_encargado = ['Libre', 'Ocupado']
        estados_terminales = ['Libre', 'Disponible', 'Ocupado']
        estados_mozo = ['Libre', 'Ocupado']
        estados_impresora = ['Libre', 'Ocupado']
        terminal1 = clases.Terminal(1, estados_terminales[0], 1)
        terminal2 = clases.Terminal(2, estados_terminales[0], 1)
        terminal3 = clases.Terminal(3, estados_terminales[0], 1)
        encargado = clases.Encargado(1, estados_encargado[0], 1, 0, 0, terminal1, terminal2, terminal3)
        mozo = clases.Mozo(1, estados_mozo[0], 1, 0)
        impresora = clases.Impresora(1, estados_impresora[0], 1, 0)
        clientes_completados = 0
        ac_costo = 0
        promedio = 0


        while reloj <= fin:

            if init:
                evento = eventos[0]
                proxima_llegada = reloj + 15
                init = False

            elif llegada_cliente:
                evento = eventos[1]
                proxima_llegada = reloj + 15
                id_cliente += 1
                clientes.append(clases.Cliente(id_cliente, encargado, mozo, impresora))

                matriz_cliente = [[''] * 5 for f in range(len(matriz))]
                matriz = np.hstack((matriz, matriz_cliente))
                for cliente in clientes:
                    cliente.ejecutar(reloj)

            else:
                if asignacion_cliente:
                    evento = eventos[2]
                    asignacion_cliente = False

                elif pedido_cliente:
                    evento = eventos[3]
                    pedido_cliente = False

                elif fin_turno_cliente:
                    evento = eventos[4]
                    fin_turno_cliente = False

                elif impresion_cliente:
                    evento = eventos[5]
                    impresion_cliente = False

                elif cobro_cliente:
                    evento = eventos[6]
                    cobro_cliente = False

                for cliente in clientes:
                    cliente.ejecutar(reloj)

            if reloj <= relojFin and reloj >= relojInicio:
                matriz[-1][0] = evento
                matriz[-1][1] = reloj
                matriz[-1][2] = proxima_llegada
                matriz[-1][3] = encargado.fin_asignacion
                matriz[-1][4] = encargado.estado
                matriz[-1][5] = encargado.cola
                matriz[-1][6] = encargado.cola_asig
                matriz[-1][7] = encargado.tiempo_turno
                matriz[-1][8] = encargado.importe
                matriz[-1][9] = terminal1.estado
                matriz[-1][10] = terminal1.tiempo_liberacion
                matriz[-1][11] = terminal2.estado
                matriz[-1][12] = terminal2.tiempo_liberacion
                matriz[-1][13] = terminal3.estado
                matriz[-1][14] = terminal3.tiempo_liberacion
                matriz[-1][15] = mozo.estado
                matriz[-1][16] = mozo.fin_entrega
                matriz[-1][17] = impresora.estado
                matriz[-1][18] = impresora.fin_impresion

                matriz[-1][19] = 0
                matriz[-1][20] = 0
                matriz[-1][21] = 0
                matriz[-1][22] = 0
                matriz[-1][23] = 0
                for i in range(id_cliente):
                    matriz[-1][24 + (i * 5)] = clientes[i].estado
                    matriz[-1][25 + (i * 5)] = '$' + str(clientes[i].gasto_individual)
                    matriz[-1][26 + (i * 5)] = clientes[i].nro_terminal
                    matriz[-1][27 + (i * 5)] = clientes[i].en_cola_asig
                    matriz[-1][28 + (i * 5)] = clientes[i].tiempo_asignacion

                vector_temporal = [''] * len(matriz[0])
                matriz = np.vstack([matriz, vector_temporal])

            # logico proximo evento
            temporal_tiempo = proxima_llegada
            llegada_cliente = True

            for cliente in clientes:
                if cliente.tiempo_asignacion != '':
                    if cliente.tiempo_asignacion < temporal_tiempo and cliente.estado == "SA":
                        llegada_cliente = False
                        asignacion_cliente = True
                        pedido_cliente = False
                        fin_turno_cliente = False
                        impresion_cliente = False
                        cobro_cliente = False
                        temporal_tiempo = cliente.tiempo_asignacion


                if cliente.tiempo_fin_turno != '':
                    if cliente.tiempo_fin_turno < temporal_tiempo and cliente.estado == "ET":
                        llegada_cliente = False
                        asignacion_cliente = False
                        pedido_cliente = False
                        fin_turno_cliente = True
                        impresion_cliente = False
                        cobro_cliente = False
                        temporal_tiempo = cliente.tiempo_fin_turno


                if cliente.tiempo_entrega_pedido != '':
                    if cliente.tiempo_entrega_pedido < temporal_tiempo and cliente.estado == "ET":
                        llegada_cliente = False
                        asignacion_cliente = False
                        pedido_cliente = True
                        fin_turno_cliente = False
                        impresion_cliente = False
                        cobro_cliente = False
                        temporal_tiempo = cliente.tiempo_entrega_pedido


                if cliente.tiempo_fin_impresion != '':
                    if cliente.tiempo_fin_impresion < temporal_tiempo and cliente.estado == "SI":
                        llegada_cliente = False
                        asignacion_cliente = False
                        pedido_cliente = False
                        fin_turno_cliente = False
                        impresion_cliente = True
                        cobro_cliente = False
                        temporal_tiempo = cliente.tiempo_fin_impresion


                if cliente.tiempo_fin_cobro != '':
                    if cliente.tiempo_fin_cobro < temporal_tiempo and cliente.estado == "SC":
                        llegada_cliente = False
                        asignacion_cliente = False
                        pedido_cliente = False
                        fin_turno_cliente = False
                        impresion_cliente = False
                        cobro_cliente = True
                        temporal_tiempo = cliente.tiempo_fin_cobro


            reloj = temporal_tiempo

        return render(self.request, self.template_name, {"matrizResultado": matriz, "vectorEntrada": [fin, relojInicio, relojFin]})
