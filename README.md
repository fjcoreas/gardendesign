# Garden Design

Rediseño de jardines a partir de fotos y una conversación. El primer proyecto es el jardín de mis papás en San Salvador.

**Qué produce:**
- un plan de rediseño por zona, en español, con plantas aptas para el clima, compras en 3 niveles de presupuesto y fases;
- imágenes **antes/después** fotorrealistas donde la casa, los muros y los árboles quedan idénticos a la foto original.

**Cómo funciona (framework WAT):**
- **Claude** diseña: analiza las fotos, entrevista, propone conceptos, escribe los prompts y revisa los resultados.
- **Gemini** renderiza las imágenes.
- **Scripts de Python** hacen el trabajo mecánico. El más importante pega de vuelta los píxeles originales de lo que no debe cambiar.

## Estructura
```
CLAUDE.md                 instrucciones para Claude
workflows/                procedimientos paso a paso (entender, diseñar/renderizar, plan final)
tools/                    scripts de Python (por ahora esqueletos)
inputs/fotos/             fotos del jardín
inputs/reference/         reglas de seguridad, plantilla de prompt, estilos, medidas
outputs/                  entregables: brief, conceptos, renders, plan
reports/                  investigación: diseño de jardines y modelos de imagen
research_notes/           notas de la investigación
.kickstart/               historial de planeación (brief, decisiones, checklist)
```

## Preparación
1. Python 3.10 o más reciente.
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Copia el archivo de ejemplo y llena `GEMINI_API_KEY` y `GEMINI_IMAGE_MODEL` (instrucciones dentro del archivo):
   ```bash
   cp .env.example .env
   ```
   En una sesión de Claude en la nube, la clave se guarda con el formulario seguro, no en `.env`.

## Cómo empezar
Abre Claude Code en esta carpeta y di:

> *Corre el workflow entender_jardin*

o, para el primer slice:

> *Implementa render_redesign.py y pruébalo con inputs/fotos/01_cesped_muro_panoramica.jpg*

Lo que falta para construir está en `.kickstart/materials-checklist.md`.
