import json
import os
from datetime import datetime

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

def cargar_json(nombre_archivo, default=[]):
    try:
        with open(f"{DATA_DIR}/{nombre_archivo}", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default

def guardar_json(nombre_archivo, datos):
    with open(f"{DATA_DIR}/{nombre_archivo}", "w") as f:
        json.dump(datos, f, indent=2)

def obtener_productos():
    return cargar_json("productos.json")

def buscar_producto(producto_id):
    productos = obtener_productos()
    for producto in productos:
        if producto["id"] == producto_id:
            return producto
    return None

def verificar_inventario(producto_id, ubicacion, estanteria):
    inventario = cargar_json("inventario.json", default={})
    try:
        return inventario[ubicacion][estanteria].get(producto_id, 0)
    except KeyError:
        return 0

def actualizar_inventario(producto_id, cantidad, ubicacion, estanteria):
    inventario = cargar_json("inventario.json", default={})
    
    if ubicacion not in inventario:
        inventario[ubicacion] = {}
    if estanteria not in inventario[ubicacion]:
        inventario[ubicacion][estanteria] = {}
    
    inventario[ubicacion][estanteria][producto_id] = max(0, inventario[ubicacion][estanteria].get(producto_id, 0) - cantidad)
    guardar_json("inventario.json", inventario)

def registrar_venta(datos_venta):
    transacciones = cargar_json("transacciones.json")
    transacciones.append(datos_venta)
    guardar_json("transacciones.json", transacciones)
    return datos_venta

def procesar_venta(producto_id, cantidad, ubicacion, estanteria, metodo_pago="tarjeta"):
    from pago_service import procesar_pago
    
    producto = buscar_producto(producto_id)
    if not producto:
        raise ValueError(f"Producto {producto_id} no encontrado")
    
    stock = verificar_inventario(producto_id, ubicacion, estanteria)
    if stock < cantidad:
        raise ValueError(f"Stock insuficiente. Disponible: {stock}")
    
    total = producto["precio"] * cantidad
    resultado_pago = procesar_pago(total, metodo_pago)
    
    if not resultado_pago["exitoso"]:
        raise ValueError(resultado_pago['mensaje'])
    
    actualizar_inventario(producto_id, cantidad, ubicacion, estanteria)
    
    venta = {
        "id": len(cargar_json("transacciones.json")) + 1,
        "fecha": datetime.now().isoformat(),
        "producto": producto,
        "cantidad": cantidad,
        "total": total,
        "ubicacion": ubicacion,
        "estanteria": estanteria,
        "pago": resultado_pago
    }
    
    return registrar_venta(venta)