# controlador/gestor.py
"""
Controlador: centraliza la lógica de negocio y coordina las acciones entre
la vista y el modelo. Aplica Inversión de Dependencia (D) permitiendo inyectar
una dependencia de persistencia (EstudianteDB u otro objeto con la misma interfaz).
También sigue el principio Abierto/Cerrado (O) al permitir extender sin modificar.
"""

from modelo.estudiante import Estudiante, EstudianteDB
from typing import List, Tuple, Optional


class GestorEstudiantes:
    def __init__(self, db: Optional[EstudianteDB] = None):
        """
        db: instancia de EstudianteDB (o un objeto compatible). Si es None,
        se crea una instancia por defecto. Esto permite sustituir la dependencia
        en pruebas o extensiones.
        """
        self.db = db if db is not None else EstudianteDB()

    def agregar_estudiante(self, nombre: str, edad: int, carrera: str, nota: float) -> int:
        """Valida y agrega un estudiante, devolviendo su id."""
        if edad <= 0:
            raise ValueError("La edad debe ser un entero positivo.")
        if nota < 0 or nota > 5:
            raise ValueError("La nota debe estar entre 0.0 y 5.0.")
        estudiante = Estudiante(nombre=nombre, edad=edad, carrera=carrera, nota=nota)
        return self.db.insertar(estudiante)

    def listar_estudiantes(self) -> List[Tuple[int, str, int, str, float]]:
        """Retorna la lista completa de estudiantes."""
        return self.db.listar()

    def actualizar_nota(self, nombre: str, nueva_nota: float) -> int:
        """Actualiza la nota de los estudiantes con el nombre dado. Devuelve filas afectadas."""
        if nueva_nota < 0 or nueva_nota > 5:
            raise ValueError("La nota debe estar entre 0.0 y 5.0.")
        return self.db.actualizar_nota(nombre, nueva_nota)

    def eliminar_estudiante_por_id(self, id_estudiante: int) -> int:
        """Elimina un estudiante por ID. Devuelve filas eliminadas."""
        return self.db.eliminar_por_id(id_estudiante)

    def eliminar_estudiantes_nota_menor(self, umbral: float) -> int:
        """Elimina estudiantes cuya nota sea menor que el umbral."""
        return self.db.eliminar_por_nota_menor(umbral)

    def listar_por_nota_desc(self) -> List[Tuple[int, str, int, str, float]]:
        """Lista estudiantes ordenados por nota descendente."""
        return self.db.listar_ordenados_por_nota_desc()

    def buscar_por_nombre(self, termino: str) -> List[Tuple[int, str, int, str, float]]:
        """Busca estudiantes cuyo nombre contenga 'termino'."""
        return self.db.buscar_por_nombre_parcial(termino)

    def cerrar(self):
        """Cierra la conexión subyacente de la base de datos."""
        self.db.cerrar()
