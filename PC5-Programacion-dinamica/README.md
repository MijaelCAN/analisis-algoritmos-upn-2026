# PC5 · Programación dinámica

- **Semana:** 5
- **Fecha límite:** 15/11/2026
- **Tema:** Caso SmartOptimizer S.A.C.: rutas de costo mínimo, formas de llegar a un nivel y selección de proyectos no consecutivos (app tkinter)
- **Modalidad:** grupal (Grupo 7)

## Enunciado
Una sola app **tkinter** con módulos seleccionables (caso SmartOptimizer S.A.C.):

1. **Rutas de desplazamiento:** costo mínimo para ir de la posición 0 a la 10 avanzando 1, 2 o 3 posiciones (S/10, S/18 y S/25).
2. **Ingreso de técnicos:** número de formas de llegar al nivel 8 avanzando 1, 2 o 3 niveles. Mostrar resultados parciales y la relación de recurrencia.
3. **Selección de proyectos:** maximizar el beneficio sin elegir dos proyectos consecutivos. P1..P8 = 4000, 2500, 5000, 3500, 6000, 4500, 7000, 3000. Mostrar beneficio máximo, proyectos elegidos y descartados, tabla DP y estrategia.

## Cómo ejecutar
```bash
python src/smartoptimizer_app.py              # app con las 3 pestañas
python src/smartoptimizer_app.py --capturas   # regenera las capturas en capturas/
python src/dp_logica.py                       # solo la lógica, por consola
```

## Resultados y análisis
| Casuística | Recurrencia | Resultado | Complejidad |
|---|---|---|---|
| 1. Rutas (0 → 10, pasos 1/2/3 a S/10/18/25) | `dp[i] = min(dp[i-1]+10, dp[i-2]+18, dp[i-3]+25)` | **S/ 85**, ruta 0→3→6→9→10 | O(n·k) |
| 2. Técnicos (nivel 8, saltos 1/2/3) | `f(n) = f(n-1)+f(n-2)+f(n-3)`, `f(0)=1` | **81 formas** | O(n) |
| 3. Proyectos sin consecutivos | `dp[i] = max(dp[i-1], dp[i-2]+b[i])` | **S/ 22 000** con P1, P3, P5, P7 | O(n) |

## Entrega
- [x] Código comentado en `src/`
- [x] Capturas de ejecución en `capturas/`
- [x] Análisis de resultados
- [x] Informe PDF (integrantes en la primera hoja) en `informe/PC5_Semana5_Grupo7.pdf`
- [ ] Subido a Blackboard
