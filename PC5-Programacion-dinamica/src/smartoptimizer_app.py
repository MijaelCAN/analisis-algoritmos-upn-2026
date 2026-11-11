# -*- coding: utf-8 -*-
"""
PC5 - Programación Dinámica (UPN 2026-2) - Grupo 7
Caso SmartOptimizer S.A.C.: aplicación Tkinter con tres módulos de optimización.

  1. Rutas de desplazamiento  -> costo mínimo de la posición inicial al destino
  2. Ingreso de técnicos      -> número de formas de llegar a un nivel
  3. Selección de proyectos   -> máximo beneficio sin proyectos consecutivos

Ejecutar:  python src/smartoptimizer_app.py
Capturas:  python src/smartoptimizer_app.py --capturas   (guarda una imagen por módulo en capturas/)
"""
import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox

from dp_logica import (ruta_costo_minimo, formas_de_llegar, relacion_recurrencia,
                       seleccion_proyectos)

COLOR_PRIMARIO = "#1f4e79"
COLOR_ACENTO = "#f4b400"
COLOR_OK = "#2e7d32"
COLOR_NO = "#c62828"
FUENTE = ("Segoe UI", 10)
FUENTE_TITULO = ("Segoe UI", 15, "bold")
FUENTE_RESULTADO = ("Segoe UI", 12, "bold")
FUENTE_MONO = ("Consolas", 10)


def entero(entry, nombre, minimo=None):
    """Lee un entero de un Entry y valida el rango; lanza ValueError con un mensaje claro."""
    try:
        valor = int(entry.get().strip())
    except ValueError:
        raise ValueError(f"'{nombre}' debe ser un número entero.")
    if minimo is not None and valor < minimo:
        raise ValueError(f"'{nombre}' debe ser mayor o igual que {minimo}.")
    return valor


def tabla(padre, columnas, alto=8):
    """Crea un Treeview con columnas centradas y barra de desplazamiento."""
    marco = ttk.Frame(padre)
    tv = ttk.Treeview(marco, columns=columnas, show="headings", height=alto)
    for c in columnas:
        tv.heading(c, text=c)
        tv.column(c, anchor="center", width=max(70, 9 * len(c)))
    sb = ttk.Scrollbar(marco, orient="vertical", command=tv.yview)
    tv.configure(yscrollcommand=sb.set)
    tv.pack(side="left", fill="both", expand=True)
    sb.pack(side="right", fill="y")
    return marco, tv


def caja_texto(padre, alto=7):
    txt = tk.Text(padre, height=alto, font=FUENTE_MONO, wrap="word", relief="solid", bd=1,
                  bg="#fbfbfb", padx=8, pady=6)
    return txt


def escribir(txt, contenido):
    txt.configure(state="normal")
    txt.delete("1.0", "end")
    txt.insert("1.0", contenido)
    txt.configure(state="disabled")


# ---------------------------------------------------------------------------
# Módulo 1: Rutas de desplazamiento
# ---------------------------------------------------------------------------
class ModuloRutas(ttk.Frame):
    def __init__(self, padre):
        super().__init__(padre, padding=12)
        ttk.Label(self, text="Casuística 01 · Optimización de rutas de desplazamiento",
                  style="Sub.TLabel").grid(row=0, column=0, columnspan=4, sticky="w")
        ttk.Label(self, text="Costo mínimo acumulado para llegar al destino avanzando 1, 2 o 3 posiciones.",
                  ).grid(row=1, column=0, columnspan=4, sticky="w", pady=(0, 8))

        datos = ttk.LabelFrame(self, text="Datos", padding=8)
        datos.grid(row=2, column=0, sticky="nw")
        self.e_ini = self._campo(datos, "Posición inicial", "0", 0)
        self.e_des = self._campo(datos, "Destino", "10", 1)
        self.e_c1 = self._campo(datos, "Costo avanzar 1 (S/)", "10", 2)
        self.e_c2 = self._campo(datos, "Costo avanzar 2 (S/)", "18", 3)
        self.e_c3 = self._campo(datos, "Costo avanzar 3 (S/)", "25", 4)
        ttk.Button(datos, text="Calcular ruta óptima", style="Accent.TButton",
                   command=self.resolver).grid(row=5, column=0, columnspan=2, pady=(10, 0), sticky="ew")

        der = ttk.Frame(self)
        der.grid(row=2, column=1, sticky="nsew", padx=(14, 0))
        self.lbl = ttk.Label(der, text="", style="Res.TLabel")
        self.lbl.pack(anchor="w")
        self.canvas = tk.Canvas(der, height=120, bg="white", highlightthickness=1,
                                highlightbackground="#d0d0d0")
        self.canvas.pack(fill="x", pady=(6, 6))
        marco, self.tv = tabla(der, ("Posición", "Costo mínimo dp[i]", "Último paso", "Viene de"), alto=11)
        marco.pack(fill="both", expand=True)
        self.txt = caja_texto(der, 5)
        self.txt.pack(fill="x", pady=(6, 0))
        self.columnconfigure(1, weight=1)
        self.resolver()

    def _campo(self, padre, texto, valor, fila):
        ttk.Label(padre, text=texto).grid(row=fila, column=0, sticky="w", pady=2)
        e = ttk.Entry(padre, width=8, justify="center")
        e.insert(0, valor)
        e.grid(row=fila, column=1, padx=(8, 0), pady=2)
        return e

    def resolver(self):
        try:
            ini = entero(self.e_ini, "Posición inicial", 0)
            des = entero(self.e_des, "Destino", ini)
            costos = {1: entero(self.e_c1, "Costo 1", 0), 2: entero(self.e_c2, "Costo 2", 0),
                      3: entero(self.e_c3, "Costo 3", 0)}
            if des - ini > 60:
                raise ValueError("Use como máximo 60 posiciones para que el gráfico sea legible.")
        except ValueError as e:
            messagebox.showerror("Dato inválido", str(e))
            return
        costo, dp, decision, camino = ruta_costo_minimo(ini, des, costos)

        self.lbl.configure(text=f"Costo mínimo de {ini} a {des}: S/ {costo}")
        self.tv.delete(*self.tv.get_children())
        for j, v in enumerate(dp):
            p = decision[j]
            self.tv.insert("", "end", values=(ini + j, f"S/ {v}", f"+{p}" if p else "—",
                                              ini + j - p if p else "inicio"))
        ruta = " → ".join([str(ini)] + [str(b) for _, b, _, _ in camino])
        pasos = " + ".join(f"S/{k}" for _, _, _, k in camino)
        escribir(self.txt,
                 f"Ruta óptima: {ruta}\n"
                 f"Costo: {pasos} = S/ {costo}  ({len(camino)} movimientos)\n"
                 f"Recurrencia: dp[i] = min(dp[i-1] + {costos[1]}, dp[i-2] + {costos[2]}, dp[i-3] + {costos[3]}),"
                 f" dp[{ini}] = 0\n"
                 f"Complejidad: O(n·k) = O({des - ini}·3) operaciones; cada posición se calcula una sola vez.")
        self._dibujar(ini, des, dp, camino)

    def _dibujar(self, ini, des, dp, camino):
        c = self.canvas
        c.delete("all")
        c.update_idletasks()
        ancho = max(c.winfo_width(), 600)
        n = des - ini
        margen = 30
        paso_x = (ancho - 2 * margen) / max(n, 1)
        y = 80
        xs = [margen + j * paso_x for j in range(n + 1)]
        usados = {b for _, b, _, _ in camino} | {ini}
        # arcos de la ruta óptima
        for a, b, p, k in camino:
            x1, x2 = xs[a - ini], xs[b - ini]
            c.create_arc(x1, y - 55, x2, y + 5, start=0, extent=180, style="arc",
                         outline=COLOR_ACENTO, width=3)
            c.create_text((x1 + x2) / 2, y - 62, text=f"+{p} · S/{k}", font=("Segoe UI", 8, "bold"),
                          fill="#8a6d00")
        for j, x in enumerate(xs):
            pos = ini + j
            color = COLOR_PRIMARIO if pos in usados else "#b0b0b0"
            c.create_oval(x - 11, y - 11, x + 11, y + 11, fill=color, outline="")
            c.create_text(x, y, text=str(pos), fill="white", font=("Segoe UI", 8, "bold"))
            c.create_text(x, y + 22, text=f"{dp[j]}", font=("Segoe UI", 8), fill="#555")


# ---------------------------------------------------------------------------
# Módulo 2: Ingreso de técnicos
# ---------------------------------------------------------------------------
class ModuloTecnicos(ttk.Frame):
    def __init__(self, padre):
        super().__init__(padre, padding=12)
        ttk.Label(self, text="Casuística 02 · Optimización del ingreso de técnicos",
                  style="Sub.TLabel").grid(row=0, column=0, columnspan=2, sticky="w")
        ttk.Label(self, text="Número de formas distintas de llegar a un nivel de certificación "
                             "avanzando 1, 2 o 3 niveles.").grid(row=1, column=0, columnspan=2,
                                                                 sticky="w", pady=(0, 8))
        datos = ttk.LabelFrame(self, text="Datos", padding=8)
        datos.grid(row=2, column=0, sticky="nw")
        ttk.Label(datos, text="Cantidad de niveles").grid(row=0, column=0, sticky="w")
        self.e_niv = ttk.Entry(datos, width=8, justify="center")
        self.e_niv.insert(0, "8")
        self.e_niv.grid(row=0, column=1, padx=(8, 0))
        ttk.Label(datos, text="Saltos permitidos: 1, 2 y 3").grid(row=1, column=0, columnspan=2,
                                                                 sticky="w", pady=(6, 0))
        ttk.Button(datos, text="Calcular formas", style="Accent.TButton",
                   command=self.resolver).grid(row=2, column=0, columnspan=2, pady=(10, 0), sticky="ew")

        der = ttk.Frame(self)
        der.grid(row=2, column=1, sticky="nsew", padx=(14, 0))
        self.lbl = ttk.Label(der, text="", style="Res.TLabel")
        self.lbl.pack(anchor="w")
        ttk.Label(der, text="Relación de recurrencia:\n" + relacion_recurrencia(),
                  font=("Consolas", 10, "bold"), foreground=COLOR_PRIMARIO).pack(anchor="w", pady=(4, 6))
        marco, self.tv = tabla(der, ("Nivel n", "f(n-1)", "f(n-2)", "f(n-3)", "f(n) formas"), alto=9)
        marco.pack(fill="both", expand=True)
        ttk.Label(der, text="Resultados parciales:").pack(anchor="w", pady=(6, 0))
        self.txt = caja_texto(der, 9)
        self.txt.pack(fill="x")
        self.columnconfigure(1, weight=1)
        self.resolver()

    def resolver(self):
        try:
            n = entero(self.e_niv, "Cantidad de niveles", 0)
            if n > 60:
                raise ValueError("Use como máximo 60 niveles.")
        except ValueError as e:
            messagebox.showerror("Dato inválido", str(e))
            return
        total, f, detalle = formas_de_llegar(n)
        self.lbl.configure(text=f"Formas de llegar al nivel {n}: {total}")
        self.tv.delete(*self.tv.get_children())
        val = lambda i: f[i] if i >= 0 else 0
        for i in range(n + 1):
            if i == 0:
                self.tv.insert("", "end", values=(0, "—", "—", "—", "1 (base)"))
            else:
                self.tv.insert("", "end", values=(i, val(i - 1), val(i - 2), val(i - 3), f[i]))
        escribir(self.txt, "\n".join(detalle))


# ---------------------------------------------------------------------------
# Módulo 3: Selección de proyectos
# ---------------------------------------------------------------------------
class ModuloProyectos(ttk.Frame):
    BENEFICIOS = [4000, 2500, 5000, 3500, 6000, 4500, 7000, 3000]

    def __init__(self, padre):
        super().__init__(padre, padding=12)
        ttk.Label(self, text="Casuística 03 · Selección óptima de proyectos tecnológicos",
                  style="Sub.TLabel").grid(row=0, column=0, columnspan=2, sticky="w")
        ttk.Label(self, text="Máximo beneficio sin seleccionar dos proyectos consecutivos "
                             "(usan el mismo equipo especializado).").grid(row=1, column=0, columnspan=2,
                                                                         sticky="w", pady=(0, 8))
        datos = ttk.LabelFrame(self, text="Beneficio por proyecto (S/)", padding=8)
        datos.grid(row=2, column=0, sticky="nw")
        self.entradas = []
        for i, b in enumerate(self.BENEFICIOS):
            ttk.Label(datos, text=f"P{i + 1}").grid(row=i, column=0, sticky="w", pady=1)
            e = ttk.Entry(datos, width=9, justify="center")
            e.insert(0, str(b))
            e.grid(row=i, column=1, padx=(8, 0), pady=1)
            self.entradas.append(e)
        ttk.Button(datos, text="Calcular selección", style="Accent.TButton",
                   command=self.resolver).grid(row=len(self.BENEFICIOS), column=0, columnspan=2,
                                               pady=(10, 0), sticky="ew")

        der = ttk.Frame(self)
        der.grid(row=2, column=1, sticky="nsew", padx=(14, 0))
        self.lbl = ttk.Label(der, text="", style="Res.TLabel")
        self.lbl.pack(anchor="w")
        self.canvas = tk.Canvas(der, height=62, bg="white", highlightthickness=1,
                                highlightbackground="#d0d0d0")
        self.canvas.pack(fill="x", pady=(6, 6))
        marco, self.tv = tabla(der, ("i", "Proyecto", "Beneficio", "Sin Pi: dp[i-1]",
                                     "Con Pi: dp[i-2]+b", "dp[i]", "Decisión"), alto=8)
        marco.pack(fill="both", expand=True)
        self.txt = caja_texto(der, 5)
        self.txt.pack(fill="x", pady=(6, 0))
        self.columnconfigure(1, weight=1)
        self.resolver()

    def resolver(self):
        try:
            b = [entero(e, f"P{i + 1}", 0) for i, e in enumerate(self.entradas)]
        except ValueError as e:
            messagebox.showerror("Dato inválido", str(e))
            return
        maximo, dp, sel, des, filas = seleccion_proyectos(b)
        self.lbl.configure(text=f"Beneficio máximo: S/ {maximo:,}")
        self.tv.delete(*self.tv.get_children())
        for i, bi, sin_i, con_i, dpi, dec in filas:
            self.tv.insert("", "end", values=(i, f"P{i}", f"{bi:,}", f"{sin_i:,}", f"{con_i:,}",
                                              f"{dpi:,}", dec))
        escribir(self.txt,
                 f"Seleccionados: {', '.join(f'P{i}' for i in sel)}  "
                 f"(S/ {' + '.join(f'{b[i - 1]:,}' for i in sel)} = S/ {maximo:,})\n"
                 f"Descartados:   {', '.join(f'P{i}' for i in des)}\n"
                 "Estrategia: para cada proyecto Pi se compara no tomarlo (dp[i-1]) con tomarlo y "
                 "saltar el anterior (dp[i-2] + b[i]); dp[i] guarda el mejor. Luego se recorre la tabla "
                 "de atrás hacia adelante para saber qué proyectos se eligieron. Complejidad O(n).")
        self._dibujar(b, sel)

    def _dibujar(self, b, sel):
        c = self.canvas
        c.delete("all")
        c.update_idletasks()
        ancho = max(c.winfo_width(), 600)
        n = len(b)
        w = (ancho - 20) / n
        for i in range(n):
            x0 = 10 + i * w
            elegido = (i + 1) in sel
            c.create_rectangle(x0 + 3, 8, x0 + w - 3, 54, fill=COLOR_OK if elegido else "#eeeeee",
                               outline=COLOR_OK if elegido else "#bdbdbd")
            col = "white" if elegido else "#616161"
            c.create_text(x0 + w / 2, 22, text=f"P{i + 1}", fill=col, font=("Segoe UI", 9, "bold"))
            c.create_text(x0 + w / 2, 40, text=f"S/ {b[i]:,}", fill=col, font=("Segoe UI", 8))


# ---------------------------------------------------------------------------
# Ventana principal
# ---------------------------------------------------------------------------
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SmartOptimizer S.A.C. · Optimización con Programación Dinámica")
        self.geometry("1100x800")
        self.minsize(980, 700)
        estilo = ttk.Style(self)
        if "vista" in estilo.theme_names():
            estilo.theme_use("vista")
        estilo.configure(".", font=FUENTE)
        estilo.configure("Sub.TLabel", font=("Segoe UI", 12, "bold"), foreground=COLOR_PRIMARIO)
        estilo.configure("Res.TLabel", font=FUENTE_RESULTADO, foreground=COLOR_OK)
        estilo.configure("Accent.TButton", font=("Segoe UI", 10, "bold"))
        estilo.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))

        cab = tk.Frame(self, bg=COLOR_PRIMARIO)
        cab.pack(fill="x")
        tk.Label(cab, text="SmartOptimizer S.A.C.", bg=COLOR_PRIMARIO, fg="white",
                 font=FUENTE_TITULO).pack(side="left", padx=14, pady=8)
        tk.Label(cab, text="Sistema de optimización · Programación Dinámica · Grupo 7 UPN",
                 bg=COLOR_PRIMARIO, fg="#cfe0f3", font=FUENTE).pack(side="left", pady=8)

        self.nb = ttk.Notebook(self)
        self.nb.pack(fill="both", expand=True, padx=10, pady=10)
        self.modulos = [ModuloRutas(self.nb), ModuloTecnicos(self.nb), ModuloProyectos(self.nb)]
        for m, nombre in zip(self.modulos, ["1. Rutas de desplazamiento", "2. Ingreso de técnicos",
                                            "3. Selección de proyectos"]):
            self.nb.add(m, text=f"  {nombre}  ")
        # al cambiar de pestaña se recalcula para que los gráficos tomen el ancho real
        self.nb.bind("<<NotebookTabChanged>>", lambda e: self.modulos[self.nb.index("current")].resolver())


def guardar_capturas(app, carpeta):
    """Muestra cada módulo y guarda una imagen de la ventana (evidencia de ejecución)."""
    from PIL import ImageGrab
    os.makedirs(carpeta, exist_ok=True)
    nombres = ["modulo1_rutas.png", "modulo2_tecnicos.png", "modulo3_proyectos.png"]

    def tomar(i=0):
        if i == len(nombres):
            app.destroy()
            return
        app.nb.select(i)
        app.update()

        def grab():
            app.lift()
            app.attributes("-topmost", True)
            app.update()
            x, y = app.winfo_rootx(), app.winfo_rooty()
            w, h = app.winfo_width(), app.winfo_height()
            ImageGrab.grab(bbox=(x, y, x + w, y + h)).save(os.path.join(carpeta, nombres[i]))
            print("captura:", nombres[i])
            tomar(i + 1)
        app.after(900, grab)

    app.after(800, tomar)


if __name__ == "__main__":
    if sys.platform == "win32":
        try:  # coordenadas reales en pantallas con escala (125 %, 150 %)
            import ctypes
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass
    app = App()
    if "--capturas" in sys.argv:
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        guardar_capturas(app, os.path.join(base, "capturas"))
    app.mainloop()
