# Workflow: Armar el plan final

## Objetivo
Un documento en español, bonito y realizable, para los dueños: qué se hace en cada zona, con qué plantas, qué hay que comprar en 3 niveles de presupuesto, en qué orden, y cómo se ve antes y después.

## Disparador
Conceptos de todas las zonas aprobados, con sus renders. El usuario pide "arma el plan final".

## Inputs requeridos
| Input | Fuente | Formato |
|---|---|---|
| Brief del cliente | `outputs/brief_cliente.md` | Markdown |
| Conceptos y fichas aprobadas | `outputs/conceptos/` | Markdown |
| Renders compuestos | `outputs/renders/<zona>/` | PNG |
| Medidas | `inputs/reference/data/medidas.md` | Texto |
| Seguridad | `inputs/reference/rules/seguridad.md` | Markdown |

## Pipeline
```
[Conceptos + renders aprobados] → (Agente: redacta el plan) → build_plan_doc.py → [Humano: revisión final] → [Output]
```

## Pasos
1. **Redactar el plan.** Agente. Escribe `outputs/plan_jardin.md` con esta estructura:
   1. Resumen en una página: la idea general y por qué.
   2. Por zona:
      - antes/después (imágenes);
      - qué cambia y por qué;
      - distribución con medidas (marcadas como estimadas si no hay medidas reales);
      - plantas (nombre común, nombre científico, cantidad, sol/sombra, cuidado, ¿segura para niños?);
      - qué se reubica de la colección actual.
   3. Lista de compras en tres niveles:
      - **Básico:** reorganizar y comprar lo mínimo.
      - **Medio:** estanterías, bordillo, mobiliario.
      - **Completo:** pérgola o toldo, zona de juego, iluminación, riego.

      Cada nivel con costo estimado en USD, marcado como estimado.
   4. Fases y orden de trabajo: primero seguridad y despeje, luego estructura, luego plantas. Incluye la mejor época, que es al inicio de la época lluviosa (mayo) para plantar.
   5. Mantenimiento: rutina semanal y mensual, pensada para una persona de 70 años.
   6. Seguridad: plantas que se reubicaron por toxicidad o espinas, y recorridos sin obstáculos.
2. **Revisión de criterio.** Agente.
   - Pasa el checklist de 18 errores y `seguridad.md` sobre el plan completo.
   - Verifica que cada planta sirva para el clima de San Salvador.
3. **Generar el documento.** Tool: `tools/build_plan_doc.py`.
   - Corre: `python tools/build_plan_doc.py --input outputs/plan_jardin.md --output outputs/plan_jardin.html [--pdf]`.
4. **Revisión final.** Humano. El usuario revisa antes de mostrárselo a los papás.

## Output
- **Qué:** `outputs/plan_jardin.md` y `outputs/plan_jardin.html` (y `.pdf` si se pide).
- **Listo cuando:** el usuario lo aprueba.

## Casos borde
| Caso | Qué hacer |
|---|---|
| Sin presupuesto definido | Los 3 niveles, con rangos; nunca un solo número |
| Precios locales desconocidos | Rangos marcados como estimados; sugerir cotizar en viveros y ferreterías locales |
| Una planta de la colección es tóxica (p. ej., rosa del desierto) | No eliminarla: reubicarla en alto o en zona sin acceso de niños, y explicar por qué |

## Pendientes
- `OPEN:` presupuesto y medidas reales.

## Registro de aprendizajes
- (vacío)
