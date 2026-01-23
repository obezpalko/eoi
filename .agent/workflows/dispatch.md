---
description: General instructions to route tasks to specific workflows based on file location.
---
# Workflow Router

When the user asks to process, update, or create a file, identify its location and use the corresponding workflow:

- Path starts with `10-Lecciones/` -> Use `@[.agent/workflows/10-lecciones.md]`
- Path starts with `20-Gramática/` -> Use `@[.agent/workflows/20-gramatica.md]`
- Path starts with `30-Vocabulario/` -> Use `@[.agent/workflows/30-vocabulario.md]`
- Path starts with `40-Deberes/` -> [Not yet defined, follow general A1-A2 Spanish rules]
- Path starts with `60-Cultura/` -> [Not yet defined, follow narrative A1-A2 Spanish rules]

**Rule**: Always check `structure_recommendations.md` before making structural changes.
