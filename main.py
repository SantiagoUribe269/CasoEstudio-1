from venta_service import (
    obtener_productos,
    buscar_producto,
    verificar_inventario,
    procesar_venta
)
import json

def mostrar_menu_principal():
    print("\n" + "="*50)
    print("SISTEMA DE VENTAS DE FARMACIA - POC")
    print("="*50)
    print("1. Listar productos disponibles")
    print("2. Ver inventario completo")
    print("3. Realizar una venta")
    print("4. Ver historial de transacciones")
    print("5. Salir")
    print("="*50)

def mostrar_productos():
    productos = obtener_productos()
    print("\n" + "="*50)
    print("LISTA DE PRODUCTOS DISPONIBLES")
    print("="*50)
    for producto in productos:
        print(f"\nID: {producto['id']}")
        print(f"Nombre: {producto['nombre']}")
        print(f"Precio: ${producto['precio']:.2f}")
        print(f"Descripcion: {producto['descripcion']}")
        print(f"Categoria: {producto['categoria']}")
        print(f"Requiere receta: {'Si' if producto['requiere_receta'] else 'No'}")
    print("="*50)

def mostrar_inventario():
    inventario = json.load(open("data/inventario.json"))
    print("\n" + "="*50)
    print("INVENTARIO ACTUAL")
    print("="*50)
    for ubicacion, estanterias in inventario.items():
        print(f"\nUBICACION: {ubicacion}")
        for estanteria, productos in estanterias.items():
            print(f"\nESTANTERIA: {estanteria}")
            for prod_id, cantidad in productos.items():
                producto = buscar_producto(prod_id)
                nombre = producto['nombre'] if producto else "Producto desconocido"
                print(f"  {prod_id}: {nombre} - {cantidad} unidades")
    print("="*50)

def realizar_venta():
    print("\n" + "="*50)
    print("PROCESO DE VENTA")
    print("="*50)
    
    mostrar_productos()
    
    try:
        producto_id = input("\nIngrese el ID del producto: ").strip().upper()
        cantidad = int(input("Cantidad a vender: "))
        ubicacion = input("Ubicacion (FARMACIA_CENTRAL): ").strip().upper() or "FARMACIA_CENTRAL"
        estanteria = input("Estanteria (ESTANTERIA_A): ").strip().upper() or "ESTANTERIA_A"
        metodo_pago = input("Metodo de pago (tarjeta/efectivo): ").strip().lower() or "tarjeta"
        
        print("\nProcesando venta...")
        
        venta = procesar_venta(
            producto_id=producto_id,
            cantidad=cantidad,
            ubicacion=ubicacion,
            estanteria=estanteria,
            metodo_pago=metodo_pago
        )
        
        print("\n" + "="*50)
        print("VENTA EXITOSA")
        print("="*50)
        print(f"Fecha: {venta['fecha']}")
        print(f"Producto: {venta['producto']['nombre']}")
        print(f"Cantidad: {venta['cantidad']}")
        print(f"Total: ${venta['total']:.2f}")
        print(f"Ubicacion: {venta['ubicacion']}/{venta['estanteria']}")
        print(f"Pago: {venta['pago']['mensaje']} ({venta['pago']['codigo']})")
        print("="*50)
        
    except ValueError as e:
        print(f"\nError: {str(e)}")
    except Exception as e:
        print(f"\nError inesperado: {str(e)}")

def mostrar_transacciones():
    try:
        transacciones = json.load(open("data/transacciones.json"))
        print("\n" + "="*50)
        print("HISTORIAL DE TRANSACCIONES")
        print("="*50)
        
        if not transacciones:
            print("No hay transacciones registradas aun")
        else:
            for venta in transacciones:
                print(f"\nTransaccion #{venta['id']}")
                print(f"Fecha: {venta['fecha']}")
                print(f"Producto: {venta['producto']['nombre']} ({venta['producto']['id']})")
                print(f"Cantidad: {venta['cantidad']} | Total: ${venta['total']:.2f}")
                print(f"Ubicacion: {venta['ubicacion']}/{venta['estanteria']}")
                print(f"Pago: {venta['pago']['mensaje']} ({venta['pago']['codigo']})")
                print("-"*50)
        
    except FileNotFoundError:
        print("\nNo se encontro el historial de transacciones")

def main():
    while True:
        mostrar_menu_principal()
        opcion = input("\nSeleccione una opcion (1-5): ")
        
        if opcion == "1":
            mostrar_productos()
        elif opcion == "2":
            mostrar_inventario()
        elif opcion == "3":
            realizar_venta()
        elif opcion == "4":
            mostrar_transacciones()
        elif opcion == "5":
            print("\nGracias por usar el sistema!")
            break
        else:
            print("\nOpcion no valida. Intente nuevamente.")
        
        input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    main()