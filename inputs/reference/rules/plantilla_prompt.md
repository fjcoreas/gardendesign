# Plantilla de prompt para el modelo de imagen (Gemini)

Fuente: sección "Gemini prompts should read like a designer's brief" del reporte. **No probada aún**: actualízala con lo que funcione, en el registro de aprendizajes de `workflows/disenar_y_renderizar_zona.md`.

El prompt va **en inglés**: los modelos de imagen siguen mejor las instrucciones en inglés. Lo que ven los papás va en español.

## Reglas
- **Oraciones completas**, no listas de palabras clave. Empieza con un verbo fuerte.
- **Una idea clara** pesa más que muchos detalles: Gemini sigue la instrucción más concreta, no la más larga.
- **Nombra cada elemento fijo** de forma que se pueda identificar ("the cream stucco house with black wrought-iron arched windows on the right").
- **Cámara, encuadre, perspectiva y proporción idénticos.** Además, fija la proporción en la llamada a la API.
- **Describe la luz observada** en la foto: hora, dirección y si está nublado o soleado.
- **Especies reales** con altura y color, aptas para San Salvador, "as established for about two years".
- **Pide una fotografía sin retocar**, no un render 3D.
- **Una variante = una llamada desde la foto original.** Haz como máximo 1–3 ajustes pequeños; si el cambio es grande, vuelve al original.
- **Referencias:** foto original + máximo 1–3 referencias, y explica el papel de cada una.

## Plantilla
```
Using this photo of a residential back garden in San Salvador, El Salvador, redesign only {EDITABLE_AREAS} as {STYLE_LENS}.

{DESIGN_SPEC_CANONICAL}

The following stay exactly as they are in the original photo, unchanged in shape, colour, texture and position: {FIXED_ELEMENTS_LIST}, the sky and the mountain view. Keep the identical camera position, lens, framing, perspective and {ASPECT_RATIO} aspect ratio. Match the original lighting: {LIGHTING_DESCRIPTION}, with shadows falling the same way.

The result looks like an unretouched photograph of the same garden about two years after the redesign, with plants at realistic sizes, not a 3D render or illustration.
```

### Con referencia (segunda foto en adelante)
Añade al inicio:
```
Image 1 is the photo to edit. Image 2 shows the approved redesign of the same garden from another angle; use the same plants, materials, colours and style, adapted to this viewpoint.
```

## Ejemplo de relleno (zona césped, foto 01): borrador
- **{EDITABLE_AREAS}:** "the lawn, the narrow planting bed along the brick wall and the loose pots and stands on the lawn"
- **{FIXED_ELEMENTS_LIST}:** "the long red-brick wall with cream concrete pillars and cap, the chain-link fence and hedge on top of it, the tall grey concrete-block wall with the white lattice panel on the left, the cream house corner with the black arched window grille, the overhead string lights"
- **{LIGHTING_DESCRIPTION}:** "soft overcast daylight, late morning"
