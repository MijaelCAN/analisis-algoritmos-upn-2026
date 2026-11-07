
"PARTE 1. ANÁLISIS MATEMÁTICO DE LA COMPLEJIDAD ALGORÍTMICA: 10 CASOS"



# ----------------------------------------------------------------------
# CASO 1 - Estructura secuencial: O(1)
# ----------------------------------------------------------------------

def area_y_perimetro(base, altura):
    area = base * altura               # 1 multiplicación
    perimetro = 2 * (base + altura)    # 1 suma y 1 multiplicación
    return area, perimetro             # 1 retorno
 
 
# ----------------------------------------------------------------------
# CASO 2 - Estructura condicional: O(1)
# ----------------------------------------------------------------------

def clasificar(nota):
    if nota >= 18:                     # comparación 1
        return "Excelente"
    elif nota >= 11:                   # comparación 2
        return "Aprobado"
    else:
        return "Desaprobado"
 
 
# ----------------------------------------------------------------------
# CASO 3 - Bucle simple: O(n)
# ----------------------------------------------------------------------

def suma_hasta(n):
    suma = 0                           # 1 asignación
    for i in range(1, n + 1):          # el bucle se repite n veces
        suma += i                      # operación dominante: n veces
    return suma
 
 
# ----------------------------------------------------------------------
# CASO 4 - Bucles anidados: O(n²)
# ----------------------------------------------------------------------

def contar_pares(n):
    contador = 0
    for i in range(n):                 # n veces
        for j in range(n):             # n veces por cada i
            contador += 1              # operación dominante
    return contador
 
 
# ----------------------------------------------------------------------
# CASO 5 - Bucle dependiente (triangular): O(n²)
# ----------------------------------------------------------------------

def contar_triangulo(n):
    contador = 0
    for i in range(n):                 # i = 0, 1, ..., n-1
        for j in range(i + 1):         # el bucle interno depende de i
            contador += 1              # operación dominante
    return contador
 
 
# ----------------------------------------------------------------------
# CASO 6 - Bucle con duplicación: O(log n)
# ----------------------------------------------------------------------

def potencias_de_dos(n):
    i = 1
    veces = 0
    while i < n:                       # i toma los valores 1, 2, 4, 8, ...
        veces += 1                     # operación dominante
        i *= 2                         # i se duplica en cada vuelta
    return veces
 
 
# ----------------------------------------------------------------------
# CASO 7 - Bucle lineal con logarítmico: O(n log n)
# ----------------------------------------------------------------------

def n_log_n(n):
    veces = 0
    for i in range(n):                 # n veces
        j = 1
        while j < n:                   # ⌈log2 n⌉ veces por cada i
            veces += 1                 # operación dominante
            j *= 2
    return veces
 
 
# ----------------------------------------------------------------------
# CASO 8 - Función con bucle de raíz: O(√n)
# ----------------------------------------------------------------------

def es_primo(n):
    if n < 2:                          # condicional inicial: costo constante
        return False
    d = 2
    while d * d <= n:                  # se repite hasta √n veces
        if n % d == 0:                 # operación dominante: módulo
            return False               # salida anticipada
        d += 1
    return True
 
 
# ----------------------------------------------------------------------
# CASO 9 - Recursión lineal: O(n)
# ----------------------------------------------------------------------

def suma_recursiva(n):
    if n == 0:                         # caso base: costo constante
        return 0
    return n + suma_recursiva(n - 1)   # una llamada recursiva con n-1
 
 
# ----------------------------------------------------------------------
# CASO 10 - Recursión doble (Fibonacci): O(2ⁿ)
# ----------------------------------------------------------------------

def fib(n):
    if n < 2:                          # casos base: fib(0)=0, fib(1)=1
        return n
    return fib(n - 1) + fib(n - 2)     # dos llamadas recursivas
 
 
# ----------------------------------------------------------------------
# EJECUCIÓN DE LOS 10 CASOS
# ----------------------------------------------------------------------


if __name__ == "__main__":
    print("Caso 1  area_y_perimetro(5, 3):", area_y_perimetro(5, 3))
    print("Caso 2  clasificar(19, 14, 8):", clasificar(19), clasificar(14), clasificar(8))
    print("Caso 3  suma_hasta(10), (100):", suma_hasta(10), suma_hasta(100))
    print("Caso 4  contar_pares(10), (100):", contar_pares(10), contar_pares(100))
    print("Caso 5  contar_triangulo(10), (100):", contar_triangulo(10), contar_triangulo(100))
    print("Caso 6  potencias_de_dos(10), (100):", potencias_de_dos(10), potencias_de_dos(100))
    print("Caso 7  n_log_n(10), (100):", n_log_n(10), n_log_n(100))
    print("Caso 8  es_primo(101), (100):", es_primo(101), es_primo(100))
    print("Caso 9  suma_recursiva(10), (100):", suma_recursiva(10), suma_recursiva(100))
    print("Caso 10 fib(10), (20):", fib(10), fib(20))
 