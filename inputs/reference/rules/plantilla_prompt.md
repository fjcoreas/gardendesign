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

## Plantilla (v2: probada el 2026-11-16 con éxito en la foto 06)
El **bloqueo de encuadre va primero**. La versión 1, con el diseño primero, hizo que el modelo alejara la cámara, inventara una ventana y cerrara el césped.
```
Edit this exact photo without moving the camera: keep the identical framing, zoom, perspective and {ASPECT_RATIO} aspect ratio, so {FIXED_ELEMENTS_LIST} stay exactly where they are, unchanged in shape, colour and texture. {HOUSE_SENTENCE e.g. "The cream house wall and terracotta roof edge at the top left stay exactly as in the photo, with no new windows or doors."}

Change only {EDITABLE_AREAS}: {GROUND_PLAN_LOCK e.g. "the lawn keeps exactly its current outline and full width and still runs all the way to the bottom edge of the photo, with nothing added in the foreground and nothing standing on the grass"}.

The design: {DESIGN_SPEC_CANONICAL, con cada elemento ubicado respecto a algo fijo: "at the foot of the grey block wall", "in the existing bed along the red-brick wall on the right"}. {WHAT_IS_REMOVED}.

Match the original {LIGHTING_DESCRIPTION}. The result looks like an unretouched smartphone photograph of the same garden about two years after the redesign, with plants at realistic sizes, not a 3D render.
```

## Lecciones (foto 06)
- **Ubica cada elemento nuevo respecto a algo fijo.** Si no, el modelo lo pone donde quiere (en v1 y en Pro, la banca acabó en la terraza).
- **Nombra lo que debe sobrevivir y es fácil de perder:** las guirnaldas de luces desaparecieron en v1 y se conservaron en v2 al nombrarlas.
- **Prohíbe lo que suele inventar:** "nothing added in the foreground", "no new windows or doors".
- **Nano Banana Pro no mejoró la fidelidad:** más saturado, la banca fuera de lugar y el seto amarillento, por 2–4 veces el costo. Quedarse con 2.1.

## Ejemplo de relleno (zona césped, foto 01): borrador
- **{EDITABLE_AREAS}:** "the lawn, the narrow planting bed along the brick wall and the loose pots and stands on the lawn"
- **{FIXED_ELEMENTS_LIST}:** "the long red-brick wall with cream concrete pillars and cap, the chain-link fence and hedge on top of it, the tall grey concrete-block wall with the white lattice panel on the left, the cream house corner with the black arched window grille, the overhead string lights"
- **{LIGHTING_DESCRIPTION}:** "soft overcast daylight, late morning"
