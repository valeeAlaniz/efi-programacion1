# Archivo: mi_proyecto/modulos/persistir.py
# TAREA: Implementar persistencia .TXT para Productos Y Combos.
# (Implementación del "Día 5" - Arquitectura Relacional)

from .clases import Producto, Combo

# --- NOMBRES DE ARCHIVOS TXT ---
# 3 archivos para inventario
FILE_PRODUCTOS = "productos.txt"
FILE_COMBOS = "combos.txt"
FILE_RECETAS = "recetas.txt"
# 2 archivos para ventas
FILE_VENTAS = "ventas_del_dia.txt"
FILE_CIERRES = "cierres_de_caja.txt"

DELIMITADOR = "|" # Nuestro separador de confianza


def guardar_datos(inventario: dict, ventas_del_dia: list, cierres_de_caja: list):
    """
    Guarda el estado actual en archivos .txt planos, usando una
    estructura relacional para los combos.
    """
    print(f"\nGuardando datos en archivos de texto (relacional)...")

    # 1. Abrir TODOS los archivos de inventario
    try:
        with open(FILE_PRODUCTOS, 'w', encoding='utf-8') as f_prod, \
             open(FILE_COMBOS, 'w', encoding='utf-8') as f_comb, \
             open(FILE_RECETAS, 'w', encoding='utf-8') as f_rect:

            # 2. Clasificar y guardar cada item del inventario
            for item in inventario.values():
                
                # --- Si es un Producto Simple ---
                if isinstance(item, Producto):
                    nombre = item.nombre.replace(DELIMITADOR, "")
                    linea = f"{item.codigo}{DELIMITADOR}{nombre}{DELIMITADOR}{item.costo}{DELIMITADOR}{item.precio_venta}{DELIMITADOR}{item.stock}\n"
                    f_prod.write(linea)
                
                # --- Si es un Combo ---
                elif isinstance(item, Combo):
                    # Guardar la info principal en combos.txt
                    nombre = item.nombre.replace(DELIMITADOR, "")
                    linea_combo = f"{item.codigo}{DELIMITADOR}{nombre}{DELIMITADOR}{item.precio_venta}\n"
                    f_comb.write(linea_combo)
                    
                    # Guardar los componentes en recetas.txt
                    for cod_comp, cantidad in item.receta.items():
                        linea_receta = f"{item.codigo}{DELIMITADOR}{cod_comp}{DELIMITADOR}{cantidad}\n"
                        f_rect.write(linea_receta)

    except Exception as e:
        print(f"Error CRÍTICO al guardar el inventario: {e}")

    # 3. Guardar Ventas y Cierres (lógica simple)
    try:
        with open(FILE_VENTAS, 'w', encoding='utf-8') as f:
            for venta in ventas_del_dia:
                nombre = venta['producto'].replace(DELIMITADOR, "")
                linea = f"{nombre}{DELIMITADOR}{venta['cantidad']}{DELIMITADOR}{venta['total']}{DELIMITADOR}{venta['ganancia']}\n"
                f.write(linea)
    except Exception as e:
        print(f"Error al guardar {FILE_VENTAS}: {e}")

    try:
        with open(FILE_CIERRES, 'w', encoding='utf-8') as f:
            for cierre in cierres_de_caja:
                linea = f"{cierre['fecha']}{DELIMITADOR}{cierre['total_recaudado']}{DELIMITADOR}{cierre['ganancia_total']}{DELIMITADOR}{cierre['cantidad_de_ventas']}\n"
                f.write(linea)
    except Exception as e:
        print(f"Error al guardar {FILE_CIERRES}: {e}")

    print("¡Datos guardados exitosamente!")


def cargar_datos():
    """
    Carga los datos desde los archivos .txt relacionales al iniciar.
    """
    print("Cargando datos relacionales desde archivos .txt...")
    
    inventario_cargado = {}
    ventas_cargadas = []
    cierres_cargados = []

    # 1. Cargar PRODUCTOS (simple)
    try:
        with open(FILE_PRODUCTOS, 'r', encoding='utf-8') as f:
            for linea in f:
                partes = linea.strip().split(DELIMITADOR)
                if len(partes) == 5:
                    codigo, nombre, costo, p_venta, stock = partes
                    producto = Producto(codigo, nombre, costo, p_venta, stock)
                    inventario_cargado[producto.codigo] = producto
        print(f"Productos cargados: {len(inventario_cargado)}")
    except FileNotFoundError:
        print(f"No se encontró '{FILE_PRODUCTOS}'. Creando nuevo...")
    except Exception as e:
        print(f"Error al cargar {FILE_PRODUCTOS}: {e}")

    # 2. Cargar COMBOS (la info principal)
    combos_temp = {} # Guardamos los combos temporalmente
    try:
        with open(FILE_COMBOS, 'r', encoding='utf-8') as f:
            for linea in f:
                partes = linea.strip().split(DELIMITADOR)
                if len(partes) == 3:
                    codigo, nombre, p_venta = partes
                    # Creamos el combo con receta VACÍA por ahora
                    combo = Combo(codigo, nombre, p_venta, {})
                    inventario_cargado[combo.codigo] = combo
                    combos_temp[combo.codigo] = combo # Para referencia
        print(f"Combos cargados: {len(combos_temp)}")
    except FileNotFoundError:
        print(f"No se encontró '{FILE_COMBOS}'. Creando nuevo...")
    except Exception as e:
        print(f"Error al cargar {FILE_COMBOS}: {e}")

    # 3. Cargar RECETAS (y "rellenar" los combos)
    try:
        with open(FILE_RECETAS, 'r', encoding='utf-8') as f:
            for linea in f:
                partes = linea.strip().split(DELIMITADOR)
                if len(partes) == 3:
                    cod_combo, cod_prod, cantidad = partes
                    # Buscar el combo que ya cargamos
                    if cod_combo in combos_temp:
                        # Añadir el componente a su receta
                        try:
                            combos_temp[cod_combo].receta[cod_prod] = int(cantidad)
                        except ValueError:
                            print(f"Error de formato en receta: {linea}")
        print("Recetas de combos cargadas.")
    except FileNotFoundError:
        print(f"No se encontró '{FILE_RECETAS}'. Creando nuevo...")
    except Exception as e:
        print(f"Error al cargar {FILE_RECETAS}: {e}")

    # 4. Cargar Ventas del Día (pendientes)
    try:
        with open(FILE_VENTAS, 'r', encoding='utf-8') as f:
            for linea in f:
                partes = linea.strip().split(DELIMITADOR)
                if len(partes) == 4:
                    nombre, cantidad, total, ganancia = partes
                    try:
                        ventas_cargadas.append({
                            "producto": nombre, "cantidad": int(cantidad),
                            "total": float(total), "ganancia": float(ganancia)
                        })
                    except ValueError: pass # Ignorar línea mal formada
        print(f"Ventas pendientes cargadas: {len(ventas_cargadas)}")
    except FileNotFoundError:
        print(f"No se encontró '{FILE_VENTAS}'.")

    # 5. Cargar Historial de Cierres
    try:
        with open(FILE_CIERRES, 'r', encoding='utf-8') as f:
            for linea in f:
                partes = linea.strip().split(DELIMITADOR)
                if len(partes) == 4:
                    fecha, total, ganancia, cant_ventas = partes
                    try:
                        cierres_cargados.append({
                            "fecha": fecha, "total_recaudado": float(total),
                            "ganancia_total": float(ganancia), "cantidad_de_ventas": int(cant_ventas)
                        })
                    except ValueError: pass # Ignorar línea mal formada
        print(f"Historial de cierres cargado: {len(cierres_cargados)}")
    except FileNotFoundError:
        print(f"No se encontró '{FILE_CIERRES}'.")

    return inventario_cargado, ventas_cargadas, cierres_cargados
