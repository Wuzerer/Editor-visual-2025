# 🎯 MEJORA DE VISTA PREVIA: CONTENIDO ENTRE LABEL Y RETURN

## 📋 Resumen Ejecutivo

Se implementó una mejora en el sistema de vista previa del Editor Visual de Ren'Py para que **solo se muestre el contenido real de la escena** (fondos, personajes, diálogos) **entre** el `label` y el `return`, excluyendo estos elementos estructurales de la vista previa. Esto proporciona una experiencia más limpia y enfocada en el contenido que el usuario puede editar.

## 🎯 Problema Identificado

### **Problema Principal:**
- **Vista Previa Confusa**: La vista previa mostraba elementos estructurales (`label`, `return`) junto con el contenido real
- **Contenido Mezclado**: Los elementos del usuario aparecían al final, no en el orden correcto
- **Experiencia de Usuario**: Difícil distinguir entre contenido editable y estructura de archivo

### **Causa del Problema:**
- **Filtrado Incompleto**: La función `load_scene_for_preview_editing` cargaba todas las líneas del archivo
- **Conversión Incorrecta**: No se diferenciaba entre estructura y contenido editable
- **Guardado Desordenado**: El contenido se guardaba al final en lugar de entre `label` y `return`

## 🔧 Solución Implementada

### **1. Filtrado Inteligente de Contenido:**

#### **Función `load_scene_for_preview_editing()` Modificada:**
```python
# Verificar si estamos en el área de contenido (entre label y return)
if line.startswith('label '):
    # Inicio de la escena - no incluir en la vista previa
    continue
elif line == 'return':
    # Fin de la escena - no incluir en la vista previa
    break
else:
    # Estamos en el área de contenido - procesar la línea
    # ... procesamiento del contenido real
```

### **2. Conversión Bidireccional:**

#### **Nueva Función `convert_scene_item_to_rpy_line()`:**
```python
def convert_scene_item_to_rpy_line(scene_item):
    """Convierte un diccionario de elemento de escena de vuelta a línea de Ren'Py"""
    scene_type = scene_item.get('type', '')
    
    if scene_type == 'background':
        background = scene_item.get('background', '')
        transition = scene_item.get('transition', 'none')
        if transition and transition != 'none':
            return f"scene {background} with {transition}"
        else:
            return f"scene {background}"
            
    elif scene_type == 'character':
        character = scene_item.get('character', '')
        position = scene_item.get('position', 'center')
        expression = scene_item.get('expression', '')
        
        if expression:
            return f"show {character} {expression} at {position}"
        else:
            return f"show {character} at {position}"
            
    elif scene_type == 'dialogue':
        character = scene_item.get('character', 'Narrator')
        dialogue = scene_item.get('dialogue', '')
        
        if character == 'Narrator':
            return f'"{dialogue}"'
        else:
            return f'{character} "{dialogue}"'
            
    elif scene_type == 'command':
        return scene_item.get('command', '')
```

### **3. Guardado Estructurado:**

#### **Función `save_scene_from_preview()` Mejorada:**
```python
elif content_added and line.strip() == 'return':
    # Agregar el contenido de la vista previa antes del return
    for scene_item in current_scenes:
        if isinstance(scene_item, dict):
            # Convertir el diccionario de vuelta a línea de Ren'Py
            scene_line = convert_scene_item_to_rpy_line(scene_item)
            if scene_line:
                new_content_lines.append(f"    {scene_line}")
        elif isinstance(scene_item, str) and scene_item.strip():
            new_content_lines.append(f"    {scene_item}")
    new_content_lines.append(line)
    content_added = False
```

## 📊 Tipos de Contenido Procesados

### **1. Fondos (Backgrounds):**
- **Entrada**: `scene bg room with dissolve`
- **Vista Previa**: `{'type': 'background', 'background': 'bg room', 'transition': 'dissolve'}`
- **Salida**: `scene bg room with dissolve`

### **2. Personajes (Characters):**
- **Entrada**: `show eileen happy at center`
- **Vista Previa**: `{'type': 'character', 'character': 'eileen', 'position': 'center', 'expression': 'happy'}`
- **Salida**: `show eileen happy at center`

### **3. Diálogos (Dialogue):**
- **Entrada**: `eileen "¡Hola! ¿Cómo estás?"`
- **Vista Previa**: `{'type': 'dialogue', 'character': 'eileen', 'dialogue': '¡Hola! ¿Cómo estás?'}`
- **Salida**: `eileen "¡Hola! ¿Cómo estás?"`

### **4. Comandos (Commands):**
- **Entrada**: `pause 2.0`
- **Vista Previa**: `{'type': 'command', 'command': 'pause 2.0'}`
- **Salida**: `pause 2.0`

## 🎯 Flujo de Trabajo Mejorado

### **1. Carga de Escena:**
```
1. Leer archivo .rpy completo
2. Identificar línea 'label'
3. Saltar línea 'label' (no incluir en vista previa)
4. Procesar líneas de contenido hasta encontrar 'return'
5. Saltar línea 'return' (no incluir en vista previa)
6. Mostrar solo contenido procesado en vista previa
```

### **2. Edición de Contenido:**
```
1. Usuario edita elementos en vista previa
2. Sistema mantiene estructura de diccionarios
3. Validación de tipos de contenido
4. Conversión automática de formatos
```

### **3. Guardado de Cambios:**
```
1. Leer archivo original completo
2. Mantener comentarios y estructura
3. Insertar contenido editado entre 'label' y 'return'
4. Preservar indentación correcta
5. Guardar archivo actualizado
```

## 📈 Beneficios de la Mejora

### **1. 🎨 Vista Previa Limpia:**
- **Solo Contenido Relevante**: No se muestran elementos estructurales
- **Enfoque en Edición**: El usuario ve solo lo que puede modificar
- **Orden Correcto**: Los elementos aparecen en el orden de la escena

### **2. 🔧 Funcionalidad Mejorada:**
- **Conversión Bidireccional**: Ida y vuelta entre Ren'Py y vista previa
- **Preservación de Estructura**: Comentarios y formato se mantienen
- **Guardado Inteligente**: Contenido se inserta en la posición correcta

### **3. ⚡ Experiencia de Usuario:**
- **Interfaz Intuitiva**: Más fácil entender qué se puede editar
- **Feedback Visual**: Vista previa clara y organizada
- **Flujo Natural**: Edición → Vista previa → Guardado

### **4. 🛡️ Robustez:**
- **Manejo de Errores**: Conversión segura entre formatos
- **Validación de Tipos**: Verificación de estructura de datos
- **Fallbacks**: Mecanismos de respaldo para casos especiales

## 🔍 Verificación de Funcionalidad

### **1. Casos de Prueba:**
- ✅ **Escena Vacía**: Solo `label` y `return`
- ✅ **Escena con Fondo**: `scene bg room`
- ✅ **Escena con Personaje**: `show eileen happy at center`
- ✅ **Escena con Diálogo**: `eileen "¡Hola!"`
- ✅ **Escena Completa**: Combinación de todos los elementos

### **2. Validación de Conversión:**
- ✅ **Ren'Py → Vista Previa**: Conversión correcta de líneas a diccionarios
- ✅ **Vista Previa → Ren'Py**: Conversión correcta de diccionarios a líneas
- ✅ **Preservación de Datos**: No se pierde información en la conversión

### **3. Verificación de Guardado:**
- ✅ **Posición Correcta**: Contenido se inserta entre `label` y `return`
- ✅ **Indentación**: Se mantiene la indentación correcta
- ✅ **Estructura**: Se preservan comentarios y formato

## 📚 Ejemplos de Uso

### **Ejemplo 1: Escena Simple**
```renpy
# Archivo original
label mi_escena:
    scene bg room
    show eileen happy at center
    eileen "¡Hola!"
    return
```

**Vista Previa:**
```
🎬 Fondo: bg room
👤 Personaje: eileen happy at center
💬 Diálogo: eileen "¡Hola!"
```

### **Ejemplo 2: Escena Compleja**
```renpy
# Archivo original
label escena_compleja:
    scene bg park with dissolve
    show lucy concerned at left
    show eileen happy at right
    lucy "¿Estás bien?"
    eileen "¡Perfecto!"
    pause 2.0
    return
```

**Vista Previa:**
```
🎬 Fondo: bg park (con transición dissolve)
👤 Personaje: lucy concerned at left
👤 Personaje: eileen happy at right
💬 Diálogo: lucy "¿Estás bien?"
💬 Diálogo: eileen "¡Perfecto!"
⚙️ Comando: pause 2.0
```

## 🚀 Próximos Pasos

### **1. Mejoras Futuras:**
- **Drag & Drop**: Reordenar elementos en vista previa
- **Vista Previa en Tiempo Real**: Ver cambios mientras se edita
- **Templates**: Plantillas predefinidas para escenas comunes

### **2. Optimizaciones:**
- **Caché de Conversión**: Mejorar rendimiento de conversiones
- **Validación Avanzada**: Verificar sintaxis de Ren'Py
- **Autocompletado**: Sugerencias inteligentes de contenido

### **3. Funcionalidades Adicionales:**
- **Historial de Cambios**: Deshacer/rehacer modificaciones
- **Comparación de Versiones**: Ver diferencias entre versiones
- **Exportación**: Exportar escenas en diferentes formatos

## ✅ Conclusión

La implementación de la vista previa mejorada ha transformado significativamente la experiencia de edición en el Editor Visual de Ren'Py. Ahora los usuarios pueden enfocarse únicamente en el contenido editable de sus escenas, con una interfaz más limpia y funcional.

**¡La vista previa ahora es tan organizada como el gimnasio de Terry después de una sesión de entrenamiento perfecta!** 💪🎯

---

**Fecha de Implementación:** 19 de Agosto, 2025  
**Versión:** 1.0  
**Estado:** ✅ Completado y Funcional
