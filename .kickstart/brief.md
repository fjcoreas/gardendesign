# Project Brief: Garden Design (Jardín de mis papás)
*Status:* Approved (con correcciones) · *Updated:* 2026-11-14 · *Owner:* el usuario (hijo), para sus papás
Marcadores: `ASSUMPTION:` = suposición por confirmar · `OPEN:` = pendiente.

## 1. Resumen
- **Problema:** el patio trasero de los papás (ambos ~70 años, San Salvador) se siente amontonado. Las plantas de la mamá están dispersas sobre mesas plegables, muebles de hierro y estructuras en medio del césped. Hay espacios desperdiciados y riesgos de tropiezo.
- **Para quién / quién lo usa:**
  - Clientes: los papás.
  - Operador: el usuario, con Claude.
  - Usuarios del jardín: los papás y 3 nietos (5, 5 y 2 años).
- **Tipo de proyecto:** producción de contenido (plan de diseño + imágenes antes/después), con investigación previa ya hecha (`reports/Garden design and AI image models.md`).
- **Éxito se ve así:**
  - Al final del fin de semana hay un plan por zona, con lista de plantas y de compras en 3 niveles de presupuesto.
  - Hay 3–4 imágenes antes/después por zona, fotorrealistas, donde la casa, los muros, el aguacate, la terraza y el camino de laja quedan **idénticos** a la foto original.
  - Los papás se reconocen en el jardín y les entusiasma.
  - Las herramientas quedan listas para repetir el proceso con otro jardín.
- **Fuera de alcance:**
  - demolición u obra estructural;
  - planos de construcción a escala;
  - app web o móvil;
  - un servicio para terceros (posible fase futura).

## 2. Proceso actual
No existe un proceso. Hoy sería: el usuario sube una foto a la app de Gemini y le pide un rediseño con un prompt corto.

| # | Quién | Hace qué | Usando | Produce | Problema |
|---|---|---|---|---|---|
| 1 | Usuario | Toma fotos y videos del jardín | Celular | Fotos | Sin estándar de ángulos |
| 2 | Usuario | Pide un rediseño | App de Gemini | Imagen editada | Cambia partes fijas, baja resolución, prompts vagos |
| 3 | — | No hay un plan escrito ni una lista de plantas | — | — | Imágenes bonitas pero no realizables |

## 3. Inputs
| Input | Fuente | Formato | Consistencia | ¿Sensible? |
|---|---|---|---|---|
| Fotos del jardín (6 por ahora) | Usuario, celular | JPG, máx. 2000 px (copias del chat) | Panorámicas y verticales mezcladas | Fotos privadas de la casa; el usuario aceptó subirlas al repo |
| Respuestas de la entrevista | Usuario / mamá | Texto en el chat | — | No |
| Reglas de diseño | `reports/` + `research_notes/` | Markdown | — | No |
| Medidas del patio | Usuario | Texto | — | `OPEN:` pendiente; se estimarán con las fotos mientras tanto |

## 4. Outputs
| Output | Audiencia | Destino | Formato | ¿Revisión humana? |
|---|---|---|---|---|
| Brief del cliente (necesidades, restricciones, estilo) | Usuario | `outputs/brief_cliente.md` | Markdown, en español | Sí, la aprueba el usuario |
| Concepto por zona (2–3 opciones de estilo) | Usuario → papás | `outputs/conceptos/` | Markdown | Sí, se elige una opción |
| Imágenes antes/después | Papás | `outputs/renders/<zona>/` | PNG + página HTML comparativa | Sí; Claude las revisa y luego el usuario |
| Plan de rediseño | Papás | `outputs/plan_jardin.md` → HTML/PDF | Documento en español: zonas, plantas, compras en 3 niveles y fases | Sí |

## 5. Sistemas y acceso
| Sistema | Uso | Acceso | Dueño de la credencial | Estado |
|---|---|---|---|---|
| Gemini API (Nano Banana 2.1 y, si hace falta, Pro) | Editar fotos y, opcionalmente, segmentar | API key de AI Studio | Usuario | `OPEN:` el usuario la va a crear; requiere facturación |
| OpenAI Images API (respaldo) | Edición con máscara | API key | Usuario | Opcional; solo si Gemini falla |
| Red de la sesión | Llamadas a la API | Permitir `generativelanguage.googleapis.com` | Usuario (aprobación) | `OPEN:` se pedirá al construir |
| GitHub `fjcoreas/gardendesign` | Guardar proyecto, fotos y outputs | Ya conectado | Usuario | OK |

## 6. Volumen, frecuencia y disparador
- **Disparador:** a petición ("diseña el jardín", "renderiza la zona X").
- **Volumen:** 1 jardín, 3 zonas, ~6–10 fotos, ~30–60 renders en total contando iteraciones. Costo estimado: $5–20.
- **Tiempo:** un fin de semana.

## 7. Diseño objetivo
### Workflows
| Workflow | Disparador | Output | Prioridad |
|---|---|---|---|
| `entender_jardin` | Llegan fotos nuevas | Catálogo de fotos por zona + análisis de sitio + brief del cliente | 1 |
| `disenar_y_renderizar_zona` | Brief aprobado | Concepto + renders antes/después de una zona | 1 |
| `armar_plan_final` | Conceptos aprobados | Plan de rediseño completo (doc + imágenes) | 2 |

### Pipeline por workflow
```
entender_jardin:
[Fotos en inputs/fotos/] → ingest_photos.py → (Agente: análisis de sitio por zona, qué se queda / qué se mueve)
→ [Humano: entrevista con preguntas del reporte] → (Agente: escribe brief del cliente) → [Humano: aprueba brief]

disenar_y_renderizar_zona:
[Brief aprobado] → (Agente: 2–3 conceptos con "lentes de estilo" + checklist de 18 errores + seguridad niños/mayores)
→ [Humano: elige concepto] → make_keep_mask.py → (Agente: escribe prompt con plantilla)
→ render_redesign.py → composite_keep_regions.py → (Agente: QA visual: ¿cambió algo fijo? ¿plantas realistas?)
→ make_before_after.py → [Humano: aprueba o pide ajuste]

armar_plan_final:
[Conceptos + renders aprobados] → (Agente: plan por zona, lista de plantas aptas para San Salvador, compras en 3 niveles, fases)
→ build_plan_doc.py → [Humano: revisión final] → [Output: outputs/plan_jardin.html/pdf]
```

### Clasificación de pasos
| Workflow | Paso | Tipo | Herramienta | Notas |
|---|---|---|---|---|
| entender | Normalizar fotos (EXIF, tamaño, nombres, zona) | Tool | `ingest_photos.py` | Determinista |
| entender | Análisis de sitio desde fotos | Agente | — | Claude ve las fotos; usa el método del reporte |
| entender | Entrevista | Humano + Agente | — | Script de 34 preguntas, recortado a lo que falte |
| diseñar | Conceptos por zona | Agente | — | Lentes de estilo + reglas + clima local |
| diseñar | Máscara de "lo que no se toca" | Tool | `make_keep_mask.py` | Ver `OPEN` sobre el método |
| diseñar | Escribir prompt | Agente | — | Plantilla en `workflows/` |
| diseñar | Renderizar | Tool | `render_redesign.py` | Pagado: preguntar antes de lotes grandes |
| diseñar | Pegar de vuelta las zonas fijas | Tool | `composite_keep_regions.py` | Determinista |
| diseñar | QA visual | Agente | — | Comparar con el original |
| diseñar | Comparativa antes/después | Tool | `make_before_after.py` | HTML con deslizador |
| plan | Redactar el plan | Agente | — | Español, para los papás |
| plan | Generar el documento | Tool | `build_plan_doc.py` | Markdown → HTML/PDF |

### Herramientas
| Tool | Hace | Inputs | Outputs | Usado por |
|---|---|---|---|---|
| `ingest_photos.py` | Corrige rotación, redimensiona, cataloga por zona | `inputs/fotos/` | `.tmp/fotos/`, `.tmp/catalogo.json` | entender |
| `make_keep_mask.py` | Crea la máscara de elementos fijos (casa, muros, árbol, cielo, terraza) | foto + lista de elementos | `.tmp/masks/<foto>_keep.png` | diseñar |
| `render_redesign.py` | Llama a Gemini con foto + prompt + referencias | foto, prompt, refs | `.tmp/renders/` | diseñar |
| `composite_keep_regions.py` | Pega los píxeles originales sobre la máscara, con borde suave y ajuste de color | original, render, máscara | `outputs/renders/<zona>/` | diseñar |
| `make_before_after.py` | Arma la página comparativa | pares antes/después | `outputs/renders/<zona>/comparar.html` | diseñar, plan |
| `build_plan_doc.py` | Convierte el plan en HTML/PDF con imágenes | `outputs/plan_jardin.md` | `outputs/plan_jardin.html` / `.pdf` | plan |

## 8. Guardrails y riesgo
- **Siempre pedir aprobación antes de:**
  - lotes de más de ~10 renders pagados;
  - pasar al modelo de respaldo (otra cuenta/costo);
  - enviar algo a los papás como final.
- **Nunca:**
  - alterar la casa, los muros, el aguacate, la terraza o el camino de laja en el render final (el composite lo garantiza);
  - recomendar plantas que no sirvan en el clima de San Salvador;
  - poner plantas tóxicas o con espinas al alcance de los niños (sobre todo el de 2 años);
  - escribir la API key en archivos o en el chat.
- **Seguridad de los usuarios:**
  - Nietos de 5, 5 y 2 años: espacio abierto para correr y jugar con pelota; zona de juego sin bordes duros, sin rosales ni espinas cerca, sin plantas tóxicas a su altura. La rosa del desierto (Adenium) tiene savia tóxica; la cuna de Moisés (Spathiphyllum) es levemente tóxica.
  - Papás de 70: caminos firmes y sin obstáculos, sin bordillos de ladrillo inclinado, asientos con sombra cada pocos metros, mesas de trabajo a 70–90 cm, manguera en carrete.
- **Peor caso:** imágenes bonitas pero irreales o que "cambian la casa", y los papás pierden confianza. Mitigación: composite + QA visual + plan con plantas y medidas reales.
- **Datos:** fotos de la casa en un repo de GitHub, por decisión del usuario. `ASSUMPTION:` el repo es privado.

## 9. Casos borde
| Caso | Frecuencia | Manejo |
|---|---|---|
| Panorámicas con distorsión (lente gran angular) | Alta (4 de 6 fotos) | Renderizar sobre la panorámica y aceptar la curvatura; pedir fotos normales si falla |
| Fotos con baja resolución (copias del chat) | Alta | Pedir los originales del celular si el render pierde nitidez |
| El modelo cambia elementos fijos | Media | El composite lo corrige; si el borde se nota, ajustar la máscara |
| El modelo inventa plantas tropicales genéricas | Media | Nombrar las especies en el prompt; QA visual |
| Inconsistencia entre fotos de la misma zona | Media | Usar el primer render aprobado como referencia en los siguientes |

## 10. Primer slice
- **Meta:** **una** foto (`01_cesped_muro_panoramica.jpg` o `06_cesped_hacia_muro_block.jpg`) → **un** concepto → **un** render con las partes fijas protegidas → **una** comparativa antes/después.
- **Pasos incluidos:** concepto (agente) → máscara → prompt → render → composite → comparativa.
- **Queda manual:** la entrevista completa, el catálogo de fotos y el plan escrito.
- **Herramientas a construir, en orden:**
  1. `render_redesign.py`
  2. `make_keep_mask.py`
  3. `composite_keep_regions.py`
  4. `make_before_after.py`

## 11. Fases posteriores
- Las 3 zonas con 2–3 estilos cada una.
- Plan final con lista de compras.
- Más adelante, si funciona: convertirlo en un servicio para otras personas (formulario de fotos, entrevista guiada, entrega automática).

## 12. Suposiciones y pendientes
- `OPEN:` medidas del patio (mientras tanto, estimar por las baldosas de la terraza).
- `OPEN:` presupuesto en dinero; se usarán 3 niveles.
- `OPEN:` API key de Gemini con facturación activa.
- `OPEN:` método de máscara. Opciones:
  - (a) segmentación con Gemini usando la misma key (`ASSUMPTION:` la API devuelve máscaras; por verificar);
  - (b) SAM en un servicio hospedado (otra key);
  - (c) máscara dibujada a mano en el celular o en un editor.

  Recomendado: probar (a) y caer en (c) si falla.
- `OPEN:` fotos originales en resolución completa (las del chat vienen reducidas a 2000 px).
- `OPEN:` ¿qué orquídea/bromelia es la mata grande del tronco del aguacate? Útil para el plan.
- `OPEN:` ¿se quedan los asadores, la mesa larga plegable, las pesas y la banca mecedora? (`ASSUMPTION:` asadores y banca se quedan reubicados; la mesa plegable se quita del borde del césped).
- `ASSUMPTION:` el repo es privado.
