from .clases import Producto, Combo

def registrar_articulo_nuevo(inventario):
    """
    (Opción 1) Lógica de Juani (código base).
    Añadida validación de números que faltaba del plan.
    """
    print("\n--- 1. Registrar Nuevo Producto Simple ---")
    codigo = input('Codigo del producto: ').strip()
    if not codigo:
        print('Debe ingresar un codigo')
        return
    if codigo in inventario:
        print(f'El codigo {codigo} ya existe en el inventario')
        return

    nombre = input('Nombre del producto: ').strip()
    if not nombre:
        print('Debe ingresar un nombre')
        return

    try:
        costo = float(input('Costo del producto: '))
        precio_venta = float(input('Precio de venta: '))
        stock_inicial = int(input('Stock inicial: '))
    except ValueError:
        print("Error: Costo, precio y stock deben ser números válidos.")
        return

    if costo < 0 or precio_venta < 0 or stock_inicial < 0:
        print("Error: Los valores numéricos no pueden ser negativos.")
        return

    # Crear el objeto Producto y guardarlo en el inventario
    producto = Producto(codigo, nombre, costo, precio_venta, stock_inicial)
    inventario[codigo] = producto
    print(f'Producto {nombre} agregado correctamente al inventario')
    
def ver_listado_productos(inventario):
    """
    (Opción 5) Lógica de Juani (código base)
    MODIFICADA para que entienda la diferencia entre Producto y Combo.
    """
    print('\n--- 5. Listado de productos ---')
    if not inventario:
        print('El inventario está vacio')
        return

    print("-" * 80)
    for item in inventario.values():
        if isinstance(item, Producto):
            print(item) # Llama al __str__ de Producto
        
        elif isinstance(item, Combo):
            # Para combos, debemos calcular el stock al momento
            stock_calc = item.get_stock_disponible(inventario)
            # Imprime el __str__ del combo + el stock calculado
            print(f"{item} Stock Disp: {stock_calc:>5}") 

    print("-" * 80)

def registrar_venta(inventario, ventas_del_dia):
    """
    (Opción 4) Lógica de Fabricio (código base)
    CORREGIDA por bug de stock y MODIFICADA para Combos.
    """
    print("\n--- 4. Registrar Venta ---")
    codigo=input("Ingrese el codigo del producto a vender: ").strip()

    item_a_vender = inventario.get(codigo)

    if not item_a_vender:
        print("ERROR, Producto no encontrado")
        return
    
    # --- MODIFICACIÓN (COMBO): Diferenciar lógica ---

    if isinstance(item_a_vender, Producto):
        producto = item_a_vender # Renombrar para claridad
        
        try:
            cantidad_vender = int(input(f"Producto: {producto.nombre}. Stock: {producto.stock}. Ingrese cantidad: "))
        except ValueError:
            print("ERROR, la cantidad debe ser un numero entero. ")
            return
        
        if cantidad_vender <= 0:
            print("ERROR, no se puede vender productos con cantidad negativa ")
            return
        
        if producto.stock < cantidad_vender:
            print(f"Stock insuficiente, solo hay {producto.stock} unidades ")

            return
      

        producto.stock -= cantidad_vender

        total_venta = producto.precio_venta * cantidad_vender
        ganancia = (producto.precio_venta - producto.costo) * cantidad_vender

        venta = {
            "producto": producto.nombre,
            "cantidad": cantidad_vender,
            "total": total_venta,
            "ganancia": ganancia
        }

        ventas_del_dia.append(venta)
        print(f"Venta (Producto) registrada exitosamente!")
        print(f"   Total: ${total_venta:.2f}")
        print(f"   Stock restante: {producto.stock}")

    # LÓGICA DE COMBO 
    elif isinstance(item_a_vender, Combo):
        combo = item_a_vender # Renombrar para claridad
        stock_disponible = combo.get_stock_disponible(inventario)
        
        try:
            cantidad_vender = int(input(f"Combo: {combo.nombre}. Stock DISPONIBLE: {stock_disponible}. Ingrese cantidad: "))
        except ValueError:
            print("ERROR, la cantidad debe ser un numero entero.")
            return
            
        if cantidad_vender <= 0:
            print("ERROR, no se puede vender cantidad 0 o negativa.")
            return

        if stock_disponible < cantidad_vender:
            print(f"Stock insuficiente, solo se pueden armar {stock_disponible} combos.")
            return

        for _ in range(cantidad_vender):
            for cod_comp, cant in combo.receta.items():
                inventario[cod_comp].stock -= cant
        
        costo_combo = combo.get_costo(inventario)
        total_venta = combo.precio_venta * cantidad_vender
        ganancia = (combo.precio_venta - costo_combo) * cantidad_vender

        venta = {
            "producto": combo.nombre + " (Combo)",
            "cantidad": cantidad_vender,
            "total": total_venta,
            "ganancia": ganancia
        }
        ventas_del_dia.append(venta)
        print(f" Venta (Combo) registrada! Total: ${total_venta:.2f}.")
        print("   Se descontó el stock de los componentes.")

def modificar_precio(inventario):
    """
    (Opción 6) Lógica de Fabricio (código base)
    Esta función funciona bien para Productos y Combos
    ya que ambos tienen .nombre y .precio_venta
    """
    print("\n--- 6. Modificar Precio ---")
    codigo= input("Ingre el codigo del producto ").strip()

    if codigo not in inventario:
        print("ERROR, Producto no encontrado ")
        return
    producto = inventario[codigo] # 'producto' aquí es un 'item'

    print(f"El precio actual del producto {producto.nombre} es ${producto.precio_venta} ")

    try:
        nuevo_precio= float(input("Ingrese un nuevo precio del producto "))
    except ValueError:
        print("ERROR; EL nuevo precio debe ser un nuemero ")
        return
    
    if nuevo_precio < 0:
        print("ERROR, el precio no puede ser NEGATIVO ")
        return
    
    producto.precio_venta= nuevo_precio
    print("Precio actualizado exitosamente ")

#  Funciones de Gena 
def cierre_de_caja(ventas_del_dia, cierres_de_caja):

    print("\n--- 8. Cierre de Caja ---")
    fecha = input("Ingresa fecha (dd/mm/aaaa): ").strip()
    if not fecha:
        print("Operación cancelada.")
        return
    
    if not ventas_del_dia:
        print("No se registraron ventas en el día de hoy")
        return

    total_recaudado = 0
    ganancia_total = 0

    print("--- Detalle de Ventas ---")
    for venta in ventas_del_dia:
        total_recaudado += venta["total"]
        ganancia_total += venta["ganancia"]
        print(f"  {venta['cantidad']} x {venta['producto']} - Total: ${venta['total']:.2f}")

    print("\n  --- RESUMEN DE CIERRE ---")
    print(f"Fecha: {fecha}")
    print(f"Total recaudado: ${total_recaudado: }")
    print(f"Ganancia total: ${ganancia_total: }")

    cierre = {
        "fecha": fecha,
        "total_recaudado": total_recaudado,
        "ganancia_total": ganancia_total,
        "cantidad_de_ventas": len(ventas_del_dia),
    }
    cierres_de_caja.append(cierre)

    ventas_del_dia.clear()
    print("\nCierre de caja guardado. Las ventas del día han sido reiniciadas.")


def eliminar_articulo(inventario):
    """
    (Opción 7) Lógica de Gena (código base)
    CORREGIDA para que use 'str' para el código, no 'int'.
    """
    print("\n--- 7. Eliminar Item ---")

    codigo = input("Ingrese el código del producto que desea eliminar: ").strip()

    if codigo not in inventario:
        print("ERROR: Producto no encontrado en el inventario")
    else:     
        producto = inventario[codigo]
        confirmar = input(f"¿Seguro que desea eliminar '{producto.nombre}' del inventario? (si/no): ").lower()
        if confirmar == "si":
            inventario.pop(codigo)
            print(f"Producto '{producto.nombre}' eliminado correctamente")
        else:
            print("Operación cancelada")
    
def registrar_compra_stock(inventario):
    """
    (Opción 3) Lógica de Gena (código base)
    CORREGIDA por bug de 'int' y bug de 'return'.
    MODIFICADA para no agregar stock a Combos.
    """
    print("\n--- 3. Registrar Compra (Agregar Stock) ---")
    

    codigo = input("Ingrese el código del producto a cargar en el stock: ").strip()


    if codigo not in inventario:
        print("ERROR: Producto no encontrado en el inventario")
        return 
    # Validar que no sea un combo
    item = inventario[codigo]
    if not isinstance(item, Producto):
        print(f"ERROR: '{item.nombre}' es un Combo. No se puede agregar stock a un combo.")
        print("       Debe agregar stock a sus componentes individuales.")
        return


    # Si 'item' es un 'producto'
    producto = item
    print(f"Producto seleccionado: {producto.nombre} - Stock actual: {producto.stock}")

    cantidad_agregar = input("Ingrese la cantidad a agregar al stock: ")
    
    try:
        cantidad_agregar = int(cantidad_agregar)
        if cantidad_agregar <= 0:
            print("ERROR: La cantidad debe ser mayor que cero")
        else:
            producto.stock += cantidad_agregar
            print(f"Stock actualizado correctamente. Nuevo total: {producto.stock}")
    except ValueError:
        print("ERROR: La cantidad debe ser un número entero")   


def registrar_combo_nuevo(inventario: dict):
    """
    (Opción 2) Lógica nueva para crear un Combo.
    """
    print("\n--- 2. Registrar Nuevo Combo ---")
    codigo = input("Ingrese el CÓDIGO del combo (ej: 'C001'): ").strip()
    
    if not codigo:
        print("Error: El código no puede estar vacío.")
        return
    if codigo in inventario:
        print(f"Error: El código '{codigo}' ya existe.")
        return 

    nombre = input("Ingrese el Nombre del Combo: ").strip()
    if not nombre:
        print("Error: El nombre no puede estar vacío.")
        return

    try:
        precio_venta = float(input(f"Ingrese el Precio de Venta para '{nombre}' (ej: 15.00): "))
    except ValueError:
        print("Error: Precio inválido.")
        return

    # Construir la receta
    receta = {}
    print("--- Componentes del Combo ---")
    while True:
        cod_comp = input("  Ingrese CÓDIGO de componente (o 'fin' para terminar): ").strip()
        if cod_comp == 'fin':
            break
        
        componente = inventario.get(cod_comp)
        
        # Validación del componente
        if not componente:
            print(f"Error: Código '{cod_comp}' no encontrado.")
            continue
        if not isinstance(componente, Producto):
            print(f"Error: '{componente.nombre}' es un COMBO. Un combo solo puede contener PRODUCTOS.")
            continue
        
        try:
            cantidad = int(input(f"  Ingrese CANTIDAD de '{componente.nombre}' para este combo: "))
            if cantidad <= 0:
                print("La cantidad debe ser positiva.")
                continue
            receta[cod_comp] = cantidad
            print(f"  -> Agregado: {cantidad} x {componente.nombre}")
        except ValueError:
            print("Error: Cantidad inválida.")
    
    if not receta:
        print("Error: Un combo debe tener al menos un componente. Creación cancelada.")
        return
    
    # Crear y guardar el combo
    nuevo_combo = Combo(codigo, nombre, precio_venta, receta)
    inventario[codigo] = nuevo_combo
    print(f"¡Éxito! Combo '{nuevo_combo.nombre}' (Cód: {nuevo_combo.codigo}) fue agregado.")