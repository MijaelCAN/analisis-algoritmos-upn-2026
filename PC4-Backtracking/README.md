# PC4 · Backtracking con interfaz gráfica

- **Semana:** 4
- **Fecha límite:** domingo 08/11/2026, 23:59
- **Modalidad:** grupal (Grupo 7)
- **Enunciado:** [enunciado.pdf](enunciado.pdf)

Son cuatro problemas resueltos con backtracking, cada uno en su ventana de tkinter.

| # | Problema | Qué muestra |
|---|----------|-------------|
| 1 | Sudoku 6x6 / 9x9 | Animación paso a paso (valores probados y retrocesos), contador de retrocesos y tiempo total |
| 2 | N-Reinas (N entre 4 y 10) | Todas las soluciones con anterior/siguiente, árbol de decisiones, nodos explorados y podados |
| 3 | Laberinto (Rat in a Maze) | Laberinto editable con clics, búsqueda de **todos** los caminos, celdas visitadas y camino final en distinto color |
| 4 | Coloreado de grafos | Grafo editable (nodos y aristas con el mouse), elección de k y de la paleta, animación de asignaciones y retrocesos |

## Cómo ejecutar

Solo usa la librería estándar de Python (incluido tkinter).

```bash
python src/backtracking.py      # menú principal
python src/backtracking.py 1    # abre directamente el problema 1 (igual con 2, 3 o 4)
```

Controles comunes: **Pausar / Continuar**, **Terminar sin animación**, **Detener** y **Pausa entre pasos (ms)**. Con 0 ms va a la máxima velocidad.

## Cómo está organizado el código

Cada algoritmo es un **generador** de Python (`sudoku_pasos`, `n_reinas_arbol`, `laberinto_pasos`, `coloreo_pasos`). En cada decisión hace `yield` de un evento, por ejemplo probar un valor o retroceder. La clase `Animador` consume esos eventos con `after()` de tkinter, así la ventana no se congela durante la búsqueda.

## Resultados obtenidos

| Problema | Resultado |
|---|---|
| Sudoku 9x9 clásico (30 pistas) | 4157 retrocesos, unos 20 ms sin animación |
| Sudoku 9x9 variante (29 pistas) | 2674 retrocesos, unos 14 ms sin animación |
| Sudoku 6x6 | 1 retroceso |
| N-Reinas N=4 / 6 / 8 / 10 | 2 / 4 / 92 / 724 soluciones; 60 / 894 / 15 720 / 348 150 nodos explorados |
| N-Reinas N=8 | 13 664 de 15 720 nodos podados (87 %) |
| Laberinto de ejemplo 7x7 | 17 caminos (12 a 28 movimientos); 290 nodos explorados sin poda y 153 con poda |
| Grafo de Petersen | Se puede colorear con k = 3 y no con k = 2; número cromático = 3 |

## Entrega
- [x] Código comentado en `src/`
- [ ] Capturas de ejecución en `capturas/`
- [ ] Análisis de resultados en el informe
- [ ] Informe PDF (integrantes en la primera hoja) en `informe/`
- [ ] Subido a Blackboard
