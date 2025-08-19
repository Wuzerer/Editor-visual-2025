# Solución al Error "Screen is not showing" - Creador de Escenas

## 📋 Resumen Ejecutivo

Este documento describe la solución completa implementada para resolver el error "Screen is not showing" que ocurría en el creador de escenas del Editor Visual de Ren'Py. La solución incluye un enfoque híbrido McKee-Rothamel que combina robustez técnica con claridad narrativa.

## 🎯 Problema Original

### Error Principal
```
Error agregando escena: "Screen is not showing"
```

### Síntomas
- El usuario escribía un nombre de escena
- Al hacer clic en "Aceptar" aparecía la notificación "Error guardar el nombre - intenta de nuevo"
- El sistema validaba el nombre como vacío aunque el usuario había escrito algo
- Errores de sincronización entre variables de pantalla y globales

### Causa Raíz
El error "Screen is not showing" ocurre cuando Ren'Py intenta acceder a variables de una pantalla que no está activa o visible en ese momento específico. Es un problema de **timing** y **sincronización** entre el estado de la pantalla y las operaciones de variables.

## 🏗️ Arquitectura de la Solución

### Enfoque Híbrido McKee-Rothamel

#### Enfoque McKee (Narrativo)
- **Planteamiento**: Verificar el estado del mundo antes de actuar
- **Conflicto**: Manejar errores de sincronización de forma elegante
- **Resolución**: Implementar fallbacks robustos y notificaciones claras

#### Enfoque Rothamel (Técnico)
- **Simplicidad**: Usar variables globales como base confiable
- **Robustez**: Múltiples capas de fallback
- **Debug**: Información detallada para diagnóstico

## 🔧 Implementación Técnica

### 1. Variables Globales Agregadas

```python
# En init python:
new_scene_name = ""
scene_name_active = False
created_scenes_modal_global = []
```

### 2. Sistema de Input Mejorado

#### Antes (Problemático)
```python
input:
    value ScreenVariableInputValue("new_scene_name")
```

#### Después (Funcional)
```python
input:
    value FieldInputValue(renpy.store, "new_scene_name")
```

### 3. Función `get_scene_name_safely()` - Prioridades de Fallback

```python
def get_scene_name_safely():
    # Prioridad 1: Variable global (más confiable)
    scene_name = getattr(renpy.store, 'new_scene_name', "")
    
    # Prioridad 2: Variable de pantalla
    scene_name = renpy.get_screen_variable("new_scene_name", "")
    
    # Prioridad 3: Variable global alternativa
    scene_name = getattr(renpy.store, 'new_scene_name_global', "")
    
    # Fallback final: cadena vacía
    return ""
```

### 4. Sistema de Sincronización Bidireccional

```python
def sync_scene_variables():
    # Pantalla → Global
    screen_name = renpy.get_screen_variable("new_scene_name", "")
    renpy.store.new_scene_name = screen_name
    
    # Global → Pantalla
    global_name = getattr(renpy.store, 'new_scene_name', "")
    renpy.set_screen_variable("new_scene_name", global_name)
```

### 5. Debug Detallado

Cada función incluye mensajes de debug específicos:
- `🔍 Debug: Usando variable global: 'Mi Escena'`
- `🔍 Debug: Error obteniendo variable de pantalla: Screen is not showing`
- `🔍 Debug: Campo activado, scene_name_active = True (pantalla y global)`

## 📁 Archivos Modificados

### `editor_modules/visual_editor_screen.rpy`

#### Variables Globales Agregadas
- `new_scene_name = ""`
- `scene_name_active = False`
- `created_scenes_modal_global = []`

#### Funciones Mejoradas
1. **`get_scene_name_safely()`**
   - Sistema de prioridades de fallback
   - Debug detallado de cada intento
   - Manejo de tipos de datos

2. **`activate_scene_name_edit()`**
   - Activación de variables pantalla + global
   - Fallback robusto
   - Sincronización automática

3. **`accept_scene_name()`**
   - Lectura desde variable global (más confiable)
   - Manejo de errores mejorado
   - Sincronización después de guardar

4. **`sync_scene_variables()`**
   - Sincronización bidireccional
   - Manejo de errores detallado
   - Debug de cada operación

5. **`validate_scene_name()`**
   - Validación más específica
   - Debug de tipos de datos
   - Mensajes claros de error

#### Pantalla Mejorada
- Input cambiado a `FieldInputValue(renpy.store, "new_scene_name")`
- Instrucciones claras en la interfaz
- Flujo de pasos documentado

## 🔄 Flujo de Usuario Mejorado

### Pasos del Usuario
1. **Hacer clic en "✏️ Editar Nombre"** → Activa el campo
2. **Escribir el nombre de la escena** → Se guarda en variable global
3. **Hacer clic en "✅ Aceptar"** → Se lee desde variable global
4. **Hacer clic en "➕ Crear Escena"** → Se procesa con validación

### Instrucciones en Pantalla
```
📝 PASOS: 1) Editar Nombre → 2) Escribir → 3) Aceptar → 4) Crear Escena
```

## 🧪 Sistema de Debug

### Mensajes de Debug Implementados
- Activación de campos
- Obtención de valores
- Sincronización de variables
- Validación de nombres
- Manejo de errores

### Ejemplo de Log
```
🔍 Debug: Activando edición del nombre...
🔍 Debug: Campo activado, scene_name_active = True (pantalla y global)
🔍 Debug: Aceptando nombre de escena...
🔍 Debug: Usando variable global: 'Mi Escena'
🔍 Debug: Nombre guardado exitosamente
```

## 🎯 Resultados Obtenidos

### Problemas Resueltos
1. ✅ **Error "Screen is not showing"** - Eliminado con variables globales
2. ✅ **Nombre vacío** - Resuelto con captura directa del input
3. ✅ **Sincronización** - Implementada bidireccionalmente
4. ✅ **Debug** - Sistema completo de diagnóstico
5. ✅ **UX** - Flujo claro y instrucciones visibles

### Mejoras Implementadas
- **Robustez**: Múltiples capas de fallback
- **Confiabilidad**: Variables globales como base
- **Transparencia**: Debug detallado
- **Usabilidad**: Instrucciones claras
- **Mantenibilidad**: Código bien documentado

## 🔮 Lecciones Aprendidas

### Técnicas
1. **Variables Globales > Variables de Pantalla** para datos críticos
2. **Fallbacks múltiples** son esenciales en Ren'Py
3. **Debug detallado** facilita la resolución de problemas
4. **Sincronización bidireccional** previene inconsistencias

### Arquitectónicas
1. **Enfoque híbrido** combina lo mejor de diferentes metodologías
2. **Separación de responsabilidades** mejora la mantenibilidad
3. **Documentación en tiempo real** facilita el desarrollo
4. **Testing incremental** previene regresiones

## 📚 Referencias

### Documentación Ren'Py
- `FieldInputValue` vs `ScreenVariableInputValue`
- Manejo de variables de pantalla
- Sistema de debug de Ren'Py

### Patrones de Diseño
- **Enfoque McKee**: Estructura narrativa para código
- **Enfoque Rothamel**: Simplicidad y robustez técnica
- **Fallback Pattern**: Múltiples capas de recuperación

## 🚀 Próximos Pasos

### Mejoras Futuras
1. **Testing automatizado** del flujo de creación de escenas
2. **Métricas de uso** para optimizar la UX
3. **Sistema de logs** más avanzado
4. **Validación en tiempo real** del input

### Mantenimiento
1. **Revisión periódica** de los fallbacks
2. **Actualización de debug** según necesidades
3. **Optimización** de la sincronización
4. **Documentación** de nuevos casos de uso

---

**Autor**: Terry Jeffords (Sargento de Desarrollo)  
**Fecha**: 19 de Agosto, 2025  
**Versión**: 1.0  
**Estado**: Implementado y Funcionando ✅
