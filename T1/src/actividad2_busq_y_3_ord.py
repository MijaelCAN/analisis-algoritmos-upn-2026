
# ------------------------------------------------------------
# ACTIVIDAD 1: DATOS BASE (15 PEDIDOS ORIGINALES) UPN Cargo S.A.C.
# ------------------------------------------------------------
# Esta lista se reutiliza en la Actividad 2 (busqueda) y la Actividad 3 (ordenamiento)

import random
import time


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
    {"codigo": "P015", "cliente": "Claudia Chavez", "ciudad": "Piura", "peso": 7.3, "prioridad": "Baja", "costo": 155.0},
]


# ============================================================
# Actividad 2: ALGORITMOS DE BÚSQUEDA
# ============================================================

# ------------------------------------------------------------
# Busqueda lineal
# ------------------------------------------------------------
def busqueda_lineal(lista, codigo):
    for i, pedido in enumerate(lista):
        if pedido["codigo"] == codigo:
            return i
    return -1
# ------------------------------------------------------------
# Busqueda lineal acotada 
# ------------------------------------------------------------
def busqueda_lineal_acotada(lista, codigo):
    for i, pedido in enumerate(lista):
        if pedido["codigo"] == codigo:
            return i
        if pedido["codigo"] > codigo:
            return -1    # ya se paso del valor buscado: no puede aparecer despues
    return -1
# ------------------------------------------------------------
# Busqueda binaria iterativa
# ------------------------------------------------------------
def busqueda_binaria_iterativa(lista, codigo):
    inicio = 0
    fin = len(lista) - 1

    while inicio <= fin:
        medio = (inicio + fin) // 2    # posicion central del rango actual
        codigo_medio = lista[medio]["codigo"]

        if codigo_medio == codigo:
            return medio
        elif codigo_medio < codigo:
            inicio = medio + 1         # se descarta la mitad izquierda
        else:
            fin = medio - 1            # se descarta la mitad derecha

    return -1
# ------------------------------------------------------------
# Busqueda binaria recursiva
# ------------------------------------------------------------
def busqueda_binaria_recursiva(lista, codigo, inicio=0, fin=None):
    if fin is None:
        fin = len(lista) - 1

    if inicio > fin: 
        return -1  # caso base: el rango quedo vacio, el codigo no existe

    medio = (inicio + fin) // 2
    codigo_medio = lista[medio]["codigo"]

    if codigo_medio == codigo:
        return medio
    elif codigo_medio < codigo:
        return busqueda_binaria_recursiva(
            lista, codigo, medio + 1, fin
        )
    else:
        return busqueda_binaria_recursiva(
            lista, codigo, inicio, medio - 1
        )


algoritmos_busqueda = [
    ("Búsqueda lineal", busqueda_lineal),
    ("Búsqueda lineal acotada", busqueda_lineal_acotada),
    ("Búsqueda binaria iterativa", busqueda_binaria_iterativa),
    ("Búsqueda binaria recursiva", busqueda_binaria_recursiva),
]


def ejecutar_actividad_2():

    pedidos_ordenados = sorted(
        pedidos, key=lambda p: p["codigo"]
    )
   # Prueba con los 15 pedidos de la Actividad 1 (lista "pedidos")
    print("\n===== ACT. 2: PRUEBA CON LOS 15 PEDIDOS =====")

    for nombre, funcion in algoritmos_busqueda:
        encontrado = funcion(pedidos_ordenados, "P009")
        ausente = funcion(pedidos_ordenados, "P099")

        print(
            f"{nombre:30s} "
            f"P009 -> {encontrado:2d} | "
            f"P099 -> {ausente:2d}"
        )

    # Generación de 10 000 pedidos de prueba.
    rng = random.Random(2026)                     # Semilla fija: los datos aleatorios 
    cantidad = 10000
    pedidos_grandes = []

    ciudades = [
        "Lima", "Cusco", "Trujillo",
        "Piura", "Arequipa", "Chiclayo"
    ]

    prioridades = ["Alta", "Media", "Baja"]

    for i in range(1, cantidad + 1):
        pedidos_grandes.append({
            "codigo": f"P{i:05d}",
            "cliente": f"Cliente {rng.randint(1, 5000):04d}",
            "ciudad": rng.choice(ciudades),
            "peso": round(rng.uniform(0.5, 30.0), 2),
            "prioridad": rng.choice(prioridades),
            "costo": round(rng.uniform(30.0, 500.0), 2),
        })

    pedidos_grandes.sort(key=lambda p: p["codigo"])
   # Tres casos: mejor caso (inicio), peor caso (final) y codigo que no existe
    casos = [
        ("Inicio", "P00001"),
        ("Final", "P10000"),
        ("Inexistente", "P99999"),
    ]
   # Cada tiempo es la mediana de 5 mediciones; cada medicion promedia 1000 repeticiones
    repeticiones = 1000
    lotes = 5

    print("\n===== TIEMPOS CON 10 000 PEDIDOS =====")
    print("Tiempo promedio en milisegundos (mediana de 5 mediciones).")

    print(
        f"{'Algoritmo':30s}"
        + "".join(f"{nombre:>16s}" for nombre, _ in casos)
    )

    for nombre, funcion in algoritmos_busqueda:
        resultados = []

        for _, codigo in casos:
            mediciones = []

            for _ in range(lotes):
                inicio_tiempo = time.perf_counter()

                for _ in range(repeticiones):
                    funcion(pedidos_grandes, codigo)

                duracion_ms = (
                    (time.perf_counter() - inicio_tiempo)
                    * 1000 / repeticiones
                )

                mediciones.append(duracion_ms)

            mediciones.sort()
            resultados.append(mediciones[len(mediciones) // 2])

        print(
            f"{nombre:30s}"
            + "".join(f"{valor:16.6f}" for valor in resultados)
        )


# ============================================================
# Actividad 3: ALGORITMOS DE ORDENAMIENTO
# ============================================================


# ------------------------------------------------------------
# Ordenamiento burbuja
# ------------------------------------------------------------
def burbuja(lista):
    datos = lista.copy() # se ordena una copia para no alterar la lista original
    comparaciones = 0
    intercambios = 0

    for fin in range(len(datos) - 1, 0, -1):
        hubo_intercambio = False # permite detener el ciclo si ya esta ordenada

        for j in range(fin):
            comparaciones += 1

            if datos[j]["costo"] > datos[j + 1]["costo"]:
                datos[j], datos[j + 1] = datos[j + 1], datos[j]
                intercambios += 1
                hubo_intercambio = True

        if not hubo_intercambio:
            break # sin cambios: la lista ya esta ordenada

    return datos, comparaciones, intercambios

# ------------------------------------------------------------
# Ordenamiento por seleccion
# ------------------------------------------------------------
def seleccion(lista):
    datos = lista.copy()
    comparaciones = 0
    intercambios = 0

    for i in range(len(datos) - 1):
        indice_minimo = i  # posicion del menor costo encontrado hasta ahora

        for j in range(i + 1, len(datos)):
            comparaciones += 1

            if datos[j]["costo"] < datos[indice_minimo]["costo"]:
                indice_minimo = j

        if indice_minimo != i: # solo se intercambia si el menor no esta ya en su lugar
            datos[i], datos[indice_minimo] = datos[indice_minimo], datos[i]
            intercambios += 1

    return datos, comparaciones, intercambios

# ------------------------------------------------------------
# Ordenamiento por insercion
# ------------------------------------------------------------
def insercion(lista):
    datos = lista.copy()
    comparaciones = 0
    intercambios = 0

    for i in range(1, len(datos)):
        j = i           # el elemento en la posicion i se mueve hacia la izquierda

        while j > 0:
            comparaciones += 1

            if datos[j - 1]["costo"] > datos[j]["costo"]:
                datos[j - 1], datos[j] = datos[j], datos[j - 1]
                intercambios += 1
                j -= 1
            else:
                break # el elemento ya esta en su posicion correcta

    return datos, comparaciones, intercambios


def ejecutar_actividad_3():
    # Se prueban los tres algoritmos con el mismo ciclo
    algoritmos_ordenamiento = [
        ("Burbuja", burbuja),
        ("Selección", seleccion),
        ("Inserción", insercion),
    ]

    print("\n===== ACT. 3: PEDIDOS ORDENADOS POR COSTO =====")
    print(
        f"{'Código':10s} "
        f"{'Cliente':22s} "
        f"{'Costo (S/)':>12s}"
    )

    resultados = []

    for nombre, funcion in algoritmos_ordenamiento:

        lista_ordenada, comparaciones, intercambios = funcion(pedidos)

        resultados.append((
            nombre,
            len(lista_ordenada),
            comparaciones,
            intercambios
        ))

        costos = [
            pedido["costo"] for pedido in lista_ordenada
        ]
        # Verifica que el resultado quedo ordenado de menor a mayor costo
        assert costos == sorted(costos), (
            f"Error: {nombre} no ordenó correctamente."
        )

        if nombre == "Burbuja":
            for pedido in lista_ordenada:
                print(
                    f"{pedido['codigo']:10s} "
                    f"{pedido['cliente']:22s} "
                    f"{pedido['costo']:12.2f}"
                )

    print("\n===== CONTEO DE OPERACIONES =====")

    print(
        f"{'Algoritmo':15s} "
        f"{'Pedidos':>10s} "
        f"{'Comparaciones':>16s} "
        f"{'Intercambios':>15s}"
    )

    for nombre, n, comparaciones, intercambios in resultados:
        print(
            f"{nombre:15s} "
            f"{n:10d} "
            f"{comparaciones:16d} "
            f"{intercambios:15d}"
        )


# ============================================================
# PROGRAMA PRINCIPAL
# EJECUCIÓN DE LAS ACTIVIDADES 2 Y 3
# ============================================================

if __name__ == "__main__":
    ejecutar_actividad_2()
    ejecutar_actividad_3()

    print("\n===== PROGRAMA FINALIZADO CORRECTAMENTE =====")
