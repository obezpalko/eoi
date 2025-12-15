# Recomendaciones de Estructura del Proyecto

Este documento describe las mejores prácticas para mantener el proyecto EOI organizado y escalable.

## 1. Convenciones de Nombrado

### Idioma

- Mantener los nombres de carpetas y archivos en **Español** para consistencia con el contenido (Nivel A1).
- **Correcto:** `30-Vocabulario`, `Temas`, `Verbos`.
- **Incorrecto:** `Vocabulary`, `Topics`, `Verbs`.

### Numeración

- Utilizar prefijos numéricos (`10-`, `20-`, `30-`) para ordenar carpetas de alto nivel de manera lógica, no alfabética.
- Dejar espacios en la numeración (e.g., saltar de 40 a 90) para permitir futuras expansiones sin renombrar todo.

### Formato

- Usar espacios en nombres de archivo es aceptable si mejora la legibilidad en Obsidian (e.g., `Siempre Plural.md`).
- Para herramientas y scripts, preferir `snake_case` (e.g., `download_images.py`).

## 2. Gestión de Imágenes y Adjuntos

### Ubicación

- **Opción A (Actual):** Carpeta centralizada `90-Archivos`. Útil para reutilización.
- **Opción B (Recomendada para Temas):** Mantener las imágenes específicas de un tema dentro de su subcarpeta (e.g., `30-Vocabulario/Temas/Siempre Plural/`). Esto hace que el material sea "portable".

### Enlaces

- Usar rutas relativas siempre que sea posible para mantener la portabilidad del repositorio.
- Obsidian maneja esto automáticamente, pero los scripts deben ser conscientes de dónde se ejecutan.

## 3. Notas de Carpeta (Folder Notes)

- Si una carpeta representa un tema (e.g., `Siempre Plural`), es buena práctica tener una nota con el mismo nombre EXACTO dentro (o al mismo nivel) que actúe como índice.
  - `30-Vocabulario/Temas/Siempre Plural/` (Carpeta)
  - `30-Vocabulario/Temas/Siempre Plural/Siempre Plural.md` (Nota índice)

## 4. Herramientas y Scripts

- Almacenar scripts de utilidad en `80-Tools` (o `Herramientas`) para no ensuciar la raíz.
- Los scripts deben ser **genéricos**: aceptar argumentos para rutas y datos, en lugar de tener información "hardcoded" (escrita directamente en el código).
