"""
===========================================================================
 Práctica de campo - Semana 4
 Análisis de Algoritmos y Estrategias de Programación (UPN)
 Tema: Backtracking con interfaz gráfica (tkinter)
===========================================================================

 Problemas resueltos:
   1. Sudoku 6x6 / 9x9 con visualización paso a paso
   2. N-Reinas con visualización del árbol de decisiones
   3. Laberinto (Rat in a Maze): búsqueda de TODOS los caminos
   4. Coloreado de grafos con selección interactiva de colores

 Cómo ejecutar:
   python backtracking.py        -> abre el menú principal
   python backtracking.py 1      -> abre directamente el problema 1 (igual 2, 3, 4)

 Idea general de la animación
 ----------------------------
 Cada algoritmo de backtracking está escrito como un GENERADOR de Python.
 En cada decisión importante (probar un valor, retroceder, encontrar una
 solución) el algoritmo hace `yield` de un "evento", por ejemplo:

        ("probar", fila, columna, valor)
        ("retroceder", fila, columna)

 La interfaz consume esos eventos de a uno con `ventana.after(ms, ...)`
 (clase Animador). Así:
   - la ventana nunca se congela (no se usa time.sleep),
   - se puede pausar, continuar, detener o terminar sin animación,
   - se puede cambiar la velocidad en plena ejecución,
   - y se puede cerrar la ventana sin que el programa se caiga.

 La lógica del algoritmo queda separada de la parte gráfica: las funciones
 `*_pasos` no saben nada de tkinter.
===========================================================================
"""

import random
import sys
import time
import tkinter as tk
from collections import deque
from tkinter import colorchooser, messagebox


# ===========================================================================
# UTILIDAD COMÚN: ANIMADOR PASO A PASO
# ===========================================================================
class Animador:
    """
    Ejecuta, paso a paso, un generador de eventos de backtracking.

    Recibe tres funciones de la ventana que lo usa:
      - procesar(evento): actualiza el modelo y los contadores con un evento.
      - redibujar():      pinta en pantalla el estado actual.
      - al_terminar(resultado, detenido): se llama una sola vez al final.
        `resultado` es lo que retorna el generador (return ...).
    """

    # Con velocidad máxima (0 ms) se procesan muchos eventos por cuadro
    PASOS_POR_CUADRO_RAPIDO = 400

    def __init__(self, ventana, procesar, redibujar, al_terminar, retardo=60):
        self.ventana = ventana
        self.procesar = procesar
        self.redibujar = redibujar
        self.al_terminar = al_terminar
        self.retardo = tk.IntVar(master=ventana, value=retardo)  # ms entre pasos
        self.gen = None          # generador en ejecución (None = inactivo)
        self.job = None          # id del after() programado
        self.pausado = False
        self.tiempo = 0.0        # segundos transcurridos (sin contar pausas)
        self._t0 = 0.0
        self._t_pausa = 0.0
        self.botones = []        # botones que solo sirven mientras se ejecuta
        self.b_pausa = None

    @property
    def activo(self):
        return self.gen is not None

    # ---------------------------------------------------------------- control
    def iniciar(self, generador):
        self._cancelar()
        self.gen = generador
        self.pausado = False
        self.tiempo = 0.0
        self._t0 = time.perf_counter()
        self._actualizar_botones()
        self._programar()

    def pausar_continuar(self):
        if self.gen is None:
            return
        self.pausado = not self.pausado
        if self.pausado:
            self._t_pausa = time.perf_counter()
            self._cancelar()
        else:
            self._t0 += time.perf_counter() - self._t_pausa  # no contar la pausa
            self._programar()
        self._actualizar_botones()

    def terminar_ya(self):
        """Procesa todos los eventos que faltan, sin animar."""
        if self.gen is None:
            return
        self._quitar_pausa()
        self._cancelar()
        try:
            while True:
                self.procesar(next(self.gen))
        except StopIteration as fin:
            self._finalizar(fin.value, detenido=False)

    def detener(self):
        """Corta la búsqueda en el punto en que está."""
        if self.gen is None:
            return
        self._quitar_pausa()
        self.gen.close()
        self._finalizar(None, detenido=True)

    # ---------------------------------------------------------------- interno
    def _quitar_pausa(self):
        if self.pausado:
            self._t0 += time.perf_counter() - self._t_pausa
            self.pausado = False

    def _programar(self):
        try:
            espera = max(1, int(self.retardo.get()))
            self.job = self.ventana.after(espera, self._tick)
        except tk.TclError:          # la ventana ya fue cerrada
            self.gen = None

    def _cancelar(self):
        if self.job is not None:
            try:
                self.ventana.after_cancel(self.job)
            except tk.TclError:
                pass
            self.job = None

    def _tick(self):
        """Un 'cuadro' de animación: procesa 1 evento (o muchos si va a 0 ms)."""
        self.job = None
        if self.gen is None or self.pausado:
            return
        try:
            pasos = 1 if self.retardo.get() > 0 else self.PASOS_POR_CUADRO_RAPIDO
            try:
                for _ in range(pasos):
                    self.procesar(next(self.gen))
            except StopIteration as fin:
                self._finalizar(fin.value, detenido=False)
                return
            self.tiempo = time.perf_counter() - self._t0
            self.redibujar()
            self._programar()
        except tk.TclError:          # la ventana se cerró en plena animación
            self.gen = None

    def _finalizar(self, resultado, detenido):
        self.tiempo = time.perf_counter() - self._t0
        self.gen = None
        self._cancelar()
        self._actualizar_botones()
        self.redibujar()
        self.al_terminar(resultado, detenido)

    def _actualizar_botones(self):
        try:
            estado = "normal" if self.gen is not None else "disabled"
            for b in self.botones:
                b.config(state=estado)
            if self.b_pausa is not None:
                self.b_pausa.config(text="▶ Continuar" if self.pausado else "⏸ Pausar")
        except tk.TclError:
            pass


def barra_animacion(padre, anim):
    """Controles comunes a los 4 problemas: pausar, terminar, detener, velocidad."""
    fr = tk.Frame(padre)
    anim.b_pausa = tk.Button(fr, text="⏸ Pausar", width=11, command=anim.pausar_continuar)
    b_terminar = tk.Button(fr, text="⏭ Terminar sin animación", command=anim.terminar_ya)
    b_detener = tk.Button(fr, text="⏹ Detener", width=9, command=anim.detener)
    anim.b_pausa.pack(side="left", padx=3)
    b_terminar.pack(side="left", padx=3)
    b_detener.pack(side="left", padx=3)
    tk.Scale(fr, from_=0, to=500, orient="horizontal", variable=anim.retardo,
             label="Pausa entre pasos (ms)", length=170).pack(side="left", padx=8)
    anim.botones = [anim.b_pausa, b_terminar, b_detener]
    anim._actualizar_botones()
    return fr


def leyenda(padre, items):
    """Dibuja una leyenda de colores: items = [(color, texto), ...]."""
    fr = tk.Frame(padre)
    for color, texto in items:
        tk.Label(fr, bg=color, width=2, relief="solid", bd=1).pack(side="left", padx=(8, 2))
        tk.Label(fr, text=texto).pack(side="left")
    return fr


def ejecutar_completo(generador):
    """Corre un generador hasta el final (sin animar) y devuelve (resultado, eventos)."""
    eventos = 0
    try:
        while True:
            next(generador)
            eventos += 1
    except StopIteration as fin:
        return fin.value, eventos


# ===========================================================================
# PROBLEMA 1: SUDOKU 6x6 / 9x9
# ===========================================================================
# Cada tablero: (filas por bloque, columnas por bloque, matriz). 0 = vacía.
# El tamaño del tablero es n = filas_bloque * columnas_bloque.
SUDOKUS = {
    "9x9 - Clásico (30 pistas)": (3, 3, [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]),
    "9x9 - Variante (29 pistas)": (3, 3, [
        [5, 0, 0, 0, 0, 8, 0, 0, 0],
        [0, 7, 2, 1, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 2, 5, 0, 0],
        [0, 5, 0, 0, 0, 0, 4, 0, 0],
        [0, 0, 6, 8, 0, 3, 0, 0, 0],
        [0, 0, 3, 0, 0, 4, 0, 0, 6],
        [0, 0, 0, 5, 3, 7, 2, 8, 0],
        [0, 0, 7, 0, 0, 0, 0, 0, 5],
        [0, 4, 0, 2, 8, 6, 0, 7, 9],
    ]),
    "6x6": (2, 3, [
        [1, 0, 3, 0, 5, 0],
        [0, 5, 0, 1, 0, 3],
        [2, 0, 0, 5, 0, 4],
        [0, 6, 4, 0, 0, 1],
        [3, 0, 2, 0, 4, 0],
        [0, 4, 0, 3, 0, 2],
    ]),
}


def sudoku_es_valido(tab, br, bc, f, c, v):
    """¿Se puede poner v en (f, c) sin repetir en la fila, columna ni bloque?"""
    n = br * bc
    for i in range(n):
        if tab[f][i] == v or tab[i][c] == v:
            return False
    f0, c0 = br * (f // br), bc * (c // bc)   # esquina superior del bloque
    for i in range(f0, f0 + br):
        for j in range(c0, c0 + bc):
            if tab[i][j] == v:
                return False
    return True


def sudoku_pasos(tab, br, bc):
    """
    Backtracking del Sudoku como generador. Modifica `tab` en el lugar.

    1. Busca la primera celda vacía. Si no hay, el tablero está resuelto.
    2. Prueba los valores 1..n que no rompan las reglas.
    3. Por cada valor válido avanza recursivamente a la siguiente celda.
    4. Si ninguna opción lleva a una solución, borra la celda (RETROCEDE)
       y devuelve False para que la llamada anterior pruebe otro valor.

    Eventos: ("probar", f, c, v) y ("retroceder", f, c).
    Retorna True si encontró solución, False si no existe.
    """
    n = br * bc
    vacia = next(((f, c) for f in range(n) for c in range(n) if tab[f][c] == 0), None)
    if vacia is None:
        return True                                   # caso base: tablero lleno
    f, c = vacia
    for v in range(1, n + 1):
        if sudoku_es_valido(tab, br, bc, f, c, v):
            tab[f][c] = v                             # decisión
            yield ("probar", f, c, v)
            if (yield from sudoku_pasos(tab, br, bc)):
                return True                           # éxito: se propaga hacia arriba
            tab[f][c] = 0                             # deshacer la decisión
            yield ("retroceder", f, c)
    return False                                      # ningún valor sirve -> retroceso


class SudokuApp:
    """Ventana del problema 1."""

    COLOR_FIJA = "#d0d0d0"
    COLOR_VACIA = "white"
    COLOR_PRUEBA = "#b9f0b9"
    COLOR_RETROCESO = "#f7a8a0"
    COLOR_RESUELTA = "#cfe3ff"

    def __init__(self, root):
        self.root = root
        root.title("Problema 1 - Sudoku con backtracking")
        self.anim = Animador(root, self._procesar, self._redibujar, self._al_terminar, retardo=10)

        self.br = self.bc = self.n = 0
        self.entradas = []        # matriz de widgets Entry
        self.tablero = []         # modelo que modifica el algoritmo
        self.inicial = None       # tablero tal como estaba al presionar Resolver
        self.fijas = set()        # celdas dadas por el enunciado
        self.color = {}           # color actual de cada celda
        self.sucias = set()       # celdas que hay que repintar
        self.probados = self.retrocesos = 0
        self.t_algoritmo = 0.0

        # ---- fila superior: elegir tablero
        top = tk.Frame(root)
        top.pack(pady=6)
        tk.Label(top, text="Tablero:").pack(side="left")
        self.var_tablero = tk.StringVar(value="9x9 - Clásico (30 pistas)")
        tk.OptionMenu(top, self.var_tablero, *SUDOKUS, command=self._cargar).pack(side="left", padx=4)
        tk.Button(top, text="Vaciar (ingresar uno propio)", command=self._vaciar).pack(side="left", padx=4)

        # ---- grilla
        self.marco = tk.Frame(root, bg="black", bd=2)
        self.marco.pack(padx=12, pady=4)

        leyenda(root, [(self.COLOR_FIJA, "Fija"), (self.COLOR_PRUEBA, "Probando"),
                       (self.COLOR_RETROCESO, "Retroceso"), (self.COLOR_RESUELTA, "Solución")]).pack(pady=4)

        # ---- botones
        fb = tk.Frame(root)
        fb.pack(pady=4)
        self.b_resolver = tk.Button(fb, text="▶ Resolver", bg="#2e7d32", fg="white", width=12,
                                    command=self.resolver)
        self.b_resolver.pack(side="left", padx=3)
        tk.Button(fb, text="↺ Reiniciar", width=10, command=self.reiniciar).pack(side="left", padx=3)
        barra_animacion(root, self.anim).pack(pady=4)

        self.lbl_stats = tk.Label(root, font=("Arial", 11), justify="left")
        self.lbl_stats.pack(pady=(6, 0))
        self.lbl_msg = tk.Label(root, font=("Arial", 12, "bold"))
        self.lbl_msg.pack(pady=(2, 10))

        self._cargar("9x9 - Clásico (30 pistas)")

    # ------------------------------------------------------------ construir
    def _cargar(self, nombre):
        if self.anim.activo:
            self.anim.detener()
        br, bc, datos = SUDOKUS[nombre]
        self._construir(br, bc, datos)
        self.lbl_msg.config(text="Celdas grises = fijas. Presiona Resolver.", fg="black")

    def _vaciar(self):
        if self.anim.activo:
            self.anim.detener()
        self._construir(self.br, self.bc, [[0] * self.n for _ in range(self.n)])
        self.lbl_msg.config(text="Escribe los números del tablero y presiona Resolver.", fg="black")

    def _construir(self, br, bc, datos):
        """Crea la grilla de Entry; los bloques se separan con un borde más grueso."""
        for w in self.marco.winfo_children():
            w.destroy()
        self.br, self.bc, self.n = br, bc, br * bc
        self.inicial = None
        self._reset_contadores()
        n = self.n
        valida = (self.root.register(self._validar_tecla), "%P")
        fuente = ("Arial", 18 if n == 9 else 22, "bold")
        self.entradas = []
        for f in range(n):
            fila = []
            for c in range(n):
                e = tk.Entry(self.marco, width=2, font=fuente, justify="center", relief="flat",
                             validate="key", validatecommand=valida)
                padx = (3 if c % bc == 0 and c else 1, 0)
                pady = (3 if f % br == 0 and f else 1, 0)
                e.grid(row=f, column=c, padx=padx, pady=pady, ipady=2)
                if datos[f][c]:
                    e.insert(0, str(datos[f][c]))
                e.config(bg=self.COLOR_FIJA if datos[f][c] else self.COLOR_VACIA)
                e.bind("<KeyRelease>", lambda ev, ff=f, cc=c: self._al_escribir(ff, cc))
                fila.append(e)
            self.entradas.append(fila)

    def _validar_tecla(self, texto):
        """Solo deja escribir un dígito entre 1 y n (o dejar la celda vacía)."""
        return texto == "" or (len(texto) == 1 and texto.isdigit() and 1 <= int(texto) <= self.n)

    def _al_escribir(self, f, c):
        e = self.entradas[f][c]
        if str(e.cget("state")) == "normal":
            e.config(bg=self.COLOR_FIJA if e.get() else self.COLOR_VACIA)

    def _reset_contadores(self):
        self.probados = self.retrocesos = 0
        self.t_algoritmo = 0.0
        self.anim.tiempo = 0.0
        self._mostrar_stats()

    # ------------------------------------------------------------ resolver
    def _leer_tablero(self):
        return [[int(self.entradas[f][c].get() or 0) for c in range(self.n)] for f in range(self.n)]

    def _validar_inicial(self, tab):
        """Revisa que el tablero inicial no tenga números repetidos."""
        for f in range(self.n):
            for c in range(self.n):
                v = tab[f][c]
                if v:
                    tab[f][c] = 0
                    ok = sudoku_es_valido(tab, self.br, self.bc, f, c, v)
                    tab[f][c] = v
                    if not ok:
                        return f"El {v} de la fila {f + 1}, columna {c + 1} se repite en su fila, columna o bloque."
        return None

    def resolver(self):
        if self.anim.activo:
            return
        tab = self._leer_tablero()
        error = self._validar_inicial(tab)
        if error:
            messagebox.showerror("Tablero inválido", error, parent=self.root)
            return
        self.inicial = [fila[:] for fila in tab]
        self.tablero = tab
        self.fijas = {(f, c) for f in range(self.n) for c in range(self.n) if tab[f][c]}
        self._reset_contadores()

        # Tiempo del algoritmo "puro": se resuelve una copia sin dibujar nada.
        copia = [fila[:] for fila in tab]
        t0 = time.perf_counter()
        ejecutar_completo(sudoku_pasos(copia, self.br, self.bc))
        self.t_algoritmo = time.perf_counter() - t0

        # Bloquear la edición y pintar el estado inicial
        self.color = {}
        for f in range(self.n):
            for c in range(self.n):
                self.color[(f, c)] = self.COLOR_FIJA if (f, c) in self.fijas else self.COLOR_VACIA
        self.sucias = set(self.color)
        self._redibujar()
        self.b_resolver.config(state="disabled")
        self.lbl_msg.config(text="Resolviendo...", fg="#1f4fd1")
        self.anim.iniciar(sudoku_pasos(self.tablero, self.br, self.bc))

    def _procesar(self, ev):
        if ev[0] == "probar":
            _, f, c, _v = ev
            self.probados += 1
            self.color[(f, c)] = self.COLOR_PRUEBA
        else:  # retroceder
            _, f, c = ev
            self.retrocesos += 1
            self.color[(f, c)] = self.COLOR_RETROCESO
        self.sucias.add((f, c))

    def _redibujar(self):
        for (f, c) in self.sucias:
            e = self.entradas[f][c]
            v = self.tablero[f][c]
            e.config(state="normal", validate="none")
            e.delete(0, tk.END)
            if v:
                e.insert(0, str(v))
            e.config(state="readonly", readonlybackground=self.color[(f, c)])
        self.sucias.clear()
        self._mostrar_stats()

    def _mostrar_stats(self):
        self.lbl_stats.config(text=(
            f"Valores probados: {self.probados}     Retrocesos (backtracks): {self.retrocesos}\n"
            f"Tiempo de ejecución con animación: {self.anim.tiempo:.2f} s     "
            f"Tiempo del algoritmo sin animación: {self.t_algoritmo * 1000:.1f} ms"))

    def _al_terminar(self, resuelto, detenido):
        self.b_resolver.config(state="normal")
        if detenido:
            self.lbl_msg.config(text="Búsqueda detenida. Usa Reiniciar para volver al inicio.", fg="#b26a00")
        elif resuelto:
            for celda in self.color:
                if celda not in self.fijas:
                    self.color[celda] = self.COLOR_RESUELTA
            self.sucias = set(self.color)
            self._redibujar()
            self.lbl_msg.config(text="✔ Sudoku resuelto", fg="#2e7d32")
        else:
            self.lbl_msg.config(text="✘ Este tablero no tiene solución", fg="#c62828")
        self.b_resolver.config(state="disabled" if resuelto else "normal")

    def reiniciar(self):
        """Vuelve al tablero inicial (el que había al presionar Resolver)."""
        if self.anim.activo:
            self.anim.detener()
        datos = self.inicial or self._leer_tablero()
        self._construir(self.br, self.bc, datos)
        self.b_resolver.config(state="normal")
        self.lbl_msg.config(text="Tablero reiniciado.", fg="black")


# ===========================================================================
# PROBLEMA 2: N-REINAS CON ÁRBOL DE DECISIONES
# ===========================================================================
def n_reinas_arbol(n):
    """
    Encuentra TODAS las soluciones de las N-Reinas y guarda el árbol de decisiones.

    Cada nodo del árbol es un intento "poner la reina de la fila f en la columna c".
    Estados posibles de un nodo:
      - "valido":   la reina no es atacada -> se sigue a la fila siguiente
      - "podado":   la reina sería atacada -> se corta esa rama (poda)
      - "solucion": se colocó la última reina sin conflictos

    Retorna un diccionario con el árbol (listas paralelas) y las soluciones.
    """
    padre, fila, col, estado = [-1], [-1], [-1], ["raiz"]   # nodo 0 = raíz
    soluciones = []                                         # (tablero, id_hoja)
    tablero = [-1] * n            # tablero[f] = columna de la reina en la fila f

    def es_segura(f, c):
        # Basta revisar las filas anteriores: misma columna o misma diagonal.
        for i in range(f):
            if tablero[i] == c or abs(tablero[i] - c) == f - i:
                return False
        return True

    def backtrack(f, id_padre):
        for c in range(n):
            nid = len(padre)                 # nuevo nodo explorado
            padre.append(id_padre)
            fila.append(f)
            col.append(c)
            if not es_segura(f, c):
                estado.append("podado")      # PODA: no se explora esta rama
                continue
            tablero[f] = c                   # decisión
            if f == n - 1:
                estado.append("solucion")
                soluciones.append((tablero[:], nid))
            else:
                estado.append("valido")
                backtrack(f + 1, nid)        # avanzar a la siguiente fila
            tablero[f] = -1                  # deshacer (retroceso)

    backtrack(0, 0)
    return {
        "n": n, "padre": padre, "fila": fila, "col": col, "estado": estado,
        "soluciones": soluciones,
        "explorados": len(padre) - 1,
        "podados": estado.count("podado"),
    }


class NReinasApp:
    """Ventana del problema 2."""

    LIMITE_NODOS_ARBOL = 1500     # para que el dibujo del árbol sea legible
    TAM_TABLERO = 380
    COLORES_NODO = {"raiz": "#9e9e9e", "valido": "#a5d6a7", "podado": "#ef9a9a", "solucion": "#ffd54f"}

    def __init__(self, root):
        self.root = root
        root.title("Problema 2 - N-Reinas y árbol de decisiones")
        self.res = None
        self.idx = 0
        self.items_nodo = {}
        self.items_arista = {}
        self.x_nodo = {}
        self.resaltados = []

        # ---- controles
        top = tk.Frame(root)
        top.pack(pady=6)
        tk.Label(top, text="Valor de N (4-10):").pack(side="left")
        self.var_n = tk.StringVar(value="4")
        sp = tk.Spinbox(top, from_=4, to=10, textvariable=self.var_n, width=5)
        sp.pack(side="left", padx=4)
        sp.bind("<Return>", lambda e: self.calcular())
        tk.Button(top, text="Calcular", bg="#1565c0", fg="white", command=self.calcular).pack(side="left", padx=6)

        cuerpo = tk.Frame(root)
        cuerpo.pack(padx=10, pady=4)

        # ---- izquierda: tablero + navegación
        izq = tk.Frame(cuerpo)
        izq.pack(side="left", anchor="n")
        self.tablero = tk.Canvas(izq, width=self.TAM_TABLERO, height=self.TAM_TABLERO, bg="white",
                                 highlightthickness=0)
        self.tablero.pack()
        nav = tk.Frame(izq)
        nav.pack(pady=6)
        self.b_ant = tk.Button(nav, text="<< Anterior", command=lambda: self.mover(-1), state="disabled")
        self.b_ant.grid(row=0, column=0, padx=5)
        self.lbl_sol = tk.Label(nav, text="Solución: 0/0", width=16)
        self.lbl_sol.grid(row=0, column=1)
        self.b_sig = tk.Button(nav, text="Siguiente >>", command=lambda: self.mover(1), state="disabled")
        self.b_sig.grid(row=0, column=2, padx=5)
        self.lbl_vector = tk.Label(izq, fg="gray30")
        self.lbl_vector.pack()

        # ---- derecha: árbol de decisiones con scroll
        der = tk.LabelFrame(cuerpo, text="Árbol de decisiones (nivel = fila, número = columna)")
        der.pack(side="left", padx=10, anchor="n")
        cont = tk.Frame(der)
        cont.pack()
        self.arbol = tk.Canvas(cont, width=640, height=360, bg="white")
        sx = tk.Scrollbar(cont, orient="horizontal", command=self.arbol.xview)
        sy = tk.Scrollbar(cont, orient="vertical", command=self.arbol.yview)
        self.arbol.configure(xscrollcommand=sx.set, yscrollcommand=sy.set)
        self.arbol.grid(row=0, column=0)
        sy.grid(row=0, column=1, sticky="ns")
        sx.grid(row=1, column=0, sticky="ew")
        leyenda(der, [(self.COLORES_NODO["valido"], "Válido"), (self.COLORES_NODO["podado"], "Podado"),
                      (self.COLORES_NODO["solucion"], "Solución"), ("#1f4fd1", "Camino de la solución vista")]
                ).pack(pady=3)
        self.lbl_arbol = tk.Label(der, fg="gray30", wraplength=640, justify="left")
        self.lbl_arbol.pack(pady=(0, 4))

        # ---- estadísticas
        self.lbl_stats = tk.Label(root, font=("Arial", 12, "bold"), fg="#1f4fd1")
        self.lbl_stats.pack(pady=(4, 10))

        self.calcular()

    # ------------------------------------------------------------ cálculo
    def calcular(self):
        try:
            n = int(self.var_n.get())
        except ValueError:
            messagebox.showerror("Error", "N debe ser un número entero.", parent=self.root)
            return
        if not 4 <= n <= 10:
            messagebox.showerror("Error", "N debe estar entre 4 y 10.", parent=self.root)
            return
        t0 = time.perf_counter()
        self.res = n_reinas_arbol(n)          # el N calculado queda guardado en self.res
        t = time.perf_counter() - t0
        self.idx = 0
        r = self.res
        self.lbl_stats.config(text=(
            f"N = {n}   |   Soluciones: {len(r['soluciones'])}   |   Nodos explorados: {r['explorados']}   |   "
            f"Nodos podados: {r['podados']}   |   Tiempo: {t * 1000:.1f} ms"))
        self._dibujar_arbol()
        self._mostrar_solucion()

    def mover(self, paso):
        nuevo = self.idx + paso
        if self.res and 0 <= nuevo < len(self.res["soluciones"]):
            self.idx = nuevo
            self._mostrar_solucion()

    # ------------------------------------------------------------ tablero
    def _mostrar_solucion(self):
        cv = self.tablero
        cv.delete("all")
        n = self.res["n"]                 # se usa el N con el que se calculó
        sols = self.res["soluciones"]
        lado = self.TAM_TABLERO // n
        sol = sols[self.idx][0] if sols else None
        for f in range(n):
            for c in range(n):
                x1, y1 = c * lado, f * lado
                color = "#f0d9b5" if (f + c) % 2 == 0 else "#b58863"
                cv.create_rectangle(x1, y1, x1 + lado, y1 + lado, fill=color, outline="")
                if sol and sol[f] == c:
                    cv.create_text(x1 + lado // 2, y1 + lado // 2, text="♛", font=("Arial", int(lado * 0.55)))
        if sols:
            self.lbl_sol.config(text=f"Solución: {self.idx + 1}/{len(sols)}")
            self.lbl_vector.config(text="Columna por fila: " + str([c + 1 for c in sol]))
        else:
            self.lbl_sol.config(text="Sin soluciones")
            self.lbl_vector.config(text="")
        self.b_ant.config(state="normal" if self.idx > 0 else "disabled")
        self.b_sig.config(state="normal" if self.idx < len(sols) - 1 else "disabled")
        self._resaltar_camino()

    # ------------------------------------------------------------ árbol
    def _dibujar_arbol(self):
        """
        Dibuja el árbol con un layout simple: cada hoja ocupa una columna y
        cada nodo interno se ubica al centro de sus hijos. Si el árbol es muy
        grande se dibujan solo los primeros niveles (LIMITE_NODOS_ARBOL).
        """
        cv = self.arbol
        cv.delete("all")
        r = self.res
        n, padre, fila, col, estado = r["n"], r["padre"], r["fila"], r["col"], r["estado"]
        total = len(padre)

        # ¿Hasta qué profundidad se puede dibujar? (profundidad = fila + 1)
        por_nivel = [0] * (n + 1)
        for f in fila:
            por_nivel[f + 1] += 1
        prof_max, acumulado = 0, 0
        for d in range(n + 1):
            if acumulado + por_nivel[d] > self.LIMITE_NODOS_ARBOL:
                break
            acumulado += por_nivel[d]
            prof_max = d

        hijos = {}
        for i in range(1, total):
            if fila[i] + 1 <= prof_max:
                hijos.setdefault(padre[i], []).append(i)

        DX, DY, R, M = 22, 62, 9, 24
        x = {}
        siguiente_hoja = [0]

        def ubicar(i):
            h = hijos.get(i)
            if not h:
                x[i] = M + siguiente_hoja[0] * DX
                siguiente_hoja[0] += 1
            else:
                for j in h:
                    ubicar(j)
                x[i] = (x[h[0]] + x[h[-1]]) / 2

        ubicar(0)

        def y(i):
            return M + (fila[i] + 1) * DY

        self.items_nodo, self.items_arista, self.x_nodo = {}, {}, x
        self.resaltados = []
        for i in x:                               # primero las aristas
            if i != 0:
                self.items_arista[i] = cv.create_line(x[padre[i]], y(padre[i]), x[i], y(i), fill="#bdbdbd")
        for i in x:                               # luego los nodos
            cerrado = estado[i] == "valido" and fila[i] + 1 == prof_max and prof_max < n
            self.items_nodo[i] = cv.create_oval(x[i] - R, y(i) - R, x[i] + R, y(i) + R,
                                                fill=self.COLORES_NODO[estado[i]], outline="black",
                                                dash=(2, 2) if cerrado else None)
            cv.create_text(x[i], y(i), text="R" if i == 0 else str(col[i] + 1), font=("Arial", 7))
        for f in range(prof_max):                 # etiqueta de cada nivel
            cv.create_text(4, M + (f + 1) * DY, text=f"F{f + 1}", anchor="w", fill="gray40", font=("Arial", 8))

        ancho = max(640, M * 2 + siguiente_hoja[0] * DX)
        alto = max(360, M * 2 + prof_max * DY)
        cv.configure(scrollregion=(0, 0, ancho, alto))
        self.ancho_arbol = ancho
        if prof_max < n:
            self.lbl_arbol.config(text=(
                f"El árbol completo tiene {total} nodos; para que se lea, se dibujan solo las primeras "
                f"{prof_max} filas ({acumulado} nodos). Los nodos con borde punteado tienen más ramas debajo."))
        else:
            self.lbl_arbol.config(text=f"Árbol completo: {total} nodos (incluida la raíz R).")

    def _resaltar_camino(self):
        """Pinta de azul el camino desde la raíz hasta la solución que se está viendo."""
        cv = self.arbol
        for tipo, item in self.resaltados:
            if tipo == "n":
                cv.itemconfig(item, outline="black", width=1)
            else:
                cv.itemconfig(item, fill="#bdbdbd", width=1)
        self.resaltados = []
        sols = self.res["soluciones"]
        if not sols:
            return
        hoja = sols[self.idx][1]
        if hoja not in self.items_nodo:           # la hoja no se dibujó (árbol recortado)
            return
        i = hoja
        while i != -1 and i in self.items_nodo:
            cv.itemconfig(self.items_nodo[i], outline="#1f4fd1", width=3)
            self.resaltados.append(("n", self.items_nodo[i]))
            if i in self.items_arista:
                cv.itemconfig(self.items_arista[i], fill="#1f4fd1", width=3)
                self.resaltados.append(("a", self.items_arista[i]))
            i = self.res["padre"][i]
        # desplazar la vista para que se vea la hoja
        visible = int(cv.cget("width"))
        cv.xview_moveto(max(0.0, (self.x_nodo[hoja] - visible / 2) / self.ancho_arbol))


# ===========================================================================
# PROBLEMA 3: LABERINTO (RAT IN A MAZE) - TODOS LOS CAMINOS
# ===========================================================================
MOVIMIENTOS = [(1, 0), (0, 1), (-1, 0), (0, -1)]       # abajo, derecha, arriba, izquierda

LABERINTO_EJEMPLO = [                                  # 0 = libre, 1 = pared
    [0, 0, 0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 0, 0, 1, 0],
    [0, 0, 1, 1, 0, 0, 0],
    [1, 0, 0, 0, 0, 1, 0],
    [0, 0, 1, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0],
]


def salida_alcanzable(lab, n, desde, fin, bloqueadas):
    """BFS: ¿se puede llegar de `desde` a `fin` sin pisar paredes ni celdas bloqueadas?"""
    cola = deque([desde])
    vistos = {desde}
    while cola:
        f, c = cola.popleft()
        if (f, c) == fin:
            return True
        for df, dc in MOVIMIENTOS:
            nf, nc = f + df, c + dc
            if (0 <= nf < n and 0 <= nc < n and lab[nf][nc] == 0
                    and (nf, nc) not in vistos and not bloqueadas[nf][nc]):
                vistos.add((nf, nc))
                cola.append((nf, nc))
    return False


def laberinto_pasos(lab, n, inicio, fin, con_poda=True, max_caminos=500, max_pasos=300_000):
    """
    Backtracking que encuentra TODOS los caminos simples de `inicio` a `fin`.

    Restricciones de movimiento:
      - solo 4 direcciones (sin diagonales),
      - no se puede pisar una pared ni salir de la matriz,
      - no se puede pasar dos veces por la misma celda en un mismo camino.

    Poda opcional: antes de entrar a una celda se verifica (con BFS) que desde
    ella todavía se pueda llegar a la salida sin cruzar el camino actual. Si no
    se puede, esa rama se descarta sin explorarla.

    Eventos: ("avanzar", f, c), ("camino", lista_de_celdas), ("retroceder", f, c),
             ("podar", f, c).
    Retorna un diccionario con los caminos y si la búsqueda se cortó por un tope.
    """
    caminos = []
    camino = []
    en_camino = [[False] * n for _ in range(n)]
    info = {"pasos": 0, "podas": 0, "cortado": None}

    def backtrack(f, c):
        info["pasos"] += 1
        camino.append((f, c))                 # decisión: entrar a (f, c)
        en_camino[f][c] = True
        yield ("avanzar", f, c)
        if (f, c) == fin:
            caminos.append(list(camino))      # se encontró un camino completo
            yield ("camino", list(camino))
        else:
            for df, dc in MOVIMIENTOS:
                if len(caminos) >= max_caminos:
                    info["cortado"] = "caminos"
                    break
                if info["pasos"] >= max_pasos:
                    info["cortado"] = "pasos"
                    break
                nf, nc = f + df, c + dc
                if not (0 <= nf < n and 0 <= nc < n) or lab[nf][nc] == 1 or en_camino[nf][nc]:
                    continue                  # movimiento no permitido
                if con_poda and not salida_alcanzable(lab, n, (nf, nc), fin, en_camino):
                    info["podas"] += 1
                    yield ("podar", nf, nc)
                    continue
                yield from backtrack(nf, nc)
        camino.pop()                          # deshacer: salir de (f, c)
        en_camino[f][c] = False
        yield ("retroceder", f, c)

    yield from backtrack(*inicio)
    return {"caminos": caminos, **info}


class LaberintoApp:
    """Ventana del problema 3."""

    TAM = 440
    MAX_CAMINOS = 500
    C_LIBRE, C_PARED = "white", "#263238"
    C_VISITADA, C_ACTUAL = "#b3e5fc", "#ffb74d"
    C_CAMINO, C_PODA = "#fff176", "#e1bee7"
    C_INICIO, C_FIN = "#43a047", "#e53935"

    def __init__(self, root):
        self.root = root
        root.title("Problema 3 - Laberinto: todos los caminos (backtracking)")
        self.anim = Animador(root, self._procesar, self._redibujar, self._al_terminar, retardo=40)
        self.n = 7
        self.lab = []
        self.rects = []
        self.visitadas = set()
        self.podadas = set()
        self.camino_actual = []
        self.ultimo_camino = None
        self.caminos = []
        self.sel = None
        self.valor_pintar = None
        self.retrocesos = 0

        # ---- fila superior
        top = tk.Frame(root)
        top.pack(pady=6)
        tk.Label(top, text="Tamaño (4-10):").pack(side="left")
        self.var_n = tk.StringVar(value="7")
        tk.Spinbox(top, from_=4, to=10, textvariable=self.var_n, width=4).pack(side="left", padx=3)
        tk.Button(top, text="Nuevo vacío", command=self._nuevo_vacio).pack(side="left", padx=3)
        tk.Button(top, text="Ejemplo", command=self._ejemplo).pack(side="left", padx=3)
        tk.Button(top, text="Aleatorio", command=self._aleatorio).pack(side="left", padx=3)
        tk.Button(top, text="Borrar búsqueda", command=self._limpiar_busqueda).pack(side="left", padx=3)
        tk.Label(root, text="Haz clic o arrastra sobre las celdas para poner/quitar paredes.  "
                            "E = entrada (arriba-izquierda), S = salida (abajo-derecha).", fg="gray30").pack()

        cuerpo = tk.Frame(root)
        cuerpo.pack(padx=10, pady=4)
        self.canvas = tk.Canvas(cuerpo, width=self.TAM, height=self.TAM, bg="white", highlightthickness=0)
        self.canvas.pack(side="left")
        self.canvas.bind("<Button-1>", self._click)
        self.canvas.bind("<B1-Motion>", self._arrastrar)

        # ---- panel derecho: lista de caminos
        der = tk.Frame(cuerpo)
        der.pack(side="left", padx=10, anchor="n")
        tk.Label(der, text="Caminos encontrados\n(de más corto a más largo)", font=("Arial", 10, "bold")).pack()
        lf = tk.Frame(der)
        lf.pack()
        self.lista = tk.Listbox(lf, width=26, height=16, exportselection=False)
        sb = tk.Scrollbar(lf, command=self.lista.yview)
        self.lista.config(yscrollcommand=sb.set)
        self.lista.pack(side="left")
        sb.pack(side="left", fill="y")
        self.lista.bind("<<ListboxSelect>>", self._seleccionar)
        nav = tk.Frame(der)
        nav.pack(pady=4)
        tk.Button(nav, text="<< Anterior", command=lambda: self._mover(-1)).pack(side="left", padx=2)
        tk.Button(nav, text="Siguiente >>", command=lambda: self._mover(1)).pack(side="left", padx=2)
        self.var_poda = tk.BooleanVar(value=True)
        tk.Checkbutton(der, text="Poda: no entrar si la salida\nya no es alcanzable",
                       variable=self.var_poda, justify="left").pack(anchor="w", pady=6)

        leyenda(root, [(self.C_VISITADA, "Visitada"), (self.C_ACTUAL, "Camino en exploración"),
                       (self.C_PODA, "Podada"), (self.C_CAMINO, "Camino final"),
                       (self.C_PARED, "Pared")]).pack(pady=3)

        fb = tk.Frame(root)
        fb.pack(pady=3)
        self.b_buscar = tk.Button(fb, text="▶ Buscar todos los caminos", bg="#1565c0", fg="white",
                                  command=self.buscar)
        self.b_buscar.pack()
        barra_animacion(root, self.anim).pack(pady=3)

        self.lbl_stats = tk.Label(root, font=("Arial", 11))
        self.lbl_stats.pack()
        self.lbl_msg = tk.Label(root, font=("Arial", 11, "bold"), wraplength=700)
        self.lbl_msg.pack(pady=(2, 10))

        self._ejemplo()

    # ------------------------------------------------------------ armado del laberinto
    def _leer_n(self):
        try:
            n = int(self.var_n.get())
        except ValueError:
            n = 0
        if not 4 <= n <= 10:
            messagebox.showerror("Error", "El tamaño debe ser un número entre 4 y 10.", parent=self.root)
            return None
        return n

    def _crear(self, lab):
        if self.anim.activo:
            self.anim.detener()
        self.n = len(lab)
        self.var_n.set(str(self.n))
        self.lab = [fila[:] for fila in lab]
        self.lado = self.TAM // self.n
        self.canvas.delete("all")
        self.rects = [[self.canvas.create_rectangle(c * self.lado, f * self.lado, (c + 1) * self.lado,
                                                    (f + 1) * self.lado, outline="#9e9e9e")
                       for c in range(self.n)] for f in range(self.n)]
        fuente = ("Arial", max(10, self.lado // 3), "bold")
        self.canvas.create_text(self.lado / 2, self.lado / 2, text="E", fill="white", font=fuente)
        self.canvas.create_text((self.n - 0.5) * self.lado, (self.n - 0.5) * self.lado, text="S",
                                fill="white", font=fuente)
        self._limpiar_busqueda()

    def _nuevo_vacio(self):
        n = self._leer_n()
        if n:
            self._crear([[0] * n for _ in range(n)])

    def _ejemplo(self):
        self._crear(LABERINTO_EJEMPLO)

    def _aleatorio(self):
        n = self._leer_n()
        if not n:
            return
        for _ in range(200):                       # repetir hasta que tenga salida
            lab = [[1 if random.random() < 0.3 else 0 for _ in range(n)] for _ in range(n)]
            lab[0][0] = lab[n - 1][n - 1] = 0
            if salida_alcanzable(lab, n, (0, 0), (n - 1, n - 1), [[False] * n for _ in range(n)]):
                break
        self._crear(lab)

    def _celda(self, ev):
        c, f = int(ev.x // self.lado), int(ev.y // self.lado)
        if 0 <= f < self.n and 0 <= c < self.n and (f, c) not in ((0, 0), (self.n - 1, self.n - 1)):
            return f, c
        return None

    def _click(self, ev):
        if self.anim.activo:
            return                                  # no se edita durante la búsqueda
        celda = self._celda(ev)
        if celda:
            f, c = celda
            self.valor_pintar = 1 - self.lab[f][c]   # al arrastrar se pinta lo mismo
            self.lab[f][c] = self.valor_pintar
            self._limpiar_busqueda()

    def _arrastrar(self, ev):
        if self.anim.activo or self.valor_pintar is None:
            return
        celda = self._celda(ev)
        if celda and self.lab[celda[0]][celda[1]] != self.valor_pintar:
            self.lab[celda[0]][celda[1]] = self.valor_pintar
            self._redibujar()

    def _limpiar_busqueda(self):
        if self.anim.activo:
            self.anim.detener()
        self.visitadas, self.podadas = set(), set()
        self.camino_actual, self.caminos = [], []
        self.ultimo_camino, self.sel = None, None
        self.retrocesos = 0
        self.lista.delete(0, tk.END)
        self.lbl_stats.config(text="")
        self.lbl_msg.config(text="")
        self._redibujar()

    # ------------------------------------------------------------ búsqueda
    def buscar(self):
        if self.anim.activo:
            return
        self._limpiar_busqueda()
        n = self.n
        inicio, fin = (0, 0), (n - 1, n - 1)
        if not salida_alcanzable(self.lab, n, inicio, fin, [[False] * n for _ in range(n)]):
            self.lbl_msg.config(text="✘ No existe ningún camino de E a S: las paredes bloquean la salida.",
                                fg="#c62828")
            return
        self.b_buscar.config(state="disabled")
        self.lbl_msg.config(text="Buscando todos los caminos...", fg="#1f4fd1")
        self.anim.iniciar(laberinto_pasos(self.lab, n, inicio, fin, con_poda=self.var_poda.get(),
                                          max_caminos=self.MAX_CAMINOS))

    def _procesar(self, ev):
        tipo = ev[0]
        if tipo == "avanzar":
            self.camino_actual.append((ev[1], ev[2]))
            self.visitadas.add((ev[1], ev[2]))
        elif tipo == "retroceder":
            self.camino_actual.pop()
            self.retrocesos += 1
        elif tipo == "podar":
            self.podadas.add((ev[1], ev[2]))
        elif tipo == "camino":
            self.caminos.append(ev[1])
            self.ultimo_camino = ev[1]

    def _redibujar(self):
        resaltado = set()
        if self.sel is not None:
            resaltado = set(self.caminos[self.sel])
        elif self.anim.activo and self.ultimo_camino:
            resaltado = set(self.ultimo_camino)       # último camino hallado
        actual = set(self.camino_actual)
        for f in range(self.n):
            for c in range(self.n):
                if (f, c) == (0, 0):
                    color = self.C_INICIO
                elif (f, c) == (self.n - 1, self.n - 1):
                    color = self.C_FIN
                elif self.lab[f][c] == 1:
                    color = self.C_PARED
                elif (f, c) in actual:
                    color = self.C_ACTUAL
                elif (f, c) in resaltado:
                    color = self.C_CAMINO
                elif (f, c) in self.visitadas:
                    color = self.C_VISITADA
                elif (f, c) in self.podadas:
                    color = self.C_PODA
                else:
                    color = self.C_LIBRE
                self.canvas.itemconfig(self.rects[f][c], fill=color)
        if self.anim.activo:
            self.lbl_stats.config(text=f"Caminos: {len(self.caminos)}   |   Celdas exploradas: "
                                       f"{len(self.visitadas)}   |   Retrocesos: {self.retrocesos}   |   "
                                       f"Tiempo: {self.anim.tiempo:.2f} s")

    def _al_terminar(self, res, detenido):
        self.b_buscar.config(state="normal")
        self.camino_actual = []
        self.caminos.sort(key=len)                     # más cortos primero
        self.lista.delete(0, tk.END)
        for i, cam in enumerate(self.caminos, 1):
            self.lista.insert(tk.END, f"Camino {i}: {len(cam) - 1} movimientos")
        pasos = res["pasos"] if res else len(self.visitadas)
        podas = res["podas"] if res else len(self.podadas)
        self.lbl_stats.config(text=(
            f"Caminos: {len(self.caminos)}   |   Nodos explorados: {pasos}   |   Retrocesos: {self.retrocesos}   |   "
            f"Podas: {podas}   |   Tiempo: {self.anim.tiempo:.2f} s"))
        if self.caminos:
            corto, largo = len(self.caminos[0]) - 1, len(self.caminos[-1]) - 1
            texto = f"✔ {len(self.caminos)} camino(s). Más corto: {corto} movimientos, más largo: {largo}."
            color = "#2e7d32"
            self._elegir(0)
        else:
            texto, color = "✘ No existe ningún camino de E a S.", "#c62828"
            self._redibujar()
        if detenido:
            texto, color = "Búsqueda detenida. " + texto, "#b26a00"
        elif res and res["cortado"] == "caminos":
            texto += f" Se llegó al tope de {self.MAX_CAMINOS} caminos: hay más, pero no se listan."
            color = "#b26a00"
        elif res and res["cortado"] == "pasos":
            texto += " La búsqueda se cortó por el límite de pasos (laberinto muy abierto)."
            color = "#b26a00"
        self.lbl_msg.config(text=texto, fg=color)

    # ------------------------------------------------------------ navegación de caminos
    def _elegir(self, i):
        if not self.caminos or self.anim.activo:
            return
        self.sel = max(0, min(i, len(self.caminos) - 1))
        self.lista.selection_clear(0, tk.END)
        self.lista.selection_set(self.sel)
        self.lista.see(self.sel)
        self._redibujar()

    def _seleccionar(self, _ev):
        sel = self.lista.curselection()
        if sel:
            self._elegir(sel[0])

    def _mover(self, paso):
        if self.sel is not None:
            self._elegir(self.sel + paso)


# ===========================================================================
# PROBLEMA 4: COLOREADO DE GRAFOS
# ===========================================================================
PALETA_INICIAL = ["#e53935", "#1e88e5", "#43a047", "#fdd835", "#8e24aa", "#fb8c00", "#00acc1", "#ec407a"]


def coloreo_pasos(n, adyacentes, k, colores):
    """
    Backtracking del coloreado de grafos (modifica la lista `colores`).

    Se colorean los nodos en orden 0, 1, 2, ...  Para cada nodo se prueban los
    colores 0..k-1. Un color es válido si ningún vecino ya lo tiene. Si ningún
    color sirve, se vuelve al nodo anterior para cambiar su color (retroceso).

    Eventos: ("asignar", nodo, color), ("conflicto", nodo, color),
             ("retroceder", nodo, color).
    Retorna True si existe un coloreado con k colores.
    """
    def backtrack(i):
        if i == n:
            return True                                    # todos los nodos coloreados
        for c in range(k):
            if any(colores[v] == c for v in adyacentes[i]):
                yield ("conflicto", i, c)                  # un vecino ya usa ese color
                continue
            colores[i] = c                                 # decisión
            yield ("asignar", i, c)
            if (yield from backtrack(i + 1)):
                return True
            colores[i] = -1                                # deshacer
            yield ("retroceder", i, c)
        return False

    return (yield from backtrack(0))


class GrafosApp:
    """Ventana del problema 4."""

    R = 17                       # radio de los nodos
    ANCHO, ALTO = 680, 440

    def __init__(self, root):
        self.root = root
        root.title("Problema 4 - Coloreado de grafos (backtracking)")
        self.anim = Animador(root, self._procesar, self._redibujar, self._al_terminar, retardo=300)
        self.nodos = []           # [(x, y)]
        self.aristas = []         # [(u, v)] con u < v
        self.colores = []         # color de cada nodo (-1 = sin color)
        self.paleta = PALETA_INICIAL[:]
        self.origen = None        # nodo desde el que se arrastra una arista
        self.linea_temp = None
        self.actual = None        # nodo que el algoritmo está evaluando
        self.conflicto = None     # (nodo, color) rechazado
        self.asignaciones = self.retrocesos = self.conflictos = 0

        # ---- fila 1: k y paleta
        f1 = tk.Frame(root)
        f1.pack(pady=(8, 2))
        tk.Label(f1, text="Colores máximos (k):").pack(side="left")
        self.var_k = tk.StringVar(value="3")
        tk.Spinbox(f1, from_=1, to=len(self.paleta), textvariable=self.var_k, width=4,
                   command=self._dibujar_paleta).pack(side="left", padx=4)
        tk.Label(f1, text="   Paleta (clic en un color para cambiarlo):").pack(side="left")
        self.fr_paleta = tk.Frame(f1)
        self.fr_paleta.pack(side="left", padx=4)

        # ---- fila 2: acciones
        f2 = tk.Frame(root)
        f2.pack(pady=4)
        self.b_colorear = tk.Button(f2, text="▶ Colorear con k colores", bg="#6a1b9a", fg="white",
                                    command=self.colorear)
        self.b_colorear.pack(side="left", padx=3)
        tk.Button(f2, text="Calcular k mínimo", command=self.k_minimo).pack(side="left", padx=3)
        tk.Button(f2, text="Ejemplo (grafo de Petersen)", command=self.ejemplo).pack(side="left", padx=3)
        tk.Button(f2, text="Quitar colores", command=self._quitar_colores).pack(side="left", padx=3)
        tk.Button(f2, text="Limpiar todo", command=self.limpiar).pack(side="left", padx=3)

        tk.Label(root, fg="gray30", text="Clic en zona vacía: crear nodo  ·  Arrastrar de un nodo a otro: "
                                         "crear arista  ·  Clic derecho: borrar nodo o arista").pack()
        self.canvas = tk.Canvas(root, width=self.ANCHO, height=self.ALTO, bg="white", cursor="cross")
        self.canvas.pack(padx=10, pady=4)
        self.canvas.bind("<Button-1>", self._click)
        self.canvas.bind("<B1-Motion>", self._mover_mouse)
        self.canvas.bind("<ButtonRelease-1>", self._soltar)
        self.canvas.bind("<Button-3>", self._borrar)

        barra_animacion(root, self.anim).pack(pady=3)
        self.lbl_stats = tk.Label(root, font=("Arial", 11))
        self.lbl_stats.pack()
        self.lbl_msg = tk.Label(root, font=("Arial", 12, "bold"))
        self.lbl_msg.pack(pady=(2, 10))

        self._dibujar_paleta()
        self.ejemplo()

    # ------------------------------------------------------------ paleta de colores
    def _leer_k(self, avisar=True):
        try:
            k = int(self.var_k.get())
        except ValueError:
            k = 0
        if not 1 <= k <= len(self.paleta):
            if avisar:
                messagebox.showerror("Error", f"k debe ser un número entre 1 y {len(self.paleta)}.",
                                     parent=self.root)
            return None
        return k

    def _dibujar_paleta(self):
        for w in self.fr_paleta.winfo_children():
            w.destroy()
        k = self._leer_k(avisar=False) or 0
        for i in range(k):
            lb = tk.Label(self.fr_paleta, bg=self.paleta[i], width=3, relief="raised", bd=2,
                          text=str(i + 1), cursor="hand2")
            lb.pack(side="left", padx=1)
            lb.bind("<Button-1>", lambda e, j=i: self._elegir_color(j))

    def _elegir_color(self, i):
        if self.anim.activo:
            return
        _, nuevo = colorchooser.askcolor(self.paleta[i], title=f"Color {i + 1}", parent=self.root)
        if nuevo:
            self.paleta[i] = nuevo
            self._dibujar_paleta()
            self._redibujar()

    # ------------------------------------------------------------ edición del grafo
    def _nodo_en(self, x, y):
        for i, (nx, ny) in enumerate(self.nodos):
            if (nx - x) ** 2 + (ny - y) ** 2 <= self.R ** 2:
                return i
        return None

    def _arista_en(self, x, y):
        """Arista más cercana al punto (distancia punto-segmento < 6 px)."""
        for idx, (u, v) in enumerate(self.aristas):
            (x1, y1), (x2, y2) = self.nodos[u], self.nodos[v]
            dx, dy = x2 - x1, y2 - y1
            largo2 = dx * dx + dy * dy or 1
            t = max(0, min(1, ((x - x1) * dx + (y - y1) * dy) / largo2))
            px, py = x1 + t * dx, y1 + t * dy
            if (px - x) ** 2 + (py - y) ** 2 <= 36:
                return idx
        return None

    def _cambio_en_grafo(self):
        self.colores = [-1] * len(self.nodos)
        self.actual = self.conflicto = None
        self.lbl_msg.config(text="")
        self._redibujar()

    def _click(self, ev):
        if self.anim.activo:
            return
        i = self._nodo_en(ev.x, ev.y)
        if i is not None:
            self.origen = i                      # empieza a arrastrar una arista
            return
        muy_cerca = any((nx - ev.x) ** 2 + (ny - ev.y) ** 2 < (2.2 * self.R) ** 2 for nx, ny in self.nodos)
        dentro = self.R <= ev.x <= self.ANCHO - self.R and self.R <= ev.y <= self.ALTO - self.R
        if not muy_cerca and dentro:
            self.nodos.append((ev.x, ev.y))
            self._cambio_en_grafo()

    def _mover_mouse(self, ev):
        if self.origen is None:
            return
        x, y = self.nodos[self.origen]
        if self.linea_temp:
            self.canvas.coords(self.linea_temp, x, y, ev.x, ev.y)
        else:
            self.linea_temp = self.canvas.create_line(x, y, ev.x, ev.y, dash=(4, 2), fill="gray40")

    def _soltar(self, ev):
        if self.origen is None:
            return
        destino = self._nodo_en(ev.x, ev.y)
        if destino is not None and destino != self.origen:
            arista = (min(self.origen, destino), max(self.origen, destino))
            if arista not in self.aristas:
                self.aristas.append(arista)
        self.origen = None
        if self.linea_temp:
            self.canvas.delete(self.linea_temp)
            self.linea_temp = None
        self._cambio_en_grafo()

    def _borrar(self, ev):
        if self.anim.activo:
            return
        i = self._nodo_en(ev.x, ev.y)
        if i is not None:
            # borrar el nodo, sus aristas y renumerar los nodos siguientes
            self.nodos.pop(i)
            nuevas = []
            for u, v in self.aristas:
                if i in (u, v):
                    continue
                nuevas.append((u - (u > i), v - (v > i)))
            self.aristas = nuevas
        else:
            a = self._arista_en(ev.x, ev.y)
            if a is None:
                return
            self.aristas.pop(a)
        self._cambio_en_grafo()

    def limpiar(self):
        if self.anim.activo:
            self.anim.detener()
        self.nodos, self.aristas = [], []
        self._reset_contadores()
        self._cambio_en_grafo()

    def _quitar_colores(self):
        if self.anim.activo:
            self.anim.detener()
        self._reset_contadores()
        self._cambio_en_grafo()

    def ejemplo(self):
        """Grafo de Petersen: 10 nodos, 15 aristas, necesita exactamente 3 colores."""
        import math
        if self.anim.activo:
            self.anim.detener()
        cx, cy = self.ANCHO / 2, self.ALTO / 2
        self.nodos = []
        for radio in (180, 85):
            for i in range(5):
                ang = math.radians(-90 + 72 * i)
                self.nodos.append((cx + radio * math.cos(ang), cy + radio * math.sin(ang)))
        self.aristas = ([(i, (i + 1) % 5) for i in range(5)] +              # pentágono exterior
                        [(i, i + 5) for i in range(5)] +                    # rayos
                        [(5 + i, 5 + (i + 2) % 5) for i in range(5)])       # estrella interior
        self.aristas = [(min(u, v), max(u, v)) for u, v in self.aristas]
        self._reset_contadores()
        self._cambio_en_grafo()

    # ------------------------------------------------------------ algoritmo
    def _adyacencia(self):
        ady = [set() for _ in self.nodos]
        for u, v in self.aristas:
            ady[u].add(v)
            ady[v].add(u)
        return ady

    def _reset_contadores(self):
        self.asignaciones = self.retrocesos = self.conflictos = 0
        self.anim.tiempo = 0.0
        self.lbl_stats.config(text="")

    def colorear(self):
        if self.anim.activo:
            return
        if not self.nodos:
            messagebox.showinfo("Grafo vacío", "Primero agrega nodos haciendo clic en el lienzo.", parent=self.root)
            return
        k = self._leer_k()
        if not k:
            return
        self._dibujar_paleta()
        self._reset_contadores()
        self.k = k
        self.colores = [-1] * len(self.nodos)
        self.b_colorear.config(state="disabled")
        self.lbl_msg.config(text=f"Buscando un coloreado con k = {k}...", fg="#1f4fd1")
        self.anim.iniciar(coloreo_pasos(len(self.nodos), self._adyacencia(), k, self.colores))

    def _procesar(self, ev):
        tipo, i, c = ev
        self.actual = i
        self.conflicto = None
        if tipo == "asignar":
            self.asignaciones += 1
        elif tipo == "retroceder":
            self.retrocesos += 1
        else:
            self.conflictos += 1
            self.conflicto = (i, c)

    def _al_terminar(self, posible, detenido):
        self.b_colorear.config(state="normal")
        self.actual = self.conflicto = None
        self._redibujar()
        if detenido:
            self.lbl_msg.config(text="Búsqueda detenida.", fg="#b26a00")
        elif posible:
            usados = len(set(self.colores))
            self.lbl_msg.config(text=f"✔ SÍ es posible colorear el grafo con k = {self.k} colores "
                                     f"(se usaron {usados}).", fg="#2e7d32")
        else:
            self.lbl_msg.config(text=f"✘ NO es posible colorear el grafo con k = {self.k} colores.", fg="#c62828")

    def k_minimo(self):
        """Prueba k = 1, 2, 3... (sin animación) hasta encontrar el menor k posible."""
        if self.anim.activo or not self.nodos:
            return
        ady = self._adyacencia()
        t0 = time.perf_counter()
        for k in range(1, len(self.paleta) + 1):
            colores = [-1] * len(self.nodos)
            posible, _ = ejecutar_completo(coloreo_pasos(len(self.nodos), ady, k, colores))
            if posible:
                self.colores = colores
                self.var_k.set(str(k))
                self._dibujar_paleta()
                self._redibujar()
                self.lbl_msg.config(text=f"El menor número de colores posible (número cromático) es k = {k}.  "
                                         f"({(time.perf_counter() - t0) * 1000:.1f} ms)", fg="#2e7d32")
                return
        self.lbl_msg.config(text=f"Se necesitan más de {len(self.paleta)} colores.", fg="#c62828")

    # ------------------------------------------------------------ dibujo
    def _redibujar(self):
        cv = self.canvas
        cv.delete("all")
        self.linea_temp = None
        # aristas: en rojo las que causan el conflicto actual
        for u, v in self.aristas:
            choque = (self.conflicto is not None and self.conflicto[0] in (u, v)
                      and self.colores[v if self.conflicto[0] == u else u] == self.conflicto[1])
            (x1, y1), (x2, y2) = self.nodos[u], self.nodos[v]
            cv.create_line(x1, y1, x2, y2, width=4 if choque else 2, fill="#d50000" if choque else "#455a64")
        # nodos
        for i, (x, y) in enumerate(self.nodos):
            c = self.colores[i] if i < len(self.colores) else -1
            relleno = self.paleta[c] if c != -1 else "white"
            if self.conflicto is not None and self.conflicto[0] == i:
                # anillo con el color que se intentó y fue rechazado
                cv.create_oval(x - self.R - 7, y - self.R - 7, x + self.R + 7, y + self.R + 7,
                               outline=self.paleta[self.conflicto[1]], width=4, dash=(3, 2))
            grosor = 4 if i == self.actual else 2
            cv.create_oval(x - self.R, y - self.R, x + self.R, y + self.R, fill=relleno,
                           outline="black", width=grosor)
            cv.create_text(x, y, text=str(i), font=("Arial", 10, "bold"))
        if self.anim.activo or self.asignaciones:
            self.lbl_stats.config(text=(
                f"Asignaciones: {self.asignaciones}   |   Conflictos detectados: {self.conflictos}   |   "
                f"Retrocesos: {self.retrocesos}   |   Tiempo: {self.anim.tiempo:.2f} s"))


# ===========================================================================
# MENÚ PRINCIPAL
# ===========================================================================
PROBLEMAS = [
    ("Problema 1: Sudoku 6x6 / 9x9", "Animación paso a paso, retrocesos y tiempo", SudokuApp),
    ("Problema 2: N-Reinas", "Todas las soluciones y árbol de decisiones", NReinasApp),
    ("Problema 3: Laberinto (Rat in a Maze)", "Todos los caminos posibles", LaberintoApp),
    ("Problema 4: Coloreado de grafos", "Grafo interactivo y paleta editable", GrafosApp),
]


def main():
    # Acceso directo: python backtracking.py 3
    if len(sys.argv) > 1 and sys.argv[1] in ("1", "2", "3", "4"):
        root = tk.Tk()
        PROBLEMAS[int(sys.argv[1]) - 1][2](root)
        root.mainloop()
        return

    root = tk.Tk()
    root.title("Semana 4 - Backtracking")
    tk.Label(root, text="Práctica de campo - Backtracking", font=("Arial", 15, "bold")).pack(padx=30, pady=(16, 2))
    tk.Label(root, text="Análisis de Algoritmos y Estrategias de Programación", fg="gray30").pack(pady=(0, 10))
    for titulo, detalle, clase in PROBLEMAS:
        tk.Button(root, text=f"{titulo}\n{detalle}", width=42, justify="center",
                  command=lambda c=clase: c(tk.Toplevel(root))).pack(padx=30, pady=4)
    tk.Button(root, text="Salir", width=10, command=root.destroy).pack(pady=(10, 16))
    root.mainloop()


if __name__ == "__main__":
    main()
