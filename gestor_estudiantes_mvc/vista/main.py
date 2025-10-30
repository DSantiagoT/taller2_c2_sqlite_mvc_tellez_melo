# vista/main.py
"""
Vista por consola: menú interactivo que invoca las funciones del controlador.
Respeta la Segregación de Interfaces (I) manteniéndose independiente del modelo.
"""

from controlador.gestor import GestorEstudiantes

def mostrar_estudiantes(lista):
    if not lista:
        print("⚠️ No hay estudiantes para mostrar.")
        return
    print("-" * 60)
    print(f"{'ID':<4} {'Nombre':<20} {'Edad':<5} {'Carrera':<15} {'Nota':<5}")
    print("-" * 60)
    for e in lista:
        id_, nombre, edad, carrera, nota = e
        print(f"{id_:<4} {nombre:<20} {edad:<5} {carrera:<15} {nota:<5}")
    print("-" * 60)

def solicitar_float(prompt, minimo=None, maximo=None):
    while True:
        try:
            val = float(input(prompt))
            if minimo is not None and val < minimo:
                print(f"❌ Debe ser >= {minimo}")
                continue
            if maximo is not None and val > maximo:
                print(f"❌ Debe ser <= {maximo}")
                continue
            return val
        except ValueError:
            print("❌ Introduce un número válido.")

def solicitar_int(prompt, minimo=None):
    while True:
        try:
            val = int(input(prompt))
            if minimo is not None and val < minimo:
                print(f"❌ Debe ser >= {minimo}")
                continue
            return val
        except ValueError:
            print("❌ Introduce un entero válido.")

def menu():
    gestor = GestorEstudiantes()

    while True:
        print("\n=== GESTOR DE ESTUDIANTES (MVC) ===")
        print("1. Agregar estudiante")
        print("2. Listar estudiantes")
        print("3. Actualizar nota (por nombre)")
        print("4. Eliminar estudiante (por ID)")
        print("5. Buscar por nombre (parcial)")
        print("6. Listar por nota (descendente)")
        print("7. Eliminar estudiantes con nota menor a un valor")
        print("8. Salir")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            nombre = input("Nombre: ").strip()
            edad = solicitar_int("Edad: ", minimo=1)
            carrera = input("Carrera: ").strip()
            nota = solicitar_float("Nota (0.0 - 5.0): ", minimo=0.0, maximo=5.0)
            try:
                nuevo_id = gestor.agregar_estudiante(nombre, edad, carrera, nota)
                print(f"✅ Estudiante agregado con ID {nuevo_id}.")
            except Exception as e:
                print(f"❌ Error al agregar: {e}")

        elif opcion == "2":
            lista = gestor.listar_estudiantes()
            mostrar_estudiantes(lista)

        elif opcion == "3":
            nombre = input("Nombre del estudiante a actualizar (coincidencia exacta): ").strip()
            nueva_nota = solicitar_float("Nueva nota (0.0 - 5.0): ", minimo=0.0, maximo=5.0)
            try:
                filas = gestor.actualizar_nota(nombre, nueva_nota)
                if filas == 0:
                    print("⚠️ No se encontró ningún estudiante con ese nombre.")
                else:
                    print(f"✅ Nota actualizada en {filas} registro(s).")
            except Exception as e:
                print(f"❌ Error: {e}")

        elif opcion == "4":
            id_estudiante = solicitar_int("ID del estudiante a eliminar: ", minimo=1)
            filas = gestor.eliminar_estudiante_por_id(id_estudiante)
            if filas == 0:
                print("⚠️ No se encontró un estudiante con ese ID.")
            else:
                print("🗑️ Estudiante eliminado correctamente.")

        elif opcion == "5":
            termino = input("Cadena a buscar en nombres: ").strip()
            resultados = gestor.buscar_por_nombre(termino)
            mostrar_estudiantes(resultados)

        elif opcion == "6":
            lista = gestor.listar_por_nota_desc()
            mostrar_estudiantes(lista)

        elif opcion == "7":
            umbral = solicitar_float("Eliminar estudiantes con nota menor que: ", minimo=0.0, maximo=5.0)
            filas = gestor.eliminar_estudiantes_nota_menor(umbral)
            print(f"🗑️ Se eliminaron {filas} estudiante(s).")

        elif opcion == "8":
            gestor.cerrar()
            print("👋 Saliendo del sistema...")
            break

        else:
            print("❌ Opción inválida, intente nuevamente.")

if __name__ == "__main__":
    menu()
