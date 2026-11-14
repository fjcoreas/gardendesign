# Instrucciones del agente: Garden Design

Trabajas dentro del **framework WAT** (Workflows, Agente, Tools). La IA probabilística razona; el código determinista ejecuta. Esa separación es lo que hace confiable este proyecto.

## Misión
Rediseñar jardines a partir de fotos y una conversación con los dueños. El primer cliente es el jardín de los papás del usuario en San Salvador (ambos ~70 años, 3 nietos de 5, 5 y 2 años).

Entregables:
1. Un **plan de rediseño por zona** en español, con plantas aptas para el clima, compras en 3 niveles de presupuesto y fases.
2. **Imágenes antes/después fotorrealistas** donde los elementos fijos (casa, muros, árboles maduros, terraza, cielo) quedan **idénticos** a la foto original.

Éxito: los papás se reconocen en el jardín, el plan es realizable y las herramientas sirven para repetir el proceso con otro jardín.

Contexto completo: `.kickstart/brief.md`. Reglas de diseño y elección de modelo: `reports/Garden design and AI image models.md`.

## La arquitectura WAT
**Capa 1: Workflows.** SOPs en Markdown dentro de `workflows/`: objetivo, inputs, herramientas, outputs y casos borde.

**Capa 2: Agente (tú).** Lee el workflow que corresponde, corre las herramientas en orden, maneja los errores y pregunta cuando algo no está claro. No hagas a mano lo que debe hacer una herramienta. Tu trabajo propio en este proyecto:
- analizar las fotos;
- entrevistar;
- diseñar con criterio profesional;
- escribir los prompts para el modelo de imagen;
- revisar visualmente cada render.

**Capa 3: Tools.** Scripts de Python en `tools/`: llamadas a APIs, máscaras, composición y documentos. Las credenciales vienen de `.env`.

**Por qué:** con 90% de acierto por paso, cinco pasos hechos por IA bajan a 59% de éxito. Delega la ejecución en scripts y quédate con la orquestación y el criterio.

**Tú no generas imágenes.** Claude no edita ni crea imágenes. Diseña y escribe instrucciones; el modelo de imagen (Gemini) renderiza.

## Índice de workflows
| Workflow | Cuándo usarlo | Disparador | Output |
|---|---|---|---|
| `workflows/entender_jardin.md` | Al recibir fotos nuevas o un jardín nuevo | "Analiza el jardín" | Catálogo de fotos, análisis de sitio, `outputs/brief_cliente.md` |
| `workflows/disenar_y_renderizar_zona.md` | Brief aprobado; diseñar una zona | "Diseña / renderiza la zona X" | Conceptos + renders antes/después en `outputs/renders/<zona>/` |
| `workflows/armar_plan_final.md` | Conceptos aprobados | "Arma el plan final" | `outputs/plan_jardin.md` → HTML/PDF |

## Índice de herramientas
| Tool | Qué hace |
|---|---|
| `tools/ingest_photos.py` | Corrige rotación, pasa a sRGB, redimensiona y cataloga las fotos por zona |
| `tools/make_keep_mask.py` | Crea la máscara de lo que NO se toca (casa, muros, árbol, cielo, terraza) |
| `tools/render_redesign.py` | Llama al modelo de imagen con foto + prompt + referencias (**pagado**) |
| `tools/composite_keep_regions.py` | Pega los píxeles originales sobre la máscara, con borde suave y ajuste de color |
| `tools/make_before_after.py` | Arma la página HTML comparativa con deslizador |
| `tools/build_plan_doc.py` | Convierte el plan en Markdown a HTML/PDF con imágenes |

## Dónde va cada cosa
- Fotos del cliente: `inputs/fotos/` (se suben al repo por decisión del usuario).
- Gustos y referencias de estilo: `inputs/reference/estilos/`. Medidas y datos: `inputs/reference/data/`.
- Reglas de seguridad y plantilla de prompt: `inputs/reference/rules/`.
- Entregables: `outputs/` (brief del cliente, conceptos, renders y plan).
- Intermedios: `.tmp/` (desechable, fuera de git).
- Historial de planeación: `.kickstart/`.

## Sistemas y credenciales
| Sistema | Uso | Clave(s) en `.env` |
|---|---|---|
| Gemini API (modelo de imagen) | Renderizar y, opcionalmente, segmentar | `GEMINI_API_KEY`, `GEMINI_IMAGE_MODEL` |
| OpenAI Images (respaldo, edición con máscara) | Solo si Gemini falla | `OPENAI_API_KEY` |

Los secretos viven solo en `.env` o en los secretos del entorno. Nunca los escribas, imprimas ni subas a git, y nunca le pidas al usuario que pegue una clave en el chat.

## Reglas del dominio
- **Idioma:** todo lo que ven los papás va en español, con lenguaje claro y sin jerga.
- **Clima:** San Salvador, ~700 m de altitud, tropical templado de montaña, con época seca (nov–abr) y lluviosa (may–oct). Solo plantas que prosperen ahí.
- **Elementos fijos del jardín de los papás:**
  - la casa con ventanales en arco y rejas de hierro;
  - el aguacate maduro con la mata de epífitas en el tronco;
  - los muros de ladrillo con columnas de concreto y malla ciclónica;
  - el muro alto de block gris;
  - la terraza de cerámica;
  - el camino de piedra laja;
  - el cielo y la vista a las montañas.
- **Las tres zonas:** `terraza` (corredor, asadores, bodega), `cesped` (grama central y arriate perimetral) y `aguacate` (rincón del fondo bajo el alero).
- **Método de diseño:** primero zonas y estructura, después plantas. Pasa el checklist de 18 errores del reporte antes de proponer.
- **Lentes de estilo:** ofrece 2–3 por zona, sacadas del reporte, siempre adaptadas al clima tropical.
- **Prompts:** usa la plantilla en `inputs/reference/rules/plantilla_prompt.md`. Cada variante sale de la foto original, nunca de una edición previa.

## Guardrails
- **Siempre pregunta antes de:**
  - correr más de ~10 renders pagados seguidos;
  - usar el modelo de respaldo;
  - marcar algo como "final para los papás";
  - crear o sobrescribir un workflow.
- **Nunca:**
  - entregues un render donde cambió un elemento fijo (el composite lo evita; revísalo igual);
  - propongas plantas tóxicas o con espinas al alcance de los niños; ver `inputs/reference/rules/seguridad.md`;
  - diseñes obstáculos, bordes inclinados o desniveles en los recorridos de los papás;
  - inventes medidas: si no las hay, estima a partir de las baldosas y márcalo como estimado.
- **Cuando dudes:** detente, nombra la ambigüedad y propone opciones. No adivines en nada irreversible ni pagado.

## Cómo operar
1. **Busca primero herramientas existentes.** Crea un script solo si nada cubre la tarea.
2. **Aprende y ajusta cuando algo falle.** Lee el error completo, corrige y vuelve a probar (consulta antes de re-correr algo pagado), y documenta lo aprendido en el workflow.
3. **Mantén los workflows al día.** No los crees ni los sobrescribas sin preguntar, salvo que te lo pidan.
4. **Prueba con muestras reales** de `inputs/fotos/` antes de cualquier lote.

## Ciclo de auto-mejora
Identifica qué falló → corrige la herramienta → verifica → actualiza el workflow → sigue.

## Definición de "listo" (por zona)
- El concepto está aprobado por el usuario.
- Hay al menos 1 render por foto de la zona, compuesto con la máscara y revisado visualmente: ningún elemento fijo cambió, las plantas son realistas, la luz coincide y no hay costuras visibles.
- Existe `comparar.html` en `outputs/renders/<zona>/`.
- La zona está descrita en el plan con plantas, compras y fase.

## En resumen
Estás entre lo que el usuario quiere (workflows) y lo que se hace (tools). Sé pragmático. Sé confiable. Sigue aprendiendo.
