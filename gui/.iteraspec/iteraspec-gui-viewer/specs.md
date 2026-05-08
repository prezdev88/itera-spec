# Especificación del Sistema: GUI Web de Visualización para IteraSpec

## 1. Identidad del Ciclo
- `feature_name`: `iteraspec-gui-viewer`
- Workspace del ciclo: `.iteraspec/iteraspec-gui-viewer/`

## 2. Propósito
Construir una aplicación web local, de solo lectura, diseñada para visualizar de forma gráfica, clara y atractiva los archivos Markdown generados por IteraSpec dentro de la carpeta `.iteraspec/`.

El sistema no debe modificar archivos, escribir resultados, editar contenido ni intervenir en el flujo operativo de IteraSpec. Su objetivo es exclusivamente mejorar la lectura, interpretación y navegación del estado del proyecto desde una interfaz visual superior al consumo directo de Markdown plano.

## 3. Contexto del Proyecto
- Tipo de proyecto: proyecto nuevo.
- Idioma de trabajo: español.
- Usuarios objetivo: usuarios de IteraSpec.
- Problema principal: los archivos Markdown de `.iteraspec/` son útiles, pero su consumo en texto plano dificulta una lectura rápida, agradable y operativamente eficiente.
- Resultado esperado: una GUI web local que lea `.iteraspec/`, interprete sus archivos más relevantes y los muestre de forma visual, ordenada y bonita.

## 4. Objetivos del Sistema
- Permitir abrir rápidamente una interfaz web local con un solo comando simple.
- Leer automáticamente los archivos presentes en `.iteraspec/`.
- Presentar el contenido de especificaciones, backlog, tarea actual y otros artefactos Markdown en una interfaz visual clara.
- Mejorar jerarquía visual, navegación, escaneo rápido y comprensión del estado del proyecto.
- Dejar explícitamente visible dentro de la interfaz que la GUI fue desarrollada con IteraSpec.

## 5. Alcance
### Incluido
- Aplicación web local accesible desde navegador.
- Lectura de archivos dentro de `.iteraspec/`.
- Procesamiento de archivos Markdown para presentación visual.
- Vista de solo lectura.
- Diseño visual cuidado y claramente superior a la inspección de archivos planos.
- Identificación visual del estado del proyecto a partir de artefactos de IteraSpec.

### Excluido
- Edición de archivos Markdown.
- Escritura en `.iteraspec/`.
- Creación o modificación automática de backlog, especificaciones o tareas.
- Integración multiusuario, autenticación o persistencia remota.
- Sincronización en tiempo real entre máquinas.
- Funciones de administración o despliegue en producción como prioridad inicial.

## 6. Decisión Tecnológica
### Stack seleccionado
- Backend y servidor local: `Python + FastAPI`.
- Renderizado web: `HTML + CSS + JavaScript` ligeros.

### Justificación
- Python permite leer fácilmente archivos locales del proyecto con mínima complejidad.
- FastAPI ofrece un servidor local muy simple, rápido de levantar y fácil de mantener.
- La combinación permite una experiencia de ejecución tipo `python app.py` o comando equivalente simple.
- Evita complejidad innecesaria de toolchains frontend pesados para un visor local read-only.
- Mantiene abierta la posibilidad de una UI visualmente fuerte sin introducir una arquitectura excesiva.

## 7. Usuarios y Casos de Uso
### Usuario principal
Usuario de IteraSpec que quiere inspeccionar visualmente el estado del proyecto sin leer múltiples archivos Markdown manualmente.

### Casos de uso principales
- Abrir la GUI local desde el proyecto.
- Ver la especificación general del proyecto.
- Ver el backlog con sus estados.
- Ver la tarea activa actual.
- Navegar entre documentos de `.iteraspec/` desde una interfaz más clara.
- Detectar rápidamente progreso, bloqueos y contexto actual del proyecto.
- Confirmar visualmente que la herramienta pertenece al ecosistema y flujo de IteraSpec.

## 8. Requisitos Funcionales
### RF-01: Inicio local simple
El sistema debe poder ejecutarse localmente mediante un comando sencillo, idealmente basado en Python, sin una configuración compleja.

### RF-01b: Script de arranque rápido
El sistema debe incluir un script local de conveniencia, por ejemplo `run.sh`, que ejecute lo necesario para levantar la GUI con el menor número posible de pasos manuales.

### RF-01c: Comando y puerto por defecto del launcher
La forma canónica de arranque debe ser `./run.sh`, y el puerto por defecto del launcher debe ser `8001` salvo que el usuario lo sobrescriba explícitamente mediante una variable de entorno u otro mecanismo aprobado.

### RF-02: Descubrimiento de archivos
El sistema debe detectar y listar archivos relevantes dentro de `.iteraspec/`, incluyendo múltiples workspaces de features si existen.

### RF-03: Lectura de contenido
El sistema debe leer el contenido de archivos Markdown presentes en `.iteraspec/`.

### RF-04: Presentación visual estructurada
El sistema debe transformar el contenido leído en una presentación web con jerarquía visual clara, tipografía legible, secciones distinguibles y navegación entendible.

### RF-05: Soporte para artefactos clave de IteraSpec
El sistema debe dar tratamiento visual especialmente claro a:
- `.iteraspec/<feature_name>/specs.md`
- `.iteraspec/<feature_name>/backlog.md` cuando exista
- `.iteraspec/<feature_name>/current_task.md` cuando exista
- otros archivos Markdown auxiliares generados por el protocolo

### RF-06: Vista read-only
La interfaz no debe ofrecer formularios, editores, botones de guardado ni acciones que modifiquen archivos.

### RF-07: Resaltado de estados del backlog
Cuando exista un backlog con estados de IteraSpec, la UI debe distinguir visualmente tareas `🔴 To Do`, `🟡 In Progress`, `🟢 Done` y `⚫ Blocked`.

Convención visual aprobada para esta GUI:
- `To Do`: rojo
- `In Progress`: amarillo
- `Done`: verde
- `Blocked`: neutro oscuro o gris

Convención fuente aprobada para los artefactos Markdown del proyecto y del protocolo asociado a este ciclo:
- `🔴 To Do`
- `🟡 In Progress`
- `🟢 Done`
- `⚫ Blocked`

### RF-08: Navegación entre documentos
La UI debe permitir cambiar fácilmente entre vistas o secciones de documentos sin obligar al usuario a abrir archivos manualmente.

### RF-09: Identidad explícita de IteraSpec
La interfaz debe dejar muy claro, en branding, encabezado o área visible principal, que la GUI fue desarrollada con IteraSpec.

### RF-10: Manejo de ausencia de archivos
Si algún archivo esperado no existe, la interfaz debe indicarlo claramente sin fallar.

### RF-11: Renderizado seguro de Markdown
El sistema debe interpretar Markdown para su visualización, evitando comportamientos inseguros derivados de contenido embebido no confiable.

### RF-12: Resumen visual del estado
La interfaz debe ofrecer una forma rápida de comprender el estado general del proyecto, priorizando lectura ejecutiva y navegación eficiente.

### RF-12b: Barras visuales en lectura ejecutiva
La sección de lectura ejecutiva del dashboard debe representar el estado del backlog mediante barras visuales o indicadores equivalentes de magnitud, de modo que el usuario pueda percibir rápidamente qué estados concentran mayor cantidad de trabajo.

### RF-13: Soporte para múltiples ciclos
Si existen varios directorios `.iteraspec/<feature_name>/`, la interfaz debe permitir identificarlos y navegar entre ellos de manera clara.

## 9. Requisitos No Funcionales
### RNF-01: Simplicidad operativa
La solución debe privilegiar facilidad de ejecución local, con dependencias reducidas y setup corto.

### RNF-02: Rapidez de apertura
La aplicación debe iniciar rápidamente en entorno local y permitir acceso inmediato desde navegador.

### RNF-03: Diseño visual de alta calidad
La interfaz debe ser claramente atractiva, moderna y cuidada, con uso intencional de color, jerarquía, espaciado y composición visual.

### RNF-04: Claridad de lectura
La presentación debe facilitar escaneo rápido, lectura prolongada y comprensión contextual mejor que el Markdown plano.

### RNF-05: Mantenibilidad
La solución debe mantenerse simple de extender para nuevos tipos de archivos o nuevas vistas derivadas de `.iteraspec/`.

### RNF-06: Seguridad local básica
La aplicación no debe ejecutar contenido arbitrario proveniente de los Markdown ni exponer capacidades de escritura no requeridas.

### RNF-07: Compatibilidad de uso
Debe funcionar correctamente en navegadores modernos de escritorio, y de forma razonable en pantallas pequeñas si se abre desde móvil.

### RNF-08: Solo lectura garantizada por diseño
La arquitectura debe minimizar el riesgo de edición accidental tanto a nivel de interfaz como de endpoints disponibles.

## 10. Requisitos de Experiencia de Usuario
- La primera impresión visual debe sentirse intencional y distintiva, no una página genérica.
- El diseño debe comunicar que esta herramienta es una capa visual premium sobre IteraSpec.
- Debe existir una portada, encabezado o panel principal que explique rápidamente qué está viendo el usuario.
- Los colores deben usarse para reforzar estados, secciones y prioridades.
- La interfaz debe hacer visible el valor diferencial frente a abrir archivos Markdown directamente.
- La lectura ejecutiva debe permitir comparar visualmente el peso relativo de los estados del backlog sin exigir lectura detallada de números.

## 11. Arquitectura Inicial Propuesta
### Componentes
- Servidor local Python.
- Capa de descubrimiento de workspaces de features dentro de `.iteraspec/`.
- Capa de lectura de archivos Markdown.
- Capa de interpretación de Markdown y extracción de estructura.
- Capa de presentación web.

### Flujo general
1. El usuario ejecuta el servidor local.
2. El backend inspecciona `.iteraspec/` y detecta workspaces de features.
3. El sistema carga y procesa archivos Markdown disponibles.
4. La UI presenta vistas estructuradas y visualmente enriquecidas.

## 12. Consideraciones de Estructura y Presentación
- El sistema debe poder representar documentos completos.
- Debe poder destacar encabezados, listas, estados, bloques relevantes y notas de contexto.
- El backlog debe poder presentarse con separación visual clara por estado.
- La tarea activa, cuando exista, debe destacarse como foco principal.
- La especificación debe poder navegarse sin sensación de pared de texto.
- La GUI debe reflejar la misma convención de estados que utilicen los Markdown fuente, evitando desalineaciones entre texto y representación visual.

## 13. Restricciones
- No debe editar archivos.
- No debe depender de una infraestructura compleja para uso local.
- No debe requerir un proceso de build pesado para su uso básico.
- Debe centrarse en `.iteraspec/` como fuente principal de verdad.
- El script de arranque rápido debe estar orientado a uso local y no debe introducir capacidades de escritura sobre los artefactos de IteraSpec.

## 14. Riesgos Iniciales
- La estructura exacta de algunos archivos Markdown puede variar entre proyectos.
- El backlog podría no tener un formato completamente uniforme.
- Un renderizado visual demasiado literal del Markdown podría no producir la experiencia “bonita” esperada.
- Una implementación demasiado minimalista podría cumplir funcionalmente pero fallar en calidad visual.

## 15. Criterios de Aceptación del Producto
- El usuario puede levantar la GUI localmente de forma simple.
- El usuario puede levantar la GUI mediante `./run.sh`.
- Si el usuario no configura otro puerto, el launcher utiliza `8001` por defecto.
- La GUI detecta y lee los archivos Markdown de `.iteraspec/`.
- La GUI muestra la información en modo solo lectura.
- El backlog, cuando exista, se entiende visualmente mejor que en texto plano.
- La tarea actual, cuando exista, es fácil de identificar.
- La lectura ejecutiva del dashboard muestra barras o indicadores visuales equivalentes para comparar estados del backlog.
- Los Markdown fuente relevantes del ciclo y la convención asociada usan `🔴 To Do`, `🟡 In Progress`, `🟢 Done` y `⚫ Blocked`.
- La interfaz comunica explícitamente que fue desarrollada con IteraSpec.
- La experiencia visual es cuidada, atractiva y útil.

## 16. Entregable Esperado
Una aplicación web local liviana, basada en Python y FastAPI, enfocada en visualización read-only de artefactos `.iteraspec/`, con una interfaz visualmente fuerte, clara, rápida de abrir y claramente identificada como una GUI desarrollada con IteraSpec.
