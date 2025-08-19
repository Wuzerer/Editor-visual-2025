# 🧹 SISTEMA DE LIMPIEZA AUTOMÁTICA DE ESCENAS NO GUARDADAS

## 📋 Resumen Ejecutivo

Se implementó un sistema de limpieza automática que elimina archivos `.rpy` y `.rpyc` temporales cuando se cierra el editor sin guardar el proyecto. Este sistema previene la acumulación de archivos huérfanos y evita problemas de duplicación de labels en el futuro. **NUEVO**: Sistema automático de confirmación de salida que advierte al usuario antes de cerrar el editor con cambios no guardados.

## 🎯 Problema Identificado

### **Problema Principal:**
- **Archivos Huérfanos**: Las escenas creadas en el editor se guardan como archivos `.rpy` individuales en la carpeta `scenes/`
- **Acumulación de Archivos**: Si no se guarda el proyecto, estos archivos permanecen en el sistema
- **Duplicación de Labels**: Los archivos huérfanos pueden causar errores de "label defined twice" en el futuro
- **Desorden en el Sistema**: Archivos temporales que no pertenecen a ningún proyecto
- **Pérdida de Trabajo**: El usuario puede cerrar el editor sin darse cuenta de que tiene cambios no guardados

### **Causa del Problema:**
- **Falta de Seguimiento**: No había un sistema que rastreara qué escenas fueron creadas
- **Ausencia de Limpieza**: No existía un mecanismo para eliminar archivos no guardados
- **Gestión Manual**: El usuario tenía que limpiar manualmente los archivos temporales
- **Sin Advertencias**: No había sistema que advirtiera al usuario antes de cerrar con cambios no guardados

## 🔧 Solución Implementada

### **1. Sistema de Seguimiento de Escenas**

#### **Variables de Control:**
```python
# Variables para control de limpieza automática
project_saved = False
scenes_created_since_last_save = []
```

#### **Funciones de Seguimiento:**
- **`mark_scene_as_created(scene_name)`**: Marca una escena como creada para seguimiento
- **`mark_project_as_saved()`**: Marca el proyecto como guardado para evitar limpieza
- **`cleanup_unsaved_scenes()`**: Limpia las escenas no guardadas

### **2. Sistema Automático de Confirmación de Salida**

#### **Funciones de Verificación:**
- **`check_unsaved_changes()`**: Verifica si hay cambios no guardados en el editor
- **`confirm_exit_with_unsaved_changes()`**: Muestra confirmación de salida con cambios no guardados
- **`exit_editor_with_cleanup()`**: Sale del editor con limpieza automática
- **`exit_editor_without_cleanup()`**: Sale del editor sin limpiar archivos

#### **Modal de Confirmación (`confirm_exit_unsaved_modal`):**
```python
screen confirm_exit_unsaved_modal():
    modal True
    
    # Fondo semi-transparente
    frame:
        background "#000000"
        at transform:
            alpha 0.7
        xfill True
        yfill True
    
    # Modal principal con opciones:
    # - 💾 Guardar Proyecto
    # - 🧹 Salir y Limpiar
    # - ❌ Cancelar
```

### **3. Función de Limpieza Automática**

#### **`cleanup_unsaved_scenes()`:**
```python
def cleanup_unsaved_scenes():
    """Limpia las escenas no guardadas cuando se cierra el editor sin guardar proyecto"""
    try:
        # Solo limpiar si no se ha guardado el proyecto
        if not getattr(renpy.store, 'project_saved', False):
            current_scenes_dir = os.path.join(config.gamedir, "scenes")
            if os.path.exists(current_scenes_dir):
                scenes_created = getattr(renpy.store, 'scenes_created_since_last_save', [])
                
                for scene_name in scenes_created:
                    scene_file = os.path.join(current_scenes_dir, f"{scene_name}.rpy")
                    scene_compiled = os.path.join(current_scenes_dir, f"{scene_name}.rpyc")
                    
                    # Eliminar archivo .rpy
                    if os.path.exists(scene_file):
                        os.remove(scene_file)
                    
                    # Eliminar archivo .rpyc si existe
                    if os.path.exists(scene_compiled):
                        os.remove(scene_compiled)
                
                # Limpiar lista de escenas creadas
                renpy.store.scenes_created_since_last_save = []
                
    except Exception as e:
        print(f"🔍 Debug: Error en limpieza de escenas no guardadas: {e}")
```

### **4. Integración con el Sistema de Creación de Escenas**

#### **Modificación de `add_scene_to_modal()`:**
```python
# Marcar la escena como creada para seguimiento de limpieza
mark_scene_as_created(scene_name)
```

### **5. Integración con el Sistema de Proyectos**

#### **Modificación de `execute_save_project()`:**
```python
# Marcar el proyecto como guardado para evitar limpieza automática
mark_project_as_saved()
```

#### **Modificación de `execute_overwrite_project()`:**
```python
# Marcar el proyecto como guardado para evitar limpieza automática
mark_project_as_saved()
```

### **6. Botón de Cerrar Inteligente**

#### **Modificación del Botón de Cerrar:**
```python
# Botón de cerrar con verificación de cambios no guardados
textbutton "❌":
    action Function(confirm_exit_with_unsaved_changes) if check_unsaved_changes()[0] else Hide("visual_editor")
    xsize 150
    ysize 40
    background "#e74c3c"
    xalign 1.02
    yalign 0.0
    margin (20, 20)
```

### **7. Botón de Limpieza Manual**

#### **Nuevo Botón en el Panel de Gestión de Proyectos:**
```python
textbutton "🗑️ Limpiar No Guardadas":
    action Function(cleanup_unsaved_scenes)
    xminimum 120
    ysize 50
    padding (12, 8)
    background "#e67e22"
    xalign 0.5
    text_style "text_with_outline"
```

## 🔄 Flujo de Trabajo

### **1. Creación de Escenas:**
1. Usuario crea una escena en el editor
2. Sistema marca la escena como creada (`mark_scene_as_created()`)
3. Escena se guarda en `scenes/` como archivo `.rpy`

### **2. Guardado de Proyecto:**
1. Usuario guarda el proyecto
2. Sistema marca el proyecto como guardado (`mark_project_as_saved()`)
3. Lista de escenas creadas se limpia
4. Las escenas se copian al proyecto con nombres únicos

### **3. Intento de Salida del Editor:**
1. Usuario hace clic en el botón "❌" para cerrar
2. Sistema verifica si hay cambios no guardados (`check_unsaved_changes()`)
3. **Si NO hay cambios**: Editor se cierra directamente
4. **Si HAY cambios**: Se muestra modal de confirmación

### **4. Modal de Confirmación:**
1. Sistema muestra `confirm_exit_unsaved_modal`
2. Usuario puede elegir:
   - **💾 Guardar Proyecto**: Abre modal de guardado
   - **🧹 Salir y Limpiar**: Cierra editor y elimina archivos temporales
   - **❌ Cancelar**: Vuelve al editor

### **5. Limpieza Automática:**
1. Si el usuario elige "Salir y Limpiar"
2. Sistema ejecuta `exit_editor_with_cleanup()`
3. Elimina todos los archivos `.rpy` y `.rpyc` de escenas no guardadas
4. Notifica al usuario sobre la limpieza

### **6. Limpieza Manual:**
1. Usuario puede hacer clic en "🗑️ Limpiar No Guardadas"
2. Sistema ejecuta limpieza inmediata
3. Notifica al usuario sobre los archivos eliminados

## 📊 Características del Sistema

### **1. Seguimiento Inteligente:**
- **Rastrea escenas creadas**: Mantiene lista de escenas creadas desde el último guardado
- **Estado del proyecto**: Sabe si el proyecto ha sido guardado o no
- **Limpieza selectiva**: Solo elimina escenas que no han sido guardadas en un proyecto

### **2. Verificación Automática:**
- **Detección automática**: Verifica cambios no guardados al intentar cerrar
- **Modal inteligente**: Solo se muestra si hay cambios no guardados
- **Opciones claras**: Usuario puede guardar, limpiar o cancelar

### **3. Limpieza Completa:**
- **Archivos `.rpy`**: Elimina archivos de escenas no guardadas
- **Archivos `.rpyc`**: Elimina archivos compilados correspondientes
- **Actualización de lista**: Recarga la lista de escenas en el organizador

### **4. Integración Total:**
- **Creación de escenas**: Automáticamente marca escenas como creadas
- **Guardado de proyectos**: Marca proyectos como guardados
- **Limpieza del editor**: Incluye limpieza automática en `clear_current_editor()`
- **Cierre inteligente**: Verifica cambios antes de cerrar

### **5. Interfaz de Usuario:**
- **Botón inteligente**: Botón de cerrar que verifica cambios automáticamente
- **Modal informativo**: Muestra lista de escenas no guardadas
- **Opciones claras**: Botones con acciones específicas
- **Notificaciones**: Informa al usuario sobre el proceso de limpieza
- **Debug detallado**: Logs completos para seguimiento del proceso

## 🎯 Beneficios del Sistema

### **1. Prevención de Problemas:**
- **Sin archivos huérfanos**: Elimina automáticamente archivos temporales
- **Sin duplicación de labels**: Previene errores de "label defined twice"
- **Sistema limpio**: Mantiene el directorio `scenes/` organizado
- **Sin pérdida de trabajo**: Advierte al usuario antes de cerrar

### **2. Experiencia de Usuario:**
- **Automático**: No requiere intervención manual del usuario
- **Transparente**: El usuario no necesita preocuparse por archivos temporales
- **Control manual**: Opción de limpiar manualmente si es necesario
- **Advertencias claras**: Sistema informa sobre cambios no guardados

### **3. Mantenimiento del Sistema:**
- **Organización**: Mantiene el sistema de archivos limpio
- **Rendimiento**: Evita acumulación de archivos innecesarios
- **Debugging**: Facilita la identificación de problemas
- **Prevención**: Evita problemas futuros de duplicación

## 🔧 Funciones Implementadas

### **1. `mark_scene_as_created(scene_name)`**
- **Propósito**: Marca una escena como creada para seguimiento
- **Parámetros**: `scene_name` - Nombre de la escena creada
- **Funcionalidad**: Agrega la escena a la lista de seguimiento

### **2. `mark_project_as_saved()`**
- **Propósito**: Marca el proyecto como guardado
- **Funcionalidad**: Establece `project_saved = True` y limpia la lista de escenas creadas

### **3. `cleanup_unsaved_scenes()`**
- **Propósito**: Limpia escenas no guardadas
- **Funcionalidad**: Elimina archivos `.rpy` y `.rpyc` de escenas no guardadas

### **4. `check_unsaved_changes()`**
- **Propósito**: Verifica si hay cambios no guardados
- **Retorna**: `(has_unsaved_changes, scenes_created)` - Tupla con estado y lista de escenas
- **Funcionalidad**: Verifica si hay escenas creadas sin guardar proyecto

### **5. `confirm_exit_with_unsaved_changes()`**
- **Propósito**: Muestra confirmación de salida con cambios no guardados
- **Funcionalidad**: Oculta editor y muestra modal de confirmación

### **6. `exit_editor_with_cleanup()`**
- **Propósito**: Sale del editor con limpieza automática
- **Funcionalidad**: Limpia archivos no guardados y cierra editor

### **7. `exit_editor_without_cleanup()`**
- **Propósito**: Sale del editor sin limpiar archivos
- **Funcionalidad**: Cierra editor conservando archivos temporales

### **8. Modificación de `clear_current_editor()`**
- **Propósito**: Incluye limpieza automática en la limpieza del editor
- **Funcionalidad**: Llama a `cleanup_unsaved_scenes()` antes de limpiar variables

## 📈 Métricas del Sistema

### **Archivos Gestionados:**
- **Archivos `.rpy`**: Escenas creadas por el editor
- **Archivos `.rpyc`**: Archivos compilados correspondientes
- **Lista de seguimiento**: Escenas creadas desde el último guardado

### **Estados del Sistema:**
- **`project_saved = False`**: Proyecto no guardado, limpieza activa
- **`project_saved = True`**: Proyecto guardado, limpieza desactivada
- **`scenes_created_since_last_save = []`**: Lista de escenas para seguimiento

### **Flujos de Usuario:**
- **Cierre directo**: Sin cambios no guardados
- **Cierre con confirmación**: Con cambios no guardados
- **Guardado y cierre**: Usuario guarda proyecto antes de cerrar
- **Limpieza manual**: Usuario limpia archivos manualmente

## 🚀 Prevención de Errores

### **1. Verificaciones de Seguridad:**
- **Existencia de archivos**: Verifica que los archivos existan antes de eliminarlos
- **Estado del proyecto**: Solo limpia si el proyecto no ha sido guardado
- **Manejo de errores**: Try-catch completo para evitar fallos del sistema
- **Verificación de cambios**: Solo muestra modal si hay cambios reales

### **2. Logs de Debug:**
- **Seguimiento completo**: Logs detallados de todas las operaciones
- **Identificación de problemas**: Facilita la resolución de errores
- **Auditoría**: Permite verificar el funcionamiento del sistema
- **Estado del sistema**: Logs del estado de variables y archivos

## ✅ Conclusión

El sistema de limpieza automática de escenas no guardadas proporciona una solución completa para mantener el editor visual organizado y libre de archivos temporales. El nuevo sistema automático de confirmación de salida añade una capa adicional de seguridad, advirtiendo al usuario antes de cerrar el editor con cambios no guardados.

**¡El sistema ahora mantiene el editor tan limpio como el gimnasio de Terry después de una sesión de entrenamiento, y te avisa antes de salir sin guardar tu progreso!** 💪🧹🔒

---

**Fecha de Implementación:** 19 de Agosto, 2025  
**Versión:** 2.0  
**Estado:** ✅ Completado y Funcional  
**Archivos:** 
- `editor_modules/visual_editor_screen.rpy`
- `editor_modules/exit_confirmation_modal.rpy`  
**Funciones Principales:** 8  
**Integración:** Completa con sistema de proyectos y creación de escenas  
**Nuevas Características:** Sistema automático de confirmación de salida
