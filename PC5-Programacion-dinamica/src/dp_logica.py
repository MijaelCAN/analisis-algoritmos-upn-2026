# -*- coding: utf-8 -*-
"""
PC5 - Programación Dinámica (UPN 2026-2) - Caso SmartOptimizer S.A.C.
Lógica de los tres módulos, separada de la interfaz para poder probarla.

Las tres soluciones son "bottom-up" (tabulación): se resuelve primero el
subproblema más pequeño, se guarda en una tabla y se reutiliza para construir
los siguientes, así cada subproblema se calcula una sola vez.
"""


# ---------------------------------------------------------------------------
# Casuística 01 - Optimización de rutas de desplazamiento
# ---------------------------------------------------------------------------
def ruta_costo_minimo(inicio, destino, costos):
    """Costo mínimo para ir de `inicio` a `destino`.

    costos: dict {pasos: costo}, p. ej. {1: 10, 2: 18, 3: 25}
    Recurrencia: dp[i] = min(dp[i - p] + costo[p])  para cada paso p con i - p >= inicio
    Caso base:   dp[inicio] = 0
    Complejidad: O(n * k) en tiempo y O(n) en espacio (n = posiciones, k = tipos de paso).
    Devuelve (costo_minimo, tabla_dp, decision, camino).
    """
    if destino < inicio:
        raise ValueError("El destino debe ser mayor o igual que la posición inicial.")
    n = destino - inicio
    INF = float("inf")
    dp = [INF] * (n + 1)          # dp[j] = costo mínimo para llegar a la posición inicio + j
    decision = [None] * (n + 1)   # paso usado para llegar a j (para reconstruir el camino)
    dp[0] = 0
    for j in range(1, n + 1):
        for pasos, costo in sorted(costos.items()):
            if j - pasos >= 0 and dp[j - pasos] + costo < dp[j]:
                dp[j] = dp[j - pasos] + costo
                decision[j] = pasos

    # Reconstrucción del camino desde el destino hacia atrás
    camino, j = [], n
    while j > 0:
        p = decision[j]
        camino.append((inicio + j - p, inicio + j, p, costos[p]))
        j -= p
    camino.reverse()
    return dp[n], dp, decision, camino


# ---------------------------------------------------------------------------
# Casuística 02 - Optimización del ingreso de técnicos
# ---------------------------------------------------------------------------
def formas_de_llegar(niveles, saltos=(1, 2, 3)):
    """Número de formas distintas de llegar al nivel `niveles` avanzando con `saltos`.

    Recurrencia: f(n) = f(n-1) + f(n-2) + f(n-3)   (con saltos 1, 2 y 3)
    Caso base:   f(0) = 1 (una forma de "no moverse"); f(n) = 0 si n < 0
    Complejidad: O(n * k) en tiempo y O(n) en espacio.
    Devuelve (total, tabla_f, detalle) donde detalle[i] es el texto del cálculo de f(i).
    """
    if niveles < 0:
        raise ValueError("La cantidad de niveles no puede ser negativa.")
    f = [0] * (niveles + 1)
    f[0] = 1
    detalle = ["f(0) = 1  (caso base)"]
    for i in range(1, niveles + 1):
        partes, nombres = [], []
        for s in saltos:
            if i - s >= 0:
                f[i] += f[i - s]
                partes.append(str(f[i - s]))
                nombres.append(f"f({i - s})")
        detalle.append(f"f({i}) = {' + '.join(nombres)} = {' + '.join(partes)} = {f[i]}")
    return f[niveles], f, detalle


def relacion_recurrencia(saltos=(1, 2, 3)):
    terminos = " + ".join(f"f(n-{s})" for s in saltos)
    return f"f(n) = {terminos},  con f(0) = 1 y f(n) = 0 si n < 0"


# ---------------------------------------------------------------------------
# Casuística 03 - Selección óptima de proyectos (sin consecutivos)
# ---------------------------------------------------------------------------
def seleccion_proyectos(beneficios):
    """Máximo beneficio sin elegir dos proyectos consecutivos.

    Recurrencia: dp[i] = max(dp[i-1],  dp[i-2] + b[i])
                 (no tomar el proyecto i  |  tomarlo y saltar el anterior)
    Caso base:   dp[0] = 0, dp[1] = b[1]
    Complejidad: O(n) en tiempo y O(n) en espacio.
    Devuelve (maximo, dp, seleccionados, descartados, filas) con índices 1..n.
    """
    n = len(beneficios)
    b = [0] + list(beneficios)            # b[1..n]
    dp = [0] * (n + 1)
    if n >= 1:
        dp[1] = b[1]
    filas = []                             # para mostrar la tabla DP paso a paso
    if n >= 1:
        filas.append((1, b[1], 0, b[1], dp[1], "Tomar"))
    for i in range(2, n + 1):
        sin_i = dp[i - 1]
        con_i = dp[i - 2] + b[i]
        dp[i] = max(sin_i, con_i)
        filas.append((i, b[i], sin_i, con_i, dp[i], "Tomar" if con_i > sin_i else "Saltar"))

    # Reconstrucción: si dp[i] viene de tomar i, se elige i y se salta a i-2
    seleccionados, i = [], n
    while i >= 1:
        if i == 1 or dp[i - 2] + b[i] > dp[i - 1]:
            if i == 1 and dp[1] == 0:
                break
            seleccionados.append(i)
            i -= 2
        else:
            i -= 1
    seleccionados.reverse()
    descartados = [i for i in range(1, n + 1) if i not in seleccionados]
    return dp[n], dp, seleccionados, descartados, filas


if __name__ == "__main__":
    c, dp, _, camino = ruta_costo_minimo(0, 10, {1: 10, 2: 18, 3: 25})
    print("Casuística 01 - costo mínimo:", c, "| dp:", dp)
    print("  camino:", " -> ".join(f"{a}->{b} (+{p}, S/{k})" for a, b, p, k in camino))
    t, f, _ = formas_de_llegar(8)
    print("Casuística 02 - formas:", t, "| f:", f)
    m, dp, sel, des, _ = seleccion_proyectos([4000, 2500, 5000, 3500, 6000, 4500, 7000, 3000])
    print("Casuística 03 - beneficio:", m, "| elegidos:", [f"P{i}" for i in sel],
          "| descartados:", [f"P{i}" for i in des])
