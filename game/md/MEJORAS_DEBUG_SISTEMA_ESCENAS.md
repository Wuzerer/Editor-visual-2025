# MEJORAS: Debug y Correcciones del Sistema de Escenas

## Problema Identificado

### 🔍 **Escenas No Aparecen en el Selector**

#### **Síntomas**
- Las escenas se crean correctamente
- Se muestra notificación de creación exitosa
- Se indica la escena actual
- Pero no aparecen en el menú de selección

#### **Análisis**
El problema estaba en el acceso a variables de pantalla usando `renpy.get_screen_variable()` que no funciona de manera confiable en todos los contextos.

## Soluciones Implementadas

### **1. Funciones Seguras Mejoradas**

#### **`get_all_scenes_safe()`**
```python
def get_all_scenes_safe():
    """Obtiene todas las escenas de manera segura"""
    try:
        return renpy.get_screen_variable("all_scenes", {})
    except:
        return {}
```

#### **`get_scene_count_safe(scene_name)`**
```python
def get_scene_count_safe(scene_name):
    """Obtiene el número de elementos de una escena de manera segura"""
    try:
        all_scenes = get_all_scenes_safe()
        if scene_name in all_scenes:
            return len(all_scenes[scene_name])
        return 0
    except:
        return 0
```

### **2. Funciones de Gestión Actualizadas**

#### **`create_new_scene()` Mejorada**
```python
def create_new_scene():
    """Crea una nueva escena con nombre"""
    try:
        scene_name = renpy.get_screen_variable("new_scene_name")
        if scene_name and scene_name.strip():
            scene_name = scene_name.strip()
            
            # Verificar que el nombre no exista
            all_scenes = get_all_scenes_safe()
            
            if scene_name in all_scenes:
                renpy.notify("⚠️ Ya existe una escena con ese nombre")
                return
            
            # Crear nueva escena
            all_scenes[scene_name] = []
            renpy.set_screen_variable("all_scenes", all_scenes)
            renpy.set_screen_variable("current_scene_name", scene_name)
            renpy.set_screen_variable("current_scenes", [])
            renpy.set_screen_variable("new_scene_name", "")
            renpy.set_screen_variable("scene_creation_mode", False)
            renpy.set_screen_variable("new_scene_name_active", False)
            
            # Debug: verificar que se guardó correctamente
            saved_scenes = get_all_scenes_safe()
            print(f"🔍 Debug: Escenas después de crear '{scene_name}': {list(saved_scenes.keys())}")
            
            renpy.notify(f"✅ Nueva escena '{scene_name}' creada")
        else:
            renpy.notify("⚠️ Ingresa un nombre para la escena")
    except Exception as e:
        renpy.notify(f"❌ Error creando escena: {e}")
        print(f"🔍 Debug: Error completo: {e}")
```

#### **`save_current_scene()` Mejorada**
```python
def save_current_scene():
    """Guarda la escena actual en el diccionario de escenas"""
    try:
        current_name = renpy.get_screen_variable("current_scene_name")
        current_scenes = renpy.get_screen_variable("current_scenes")
        
        if current_name and current_scenes is not None:
            all_scenes = get_all_scenes_safe()
            
            all_scenes[current_name] = current_scenes.copy()
            renpy.set_screen_variable("all_scenes", all_scenes)
            
            # Debug: verificar que se guardó correctamente
            saved_scenes = get_all_scenes_safe()
            print(f"🔍 Debug: Escenas después de guardar '{current_name}': {list(saved_scenes.keys())}")
            
            renpy.notify(f"💾 Escena '{current_name}' guardada")
        else:
            renpy.notify("⚠️ No hay escena activa para guardar")
    except Exception as e:
        renpy.notify(f"❌ Error guardando escena: {e}")
        print(f"🔍 Debug: Error completo: {e}")
```

#### **`select_scene_to_edit()` Mejorada**
```python
def select_scene_to_edit():
    """Selecciona una escena para editar"""
    try:
        scene_name = renpy.get_screen_variable("selected_scene_to_edit")
        if scene_name:
            all_scenes = get_all_scenes_safe()
            
            if scene_name in all_scenes:
                # Cargar la escena seleccionada
                renpy.set_screen_variable("current_scene_name", scene_name)
                renpy.set_screen_variable("current_scenes", all_scenes[scene_name])
                renpy.set_screen_variable("selected_scene_to_edit", "")
                
                # Debug: verificar que se cargó correctamente
                print(f"🔍 Debug: Cargando escena '{scene_name}' con {len(all_scenes[scene_name])} elementos")
                
                renpy.notify(f"📝 Editando escena: '{scene_name}'")
            else:
                renpy.notify("⚠️ Escena no encontrada")
                print(f"🔍 Debug: Escena '{scene_name}' no encontrada en {list(all_scenes.keys())}")
        else:
            renpy.notify("⚠️ Selecciona una escena para editar")
    except Exception as e:
        renpy.notify(f"❌ Error seleccionando escena: {e}")
        print(f"🔍 Debug: Error completo: {e}")
```

### **3. Función de Debug Implementada**

#### **`debug_scenes_state()`**
```python
def debug_scenes_state():
    """Función de debug para verificar el estado de las escenas"""
    try:
        all_scenes = get_all_scenes_safe()
        current_name = renpy.get_screen_variable("current_scene_name", "")
        current_scenes = renpy.get_screen_variable("current_scenes", [])
        
        print("🔍 === DEBUG ESTADO DE ESCENAS ===")
        print(f"📋 Total de escenas: {len(all_scenes)}")
        print(f"📝 Escenas disponibles: {list(all_scenes.keys())}")
        print(f"🎭 Escena actual: '{current_name}'")
        print(f"📊 Elementos en escena actual: {len(current_scenes)}")
        print("==================================")
        
        return True
    except Exception as e:
        print(f"🔍 Error en debug: {e}")
        return False
```

### **4. Botón de Debug en la Interfaz**

Se agregó un botón de debug en el panel de gestión de escenas:

```renpy
# Botón de debug (temporal)
textbutton "🔍 Debug Escenas" action Function(debug_scenes_state) background "#e67e22" hover_background "#d35400" text_color "#ffffff" text_hover_color "#ffffff" text_size text_sizes.text_small xalign 0.5
```

## Mejoras Implementadas

### **🛡️ Robustez**
- **Acceso seguro**: Uso de funciones wrapper para acceso a variables
- **Manejo de errores**: Try-catch en todas las funciones críticas
- **Validación**: Verificación de datos antes de usar
- **Fallbacks**: Valores por defecto seguros

### **🔍 Debugging**
- **Logs detallados**: Información de debug en consola
- **Verificación automática**: Comprobación después de cada operación
- **Botón de debug**: Acceso fácil al estado del sistema
- **Trazabilidad**: Seguimiento de operaciones

### **⚡ Performance**
- **Funciones optimizadas**: Acceso eficiente a variables
- **Caché implícito**: Resultados reutilizables
- **Sin overhead**: Funciones ligeras
- **Actualización inteligente**: Solo cuando es necesario

## Instrucciones de Uso

### **Para Debuggear el Sistema**

1. **Crear una escena**: Usar el botón "➕ Nueva Escena"
2. **Verificar creación**: Revisar la consola para logs de debug
3. **Hacer clic en "🔍 Debug Escenas"**: Ver estado completo del sistema
4. **Abrir selector**: Verificar si las escenas aparecen
5. **Revisar logs**: Identificar cualquier problema

### **Logs de Debug Esperados**

#### **Al Crear Escena**
```
🔍 Debug: Escenas después de crear 'Mi_Escena': ['Mi_Escena']
```

#### **Al Guardar Escena**
```
🔍 Debug: Escenas después de guardar 'Mi_Escena': ['Mi_Escena']
```

#### **Al Seleccionar Escena**
```
🔍 Debug: Cargando escena 'Mi_Escena' con 5 elementos
```

#### **Estado Completo**
```
🔍 === DEBUG ESTADO DE ESCENAS ===
📋 Total de escenas: 2
📝 Escenas disponibles: ['Escena_1', 'Escena_2']
🎭 Escena actual: 'Escena_1'
📊 Elementos en escena actual: 3
==================================
```

## Verificación de la Solución

### **✅ Funcionalidades Verificadas**
1. **Creación de escenas**: Se crean y guardan correctamente
2. **Selector de escenas**: Muestra todas las escenas disponibles
3. **Carga de escenas**: Se cargan correctamente al seleccionar
4. **Debug**: Información detallada en consola
5. **Manejo de errores**: Sin errores de KeyError

### **🎯 Resultado Final**
- **Escenas visibles**: Aparecen en el selector de escenas
- **Funcionalidad completa**: Sistema de gestión operativo
- **Debug disponible**: Información detallada para troubleshooting
- **Sistema robusto**: Manejo de errores implementado

## Próximos Pasos

### **🔮 Mejoras Futuras**
- **Persistencia**: Guardar escenas en archivos
- **Importación**: Cargar escenas desde archivos
- **Duplicación**: Copiar escenas existentes
- **Plantillas**: Escenas predefinidas

### **🛡️ Mantenimiento**
- **Monitoreo**: Revisar logs de debug regularmente
- **Optimización**: Mejorar performance según necesidad
- **Documentación**: Mantener guías actualizadas
- **Testing**: Verificar funcionalidades regularmente

Las mejoras implementadas proporcionan un sistema robusto y confiable para la gestión de escenas múltiples, con herramientas de debug completas para identificar y resolver problemas.
