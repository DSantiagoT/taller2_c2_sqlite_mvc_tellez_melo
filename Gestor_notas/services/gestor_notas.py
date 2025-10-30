import os
import shutil
from models.nota import Nota


class GestorNotas:
    """
    Administra las operaciones de creación, lectura, edición,
    búsqueda y eliminación de notas.
    """

    def __init__(self, carpeta="notas"):
        self.carpeta = carpeta
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)

    def guardar(self, nota: Nota):
        ruta = os.path.join(self.carpeta, f"{nota.nombre}.txt")
        with open(ruta, "w", encoding="utf-8") as archivo:
            archivo.write(str(nota))

    def leer(self, nombre):
        """
        Lee el contenido de una nota. 
        Maneja errores en caso de que el archivo no exista o no pueda leerse.
        """
        try:
            ruta = os.path.join(self.carpeta, f"{nombre}.txt")
            if not os.path.exists(ruta):
                return "Error: la nota no existe."
            with open(ruta, "r", encoding="utf-8") as archivo:
                return archivo.read()
        except Exception as e:
            # Manejo de errores dentro del servicio, no en main.py
            return f"Ocurrió un error al leer la nota: {str(e)}"

    def listar(self):
        return [a[:-4] for a in os.listdir(self.carpeta) if a.endswith(".txt")]

    def buscar(self, palabra):
        resultados = []
        for archivo in os.listdir(self.carpeta):
            ruta = os.path.join(self.carpeta, archivo)
            with open(ruta, "r", encoding="utf-8") as f:
                if palabra.lower() in f.read().lower():
                    resultados.append(archivo[:-4])
        return resultados

    def editar(self, nombre, nuevo_contenido):
        """
        Edita una nota existente. Crea un respaldo antes de sobrescribir.
        Se usa try-except para evitar fallos si el archivo está bloqueado o no existe.
        """
        try:
            ruta = os.path.join(self.carpeta, f"{nombre}.txt")
            if not os.path.exists(ruta):
                return False
            respaldo = os.path.join(self.carpeta, f"{nombre}_bak.txt")
            shutil.copy(ruta, respaldo)
            with open(ruta, "w", encoding="utf-8") as archivo:
                archivo.write(nuevo_contenido)
            return True
        except Exception as e:
            print(f"Error al editar la nota: {str(e)}")
            return False

    def eliminar(self, nombre):
        """
        Elimina una nota del sistema.
        Si ocurre un error (por permisos o inexistencia), se captura sin detener el programa.
        """
        try:
            ruta = os.path.join(self.carpeta, f"{nombre}.txt")
            if not os.path.exists(ruta):
                return False
            os.remove(ruta)
            return True
        except Exception as e:
            print(f"Error al eliminar la nota: {str(e)}")
            return False

    def contar_notas(self):
        """
        Devuelve la cantidad total de notas válidas (.txt) almacenadas,
        excluyendo respaldos (_bak) o exportaciones.
        """
        notas_validas = [
            a for a in os.listdir(self.carpeta)
            if a.endswith(".txt") and "_bak" not in a and "export" not in a.lower()
        ]
        return len(notas_validas)
    
    def exportar_a_json(self):
        """
        Exporta todas las notas válidas a un archivo 'notas.json'.
        Cada nota se guarda como un objeto con nombre, fecha y contenido.
        """
        import json

        notas_data = []

        for archivo in os.listdir(self.carpeta):
            if archivo.endswith(".txt") and "_bak" not in archivo and "export" not in archivo.lower():
                ruta = os.path.join(self.carpeta, archivo)
                with open(ruta, "r", encoding="utf-8") as f:
                    contenido = f.read()

                # Extraer la fecha (línea 1) y el contenido (resto del archivo)
                lineas = contenido.splitlines()
                fecha = ""
                cuerpo = ""
                if lineas and lineas[0].startswith("Fecha:"):
                    fecha = lineas[0].replace("Fecha:", "").strip()
                    cuerpo = "\n".join(lineas[2:])  # El contenido empieza después de la línea vacía
                else:
                    cuerpo = contenido.strip()

                notas_data.append({
                    "nombre": archivo[:-4],
                    "fecha": fecha,
                    "contenido": cuerpo
                })

        # Guardar en JSON
        with open("notas.json", "w", encoding="utf-8") as json_file:
            json.dump(notas_data, json_file, ensure_ascii=False, indent=4)

        return f"Se exportaron {len(notas_data)} notas a 'notas.json'."
