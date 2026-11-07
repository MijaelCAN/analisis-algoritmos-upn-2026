# Análisis de Algoritmos y Estrategias de Programación · UPN 2026

Repositorio del **Grupo 7** para el curso **Análisis de Algoritmos y Estrategias de Programación** (COMP1303A), Ingeniería de Sistemas Computacionales, Universidad Privada del Norte, periodo 2026-5.

Aquí se guarda el código, las evidencias y los informes de cada práctica de campo (PC1 a PC8), de las evaluaciones T1 y T2 y del proyecto final (EF). Todo está en **Python**. Las interfaces gráficas usan tkinter salvo que una entrega diga otra cosa.

## Entregas

| Entrega | Semana · fecha límite | Tema | Estado |
|---|---|---|---|
| [PC1](PC1-Fuerza-bruta/) | Sem 1 · 18/10/2026 | Fuerza bruta + Cisco Python Essentials 1 | ⛔ No entregada |
| [PC2](PC2-Complejidad-busqueda-ordenamiento/) | Sem 2 · 25/10/2026 | Complejidad, búsqueda y ordenamiento | ✅ Entregada |
| [PC3](PC3-Voraces-recursivos/) | Sem 3 · 01/11/2026 | Voraces, recursivos, divide y vencerás | ✅ Entregada (falta subir el código) |
| [PC4](PC4-Backtracking/) | Sem 4 · 08/11/2026 | Backtracking con interfaz gráfica | 🟡 Código listo, falta el informe |
| [PC5](PC5-Programacion-dinamica/) | Sem 5 · 15/11/2026 | Programación dinámica | ⏳ Pendiente |
| [PC6](PC6-Probabilistas-paralelos/) | Sem 6 · 22/11/2026* | Algoritmos probabilistas y paralelos | ⏳ Pendiente |
| [PC7](PC7-Grafos-paralelo/) | Sem 7 · 29/11/2026* | Grafos y evaluación de expresiones en paralelo | ⏳ Pendiente |
| [PC8](PC8-Ordenacion-distribuidos/) | Sem 8 · 06/12/2026* | Redes de ordenación y algoritmos distribuidos | ⏳ Pendiente |
| [T1](T1/) **30%** | Sem 5 | Desarrollo de casos | ⏳ Pendiente |
| [T2](T2/) **30%** | Sem 7 | Evaluación de práctica de campo | ⏳ Pendiente |
| [EF](EF-Proyecto-final/) **40%** | Sem 8 | Proyecto final: presentación y sustentación | ⏳ Pendiente |

\* Fecha estimada. Confirmar cuando se publique la actividad en Blackboard.

## Estructura de cada carpeta

```
PCx-Tema/
├── README.md     enunciado resumido, cómo ejecutar, integrantes, resultados
├── enunciado.pdf indicaciones del docente
├── src/          código fuente
├── capturas/     evidencias de ejecución (PNG)
└── informe/      PDF entregado en Blackboard
```

Cada informe es **un solo PDF**. La primera hoja lleva los integrantes del grupo. Después van el código comentado, las capturas de ejecución y el análisis de resultados.

## Cómo ejecutar

```bash
git clone <url-del-repositorio>
cd analisis-algoritmos-upn-2026
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
python PC4-Backtracking/src/backtracking.py
```

Requiere Python 3.10 o superior.

## Forma de trabajo

1. Antes de empezar: `git pull`.
2. Una rama por entrega: `git checkout -b pc5`.
3. Commits cortos y descriptivos, por ejemplo `PC5: tabla DP de selección de proyectos`.
4. Cuando la entrega está lista, se une a `main` (pull request o merge).
5. Después de subir el PDF a Blackboard, se guarda también en `informe/` y se actualiza el estado en esta tabla.

## Integrantes (Grupo 7)

| Integrante | GitHub |
|---|---|
| Mijael Cano | [@MijaelCAN](https://github.com/MijaelCAN) |
| Nayda | [@qoriankaq20](https://github.com/qoriankaq20) |
| _por completar_ | |

Docente: Herber De La Cruz Pampañaupa.
