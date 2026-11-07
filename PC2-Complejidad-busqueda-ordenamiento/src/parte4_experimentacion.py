
"""Experimentacion y comparacion de algoritmos de busqueda y ordenamiento."""
import argparse
import csv
import json
import math
import platform
import random
import statistics
import sys
from collections import Counter
from pathlib import Path
from time import perf_counter_ns, get_clock_info
from xml.sax.saxutils import escape


def busqueda_lineal(lista, objetivo):
    comparaciones = 0
    for i in range(len(lista)):
        comparaciones += 1
        if lista[i] == objetivo:
            return i, comparaciones
    return -1, comparaciones


def busqueda_lineal_acotada(lista, objetivo):
    # Requiere orden ascendente. Cuenta igualdad y cota por separado.
    comparaciones = 0
    for i in range(len(lista)):
        comparaciones += 1
        if lista[i] == objetivo:
            return i, comparaciones
        comparaciones += 1
        if lista[i] > objetivo:
            return -1, comparaciones
    return -1, comparaciones


def busqueda_binaria_iterativa(lista, objetivo):
    # Requiere orden ascendente. No cuenta inicio <= fin como dato comparado.
    inicio, fin, comparaciones = 0, len(lista) - 1, 0
    while inicio <= fin:
        medio = (inicio + fin) // 2
        comparaciones += 1
        if lista[medio] == objetivo:
            return medio, comparaciones
        comparaciones += 1
        if lista[medio] < objetivo:
            inicio = medio + 1
        else:
            fin = medio - 1
    return -1, comparaciones


def busqueda_binaria_recursiva(lista, objetivo, inicio=0, fin=None,
                              comparaciones=0):
    # Usa indices: no copia sublistas. Espacio de pila O(log n).
    if fin is None:
        fin = len(lista) - 1
    if inicio > fin:
        return -1, comparaciones
    medio = (inicio + fin) // 2
    comparaciones += 1
    if lista[medio] == objetivo:
        return medio, comparaciones
    comparaciones += 1
    if lista[medio] < objetivo:
        return busqueda_binaria_recursiva(
            lista, objetivo, medio + 1, fin, comparaciones)
    return busqueda_binaria_recursiva(
        lista, objetivo, inicio, medio - 1, comparaciones)


def intercambio(a):
    comp = mov = 0
    n = len(a)
    for i in range(n - 1):
        for j in range(i + 1, n):
            comp += 1
            if a[j] < a[i]:
                a[i], a[j] = a[j], a[i]
                mov += 2
    return comp, mov


def burbuja(a):
    comp = mov = 0
    n = len(a)
    for i in range(n - 1):
        hubo_cambio = False
        for j in range(n - 1 - i):
            comp += 1
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                mov += 2
                hubo_cambio = True
        if not hubo_cambio:        # una pasada sin cambios: ya está ordenada
            break
    return comp, mov


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
            mov += 2
    return comp, mov


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
                mov += 2
                i += 1
                j -= 1
        ordenar(inicio, j)
        ordenar(i, fin)
 
    ordenar(0, len(a) - 1)
    return comp, mov


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
            mov += 2
            i = mayor
 
    for i in range(n // 2 - 1, -1, -1):    # construcción del montículo
        hundir(i, n)
    for fin in range(n - 1, 0, -1):        # extracción de la raíz
        a[0], a[fin] = a[fin], a[0]
        mov += 2
        hundir(0, fin)
    return comp, mov

BUSQUEDAS = [
    ("Lineal", busqueda_lineal),
    ("Lineal acotada", busqueda_lineal_acotada),
    ("Binaria iterativa", busqueda_binaria_iterativa),
    ("Binaria recursiva", busqueda_binaria_recursiva),
]
ORDENAMIENTOS = [
    ("Intercambio", intercambio), ("Burbuja", burbuja),
    ("Insercion", insercion), ("Seleccion", seleccion),
    ("Quicksort", quicksort), ("Mergesort", mergesort),
    ("Heapsort", heapsort),
]
TIPOS = ("Aleatorios", "Ascendentes", "Descendentes", "Repetidos")
TAMANOS = (100, 1000, 5000, 10000)
SEMILLA = 20261020


def generar_datos(tipo, n):
    # Semilla fija para cada tamano y tipo de entrada.
    rng = random.Random(SEMILLA + 10 * n + TIPOS.index(tipo))
    if tipo == "Aleatorios":
        return rng.sample(range(1, 10 * n + 1), n)  # valores distintos
    if tipo == "Ascendentes":
        return list(range(1, n + 1))
    if tipo == "Descendentes":
        return list(range(n, 0, -1))
    return [rng.randint(1, 10) for _ in range(n)]


def verificar_ordenamiento(original, resultado):
    # Verifica orden y conservacion de todos los valores, incluidos repetidos.
    return (all(resultado[i] <= resultado[i + 1]
                for i in range(len(resultado) - 1))
            and Counter(original) == Counter(resultado))


def experimentar_busquedas(tamanos, repeticiones, lote):
    filas, crudas = [], []
    for n in tamanos:
        # Pares unicos y ordenados: los impares permiten probar ausencias.
        datos = list(range(0, 2 * n, 2))
        casos = [
            ("Existe primero", datos[0], 0),
            ("Existe centro", datos[(n - 1) // 2], (n - 1) // 2),
            ("Existe ultimo", datos[-1], n - 1),
            ("No existe menor", -1, -1),
            ("No existe intermedio", datos[n // 2] + 1, -1),
            ("No existe mayor", 2 * n + 1, -1),
        ]
        for caso, objetivo, esperado in casos:
            for nombre, funcion in BUSQUEDAS:
                funcion(datos, objetivo)  # calentamiento fuera de la medicion
                tiempos = []
                for repeticion in range(1, repeticiones + 1):
                    inicio = perf_counter_ns()
                    for _ in range(lote):
                        indice, comp = funcion(datos, objetivo)
                    tiempo_ms = (perf_counter_ns() - inicio) / lote / 1e6
                    if indice != esperado:
                        raise AssertionError((nombre, n, caso, indice))
                    tiempos.append(tiempo_ms)
                    crudas.append(dict(familia="Busqueda", tipo=caso, n=n,
                        algoritmo=nombre, repeticion=repeticion,
                        tiempo_ms=tiempo_ms, comparaciones=comp, movimientos=0,
                        llamadas_por_muestra=lote, correcto=True))
                filas.append(dict(n=n, caso=caso, objetivo=objetivo,
                    algoritmo=nombre, indice=indice, comparaciones=comp,
                    movimientos=0, tiempo_ms=statistics.median(tiempos),
                    repeticiones=repeticiones, llamadas_por_muestra=lote,
                    correcto=True))
        print("Busquedas verificadas: n =", n, flush=True)
    return filas, crudas


def experimentar_ordenamientos(tamanos, repeticiones):
    filas, crudas = [], []
    # Calentamiento para todos los metodos, fuera de la medicion.
    for _, funcion in ORDENAMIENTOS:
        funcion([3, 1, 2])
    for n in tamanos:
        for tipo in TIPOS:
            datos = generar_datos(tipo, n)
            muestras = {nombre: [] for nombre, _ in ORDENAMIENTOS}
            conteos = {}
            for repeticion in range(1, repeticiones + 1):
                # Rota el orden para reducir el efecto de ejecutar siempre
                # un algoritmo primero. No modifica los datos de entrada.
                offset = (repeticion - 1) % len(ORDENAMIENTOS)
                orden = ORDENAMIENTOS[offset:] + ORDENAMIENTOS[:offset]
                for nombre, funcion in orden:
                    copia = datos[:]  # copia excluida del tiempo
                    inicio = perf_counter_ns()
                    comp, mov = funcion(copia)
                    tiempo_ms = (perf_counter_ns() - inicio) / 1e6
                    if not verificar_ordenamiento(datos, copia):
                        raise AssertionError((nombre, n, tipo))
                    if nombre in conteos and conteos[nombre] != (comp, mov):
                        raise AssertionError("Conteos no reproducibles")
                    conteos[nombre] = (comp, mov)
                    muestras[nombre].append(tiempo_ms)
                    crudas.append(dict(familia="Ordenamiento", tipo=tipo, n=n,
                        algoritmo=nombre, repeticion=repeticion,
                        tiempo_ms=tiempo_ms, comparaciones=comp, movimientos=mov,
                        llamadas_por_muestra=1, correcto=True))
            for nombre, _ in ORDENAMIENTOS:
                comp, mov = conteos[nombre]
                filas.append(dict(n=n, tipo=tipo, algoritmo=nombre,
                    comparaciones=comp, movimientos=mov,
                    tiempo_ms=statistics.median(muestras[nombre]),
                    repeticiones=repeticiones, correcto=True))
            print("Ordenamientos verificados: n =", n, "|", tipo, flush=True)
    return filas, crudas


def guardar_csv(ruta, filas):
    with ruta.open("w", newline="", encoding="utf-8-sig") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=list(filas[0]))
        escritor.writeheader()
        escritor.writerows(filas)


def grafico_svg(ruta, titulo, etiqueta_y, series):
    # SVG sin dependencias externas. Escalas logaritmicas en ambos ejes.
    ancho, alto = 960, 570
    izq, der, arriba, abajo = 105, 720, 65, 450
    colores = ["#1763a6", "#bd3d37", "#23835b", "#9b6a08",
               "#794eb3", "#168694", "#b84984"]
    puntos = [p for _, valores in series for p in valores if p[1] > 0]
    xmin, xmax = min(p[0] for p in puntos), max(p[0] for p in puntos)
    ymin, ymax = min(p[1] for p in puntos), max(p[1] for p in puntos)
    if ymin == ymax:
        ymin, ymax = ymin / 2, ymax * 2
    if xmin == xmax:
        xmin, xmax = xmin / 2, xmax * 2
    lymin, lymax = math.log10(ymin) - .1, math.log10(ymax) + .1
    def x(v):
        return izq + (math.log10(v) - math.log10(xmin)) / (
            math.log10(xmax) - math.log10(xmin)) * (der - izq)
    def y(v):
        return abajo - (math.log10(v) - lymin) / (lymax - lymin) * (abajo - arriba)
    partes = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{ancho}" height="{alto}" viewBox="0 0 {ancho} {alto}">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<g font-family="Arial,sans-serif" font-size="13" fill="#263445">',
        f'<text x="30" y="30" font-size="20">{escape(titulo)}</text>']
    for v in dict.fromkeys(p[0] for p in puntos):
        xx = x(v)
        partes += [f'<path d="M {xx} {arriba} V {abajo}" stroke="#e2e6eb"/>',
                   f'<text x="{xx}" y="{abajo + 24}" text-anchor="middle">{v}</text>']
    for i in range(6):
        lv = lymin + i * (lymax - lymin) / 5
        v = 10 ** lv
        yy = y(v)
        partes += [f'<path d="M {izq} {yy} H {der}" stroke="#e2e6eb"/>',
                   f'<text x="{izq - 10}" y="{yy + 4}" text-anchor="end">{v:.3g}</text>']
    partes += [f'<path d="M {izq} {arriba} V {abajo} H {der}" fill="none" stroke="#263445"/>',
               f'<text x="400" y="505">Tamano n (escala logaritmica)</text>',
               f'<text transform="translate(20,300) rotate(-90)" text-anchor="middle">{escape(etiqueta_y)} (escala logaritmica)</text>']
    for i, (nombre, valores) in enumerate(series):
        color = colores[i % len(colores)]
        coords = " ".join(f"{x(a):.2f},{y(b):.2f}" for a, b in valores if b > 0)
        partes.append(f'<polyline points="{coords}" fill="none" stroke="{color}" stroke-width="2"/>')
        for a, b in valores:
            if b > 0:
                partes.append(f'<circle cx="{x(a)}" cy="{y(b)}" r="3" fill="{color}"/>')
        yy = 90 + i * 27
        partes += [f'<path d="M 745 {yy} h 22" stroke="{color}" stroke-width="3"/>',
                   f'<text x="775" y="{yy + 4}">{escape(nombre)}</text>']
    partes.append('<text x="30" y="550" font-size="12">Resultados medidos; las lineas unen los cuatro tamanos, no predicen puntos intermedios.</text></g></svg>')
    ruta.write_text("\n".join(partes), encoding="utf-8")


def guardar_graficos(carpeta, busquedas, ordenamientos):
    carpeta.mkdir(exist_ok=True)
    for tipo in TIPOS:
        for metrica in ("tiempo_ms", "comparaciones"):
            series = [(nombre, [(r["n"], r[metrica]) for r in ordenamientos
                        if r["tipo"] == tipo and r["algoritmo"] == nombre])
                      for nombre, _ in ORDENAMIENTOS]
            grafico_svg(carpeta / ("ordenamiento_" + tipo.lower() + "_" + metrica + ".svg"),
                "Ordenamiento - " + tipo, "Tiempo mediano (ms)" if metrica == "tiempo_ms" else "Comparaciones", series)
    for metrica in ("tiempo_ms", "comparaciones"):
        series = [(nombre, [(r["n"], r[metrica]) for r in busquedas
                    if r["caso"] == "No existe mayor" and r["algoritmo"] == nombre])
                  for nombre, _ in BUSQUEDAS]
        grafico_svg(carpeta / ("busqueda_" + metrica + ".svg"),
            "Busqueda - objetivo ausente mayor que el maximo",
            "Tiempo mediano (ms)" if metrica == "tiempo_ms" else "Comparaciones", series)


def mostrar_resultados(busquedas, ordenamientos):
    print("\nBUSQUEDAS: objetivo ausente mayor que el maximo")
    print(f'{"n":>6} {"Algoritmo":<18} {"Comp.":>10} {"Tiempo ms":>12}')
    for r in busquedas:
        if r["caso"] == "No existe mayor":
            print(f'{r["n"]:>6} {r["algoritmo"]:<18} {r["comparaciones"]:>10} {r["tiempo_ms"]:>12.6f}')
    print("\nORDENAMIENTOS: todas las pruebas (escrituras en lista principal)")
    print(f'{"n":>6} {"Tipo":<13} {"Algoritmo":<12} {"Comp.":>12} {"Mov.":>12} {"Tiempo ms":>12}')
    for r in ordenamientos:
        print(f'{r["n"]:>6} {r["tipo"]:<13} {r["algoritmo"]:<12} {r["comparaciones"]:>12} {r["movimientos"]:>12} {r["tiempo_ms"]:>12.6f}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--salida", default="resultados_parte4")
    parser.add_argument("--repeticiones", type=int, default=3)
    parser.add_argument("--lote", type=int, default=100)
    parser.add_argument("--rapido", action="store_true",
                        help="Ejecuta las pruebas con 100 elementos")
    parser.add_argument("--sin-archivos", action="store_true")
    args = parser.parse_args()
    if args.repeticiones < 1 or args.lote < 1:
        parser.error("repeticiones y lote deben ser positivos")
    tamanos = (100,) if args.rapido else TAMANOS
    print("PARTE 4 - Experimentos reales con verificacion", flush=True)
    print("Tamanos:", tamanos, "| repeticiones:", args.repeticiones, flush=True)
    print("Los metodos cuadraticos con 10000 elementos pueden tardar.", flush=True)
    busquedas, crudas_b = experimentar_busquedas(tamanos, args.repeticiones, args.lote)
    ordenamientos, crudas_o = experimentar_ordenamientos(tamanos, args.repeticiones)
    mostrar_resultados(busquedas, ordenamientos)
    if not args.sin_archivos:
        try:
            carpeta = Path(args.salida)
            carpeta.mkdir(parents=True, exist_ok=True)
            guardar_csv(carpeta / "busquedas.csv", busquedas)
            guardar_csv(carpeta / "ordenamientos.csv", ordenamientos)
            guardar_csv(carpeta / "mediciones_crudas.csv", crudas_b + crudas_o)
            metadata = dict(semilla=SEMILLA, tamanos=tamanos,
                repeticiones=args.repeticiones, lote_busquedas=args.lote,
                python=sys.version, plataforma=platform.platform(),
                procesador=platform.processor(),
                reloj="perf_counter_ns", resolucion_reloj_s=get_clock_info("perf_counter").resolution,
                tiempo="Mediana de ms por llamada; algoritmo instrumentado",
                comparacion="Comparaciones entre valores; excluye indices y bucles",
                movimiento="Escrituras en lista principal; intercambio=2; auxiliar excluido",
                pruebas_busqueda=len(busquedas), pruebas_ordenamiento=len(ordenamientos),
                todas_correctas=True)
            (carpeta / "metodologia.json").write_text(
                json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")
            guardar_graficos(carpeta / "graficos", busquedas, ordenamientos)
            print("\nArchivos CSV y graficos SVG guardados en:", carpeta.resolve())
        except OSError as error:
            print("\nEl entorno no permite guardar archivos:", error)
            print("Los resultados siguen disponibles en la consola.")
    print("\nTodas las pruebas fueron correctas.")


if __name__ == "__main__":
    main()
