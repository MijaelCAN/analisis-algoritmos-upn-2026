# Actividad 1 - Registro de pedidos de UPN Cargo S.A.C.

pedidos = [
    {"codigo": "P001", "cliente": "Ana Torres", "ciudad": "Trujillo", "peso": 5.5, "prioridad": "Alta", "costo": 120.0},
    {"codigo": "P002", "cliente": "Juan Perez", "ciudad": "Lima", "peso": 8.0, "prioridad": "Media", "costo": 180.0},
    {"codigo": "P003", "cliente": "Maria Lopez", "ciudad": "Chiclayo", "peso": 3.2, "prioridad": "Baja", "costo": 75.0},
    {"codigo": "P004", "cliente": "Carlos Ramirez", "ciudad": "Piura", "peso": 12.5, "prioridad": "Alta", "costo": 250.0},
    {"codigo": "P005", "cliente": "Lucia Fernandez", "ciudad": "Arequipa", "peso": 7.8, "prioridad": "Media", "costo": 210.0},
    {"codigo": "P006", "cliente": "Pedro Quispe", "ciudad": "Cusco", "peso": 4.3, "prioridad": "Baja", "costo": 140.0},
    {"codigo": "P007", "cliente": "Ana Maria Soto", "ciudad": "Lima", "peso": 6.7, "prioridad": "Alta", "costo": 165.0},
    {"codigo": "P008", "cliente": "Diego Castillo", "ciudad": "Trujillo", "peso": 2.5, "prioridad": "Media", "costo": 65.0},
    {"codigo": "P009", "cliente": "Rosa Vargas", "ciudad": "Piura", "peso": 9.4, "prioridad": "Alta", "costo": 230.0},
    {"codigo": "P010", "cliente": "Mariana Flores", "ciudad": "Chiclayo", "peso": 1.8, "prioridad": "Baja", "costo": 50.0},
    {"codigo": "P011", "cliente": "Luis Mendoza", "ciudad": "Cusco", "peso": 15.0, "prioridad": "Alta", "costo": 320.0},
    {"codigo": "P012", "cliente": "Carmen Diaz", "ciudad": "Arequipa", "peso": 5.1, "prioridad": "Media", "costo": 175.0},
    {"codigo": "P013", "cliente": "Jose Huaman", "ciudad": "Trujillo", "peso": 11.2, "prioridad": "Alta", "costo": 245.0},
    {"codigo": "P014", "cliente": "Ana Lucia Rojas", "ciudad": "Lima", "peso": 4.9, "prioridad": "Media", "costo": 130.0},
    {"codigo": "P015", "cliente": "Claudia Chavez", "ciudad": "Piura", "peso": 7.3, "prioridad": "Baja", "costo": 155.0}
]


# Funcion para buscar pedidos por nombre de cliente
def buscar_por_cliente(lista, texto):
    resultados = []
    texto = texto.strip().lower()

    if not texto:
        return resultados

    for pedido in lista:
        if texto in pedido["cliente"].lower():
            resultados.append(pedido)

    return resultados


if __name__ == "__main__":
    # Mostrar todos los pedidos registrados
    print("===== PEDIDOS REGISTRADOS - UPN CARGO =====")
    print(f"Total de pedidos: {len(pedidos)}\n")

    for pedido in pedidos:
        print(
            f"{pedido['codigo']} | {pedido['cliente']} | "
            f"{pedido['ciudad']} | {pedido['peso']} kg | "
            f"{pedido['prioridad']} | S/ {pedido['costo']:.2f}"
        )

    # Buscar clientes
    print("\n===== BUSQUEDA POR CLIENTE =====")
    nombre = input("Ingrese el nombre o parte del nombre: ")

    encontrados = buscar_por_cliente(pedidos, nombre)

    if encontrados:
        print(f"\nSe encontraron {len(encontrados)} pedidos:")
        for pedido in encontrados:
            print(
                f"{pedido['codigo']} | {pedido['cliente']} | "
                f"{pedido['ciudad']} | S/ {pedido['costo']:.2f}"
            )
    else:
        print("No se encontraron pedidos para ese cliente.")
