# Workflow: Diseñar y renderizar una zona

## Objetivo
Para **una zona**:
1. Proponer 2–3 conceptos de diseño.
2. Dejar que el usuario elija uno.
3. Producir imágenes antes/después fotorrealistas donde los elementos fijos quedan idénticos a la foto original.

## Disparador
`outputs/brief_cliente.md` aprobado, y el usuario pide "diseña la zona X" o "renderiza la zona X".

## Inputs requeridos
| Input | Fuente | Formato |
|---|---|---|
| Brief del cliente aprobado | `outputs/brief_cliente.md` | Markdown |
| Análisis de sitio | `outputs/analisis_sitio.md` | Markdown |
| Fotos de la zona | `.tmp/fotos/` (de `ingest_photos.py`) | PNG/JPG |
| Reglas de diseño y lentes de estilo | `reports/Garden design and AI image models.md` | Markdown |
| Plantilla de prompt | `inputs/reference/rules/plantilla_prompt.md` | Markdown |
| Reglas de seguridad | `inputs/reference/rules/seguridad.md` | Markdown |

## Pipeline
```
[Brief] → (Agente: 2–3 conceptos) → [Humano: elige] → (Agente: ficha de diseño canónica)
→ (Agente: prompt por foto, plantilla v2) → render_redesign.py → make_keep_mask.py + composite --measure-only
→ [si corrimiento ≤2%: composite_keep_regions.py] → (Agente: QA visual) → make_before_after.py → [Humano: aprueba]
```

## Pasos
1. **Conceptos.** Agente.
   - Escribe 2–3 opciones en `outputs/conceptos/<zona>.md`. Cada una lleva: lente de estilo (adaptada al trópico), distribución (qué va dónde y medidas estimadas), paleta de 4–8 plantas con nombre común y científico aptas para San Salvador, materiales, muebles y guardado, y cómo resuelve las necesidades del brief.
   - Pasa el checklist de 18 errores del reporte y `seguridad.md`.
2. **Elección.** Humano. Espera la elección explícita, o la mezcla que pida el usuario.
3. **Ficha de diseño canónica.** Agente.
   - Escribe `outputs/conceptos/<zona>_ficha.md`: un párrafo fijo que describe el diseño elegido (plantas, materiales, colores, época del año).
   - **Se reutiliza palabra por palabra** en cada prompt de esa zona, para que las fotos sean consistentes entre sí.
4. **Máscara de lo que no se toca** (para medir el corrimiento y, si es bajo, componer). Tool: `tools/make_keep_mask.py`, método `gemini-poly` (por defecto).
   - Corre: `python tools/make_keep_mask.py --photo .tmp/fotos/<foto> --keep "house,wall,avocado tree,sky,terrace floor" --output .tmp/masks/`.
   - Produce: `<foto>_keep.png` (blanco = se conserva) y `<foto>_overlay.jpg` para revisar.
   - Deja una **franja de plantación** al pie de muros y casa, para que las plantas nuevas puedan tapar la base.
   - La primera vez, muestra el overlay al usuario.
   - Si falla: ver la sección de pendientes (métodos alternativos de máscara).
5. **Prompt por foto.** Agente.
   - Llena la plantilla con: la ficha canónica, la lista concreta de elementos fijos de **esa** foto, la cámara, el encuadre y la luz observada.
   - Guarda el texto en `.tmp/prompts/<foto>.txt`.
6. **Render.** Tool: `tools/render_redesign.py`. **Es pagado.**
   - Corre: `python tools/render_redesign.py --photo .tmp/fotos/<foto> --prompt .tmp/prompts/<foto>.txt --output .tmp/renders/ [--ref <render_aprobado>]`.
   - Primero un render. Si convence, sigue con las demás fotos y pasa el primer render aprobado como `--ref`.
   - Antes de más de ~10 renders seguidos, pregunta.
7. **Composite (opcional).** Tool: `tools/composite_keep_regions.py`.
   - Primero mide: `python tools/composite_keep_regions.py --original … --render … --mask … --output x --measure-only`.
   - Si `drift_pct` es **≤2%** y el diseño no pone nada sobre los muros fijos, compón.
   - Si no, **no compongas**: entrega el render tras el QA visual y anótalo en la leyenda de la comparativa. Componer con corrimiento genera dobles bordes y hace reaparecer cosas viejas.
   - Corre: `python tools/composite_keep_regions.py --original .tmp/fotos/<foto> --render .tmp/renders/<render> --mask .tmp/masks/<foto>_keep.png --output outputs/renders/<zona>/`.
8. **QA visual.** Agente. Compara el original con el resultado:
   - ¿Cambió algo fijo?
   - ¿Hay costuras visibles?
   - ¿La luz coincide?
   - ¿Las plantas son realistas y las de la paleta?
   - ¿Es seguro para los niños?

   Si falla: ajusta el prompt (o la máscara) y **vuelve a partir de la foto original**, nunca de la edición. Haz como máximo 3 intentos por foto y luego consulta.
9. **Comparativa.** Tool: `tools/make_before_after.py`.
   - Corre: `python tools/make_before_after.py --pairs outputs/renders/<zona>/pairs.json --output outputs/renders/<zona>/comparar.html`.
10. **Aprobación.** Humano. Muestra la comparativa y espera aprobación o ajustes.

## Output
- **Qué:** `outputs/conceptos/<zona>.md`, `<zona>_ficha.md`, y en `outputs/renders/<zona>/` los renders compuestos y `comparar.html`.
- **Listo cuando:** se cumple la definición de "listo" de `CLAUDE.md`.

## Casos borde
| Caso | Qué hacer |
|---|---|
| El modelo cambia la geometría y se notan costuras | Más suavizado en el composite; si sigue, usa el respaldo con máscara (pregunta antes) |
| El modelo devuelve otra proporción o resolución | El composite la redimensiona al tamaño original; fija la proporción en la llamada |
| Tinte rosado o magenta en 2K/4K | Activa el ajuste de color en LAB dentro de la zona fija (`--color-match`) |
| Plantas tropicales genéricas o inventadas | Nombra especies concretas con altura y color; pide "unretouched photograph" |
| Copa del aguacate o malla con bordes irregulares en la máscara | Dilata o suaviza la máscara; acepta un borde blando en la copa |
| Inconsistencia entre fotos | Misma ficha canónica + primer render aprobado como referencia (máx. 1–3 referencias) |

## Pendientes
- RESUELTO 2026-11-16: método de máscara `gemini-poly` (polígonos con `gemini-3.5-flash`). El formato de máscara nativo devolvió datos inválidos. Opciones originales:
  - (a) SAM 3 local con `transformers` (CPU, lento pero gratis; requiere descargar el modelo de huggingface.co);
  - (b) segmentación con Gemini, con la misma key (por verificar);
  - (c) máscara dibujada a mano.

  Probar (a) o (b) y caer en (c).
- RESUELTO: `gemini-nano-banana-2.1`.

## Registro de aprendizajes
- 2026-11-16: Gemini acepta solo estas proporciones: 1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9 y 21:9. Las panorámicas (p. ej. la 01, 3.3:1) quedan 29% fuera y el render saldría estirado: recortarlas a 21:9 o 16:9 antes de renderizar. La foto 06 es exactamente 3:4, ideal para la primera prueba.
- 2026-11-16: la clave llega por el proxy (Network secret, header `x-goog-api-key`); el script manda un valor de relleno y el proxy lo reemplaza.
- 2026-11-16 (primer slice, foto 06, concepto A):
  - **v1** (prompt con el diseño primero) alejó la cámara, inventó una ventana en arco, cerró el césped con un seto en primer plano y quitó las guirnaldas. **v2** (prompt que empieza con "Edit this exact photo without moving the camera…", el contorno del césped explícito y "nothing added in the foreground") salió bien: diseño correcto y luces respetadas, aunque con un corrimiento de cámara de ~9% (escala 0.91, desplazamiento ~36 px). **Regla: el bloqueo de encuadre va primero en el prompt.**
  - **Segmentación:** con 13 etiquetas en `gemini-3.8-flash` la petición tardó más de 5 min y el proxy la cortó (502). Con 4 etiquetas en `gemini-3.5-flash-lite` tardó 2 s, pero devolvió cajas en lugar de siluetas, demasiado burdas. `gemini-2.5-flash` ya no está disponible.
  - **Composite:** con un corrimiento de cámara de ~9%, pegar los píxeles originales produce dobles bordes (celosía y luces duplicadas, una flor flotante), así que en esa vista se entregó el render sin composición. Antes de componer, medir el corrimiento; si pasa de ~2%, no componer o alinear primero. La alineación con transformación de similitud deja bordes vacíos abajo, así que falta resolverlo.
  - El ajuste de color con LAB de PIL saturaba los colores (los canales a/b se desbordan); se corrigió usando LAB de OpenCV.
  - Costo de la prueba: 2 renders a 2K más 3 llamadas de segmentación, unos $0.10–0.15.
- 2026-11-16 (refinamiento):
  - Las máscaras con polígonos (`gemini-poly`, ~10 s) siguen bien los muros, los árboles y la malla; quedan aproximadas en los bordes.
  - El corrimiento medido fue 9.3% en el v2 de 2.1, y Pro no lo mejoró. La alineación ECC tampoco sirve, porque el modelo redibuja los elementos fijos con deformaciones no rígidas, y además el diseño coloca cosas sobre los muros.
  - **Conclusión: la fidelidad viene del prompt v2, la medición y el QA visual; el composite pasa a ser opcional.**
  - `ingest_photos.py` ahora recorta cada foto a la proporción soportada más cercana. Renderiza siempre desde `.tmp/fotos/`.

- 2026-11-16 (terraza, foto 02, concepto C):
  - Con la plantilla v2 el corrimiento fue de solo **0.1%** en los dos intentos: el prompt que bloquea el encuadre funciona mejor cuando lo que se edita son objetos sobre el piso y no el terreno.
  - v1 puso el rincón de los nietos en el paso junto a la casa, quitó plantas del borde del césped y dejó la vela de sombra sin anclaje. v2 lo corrigió con instrucciones explícitas: "on the lawn side of that seating group", "clear walkway about 1.2 m… with nothing in it", "all other potted plants stay" y el poste de la vela.
  - Se compuso **solo la casa y el alero** (máscara de 2 etiquetas): sin costuras. Lección: compón solo lo que el diseño no toca.
