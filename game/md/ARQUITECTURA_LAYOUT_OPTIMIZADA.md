# Arquitectura de Layout Optimizada

## Visión General

Se ha refactorizado el sistema de layout para eliminar duplicación de código y crear una arquitectura más mantenible y eficiente.

## Estructura de Archivos

### 1. `layout_controller.rpy` - Fuente Única de Verdad
- **Propósito**: Define todas las clases e instancias de layout
- **Contenido**:
  - `VisualEditorLayout` - Configuraciones de dimensiones y espaciado
  - `PanelColors` - Colores de todos los paneles
  - `TextSizes` - Tamaños de texto
  - Instancias globales: `visual_layout`, `colors`, `text_sizes`
  - Funciones de seguridad: `get_panel_padding()`, `get_panel_padding_tuple()`

### 2. `developer_tools.rpy` - Consumidor del Layout
- **Propósito**: Usa las configuraciones desde `layout_controller.rpy`
- **Funcionalidad**:
  - Importa instancias desde `layout_controller.rpy`
  - Proporciona fallback básico si no están disponibles
  - Mantiene funciones de seguridad adicionales

## Flujo de Datos

```
layout_controller.rpy (FUENTE)
    ↓ (define classes & instances)
renpy.store (GLOBAL STORE)
    ↓ (import)
developer_tools.rpy (CONSUMER)
    ↓ (use in screens)
Editor Visual
```

## Ventajas de la Nueva Arquitectura

### ✅ Eliminación de Duplicación
- **Antes**: Clases definidas en ambos archivos
- **Ahora**: Una sola definición en `layout_controller.rpy`

### ✅ Mantenibilidad Mejorada
- Cambios en layout solo requieren modificar un archivo
- Configuraciones centralizadas y documentadas
- Menor riesgo de inconsistencias

### ✅ Robustez
- Fallback automático si el layout no está disponible
- Verificaciones de seguridad en múltiples niveles
- Manejo de errores mejorado

### ✅ Escalabilidad
- Fácil agregar nuevas configuraciones
- Estructura clara para futuras extensiones
- Separación de responsabilidades

## Funciones de Seguridad

### `get_panel_padding()`
- Obtiene el valor de `panel_padding` de forma segura
- Agrega el atributo si no existe
- Manejo de excepciones robusto

### `get_panel_padding_tuple()`
- Convierte el padding a formato compatible con Ren'Py
- Maneja enteros, tuplas y listas
- Siempre devuelve una tupla válida

### `ensure_panel_padding_global()`
- Verifica todas las instancias globales
- Agrega atributos faltantes automáticamente
- Logging detallado para debugging

## Uso en Pantallas

```python
# En lugar de:
padding visual_layout.panel_padding

# Usar:
padding get_panel_padding_tuple()
```

## Configuración de Paneles

Cada panel tiene su color distintivo:

| Panel | Color | Propósito |
|-------|-------|-----------|
| Background | `#e74c3c` (Rojo) | Fondos de escena |
| Character | `#3498db` (Azul) | Personajes |
| Expressions | `#9b59b6` (Púrpura) | Expresiones |
| Stage | `#f39c12` (Naranja) | Posicionamiento |
| Dialogue | `#27ae60` (Verde) | Diálogos |
| Structure | `#8e44ad` (Púrpura oscuro) | Estructura del script |
| Projects | `#16a085` (Verde azulado) | Gestión de proyectos |
| Developer | `#e74c3c` (Rojo) | Herramientas de desarrollo |

## Dimensiones Principales

```python
editor_width = 1800        # Ancho total del editor
editor_height = 1000       # Alto total del editor
top_area_height = 450      # Área superior (preview + scenes)
bottom_area_height = 520   # Área inferior (paneles)
panel_width = 420          # Ancho de cada panel
panel_height = 240         # Alto de cada panel
panel_padding = 20         # Padding interno de paneles
```

## Migración y Compatibilidad

### Para Nuevos Archivos
1. Importar desde `layout_controller.rpy`:
```python
if hasattr(renpy.store, 'visual_layout'):
    visual_layout = renpy.store.visual_layout
    colors = renpy.store.colors
    text_sizes = renpy.store.text_sizes
```

2. Usar funciones de seguridad:
```python
padding get_panel_padding_tuple()
```

### Para Archivos Existentes
- Reemplazar definiciones duplicadas con importaciones
- Usar funciones de seguridad en lugar de acceso directo
- Mantener fallbacks para compatibilidad

## Debugging

### Logs de Inicialización
- `✅ Layout central inicializado en layout_controller.rpy`
- `✅ Usando layout desde layout_controller.rpy`
- `⚠️ Layout no disponible, creando fallback básico`

### Logs de Verificación
- `⚠️ Agregando panel_padding faltante...`
- `✅ panel_padding agregado...`
- `⚠️ Error obteniendo panel_padding...`

## Próximos Pasos

1. **Optimización de Rendimiento**
   - Cache de configuraciones frecuentemente usadas
   - Lazy loading de configuraciones pesadas

2. **Extensibilidad**
   - Sistema de plugins para configuraciones personalizadas
   - API para modificar layout en tiempo de ejecución

3. **Documentación**
   - Guías de usuario para personalización
   - Ejemplos de uso avanzado
   - Referencia completa de API

## Conclusión

Esta nueva arquitectura proporciona:
- **Código más limpio** y mantenible
- **Menor duplicación** y riesgo de inconsistencias
- **Mayor robustez** con fallbacks automáticos
- **Mejor escalabilidad** para futuras mejoras
- **Documentación clara** para desarrolladores

El sistema ahora es más profesional, eficiente y fácil de mantener, siguiendo las mejores prácticas de desarrollo de software.
