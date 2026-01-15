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

- **Regla principal:** Las imágenes deben estar en una carpeta con el mismo nombre que el archivo markdown, en el mismo directorio padre.
- Si tienes un archivo `Ropa y Accesorios.md` en `30-Vocabulario/Temas/`, todas las imágenes deben estar en `30-Vocabulario/Temas/Ropa y Accesorios/`.
- Estructura correcta:
  - `30-Vocabulario/Temas/Ropa y Accesorios.md` (archivo markdown)
  - `30-Vocabulario/Temas/Ropa y Accesorios/` (carpeta con imágenes)
  - Referencias en el markdown: `![[Ropa y Accesorios/pantalones.jpg]]`

### Enlaces

- Usar rutas relativas siempre que sea posible para mantener la portabilidad del repositorio.
- Obsidian con la configuración "Same folder as the current file" maneja esto automáticamente.
- Las referencias deben incluir el nombre de la carpeta: `![[NombreCarpeta/imagen.jpg]]` cuando el archivo está en el nivel padre de la carpeta.

## 3. Notas de Carpeta (Folder Notes)

- Si una carpeta representa un tema (e.g., `Siempre Plural`), es buena práctica tener una nota con el mismo nombre EXACTO dentro (o al mismo nivel) que actúe como índice.
  - `30-Vocabulario/Temas/Siempre Plural/` (Carpeta)
  - `30-Vocabulario/Temas/Siempre Plural.md` (Nota índice)

## 4. Herramientas y Scripts

- Almacenar scripts de utilidad en `80-Tools` para no ensuciar la raíz.
- Los scripts deben ser **genéricos**: aceptar argumentos para rutas y datos, en lugar de tener información "hardcoded" (escrita directamente en el código).
