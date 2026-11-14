# Workflow: Entender el jardín

## Objetivo
Pasar de "fotos sueltas y una idea" a un **brief del cliente aprobado**: qué hay, qué se queda, qué molesta, qué quieren lograr y con qué restricciones.

## Disparador
Llegan fotos nuevas a `inputs/fotos/`, o el usuario pide "analiza el jardín".

## Inputs requeridos
| Input | Fuente | Formato |
|---|---|---|
| Fotos de cada zona (al menos una amplia por zona) | `inputs/fotos/` | JPG |
| Respuestas del usuario o de los dueños | Chat | Texto |
| Medidas, si las hay | `inputs/reference/data/medidas.md` | Texto |
| Gustos y referencias | `inputs/reference/estilos/` | Imágenes / texto |

## Pipeline
```
[Fotos] → ingest_photos.py → (Agente: análisis de sitio por zona) → [Humano: entrevista] → (Agente: brief) → [Humano: aprueba]
```

## Pasos
1. **Catalogar fotos.** Tool: `tools/ingest_photos.py`.
   - Corre: `python tools/ingest_photos.py --input inputs/fotos --output .tmp/catalogo.json`.
   - Produce: `.tmp/fotos/` (normalizadas) y `.tmp/catalogo.json`, con zona, tipo (panorámica/normal) y tamaño.
   - Si falla: revisa que las fotos sean JPG o PNG legibles.
2. **Asignar zona a cada foto.** Agente.
   - Mira cada foto y completa `zona` en el catálogo: `terraza`, `cesped`, `aguacate` o `varias`.
   - Si no está claro: pregunta al usuario.
3. **Análisis de sitio por zona.** Agente. Usa la sección "What photos reveal and what the homeowner must tell us" del reporte. Por zona, registra:
   - elementos fijos (no se tocan);
   - elementos movibles (macetas, muebles, estructuras);
   - problemas: desorden, tropiezos, espacio perdido, plantas en mal lugar;
   - oportunidades: vistas, sombra, muros para estanterías, ménsulas existentes;
   - luz y sombra aparentes;
   - riesgos para niños y mayores, como plantas tóxicas o espinas.

   Guarda el resultado en `outputs/analisis_sitio.md`.
4. **Entrevista.** Humano + agente.
   - Usa el guion de 34 preguntas del reporte (sección del primer encuentro) y pregunta **solo lo que no se sepa ya**: revisa `.kickstart/braindump.md` primero.
   - Haz rondas de 3–5 preguntas.
   - Siempre cubre: uso por persona, qué se queda y qué se va, gustos y colores, mantenimiento deseado, presupuesto o tope, y seguridad.
5. **Escribir el brief del cliente.** Agente.
   - Escribe `outputs/brief_cliente.md` en español, con estas secciones: objetivos, usuarios y sus necesidades, zonas (qué se queda, qué cambia), restricciones, estilo y gustos, presupuesto, seguridad, y pendientes.
   - Termina con un resumen de 5 líneas para leérselo a los dueños.
6. **Aprobación.** Humano.
   - Muestra el resumen y espera un "sí" explícito antes de pasar a diseñar.

## Output
- **Qué:** `outputs/analisis_sitio.md` + `outputs/brief_cliente.md`.
- **Listo cuando:** el usuario aprueba el brief.

## Casos borde
| Caso | Qué hacer |
|---|---|
| Foto panorámica muy deformada | Úsala para el análisis; pide una foto normal para renderizar |
| Falta una zona sin foto | Márcala `OPEN` y pide la foto; no la diseñes a ciegas |
| El usuario no sabe una respuesta | Propón un supuesto razonable, márcalo `ASSUMPTION` y sigue |
| Plantas que no reconoces | Descríbelas y pide una foto de detalle; no adivines la especie en el plan |

## Pendientes
- `OPEN:` medidas del patio, inventario de la colección, qué muebles se quedan y presupuesto (ver `.kickstart/materials-checklist.md`).

## Registro de aprendizajes
- 2026-11-14: las fotos que llegan por el chat vienen reducidas a máx. 2000 px; pedir originales si se necesita nitidez.
