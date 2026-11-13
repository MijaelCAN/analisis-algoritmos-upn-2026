
# Actividad 6 - Problema de las 8 Reinas (asignación de 8 almacenes de UPN Cargo S.A.C.)
N = 8

def es_valido(tablero, fila, col):
    for i in range(fila):
        if tablero[i] == col or \
           tablero[i] - i == col - fila or \
           tablero[i] + i == col + fila:
            return False
    return True

def resolver(tablero, fila, soluciones):
    if fila == N:
        soluciones.append(list(tablero))
        return
    
    for col in range(N):
        if es_valido(tablero, fila, col):
            tablero[fila] = col  # Asignación tentativa
            resolver(tablero, fila + 1, soluciones)
            tablero[fila] = -1   # Retroceso (Backtracking)

if __name__ == "__main__":
    tablero = [-1] * N
    soluciones = []
    resolver(tablero, 0, soluciones)
    print(f"Total de configuraciones válidas de almacenes encontradas: {len(soluciones)}")
    if soluciones:
        print("Primera configuración válida (Almacenes por franja horaria):", soluciones[0])
