import random

class Encargado:
    def __init__(self, id, estado, disponible, cola, cola_asig, terminal1, terminal2, terminal3):
        self.id = id
        self.estado = estado
        self.max = disponible
        self.disponible = disponible
        self.cola = cola
        self.cola_asig = cola_asig
        self.terminal1 = terminal1
        self.terminal2 = terminal2
        self.terminal3 = terminal3
        self.fin_cobro = ''
        self.fin_asignacion = ''
        self.tiempo_turno = ''
        self.importe = ''

    def aumentardisponible(self):
        self.disponible += 1
        if self.disponible == self.max:
            self.estado = "Libre"
        else:
            self.estado = "Ocupado"

    def disminuirdisponible(self):
        self.disponible -= 1
        if self.disponible == 0:
            self.estado = "Ocupado"
        else:
            self.estado = "Libre"

    def comenzar_asignacion(self):
        if self.estado == "Libre" and (self.terminal1.estado == 'Libre' or self.terminal2.estado == 'Libre' or self.terminal3.estado == 'Libre'):
            self.disminuirdisponible()
            if self.cola_asig > 0:
                self.cola_asig -= 1
            return True
        else:
            self.cola_asig += 1
            return False

    def asignar_terminal(self):
        if self.terminal1.estado == 'Libre':
            self.aumentardisponible()
            self.terminal1.disminuirdisponible()
            return self.terminal1
        elif self.terminal2.estado == 'Libre':
            self.aumentardisponible()
            self.terminal2.disminuirdisponible()
            return self.terminal2
        elif self.terminal3.estado == 'Libre':
            self.aumentardisponible()
            self.terminal3.disminuirdisponible()
            return self.terminal3

    def asignar_cobro(self):
        if self.estado == 'Libre':
            self.disminuirdisponible()
            if self.cola > 0:
                self.cola -= 1
            return True
        else:
            self.cola += 1
            return False


class Terminal:
    def __init__(self, id, estado, disponible):
        self.id = id
        self.estado = estado
        self.max = disponible
        self.disponible = disponible
        self.tiempo_liberacion = ''

    def aumentardisponible(self):
        self.disponible += 1
        if self.disponible == self.max:
            self.estado = "Libre"
        else:
            self.estado = "Disponible"

    def disminuirdisponible(self):
        self.disponible -= 1
        if self.disponible == 0:
            self.estado = "Ocupado"
        else:
            self.estado = "Disponible"

class Mozo:
    def __init__(self, id, estado, disponible, cola):
        self.id = id
        self.estado = estado
        self.max = disponible
        self.disponible = disponible
        self.cola = cola
        self.fin_entrega = ''

    def aumentardisponible(self):
        self.disponible += 1
        if self.disponible == self.max:
            self.estado = "Libre"
        else:
            self.estado = "Ocupado"

    def disminuirdisponible(self):
        self.disponible -= 1
        if self.disponible == 0:
            self.estado = "Ocupado"
        else:
            self.estado = "Libre"

class Impresora:
    def __init__(self, id, estado, disponible, cola):
        self.id = id
        self.estado = estado
        self.max = disponible
        self.disponible = disponible
        self.cola = cola
        self.fin_impresion = ''

    def aumentardisponible(self):
        self.disponible += 1
        if self.disponible == self.max:
            self.estado = "Libre"
        else:
            self.estado = "Ocupado"

    def disminuirdisponible(self):
        self.disponible -= 1
        if self.disponible == 0:
            self.estado = "Ocupado"
        else:
            self.estado = "Libre"

class Cliente:
    def __init__(self, id, encargado, mozo, impresora):
        self.id = id
        self.estado = 'C'
        self.tiempo_llegada = ''
        self.gasto_individual = 0
        self.terminal_asignada = ''
        self.nro_terminal = 0
        self.servidor_actual = ''
        self.tiempo_asignacion = ''
        self.tiempo_fin_turno = ''
        self.tiempo_entrega_pedido = ''
        self.tiempo_fin_impresion = ''
        self.tiempo_fin_cobro = ''
        self.en_cola = False
        self.en_cola_asig = False
        self.pedido = False
        self.impresion = False
        self.encargado = encargado
        self.mozo = mozo
        self.impresora = impresora
        self.duracion_turno = ''

    def realizar_pedido(self):
        aleatorio = random.random()
        if aleatorio < 0.01:
            return True
        else:
            return False

    def buscar_impresion(self):
        aleatorio = random.random()
        if aleatorio < 0.1:
            return True
        else:
            return False

    def definir_duracion(self):
        aleatorio = random.random()
        if aleatorio < 0.5:
            return 60
        else:
            return 30

    def ejecutar(self, reloj):

        if self.estado == 'C' or self.en_cola_asig:

            self.encargado.tiempo_turno = ''
            self.encargado.importe = ''

            if self.estado == 'C':
                self.tiempo_llegada = reloj
            asignado = self.encargado.comenzar_asignacion()
            if asignado:
                self.estado = 'SA'
                self.en_cola_asig = False
                self.tiempo_asignacion = reloj + 0.33
                self.encargado.fin_asignacion = self.tiempo_asignacion
                return
            else:
                self.estado = 'EA'
                self.en_cola_asig = True
                return

        elif self.tiempo_asignacion == reloj and self.estado == 'SA':
            self.duracion_turno = self.definir_duracion()
            self.tiempo_fin_turno = self.tiempo_asignacion + self.duracion_turno
            self.estado = 'ET'
            self.terminal_asignada = self.encargado.asignar_terminal()
            self.terminal_asignada.tiempo_liberacion = self.tiempo_fin_turno
            self.nro_terminal = self.terminal_asignada.id
            self.encargado.fin_asignacion = ''
            self.tiempo_asignacion = ''

            if self.duracion_turno == 60:
                self.gasto_individual += 3.5
            else:
                self.gasto_individual += 2

            self.encargado.tiempo_turno = self.duracion_turno
            self.encargado.importe = self.gasto_individual

            self.pedido = self.realizar_pedido()
            if self.pedido and self.mozo.estado == 'Libre':
                self.mozo.disminuirdisponible()
                self.gasto_individual += 2
                self.tiempo_entrega_pedido = reloj + 3
                self.pedido = False
                self.mozo.fin_entrega = self.tiempo_entrega_pedido
                if self.mozo.cola > 0:
                    self.mozo.cola -= 1
            elif self.pedido and self.mozo.estado == 'Ocupado':
                self.mozo.cola += 1
            return

        elif self.tiempo_entrega_pedido == reloj:
            self.mozo.aumentardisponible()
            self.tiempo_entrega_pedido = ''
            self.mozo.fin_entrega = ''

            self.encargado.tiempo_turno = ''
            self.encargado.importe = ''
            return

        elif self.tiempo_fin_turno == reloj:
            self.terminal_asignada.aumentardisponible()
            self.terminal_asignada.tiempo_liberacion = ''
            self.tiempo_fin_turno = ''

            self.impresion = self.buscar_impresion()
            if self.impresion and self.impresora.estado == 'Libre':
                self.impresora.disminuirdisponible()
                self.gasto_individual += 0.5
                self.tiempo_fin_impresion = reloj + 1
                self.impresion = False
                self.impresora.fin_impresion = self.tiempo_fin_impresion
                self.estado = 'SI'
                return

            elif self.impresion and self.impresora.estado == 'Ocupado':
                self.impresora.cola += 1
                self.estado = 'EI'
                return

            elif not self.impresion:
                paga = self.encargado.asignar_cobro()

                if paga:
                    self.estado = 'SC'
                    self.tiempo_fin_cobro = reloj + 0.5
                    self.en_cola = False
                    return
                else:
                    self.estado = 'EC'
                    self.en_cola = True
                    return

        elif self.tiempo_fin_impresion == reloj:
            self.impresora.aumentardisponible()
            self.impresora.fin_impresion = ''
            self.tiempo_fin_impresion = ''
            self.encargado.tiempo_turno = ''
            self.encargado.importe = ''

            paga = self.encargado.asignar_cobro()

            if paga:
                self.tiempo_fin_cobro = reloj + 0.5
                self.estado = 'SC'
                self.en_cola = False
                return
            else:
                self.estado = 'EC'
                self.en_cola = True
                return

        elif self.tiempo_fin_cobro == reloj:
            self.encargado.aumentardisponible()
            self.encargado.fin_cobro = ''
            self.tiempo_fin_cobro = ''
            self.estado = 'D'
            return

        if self.en_cola:
            paga = self.encargado.asignar_cobro()

            if paga:
                self.tiempo_fin_cobro = reloj + 0.5
                self.estado = 'SC'
                self.en_cola = False
                return
            else:
                self.estado = 'EC'
                self.en_cola = True
                return







