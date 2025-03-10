from handledb import DB


class Proveedor:
    def __init__(self, nombre, productos_suministrado, tiempo_entrega, confiabilidad=1, contacto="", calidad=0.5):
        self.nombre = nombre
        self.tiempo_entrega = tiempo_entrega
        self.confiabilidad = confiabilidad
        self.contacto = contacto
        self.calidad = calidad  # Calidad de los productos (0.0 a 5.0)
        self.evaluacion = self.evaluar_proveedor()
        self.categoria = self.obtener_categoria_proveedor()

        self.productos_suministrado = []
        for _ in productos_suministrado:
            self.productos_suministrado.append({"name": _["name"]})

    def register(self):
        DB.save("proveedores", self.__dict__)

    def actualizar_contacto(self, contacto_nuevo):
        self.contacto = contacto_nuevo

    def calcular_prioridad(self):
        prioridad = (self.confiabilidad * 0.8) - (self.tiempo_entrega * 0.2) + (len(self.producto_suministrado) * 0.2)
        prioridad = max(0, min(prioridad, 1))
        return prioridad * 100

    def evaluar_proveedor(self):
        """
        Evalúa al proveedor basándose en la confiabilidad, tiempo de entrega y calidad.

        Retorna:
        - Un valor entre 1 y 10 que representa la puntuación del proveedor.
        """
        # Ponderaciones para cada factor
        ponderacion_confiabilidad = 0.5
        ponderacion_tiempo_entrega = 0.3
        ponderacion_calidad = 0.2

        # Ajustar el tiempo de entrega: menor tiempo es mejor

        # Usamos 1 / tiempo_entrega para que un menor tiempo contribuya a una mayor puntuación
        if self.tiempo_entrega == 0:
            tiempo_entrega_ajustado = 10  # Si el tiempo de entrega es 0, asignamos la máxima puntuación
        else:
            tiempo_entrega_ajustado = 10 / self.tiempo_entrega

        # Calcular la puntuación
        puntuacion = (
            (self.confiabilidad * 10 * ponderacion_confiabilidad) +  # Confiabilidad (0.0 a 1.0 -> 0 a 10)
            (tiempo_entrega_ajustado * ponderacion_tiempo_entrega) +  # Tiempo de entrega (inversamente proporcional)
            (self.calidad * 2 * ponderacion_calidad)  # Calidad (0.0 a 5.0 -> 0 a 10)
        )

        # Asegurar que la puntuación esté en el rango [1, 10]
        puntuacion = max(1, min(puntuacion, 10))

        return puntuacion

    def obtener_categoria_proveedor(self):
        """
        Clasifica al proveedor en una categoría basada en su puntuación.

        Retorna:
        - Una cadena que indica la categoría del proveedor.
        """
        puntuacion = self.evaluar_proveedor()

        if puntuacion <= 4:
            return "Proveedor no confiable"
        elif puntuacion <= 7:
            return "Proveedor aceptable"
        else:
            return "Proveedor excelente"