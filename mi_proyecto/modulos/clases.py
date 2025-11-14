class Producto:
    """
    Representa un artículo simple con stock propio.
    (Definido por Valentina, Día 1)
    """
    def __init__(self, codigo, nombre, costo, precio_venta, stock_inicial):
        self.codigo = str(codigo)
        self.nombre = str(nombre)
        try:
            self.costo = float(costo)
        except (ValueError, TypeError):
            self.costo = 0.0
        try:
            self.precio_venta = float(precio_venta)
        except (ValueError, TypeError):
            self.precio_venta = 0.0
        try:
            self.stock = int(stock_inicial)
        except (ValueError, TypeError):
            self.stock = 0

    def __str__(self):
        # El __str__ es el método que usa print()
        return f"PRODUCTO: {self.codigo:<10} | Nombre: {self.nombre:<28} | Precio: ${self.precio_venta:>10.2f} | Stock: {self.stock:>5}"

class Combo:
    """
    Representa un "kit" o "combo". Su stock es virtual
    y depende de los componentes del inventario.
    (Definido por Arquitecto, Día 4)
    """
    def __init__(self, codigo, nombre, precio_venta, receta: dict):
        """
        La receta es un diccionario: {'codigo_producto': cantidad_necesaria}
        Ej: {'P001': 1, 'P002': 2}
        """
        self.codigo = str(codigo)
        self.nombre = str(nombre)
        try:
            self.precio_venta = float(precio_venta)
        except (ValueError, TypeError):
             self.precio_venta = 0.0
        self.receta = receta # Ej: {"P001": 1, "P002": 1}
    
    def get_costo(self, inventario: dict):
        """Calcula el costo total del combo basado en sus partes."""
        costo_total = 0.0
        try:
            for codigo_comp, cantidad in self.receta.items():
                producto_comp = inventario.get(codigo_comp)
                # El componente debe existir y ser un Producto
                if not producto_comp or not isinstance(producto_comp, Producto):
                    return 0.0 # Componente no existe
                costo_total += producto_comp.costo * cantidad
        except Exception:
            return 0.0
        return costo_total

    def get_stock_disponible(self, inventario: dict):
        """
        Calcula el stock MÁXIMO de combos que se pueden armar.
        Esta es la lógica clave del combo.
        """
        stocks_posibles = []
        if not self.receta:
            return 0 # Si no hay receta, no hay stock

        try:
            for codigo_comp, cantidad_necesaria in self.receta.items():
                producto_comp = inventario.get(codigo_comp)
                
                if not producto_comp or not isinstance(producto_comp, Producto):
                    return 0 # Componente no existe
                
                if producto_comp.stock <= 0 or cantidad_necesaria <= 0:
                    return 0 # No hay stock o receta mal definida
                
                # (Ej: 20 papas / 2 papas_por_combo = 10 combos)
                stock_max_item = producto_comp.stock // cantidad_necesaria
                stocks_posibles.append(stock_max_item)
            
            # El stock es el MÍNIMO de los posibles.
            if not stocks_posibles:
                return 0
            return min(stocks_posibles)
        
        except Exception:
            return 0 # Error en cálculo

    def __str__(self):
        # El stock no es un atributo, debe calcularse fuera
        return f"COMBO:    {self.codigo:<10} | Nombre: {self.nombre:<28} | Precio: ${self.precio_venta:>10.2f} |"