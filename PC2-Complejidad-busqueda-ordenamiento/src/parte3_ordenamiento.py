

"PARTE 3 - IMPLEMENTACIÓN DE ALGORITMOS DE ORDENAMIENTO CON MENÚ INTERACTIVO"


import random
import time
 
# ----------------------------------------------------------------------
# 1. ORDENAMIENTO POR INTERCAMBIO 
# ----------------------------------------------------------------------
def intercambio(a):
    comp = mov = 0
    n = len(a)
    for i in range(n - 1):
        for j in range(i + 1, n):
            comp += 1
            if a[j] < a[i]:
                a[i], a[j] = a[j], a[i]
                mov += 1
    return comp, mov
 
# ----------------------------------------------------------------------
# 2. BURBUJA 
# ----------------------------------------------------------------------
def burbuja(a):
    comp = mov = 0
    n = len(a)
    for i in range(n - 1):
        hubo_cambio = False
        for j in range(n - 1 - i):
            comp += 1
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                mov += 1
                hubo_cambio = True
        if not hubo_cambio:        # una pasada sin cambios: ya está ordenada
            break
    return comp, mov
 
# ----------------------------------------------------------------------
# 3. INSERCIÓN 
# ----------------------------------------------------------------------
def insercion(a):
    comp = mov = 0
    for i in range(1, len(a)):
        clave = a[i]
        j = i - 1
        while j >= 0:
            comp += 1
            if a[j] > clave:
                a[j + 1] = a[j]    # desplaza a la derecha
                mov += 1
                j -= 1
            else:
                break
        if j + 1 != i:
            a[j + 1] = clave
            mov += 1
    return comp, mov
 
# ----------------------------------------------------------------------
# 4. SELECCIÓN 
#----------------------------------------------------------------------
def seleccion(a):
    comp = mov = 0
    n = len(a)
    for i in range(n - 1):
        minimo = i
        for j in range(i + 1, n):
            comp += 1
            if a[j] < a[minimo]:
                minimo = j
        if minimo != i:
            a[i], a[minimo] = a[minimo], a[i]
            mov += 1
    return comp, mov
 
# ----------------------------------------------------------------------
# 5. QUICKSORT 
# ----------------------------------------------------------------------
def quicksort(a):
    comp = mov = 0
 
    def ordenar(inicio, fin):
        nonlocal comp, mov
        if inicio >= fin:
            return
        pivote = a[(inicio + fin) // 2]
        i, j = inicio, fin
        while i <= j:
            while True:                    # avanza i mientras a[i] < pivote
                comp += 1
                if a[i] < pivote:
                    i += 1
                else:
                    break
            while True:                    # retrocede j mientras a[j] > pivote
                comp += 1
                if a[j] > pivote:
                    j -= 1
                else:
                    break
            if i <= j:
                a[i], a[j] = a[j], a[i]
                mov += 1
                i += 1
                j -= 1
        ordenar(inicio, j)
        ordenar(i, fin)
 
    ordenar(0, len(a) - 1)
    return comp, mov
 
# ----------------------------------------------------------------------
# 6. MERGESORT 
# ----------------------------------------------------------------------
def mergesort(a):
    comp = mov = 0
    aux = a[:]                             # copia auxiliar para la fusión
 
    def ordenar(inicio, fin):
        nonlocal comp, mov
        if inicio >= fin:
            return
        medio = (inicio + fin) // 2
        ordenar(inicio, medio)
        ordenar(medio + 1, fin)
        for t in range(inicio, fin + 1):   # copia el tramo al auxiliar
            aux[t] = a[t]
        i, j, k = inicio, medio + 1, inicio
        while i <= medio and j <= fin:
            comp += 1
            if aux[i] <= aux[j]:
                a[k] = aux[i]
                i += 1
            else:
                a[k] = aux[j]
                j += 1
            k += 1
            mov += 1
        while i <= medio:                  # sobrantes de la mitad izquierda
            a[k] = aux[i]
            i += 1
            k += 1
            mov += 1
        # los sobrantes de la derecha ya están en su lugar
 
    ordenar(0, len(a) - 1)
    return comp, mov
 
# ----------------------------------------------------------------------
# 7. HEAPSORT  
# ----------------------------------------------------------------------

def heapsort(a):
    comp = mov = 0
    n = len(a)
 
    def hundir(i, tamano):
        nonlocal comp, mov
        while True:
            izq = 2 * i + 1
            der = izq + 1
            mayor = i
            if izq < tamano:
                comp += 1
                if a[izq] > a[mayor]:
                    mayor = izq
            if der < tamano:
                comp += 1
                if a[der] > a[mayor]:
                    mayor = der
            if mayor == i:
                break
            a[i], a[mayor] = a[mayor], a[i]
            mov += 1
            i = mayor
 
    for i in range(n // 2 - 1, -1, -1):    # construcción del montículo
        hundir(i, n)
    for fin in range(n - 1, 0, -1):        # extracción de la raíz
        a[0], a[fin] = a[fin], a[0]
        mov += 1
        hundir(0, fin)
    return comp, mov
 
 
ALGORITMOS = [
    ("Intercambio", intercambio),
    ("Burbuja", burbuja),
    ("Inserción", insercion),
    ("Selección", seleccion),
    ("Quicksort", quicksort),
    ("Mergesort", mergesort),
    ("Heapsort", heapsort),
]
 
TIPOS_DATOS = ["Aleatorios", "Ascendentes", "Descendentes", "Con elementos repetidos"]
 
# ----------------------------------------------------------------------
# GENERACIÓN Y VERIFICACIÓN DE DATOS
# ----------------------------------------------------------------------
def generar_datos(tipo, n):
    """Crea el conjunto de entrada según el tipo elegido (1 a 4)."""
    if tipo == 1:
        return [random.randint(1, 10 * n) for _ in range(n)]
    if tipo == 2:
        return list(range(1, n + 1))
    if tipo == 3:
        return list(range(n, 0, -1))
    return [random.randint(1, 10) for _ in range(n)]   # pocos valores distintos
 
 
def contar_valores(lista):
    conteo = {}
    for x in lista:
        conteo[x] = conteo.get(x, 0) + 1
    return conteo
 
 
def verificar(original, resultado):
    """Correcto si está en orden ascendente y tiene exactamente los mismos elementos."""
    for i in range(len(resultado) - 1):
        if resultado[i] > resultado[i + 1]:
            return False
    return len(original) == len(resultado) and contar_valores(original) == contar_valores(resultado)
 
 
def ejecutar(funcion, datos):
    """Ordena una COPIA de los datos; devuelve (lista, comparaciones, movimientos, segundos)."""
    copia = datos[:]
    inicio = time.perf_counter()
    comp, mov = funcion(copia)
    segundos = time.perf_counter() - inicio
    return copia, comp, mov, segundos
 
# ----------------------------------------------------------------------
# MENÚ INTERACTIVO
# ----------------------------------------------------------------------
def pedir_entero(mensaje, minimo, maximo):
    while True:
        texto = input(mensaje).strip()
        if texto.isdigit() and minimo <= int(texto) <= maximo:
            return int(texto)
        print(f"  Ingrese un número entre {minimo} y {maximo}.")
 
 
def vista_previa(lista, limite=15):
    if len(lista) <= limite:
        return str(lista)
    return str(lista[:limite])[:-1] + ", ... ] (" + str(len(lista)) + " elementos)"
 
 
def opcion_generar():
    print("\nTipo de datos:")
    for i, nombre in enumerate(TIPOS_DATOS, 1):
        print(f"  {i}. {nombre}")
    tipo = pedir_entero("Seleccione el tipo: ", 1, 4)
    n = pedir_entero("Tamaño del conjunto (1 a 20000): ", 1, 20000)
    datos = generar_datos(tipo, n)
    print(f"Conjunto generado: {TIPOS_DATOS[tipo - 1]}, n = {n}")
    print("Datos:", vista_previa(datos))
    return datos, tipo
 
 
def opcion_ordenar_uno(datos):
    print("\nAlgoritmos:")
    for i, (nombre, _) in enumerate(ALGORITMOS, 1):
        print(f"  {i}. {nombre}")
    eleccion = pedir_entero("Seleccione el algoritmo: ", 1, len(ALGORITMOS))
    nombre, funcion = ALGORITMOS[eleccion - 1]
    resultado, comp, mov, seg = ejecutar(funcion, datos)
    print(f"\nMétodo: {nombre}")
    print("Original:", vista_previa(datos))
    print("Ordenada:", vista_previa(resultado))
    print(f"Comparaciones: {comp} | Movimientos: {mov} | Tiempo: {seg * 1000:.3f} ms")
    print("Verificación:", "CORRECTO" if verificar(datos, resultado) else "ERROR")
 
 
def opcion_comparar_todos(datos, tipo):
    print(f"\nMismo conjunto para los 7 algoritmos: {TIPOS_DATOS[tipo - 1]}, n = {len(datos)}")
    if len(datos) > 5000:
        print("(Los algoritmos O(n²) pueden tardar unos segundos...)")
    print(f"{'Algoritmo':<12} | {'Comparaciones':>14} | {'Movimientos':>12} | {'Tiempo (ms)':>12} | Verificación")
    print("-" * 74)
    for nombre, funcion in ALGORITMOS:
        resultado, comp, mov, seg = ejecutar(funcion, datos)
        estado = "CORRECTO" if verificar(datos, resultado) else "ERROR"
        print(f"{nombre:<12} | {comp:>14} | {mov:>12} | {seg * 1000:>12.3f} | {estado}")
 
 
def menu():
    datos = None
    tipo = 1
    while True:
        print("\n==========================================")
        print("   MENÚ DE ALGORITMOS DE ORDENAMIENTO")
        print("==========================================")
        print("1. Generar conjunto de datos")
        print("2. Mostrar el conjunto actual")
        print("3. Ordenar con un algoritmo")
        print("4. Comparar los 7 algoritmos (mismos datos)")
        print("5. Salir")
        opcion = input("\nSeleccione una opción: ").strip()
 
        if opcion == "1":
            datos, tipo = opcion_generar()
        elif opcion in ("2", "3", "4") and datos is None:
            print("\nPrimero genere un conjunto de datos (opción 1).")
        elif opcion == "2":
            print(f"\n{TIPOS_DATOS[tipo - 1]}, n = {len(datos)}")
            print("Datos:", vista_previa(datos))
        elif opcion == "3":
            opcion_ordenar_uno(datos)
        elif opcion == "4":
            opcion_comparar_todos(datos, tipo)
        elif opcion == "5":
            print("\nPrograma finalizado.")
            break
        else:
            print("\nOpción inválida. Intente nuevamente.")
 
 
if __name__ == "__main__":
    menu()
    

