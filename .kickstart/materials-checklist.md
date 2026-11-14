# Materials Checklist: Garden Design
Pon los archivos en la carpeta indicada (o mándalos por el chat y yo los guardo).
Los 🔴 bloquean solo la *construcción* del primer slice, no la estructura del proyecto.

## 🔴 Bloqueantes
- [ ] **API key de Gemini con facturación activa.** Sin ella no hay renders. *Formato:* se guarda en un formulario seguro (nunca en el chat ni en archivos). *Dónde:* `.env` / secreto del entorno.
- [x] **Fotos amplias de las 3 zonas.** Base para analizar y renderizar. *Formato:* JPG. *Dónde:* `inputs/fotos/`. Ya hay 6.

## 🟡 Mejoran la precisión
- [ ] **Fotos originales del celular en resolución completa** (las mismas 6, sin pasar por el chat). Renders más nítidos. *Formato:* JPG original. *Dónde:* `inputs/fotos/originales/`.
- [ ] **Fotos tomadas de frente, sin modo panorámico**, una por zona, desde donde normalmente se mira (por ejemplo, desde la puerta de la casa). Las panorámicas deforman y confunden al modelo. *Formato:* JPG. *Dónde:* `inputs/fotos/`.
- [ ] **Medidas aproximadas:** largo y ancho del césped, ancho de la terraza y largo de cada muro. Así las recomendaciones tienen tamaños reales. *Formato:* texto o un croquis a mano fotografiado. *Dónde:* `inputs/reference/data/medidas.md` o el chat.
- [ ] **Inventario rápido de la colección de tu mamá:** cuántas orquídeas, bonsáis, rosales y arbolitos en bolsa, más o menos. Sirve para dimensionar las estanterías y la zona de exhibición. *Formato:* texto. *Dónde:* el chat.
- [ ] **Qué se queda y qué se va:** asadores, mesa plegable, sillas blancas, muebles de hierro blancos, estructura metálica oxidada, banca mecedora, pesas, luces. *Formato:* lista. *Dónde:* el chat.
- [ ] **Gustos de tu mamá:** colores favoritos, plantas que ama u odia, 2–5 fotos de jardines que le gusten (Pinterest, revistas, Instagram). Así los estilos le hablan a ella. *Formato:* imágenes o enlaces. *Dónde:* `inputs/reference/estilos/`.
- [ ] **Presupuesto aproximado** o un tope que no quieran pasar. Calibra los 3 niveles del plan. *Formato:* número en USD. *Dónde:* el chat.

## 🟢 Opcional
- [ ] **El video del recorrido** que mencionaste. Ayuda a entender cómo se conectan las zonas. *Dónde:* el chat o `inputs/fotos/`.
- [ ] **Fotos de detalle:** la mata del tronco del aguacate (para identificarla), los bonsáis y el rincón bajo el alero. *Dónde:* `inputs/fotos/`.
- [ ] **Dónde sale y se pone el sol**, o la dirección aproximada de la casa. Afina las zonas de sombra. *Dónde:* el chat.
- [ ] **Si se usará el respaldo de OpenAI:** su API key, por el mismo formulario seguro.
