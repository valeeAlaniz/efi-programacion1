
# Importar las funciones de lógica
from modulos.funciones import (
    registrar_articulo_nuevo,
    registrar_combo_nuevo,
    registrar_compra_stock,
    registrar_venta,
    ver_listado_productos,
    modificar_precio,
    eliminar_articulo,
    cierre_de_caja
)

# Importar las funciones de persistencia
from modulos.persistir import guardar_datos, cargar_datos


def mostrar_menu_principal():
    #Imprime el menú de opciones final
    print("\n--- SISTEMA DE GESTIÓN DE INVENTARIO (v3.0 Combos) ---")
    print("1. Registrar PRODUCTO nuevo")
    print("2. Registrar COMBO nuevo")
    print("3. Registrar compra (agregar stock a producto)")
    print("4. Registrar venta (producto o combo)")
    print("5. Ver listado de inventario (productos y combos)")
    print("6. Modificar precio (producto o combo)")
    print("7. Eliminar item (producto o combo)")
    print("8. Realizar cierre de caja")
    print("9. Guardar y Salir del sistema")
    print("---------------------------------------------------------")


def main():    #Función principal que ejecuta el bucle del programa.

    # Cargar datos al inicio.Llama a la versión .txt relacionada de cargar_datos()
    inventario, ventas_del_dia, cierres_de_caja = cargar_datos()

    # Bucle principal
    while True:
        mostrar_menu_principal()
        opcion = input("Seleccione una opción (1-9): ").strip()

        if opcion == "1":
            registrar_articulo_nuevo(inventario)
        
        elif opcion == "2":
            registrar_combo_nuevo(inventario)
        
        elif opcion == "3":
            registrar_compra_stock(inventario)
        
        elif opcion == "4":
            registrar_venta(inventario, ventas_del_dia)
        
        elif opcion == "5":
            ver_listado_productos(inventario)
        
        elif opcion == "6":
            modificar_precio(inventario)
        
        elif opcion == "7":
            eliminar_articulo(inventario)
        
        elif opcion == "8":
            cierre_de_caja(ventas_del_dia, cierres_de_caja)
        
        elif opcion == "9":
            print("Saliendo del sistema...")
            
            # Guarda datos al salir
            guardar_datos(inventario, ventas_del_dia, cierres_de_caja)
            break 
        
        else:
            print(f"Error: Opción '{opcion}' no es válida. Intente de nuevo.")


if __name__ == "__main__":
    main()