from models.nota import Nota
from services.gestor_notas import GestorNotas

gestor = GestorNotas()


def mostrar_menu():
    print("\n--- Gestor de Notas ---")
    print("1. Crear nota")
    print("2. Leer nota")
    print("3. Listar notas")
    print("4. Buscar palabra")
    print("5. Editar nota")
    print("6. Eliminar nota")
    print("7. Salir")
    print("8. Contar notas existentes")
    print("9. Exportar notas a JSON")


while True:
    mostrar_menu()
    opcion = input("Seleccione una opción: ").strip()

    if opcion == "1":
        nombre = input("Nombre de la nota: ").strip()
        contenido = input("Contenido: ").strip()
        if nombre and len(contenido) > 5:
            nota = Nota(nombre, contenido)
            gestor.guardar(nota)
            print("Nota guardada correctamente.")
        else:
            print("El nombre o el contenido no son válidos.")

    elif opcion == "2":
        nombre = input("Nombre de la nota: ").strip()
        print(gestor.leer(nombre))

    elif opcion == "3":
        print("Notas disponibles:", gestor.listar())

    elif opcion == "4":
        palabra = input("Palabra a buscar: ").strip()
        resultados = gestor.buscar(palabra)
        if resultados:
            print("Coincidencias encontradas:", resultados)
        else:
            print("No se encontraron coincidencias.")

    elif opcion == "5":
        nombre = input("Nombre de la nota a editar: ").strip()
        nuevo = input("Nuevo contenido: ").strip()
        if gestor.editar(nombre, nuevo):
            print("Nota editada y respaldo creado.")
        else:
            print("No se encontró la nota.")

    elif opcion == "6":
        nombre = input("Nombre de la nota a eliminar: ").strip()
        if gestor.eliminar(nombre):
            print("Nota eliminada correctamente.")
        else:
            print("No se encontró la nota.")

    elif opcion == "7":
        print("Programa finalizado.")
        break

    elif opcion == "8":
        cantidad = gestor.contar_notas()
        print(f"Hay {cantidad} notas almacenadas actualmente.")
    
    elif opcion == "9":
        mensaje = gestor.exportar_a_json()
        print(mensaje)

    else:
        print("Opción no válida.")
    