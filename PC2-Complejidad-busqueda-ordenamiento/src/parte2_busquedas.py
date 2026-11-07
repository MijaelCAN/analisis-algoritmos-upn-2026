#PARTE 2 - ALGORITMOS DE BÚSQUEDA

# Cada búsqueda devuelve (indice, comparaciones). El índice es -1 si el elemento no existe.
 
# ----------------------------------------------------------------------
# 1. BÚSQUEDA LINEAL
# ----------------------------------------------------------------------
def busqueda_lineal(lista, objetivo):
    """Recorre la lista de izquierda a derecha; sirve con cualquier orden. Tiempo: mejor O(1), promedio y peor O(n). Espacio: O(1)."""
    comparaciones = 0
    for i in range(len(lista)):
        comparaciones += 1
        if lista[i] == objetivo:
            return i, comparaciones
    return -1, comparaciones
 
# ----------------------------------------------------------------------
# 2. BÚSQUEDA LINEAL ACOTADA
# ----------------------------------------------------------------------
def busqueda_lineal_acotada(lista, objetivo):
    """Requiere lista ordenada: se detiene al hallar un elemento mayor que el objetivo. Tiempo: mejor O(1), promedio y peor O(n). Espacio: O(1)."""
    comparaciones = 0
    for i in range(len(lista)):
        comparaciones += 1
        if lista[i] == objetivo:
            return i, comparaciones
        if lista[i] > objetivo:            # ya nos pasamos: no existe
            return -1, comparaciones
    return -1, comparaciones
 
# ----------------------------------------------------------------------
# 3. BÚSQUEDA BINARIA ITERATIVA
# ----------------------------------------------------------------------
def busqueda_binaria_iterativa(lista, objetivo):
    """Requiere lista ordenada: descarta la mitad en cada paso. Tiempo: mejor O(1), promedio y peor O(log n). Espacio: O(1)."""
    comparaciones = 0
    inicio = 0
    fin = len(lista) - 1
    while inicio <= fin:
        medio = (inicio + fin) // 2
        comparaciones += 1
        if lista[medio] == objetivo:
            return medio, comparaciones
        elif lista[medio] < objetivo:
            inicio = medio + 1             # descarta la mitad izquierda
        else:
            fin = medio - 1                # descarta la mitad derecha
    return -1, comparaciones
 
# ----------------------------------------------------------------------
# 4. BÚSQUEDA BINARIA RECURSIVA
# ----------------------------------------------------------------------
def busqueda_binaria_recursiva(lista, objetivo, inicio=0, fin=None, comparaciones=0):
    """Requiere lista ordenada: igual que la iterativa, con llamadas recursivas. Tiempo: mejor O(1), promedio y peor O(log n). Espacio: O(log n) por la pila."""
    if fin is None:
        fin = len(lista) - 1
    if inicio > fin:                       # rango vacío: no existe
        return -1, comparaciones
    medio = (inicio + fin) // 2
    comparaciones += 1
    if lista[medio] == objetivo:
        return medio, comparaciones
    if lista[medio] < objetivo:
        return busqueda_binaria_recursiva(lista, objetivo, medio + 1, fin, comparaciones)
    return busqueda_binaria_recursiva(lista, objetivo, inicio, medio - 1, comparaciones)
 
# ----------------------------------------------------------------------
# PRUEBAS
# ----------------------------------------------------------------------
ALGORITMOS = [
    ("Lineal", busqueda_lineal),
    ("Lineal acotada", busqueda_lineal_acotada),
    ("Binaria iterativa", busqueda_binaria_iterativa),
    ("Binaria recursiva", busqueda_binaria_recursiva),
]
 
 
def pruebas_basicas():
    # Datos existentes y no existentes en una lista ordenada
    datos = [3, 8, 15, 23, 42, 57, 64, 71, 89, 96]
    print("Lista ordenada:", datos)
    casos = [
        (3, "existe (primero)"),
        (42, "existe (zona central)"),
        (96, "existe (último)"),
        (1, "NO existe (menor que el mínimo)"),
        (50, "NO existe (entre elementos)"),
        (100, "NO existe (mayor que el máximo)"),
    ]
    for objetivo, descripcion in casos:
        print(f"\nBuscar {objetivo}: {descripcion}")
        esperado = datos.index(objetivo) if objetivo in datos else -1
        for nombre, funcion in ALGORITMOS:
            indice, comps = funcion(datos, objetivo)
            ok = "OK" if indice == esperado else "ERROR"
            print(f"  {nombre:<18} índice={indice:>2}  comparaciones={comps:>2}  [{ok}]")
 
 
def prueba_lista_desordenada():
    # Muestra por qué la búsqueda binaria exige una lista ordenada
    desordenada = [42, 8, 96, 3, 57, 15, 71, 23, 89, 64]
    objetivo = 3                           # existe, en el índice 3
    print("\nLista DESORDENADA:", desordenada, "| objetivo:", objetivo, "(existe en el índice 3)")
    for nombre, funcion in ALGORITMOS:
        indice, comps = funcion(desordenada, objetivo)
        print(f"  {nombre:<18} índice={indice:>2}  comparaciones={comps:>2}")
    print("  -> Binaria (y acotada) fallan porque suponen orden; solo la lineal es válida aquí.")
 
 
def prueba_tamanos():
    # Peor caso: objetivo inexistente mayor que todos los elementos
    print("\nPeor caso: objetivo mayor que todos los elementos")
    print(f"{'n':>7} | {'Lineal':>7} | {'Acotada':>8} | {'Bin. iter.':>10} | {'Bin. rec.':>9} | ⌊log2 n⌋+1")
    for n in (100, 1000, 5000, 10000):
        datos = list(range(0, 2 * n, 2))   # pares ordenados
        objetivo = 2 * n + 1               # no existe
        resultados = [funcion(datos, objetivo)[1] for _, funcion in ALGORITMOS]
        teorico = n.bit_length()           # equivale a ⌊log2 n⌋ + 1
        print(f"{n:>7} | {resultados[0]:>7} | {resultados[1]:>8} | {resultados[2]:>10} | {resultados[3]:>9} | {teorico}")
 
 
if __name__ == "__main__":
    pruebas_basicas()
    prueba_lista_desordenada()
    prueba_tamanos()
 