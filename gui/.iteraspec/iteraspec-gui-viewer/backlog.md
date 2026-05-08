# Backlog: IteraSpec GUI Viewer

## Contexto
- `feature_name`: `iteraspec-gui-viewer`
- Workspace: `.iteraspec/iteraspec-gui-viewer/`
- Estado del ciclo: backlog implementado, listo para Fase 4
- Restricción activa: no escribir nuevas features sin reingresar a implementación aprobada

## Criterio de Tamaño y Granularidad
Este backlog contiene `9` tareas. No se usa un número redondo por defecto; la cantidad surge del alcance aprobado y del mínimo de unidades necesarias para entregar la funcionalidad de forma segura e incremental.

Cada tarea representa una unidad independiente de valor o riesgo:
- T1 aísla el arranque local y la base ejecutable.
- T2 separa el launcher operativo `run.sh`, porque agrega conveniencia de arranque sin mezclarla con la base web ya activa en T1.
- T3 separa el descubrimiento de workspaces y artefactos.
- T4 separa la lectura segura y el modelo de datos read-only.
- T5 separa el ajuste del launcher ya existente, porque cambia una expectativa operativa concreta sin mezclarla con renderizado o lectura.
- T6 separa la experiencia visual general de navegación y renderizado.
- T7 separa la interpretación especializada del backlog y la tarea activa, porque tiene reglas visuales y de parsing propias.
- T8 separa el refinamiento visual e identidad IteraSpec, porque afecta experiencia y branding transversal.
- T9 separa validación y robustez final, porque su función es verificar el comportamiento completo sin mezclarlo con construcción incremental.

## 🔴 To Do

## 🟡 In Progress
- Ninguna tarea en progreso.

## 🟢 Done
### T1. Crear la base ejecutable de la aplicación web local
- Objetivo: establecer el punto de entrada y la estructura mínima necesaria para arrancar la GUI localmente.
- Alcance:
  - crear el script o entrypoint principal
  - crear el servidor web base
  - definir la estructura inicial de archivos de la aplicación
- Criterios de aceptación:
  - la aplicación puede iniciarse localmente con un comando simple
  - existe una ruta base funcional
  - la estructura creada permite continuar sin rehacer cimientos

### T2. Crear script de arranque rápido para la GUI
- Objetivo: permitir que la GUI se levante con un único comando de conveniencia desde el proyecto.
- Alcance:
  - crear `run.sh` o equivalente aprobado
  - encapsular los pasos necesarios para iniciar la aplicación local
  - documentar o reflejar el comportamiento esperado del script dentro del propio flujo del proyecto
- Criterios de aceptación:
  - el usuario puede iniciar la GUI con un solo comando
  - el script resuelve los pasos mínimos necesarios de arranque local
  - el script no introduce capacidades de edición sobre `.iteraspec/`

### T3. Implementar descubrimiento de workspaces y artefactos IteraSpec
- Objetivo: detectar directorios `.iteraspec/<feature_name>/` y enumerar sus Markdown relevantes.
- Alcance:
  - inspección de `.iteraspec/`
  - detección de workspaces válidos
  - identificación de `specs.md`, `backlog.md`, `current_task.md` y otros `.md`
- Criterios de aceptación:
  - la aplicación detecta workspaces disponibles
  - cada workspace expone sus documentos visibles para la UI
  - la ausencia de workspaces o archivos no rompe la aplicación

### T4. Implementar lectura segura read-only y modelo de documentos
- Objetivo: cargar contenido Markdown de forma segura para consumo visual, sin capacidades de escritura.
- Alcance:
  - lectura controlada de archivos
  - validación básica de rutas
  - construcción de un modelo interno para documentos y metadatos
- Criterios de aceptación:
  - la aplicación puede recuperar el contenido de los archivos detectados
  - no se permite acceder a rutas arbitrarias fuera de `.iteraspec/`
  - errores de lectura se manejan de forma controlada y visible

### T5. Ajustar launcher para usar `./run.sh` con puerto por defecto `8001`
- Objetivo: alinear el launcher con la forma de arranque canónica y el puerto por defecto requerido.
- Alcance:
  - ajustar `run.sh` para usar `8001` como puerto por defecto
  - preservar la posibilidad de sobrescribir el puerto cuando el usuario lo necesite
  - mantener la ejecución con `./run.sh` como flujo principal de arranque
- Criterios de aceptación:
  - `./run.sh` sigue siendo suficiente para levantar la GUI
  - sin configuración adicional, el launcher intenta arrancar en `8001`
  - el usuario puede seguir definiendo otro puerto manualmente

### T6. Implementar navegación y renderizado visual base de documentos
- Objetivo: presentar documentos Markdown en una interfaz web legible, jerárquica y fácil de recorrer.
- Alcance:
  - layout principal
  - navegación entre workspaces y documentos
  - renderizado de Markdown con estilos base
- Criterios de aceptación:
  - el usuario puede abrir y leer documentos cómodamente
  - la UI distingue encabezados, listas, bloques y secciones
  - la navegación entre documentos no requiere abrir archivos manualmente

### T7. Implementar vistas especializadas para backlog y tarea activa
- Objetivo: interpretar y destacar visualmente los artefactos operativos de IteraSpec con mayor valor diario.
- Alcance:
  - representación especializada de `backlog.md`
  - diferenciación visual de `🔴 To Do`, `🟡 In Progress`, `🟢 Done` y `⚫ Blocked`
  - destaque prioritario de `current_task.md` cuando exista
- Criterios de aceptación:
  - el backlog se entiende más rápido que en Markdown plano
  - los estados de tareas se distinguen visualmente con claridad
  - la tarea activa queda identificable de inmediato

### T8. Incorporar dashboard inicial, identidad IteraSpec y refinamiento visual
- Objetivo: convertir la GUI en una experiencia claramente atractiva, informativa y explícitamente asociada a IteraSpec.
- Alcance:
  - vista de resumen del workspace activo
  - branding visible de IteraSpec
  - sistema visual de color, tipografía, espaciado y composición
  - ajustes responsive básicos
  - barras visuales en la sección `Lectura ejecutiva` para comparar estados del backlog
  - alineación de la convención fuente de estados en los Markdown relevantes y en `ITERASPEC.md`
- Criterios de aceptación:
  - la pantalla principal entrega contexto útil de un vistazo
  - queda claro que la GUI fue desarrollada con IteraSpec
  - la interfaz se percibe cuidada, moderna y visualmente fuerte
  - la sección `Lectura ejecutiva` permite ver gráficamente qué estados concentran más trabajo
  - los Markdown relevantes usan `🔴 To Do`, `🟡 In Progress`, `🟢 Done` y `⚫ Blocked` como convención fuente

### T9. Validar robustez, restricciones read-only y experiencia final
- Objetivo: verificar que el sistema cumple su propósito sin introducir edición ni comportamientos frágiles.
- Alcance:
  - pruebas o validaciones relevantes de lectura
  - verificación de estados vacíos o archivos faltantes
  - confirmación de ausencia de flujos de escritura
- Criterios de aceptación:
  - la aplicación se mantiene estrictamente en modo visualización
  - maneja workspaces incompletos sin fallos críticos
  - la funcionalidad principal queda verificada antes de cierre

## ⚫ Blocked
- Ninguna tarea bloqueada.

## Orden Propuesto de Implementación
1. T1. Crear la base ejecutable de la aplicación web local
2. T2. Crear script de arranque rápido para la GUI
3. T3. Implementar descubrimiento de workspaces y artefactos IteraSpec
4. T4. Implementar lectura segura read-only y modelo de documentos
5. T5. Ajustar launcher para usar `./run.sh` con puerto por defecto `8001`
6. T6. Implementar navegación y renderizado visual base de documentos
7. T7. Implementar vistas especializadas para backlog y tarea activa
8. T8. Incorporar dashboard inicial, identidad IteraSpec y refinamiento visual
9. T9. Validar robustez, restricciones read-only y experiencia final

## Notas de Planificación
- Solo una tarea puede pasar a `🟡 In Progress` durante Fase 3.
- La implementación no debe comenzar automáticamente tras aprobar este backlog.
- Será necesaria autorización humana explícita para iniciar Fase 3 o para arrancar una tarea concreta.
