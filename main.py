 from abc import ABC, abstractmethod

# EXCEPCIONES
class ErrorSistema(Exception):
    pass

class ErrorCliente(ErrorSistema):
    pass

class ErrorServicio(ErrorSistema):
    pass

class ErrorReserva(ErrorSistema):
    pass


# CLIENTE
class Cliente:
    def __init__(self, nombre, documento):
        if not nombre or not documento:
            raise ErrorCliente("Datos inválidos")
        self.nombre = nombre
        self.documento = documento


# SERVICIO ABSTRACTO
class Servicio(ABC):
    def __init__(self, nombre, precio):
        if precio <= 0:
            raise ErrorServicio("Precio inválido")
        self.nombre = nombre
        self.precio = precio

    @abstractmethod
    def calcular_costo(self, cantidad):
        pass


class ReservaSala(Servicio):
    def calcular_costo(self, horas):
        return self.precio * horas


class AlquilerEquipo(Servicio):
    def calcular_costo(self, dias):
        return self.precio * dias


class Asesoria(Servicio):
    def calcular_costo(self, horas):
        return self.precio * horas * 1.2


# RESERVA
class Reserva:
    def __init__(self, cliente, servicio, cantidad):
        if cantidad <= 0:
            raise ErrorReserva("Cantidad inválida")
        self.cliente = cliente
        self.servicio = servicio
        self.cantidad = cantidad
        self.estado = "Pendiente"

    def procesar(self):
        try:
            costo = self.servicio.calcular_costo(self.cantidad)
            self.estado = "Confirmada"
            return costo
        except Exception as e:
            self.estado = "Error"
            raise ErrorReserva(str(e))


# LOGS
def log_error(mensaje):
    with open("logs.txt", "a") as f:
        f.write(mensaje + "\n")


# MAIN (PRUEBAS)
def main():
    print("=== PRUEBAS DEL SISTEMA ===")

    # 1 correcto
    try:
        c1 = Cliente("Juan", "123")
        s1 = ReservaSala("Sala", 100)
        r1 = Reserva(c1, s1, 2)
        print("Costo:", r1.procesar())
    except Exception as e:
        log_error(str(e))

    # 2 error cliente
    try:
        c2 = Cliente("", "456")
    except Exception as e:
        log_error(str(e))

    # 3 error servicio
    try:
        s2 = AlquilerEquipo("Equipo", -50)
    except Exception as e:
        log_error(str(e))

    # 4 error reserva
    try:
        r2 = Reserva(c1, s1, -1)
    except Exception as e:
        log_error(str(e))

    # MÁS CASOS (hasta completar 10)
    for i in range(6):
        try:
            c = Cliente("Cliente"+str(i), str(i))
            s = Asesoria("Asesoria", 80)
            r = Reserva(c, s, i+1)
            print("Costo:", r.procesar())
        except Exception as e:
            log_error(str(e))


if __name__ == "__main__":
    main()
