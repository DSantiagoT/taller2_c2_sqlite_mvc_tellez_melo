# modelo/estudiante.py
"""
Modelo: contiene la entidad Estudiante y la clase EstudianteDB responsable
únicamente de la persistencia (crear tabla, insertar, listar, actualizar, eliminar).
Cumple el principio de Responsabilidad Única (S).
"""

from dataclasses import dataclass
import sqlite3
from typing import List, Tuple, Optional


@dataclass
class Estudiante:
    nombre: str
    edad: int
    carrera: str
    nota: float


class EstudianteDB:
    """
    Clase responsable de todas las operaciones SQL con la base de datos SQLite.
    Se mantienen aquí todas las sentencias SQL y la lógica de persistencia.

    Métodos principales:
    - crear_tabla(): crea la tabla si no existe.
    - insertar(estudiante): INSERT INTO ...
    - listar(): SELECT * FROM ...
    - actualizar_nota(nombre, nueva_nota): UPDATE estudiantes SET nota = ? WHERE nombre = ?
    - eliminar_por_id(id): DELETE FROM estudiantes WHERE id = ?
    - eliminar_por_nota_menor(valor): DELETE FROM estudiantes WHERE nota < ?
    - listar_ordenados_por_nota_desc(): SELECT * FROM estudiantes ORDER BY nota DESC
    - buscar_por_nombre_parcial(term): SELECT * FROM estudiantes WHERE nombre LIKE ?
    """

    def __init__(self, nombre_db: str = "estudiantes.db"):
        self.nombre_db = nombre_db
        self.conn = sqlite3.connect(self.nombre_db)
        self.cursor = self.conn.cursor()
        self.crear_tabla()

    def crear_tabla(self):
        """
        Crea la tabla 'estudiantes' si no existe.
        SQL:
            CREATE TABLE IF NOT EXISTS estudiantes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                edad INTEGER NOT NULL,
                carrera TEXT NOT NULL,
                nota REAL NOT NULL
            );
        """
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS estudiantes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                edad INTEGER NOT NULL,
                carrera TEXT NOT NULL,
                nota REAL NOT NULL
            )
        """)
        self.conn.commit()

    def insertar(self, estudiante: Estudiante) -> int:
        """
        Inserta un nuevo estudiante.
        SQL:
            INSERT INTO estudiantes (nombre, edad, carrera, nota) VALUES (?, ?, ?, ?)
        Devuelve: id del registro insertado.
        """
        self.cursor.execute(
            "INSERT INTO estudiantes (nombre, edad, carrera, nota) VALUES (?, ?, ?, ?)",
            (estudiante.nombre, estudiante.edad, estudiante.carrera, estudiante.nota)
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def listar(self) -> List[Tuple[int, str, int, str, float]]:
        """
        Lista todos los estudiantes.
        SQL:
            SELECT * FROM estudiantes
        """
        self.cursor.execute("SELECT * FROM estudiantes")
        return self.cursor.fetchall()

    def actualizar_nota(self, nombre: str, nueva_nota: float) -> int:
        """
        Actualiza la nota de los estudiantes que coincidan con el nombre dado.
        SQL:
            UPDATE estudiantes SET nota = ? WHERE nombre = ?
        Devuelve: número de filas afectadas.
        """
        self.cursor.execute(
            "UPDATE estudiantes SET nota = ? WHERE nombre = ?",
            (nueva_nota, nombre)
        )
        self.conn.commit()
        return self.cursor.rowcount

    def eliminar_por_id(self, id_estudiante: int) -> int:
        """
        Elimina un estudiante por su ID.
        SQL:
            DELETE FROM estudiantes WHERE id = ?
        Devuelve: número de filas eliminadas.
        """
        self.cursor.execute("DELETE FROM estudiantes WHERE id = ?", (id_estudiante,))
        self.conn.commit()
        return self.cursor.rowcount

    def eliminar_por_nota_menor(self, umbral: float) -> int:
        """
        Elimina todos los estudiantes cuya nota sea menor que el valor dado.
        SQL:
            DELETE FROM estudiantes WHERE nota < ?
        Devuelve: número de filas eliminadas.
        """
        self.cursor.execute("DELETE FROM estudiantes WHERE nota < ?", (umbral,))
        self.conn.commit()
        return self.cursor.rowcount

    def listar_ordenados_por_nota_desc(self) -> List[Tuple[int, str, int, str, float]]:
        """
        Lista estudiantes ordenados por nota de mayor a menor.
        SQL:
            SELECT * FROM estudiantes ORDER BY nota DESC
        """
        self.cursor.execute("SELECT * FROM estudiantes ORDER BY nota DESC")
        return self.cursor.fetchall()

    def buscar_por_nombre_parcial(self, termino: str) -> List[Tuple[int, str, int, str, float]]:
        """
        Busca estudiantes cuyo nombre contenga la cadena dada.
        SQL:
            SELECT * FROM estudiantes WHERE nombre LIKE ?
        Nota: se utiliza %term% para buscar en cualquier parte del nombre.
        """
        pattern = f"%{termino}%"
        self.cursor.execute("SELECT * FROM estudiantes WHERE nombre LIKE ?", (pattern,))
        return self.cursor.fetchall()

    def cerrar(self):
        """Cierra la conexión con la base de datos."""
        if self.conn:
            self.conn.close()
            self.conn = None

    def __del__(self):
        # Aseguramos cierre al destruir el objeto (defensivo).
        try:
            self.cerrar()
        except Exception:
            pass
