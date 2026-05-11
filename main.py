from abc import ABC, abstractmethod
 
#  EXCEPCIONES
 
class ErrorSistema(Exception):
    """Excepción base del sistema"""
    pass
 
class ErrorCliente(ErrorSistema):
    pass
 
class ErrorServicio(ErrorSistema):
    pass
 
class ErrorReserva(ErrorSistema):
    pass
 
 
#  LOGS
 
def log_evento(mensaje):
    with open("logs.txt", "a", encoding="utf-8") as f:
        f.write(mensaje + "\n")
 
 
#  CLASE ABSTRACTA GENERAL
 
class Entidad(ABC):
    @abstractmethod
    def descripcion(self):
        pass
 
 
#  CLIENTE
 
class Cliente(Entidad):
    def __init__(self, nombre, documento):
        if not nombre or not documento:
            raise ErrorCliente("Datos del cliente inválidos")
        self.__nombre = nombre
        self.__documento = documento
 
    def descripcion(self):
        return f"Cliente: {self.__nombre} - {self.__documento}"
 
 
#  SERVICIO ABSTRACTO
 
class Servicio(ABC):
    def __init__(self, nombre, precio):
        if precio <= 0:
            raise ErrorServicio("Precio del servicio inválido")
        self.nombre = nombre
        self.precio = precio
 
    @abstractmethod
    def calcular_costo(self, cantidad):
        pass
 
    @abstractmethod
    def descripcion(self):
        pass
 
 
#  SERVICIOS
 
class ReservaSala(Servicio):
    # Versión 1: calcular costo por horas simples
    def calcular_costo(self, horas):
        return self.precio * horas
 
    # Versión 2: sobrecarga simulada — calcular costo con descuento por cantidad de personas
    def calcular_costo_con_descuento(self, horas, personas):
        descuento = 0.1 if personas >= 5 else 0
        return self.precio * horas * (1 - descuento)
 
    def descripcion(self):
        return "Servicio de reserva de salas"
 
 
class AlquilerEquipo(Servicio):
    # Versión 1: costo estándar por días
    def calcular_costo(self, dias):
        return (self.precio * dias) + 50
 
    # Versión 2: sobrecarga simulada — costo con seguro opcional
    def calcular_costo_con_seguro(self, dias, incluir_seguro=True):
        base = (self.precio * dias) + 50
        return base + (base * 0.15) if incluir_seguro else base
 
    def descripcion(self):
        return "Servicio de alquiler de equipos"
 
 
class Asesoria(Servicio):
    # Versión 1: costo estándar por horas
    def calcular_costo(self, horas):
        return self.precio * horas * 1.2
 
    # Versión 2: sobrecarga simulada — costo con tarifa urgente
    def calcular_costo_urgente(self, horas):
        return self.precio * horas * 1.2 * 1.5
 
    def descripcion(self):
        return "Servicio de asesoría especializada"
 
 
#  SISTEMA (listas internas para gestionar clientes, servicios y reservas)
 
class SistemaFJ:
    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []
 
    def agregar_cliente(self, cliente):
        self.clientes.append(cliente)
        log_evento(f"[EVENTO] Cliente registrado: {cliente.descripcion()}")
 
    def agregar_servicio(self, servicio):
        self.servicios.append(servicio)
        log_evento(f"[EVENTO] Servicio registrado: {servicio.descripcion()} | Precio base: {servicio.precio}")
 
    def agregar_reserva(self, reserva):
        self.reservas.append(reserva)
 
    def listar_clientes(self):
        print("\n--- Clientes registrados ---")
        for c in self.clientes:
            print(" ", c.descripcion())
 
    def listar_servicios(self):
        print("\n--- Servicios registrados ---")
        for s in self.servicios:
            print(" ", s.descripcion())
 
    def listar_reservas(self):
        print("\n--- Reservas registradas ---")
        for r in self.reservas:
            print(f"  {r.servicio.descripcion()} | Estado: {r.estado}")
 
 
#  RESERVA
 
class Reserva:
    def __init__(self, cliente, servicio, cantidad):
        if cantidad <= 0:
            raise ErrorReserva("Cantidad inválida para la reserva")
        self.cliente = cliente
        self.servicio = servicio
        self.cantidad = cantidad
        self.estado = "Pendiente"
 
    def procesar(self):
        try:
            costo = self.servicio.calcular_costo(self.cantidad)
        except Exception as e:
            self.estado = "Error"
            log_evento(f"[ERROR] Error en reserva: {str(e)}")
            raise ErrorReserva("No se pudo procesar la reserva") from e
        else:
            # Se ejecuta solo si NO hubo excepción
            self.estado = "Confirmada"
            log_evento(f"[EXITOSO] Reserva confirmada | {self.servicio.descripcion()} | Costo: {costo}")
            return costo
        finally:
            log_evento("[EVENTO] Proceso de reserva finalizado")
 
    def cancelar(self):
        if self.estado == "Confirmada" or self.estado == "Pendiente":
            self.estado = "Cancelada"
            log_evento(f"[EVENTO] Reserva cancelada | {self.servicio.descripcion()} | Cliente: {self.cliente.descripcion()}")
            print(f"Reserva cancelada exitosamente: {self.servicio.descripcion()}")
        else:
            log_evento(f"[ERROR] Intento de cancelar reserva en estado inválido: {self.estado}")
            raise ErrorReserva(f"No se puede cancelar una reserva en estado: {self.estado}")
 
 
#  MAIN (PRUEBAS)
 
def main():
    print("=== PRUEBAS DEL SISTEMA SOFTWARE FJ ===")
 
    sistema = SistemaFJ()
 
    # 1. Operación correcta con try/except/else
    try:
        c1 = Cliente("Juan", "123")
        s1 = ReservaSala("Sala de Reuniones", 100)
        r1 = Reserva(c1, s1, 2)
        costo = r1.procesar()
    except Exception as e:
        log_evento(f"[ERROR] {str(e)}")
    else:
        print("Costo sala estándar:", costo)
        sistema.agregar_cliente(c1)
        sistema.agregar_servicio(s1)
        sistema.agregar_reserva(r1)
 
    # 2. Sobrecarga: calcular_costo_con_descuento
    try:
        costo_desc = s1.calcular_costo_con_descuento(2, 6)
    except Exception as e:
        log_evento(f"[ERROR] {str(e)}")
    else:
        print("Costo sala con descuento (6 personas):", costo_desc)
        log_evento(f"[EXITOSO] Costo con descuento calculado: {costo_desc}")
 
    # 3. Error cliente
    try:
        Cliente("", "456")
    except ErrorCliente as e:
        log_evento(f"[ERROR] {str(e)}")
 
    # 4. Error servicio
    try:
        AlquilerEquipo("Equipo", -50)
    except ErrorServicio as e:
        log_evento(f"[ERROR] {str(e)}")
 
    # 5. Error reserva por cantidad inválida
    try:
        r_invalida = Reserva(c1, s1, -1)
    except ErrorReserva as e:
        log_evento(f"[ERROR] {str(e)}")
 
    # 6. Cancelar una reserva
    try:
        r1.cancelar()
    except ErrorReserva as e:
        log_evento(f"[ERROR] {str(e)}")
 
    # 7. Más operaciones con Asesoria (incluyendo versión urgente)
    for i in range(1, 5):
        try:
            c = Cliente(f"Cliente{i}", str(i))
            s = Asesoria("Asesoría TI", 80)
            r = Reserva(c, s, i)
            costo = r.procesar()
        except Exception as e:
            log_evento(f"[ERROR] {str(e)}")
        else:
            print(f"Costo asesoría estándar (cliente {i}):", costo)
            costo_urgente = s.calcular_costo_urgente(i)
            print(f"Costo asesoría urgente (cliente {i}):", costo_urgente)
            log_evento(f"[EXITOSO] Costo urgente calculado: {costo_urgente}")
            sistema.agregar_cliente(c)
            sistema.agregar_servicio(s)
            sistema.agregar_reserva(r)
 
    # 8. Listar todo desde el sistema
    sistema.listar_clientes()
    sistema.listar_servicios()
    sistema.listar_reservas()
 
    print("\nSistema ejecutado correctamente.")
 
 
if __name__ == "__main__":
    main()