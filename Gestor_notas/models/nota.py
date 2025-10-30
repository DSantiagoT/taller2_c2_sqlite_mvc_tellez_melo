from datetime import datetime


class Nota:
    """
    Representa una nota con nombre, contenido y fecha de creación.
    """

    def __init__(self, nombre, contenido):
        self.nombre = nombre.strip()
        self.contenido = contenido.strip()
        self.fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self):
        """
        Retorna la nota formateada para su almacenamiento.
        """
        return f"Fecha: {self.fecha}\n\n{self.contenido}"
