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
→ make_keep_mask.py → [Humano: aprueba la máscara, solo la 1ª vez por foto] → (Agente: prompt por foto)
→ render_redesign.py → composite_keep_regions.py → (Agente: QA visual) → make_before_after.py → [Humano: aprueba]
```

## Pasos
1. **Conceptos.** Agente.
   - Escribe 2–3 opciones en `outputs/conceptos/<zona>.md`. Cada una lleva: lente de estilo (adaptada al trópico), distribución (qué va dónde y medidas estimadas), paleta de 4–8 plantas con nombre común y científico aptas para San Salvador, materiales, muebles y guardado, y cómo resuelve las necesidades del brief.
   - Pasa el checklist de 18 errores del reporte y `seguridad.md`.
2. **Elección.** Humano. Espera la elección explícita, o la mezcla que pida el usuario.
3. **Ficha de diseño canónica.** Agente.
   - Escribe `outputs/conceptos/<zona>_ficha.md`: un párrafo fijo que describe el diseño elegido (plantas, materiales, colores, época del año).
   - **Se reutiliza palabra por palabra** en cada prompt de esa zona, para que las fotos sean consistentes entre sí.
4. **Máscara de lo que no se toca.** Tool: `tools/make_keep_mask.py`.
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
7. **Composite.** Tool: `tools/composite_keep_regions.py`.
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
- `OPEN:` método de máscara. Opciones:
  - (a) SAM 3 local con `transformers` (CPU, lento pero gratis; requiere descargar el modelo de huggingface.co);
  - (b) segmentación con Gemini, con la misma key (por verificar);
  - (c) máscara dibujada a mano.

  Probar (a) o (b) y caer en (c).
- `OPEN:` ID exacto del modelo de imagen vigente; confirmarlo en AI Studio y ponerlo en `GEMINI_IMAGE_MODEL`.

## Registro de aprendizajes
- (vacío)
