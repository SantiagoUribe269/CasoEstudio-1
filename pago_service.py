import time
import random
from datetime import datetime

def procesar_pago(monto, metodo_pago="tarjeta"):
    time.sleep(1)
    exito = random.random() > 0.1
    
    return {
        "exitoso": exito,
        "codigo": f"PAGO-{random.randint(100000, 999999)}",
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "monto": monto,
        "metodo": metodo_pago,
        "mensaje": "Pago aprobado" if exito else "Pago rechazado"
    }