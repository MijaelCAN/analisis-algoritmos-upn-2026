# -*- coding: utf-8 -*-
"""
T1 - Análisis de Algoritmos y Estrategias de Programación (UPN 2026-2)
Caso: UPN Cargo S.A.C.
Actividad 4: Algoritmos voraces - Entrega de viáticos con la menor cantidad de billetes
Responsable: Mijael Deyvi Cano Rojas (Grupo 7)

Estrategia voraz: se recorren los billetes de mayor a menor valor y, en cada paso,
se toma la mayor cantidad posible del billete actual (la mejor decisión local).
Nunca se revisa una decisión ya tomada.
"""

# Denominaciones disponibles, ordenadas de mayor a menor (requisito de la estrategia voraz)
BILLETES = [200, 100, 50, 20, 10]

# Montos solicitados por la Gerencia de Operaciones
MONTOS = [380, 670, 920]


def entregar_viaticos(monto, billetes=BILLETES):
    """Devuelve un diccionario {billete: cantidad} con la menor cantidad de billetes.

    Complejidad: O(k), donde k es el número de denominaciones (aquí k = 5).
    Si las denominaciones no vienen ordenadas, ordenarlas cuesta O(k log k).
    """
    if monto < 0 or monto % min(billetes) != 0:
        raise ValueError(f"S/ {monto} no se puede entregar con billetes de {billetes}")

    restante = monto
    entrega = {}
    for billete in sorted(billetes, reverse=True):   # 1) candidato: el billete de mayor valor
        cantidad = restante // billete                # 2) selección voraz: todos los que entren
        entrega[billete] = cantidad
        restante -= cantidad * billete                # 3) se reduce el problema
        if restante == 0:                             # 4) solución completa
            break
    # Los billetes no usados quedan en 0 para mostrar la tabla completa
    for billete in billetes:
        entrega.setdefault(billete, 0)
    return entrega


def minimo_optimo(monto, billetes):
    """Mínimo real de billetes por programación dinámica (solo para validar el voraz).

    Complejidad: O(monto * k).
    """
    INF = float("inf")
    dp = [0] + [INF] * monto
    for m in range(1, monto + 1):
        for b in billetes:
            if b <= m and dp[m - b] + 1 < dp[m]:
                dp[m] = dp[m - b] + 1
    return dp[monto]


def mostrar_tabla():
    print("=" * 66)
    print(" UPN CARGO S.A.C. - Entrega de viáticos (algoritmo voraz)")
    print("=" * 66)
    encabezado = f"{'Monto':>8} |" + "".join(f"{'S/'+str(b):>7}" for b in BILLETES) + " | Total"
    print(encabezado)
    print("-" * len(encabezado))
    for monto in MONTOS:
        entrega = entregar_viaticos(monto)
        total = sum(entrega.values())
        fila = f"{'S/ '+str(monto):>8} |" + "".join(f"{entrega[b]:>7}" for b in BILLETES)
        print(f"{fila} | {total:>5}")
    print()
    for monto in MONTOS:
        entrega = entregar_viaticos(monto)
        detalle = " + ".join(f"{c} x S/{b}" for b, c in entrega.items() if c)
        optimo = minimo_optimo(monto, BILLETES)
        print(f"S/ {monto}: {detalle}  -> {sum(entrega.values())} billetes "
              f"(óptimo por PD: {optimo})")


def contraejemplo():
    """Muestra un caso donde la estrategia voraz NO es óptima (pregunta b)."""
    billetes = [4, 3, 1]
    monto = 6
    entrega = entregar_viaticos(monto, billetes)
    voraz = sum(entrega.values())
    detalle = " + ".join(f"{c} x {b}" for b, c in entrega.items() if c)
    print()
    print("Contraejemplo con billetes [4, 3, 1] y monto 6:")
    print(f"  Voraz : {detalle} -> {voraz} billetes")
    print(f"  Óptimo: 2 x 3 -> {minimo_optimo(monto, billetes)} billetes")


if __name__ == "__main__":
    mostrar_tabla()
    contraejemplo()
