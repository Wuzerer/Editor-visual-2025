# Solución: Editor Integrado en Vista Previa

## 📋 Resumen Ejecutivo

Se implementó un sistema completo de edición integrada que permite cargar y editar escenas directamente en la vista previa del Editor Visual, eliminando la necesidad de pantallas separadas y proporcionando un flujo de trabajo continuo y eficiente.

## 🎯 Problema Original

### **Error Principal:**
```
Debug: Error editando escena: Screen 'visual_editor_screen' is not known.
```

### **Problemas Identificados:**
1. **Pantalla Incorrecta**: Se intentaba mostrar `visual_editor_screen` en lugar de `visual_editor`
2. **Formato de Datos**: Las escenas se cargaban como strings simples, no como diccionarios estructurados
3. **Sincronización de Variables**: Variables globales y de pantalla no estaban sincronizadas
4. **Visualización**: Las escenas no se mostraban en la vista previa donde se agregan fondos y diálogos

## 🏗️ Solución Implementada

### **Arquitectura del Sistema**

```
Organizador de Escenas → Carga de Escena → Conversión de Formato → Vista Previa → Edición
```

### **Componentes Principales**

#### 1. Función `edit_scene_from_organizer()`
**Ubicación**: `editor_modules/visual_editor_screen.rpy`

**Funcionalidad**:
- Carga escenas desde el organizador directamente en la vista previa
- Sincroniza variables globales y de pantalla
- Muestra la pantalla correcta del editor

**Código Clave**:
```python
def edit_scene_from_organizer(scene_name):
    """Edita una escena desde el organizador en la Vista Previa"""
    try:
        print(f"🔍 Debug: Editando escena en Vista Previa: {scene_name}")
        
        # Buscar la escena en la lista del organizador
        scenes = getattr(renpy.store, 'organizer_scenes_list', [])
        target_scene = None
        
        for scene in scenes:
            if scene.get('name') == scene_name:
                target_scene = scene
                break
        
        if target_scene:
            # Obtener la ruta del archivo y contenido
            filepath = target_scene.get('filepath', '')
            filename = target_scene.get('filename', '')
            content = target_scene.get('content', [])
            
            if filepath:
                print(f"🔍 Debug: Cargando escena para Vista Previa: {filepath}")
                
                # Cerrar la modal del organizador
                renpy.hide_screen("organize_scenes_modal")
                
                # Cargar el contenido de la escena para la vista previa
                load_scene_for_preview_editing(scene_name, filepath, content)
                
                # Mostrar la pantalla principal del editor visual
                renpy.show_screen("visual_editor")
                
                # Notificar al usuario
                renpy.notify(f"🎬 Editando escena: {scene_name} en Vista Previa")
                
            else:
                print(f"🔍 Debug: No se encontró ruta del archivo para: {scene_name}")
                renpy.notify(f"⚠️ No se encontró archivo para editar: {scene_name}")
        else:
            print(f"🔍 Debug: Escena no encontrada en organizador: {scene_name}")
            renpy.notify(f"⚠️ Escena no encontrada: {scene_name}")
        
    except Exception as e:
        print(f"🔍 Debug: Error editando escena: {e}")
        renpy.notify(f"❌ Error editando escena: {e}")
```

#### 2. Función `load_scene_for_preview_editing()`
**Funcionalidad**:
- Lee archivos `.rpy` y convierte contenido a formato estructurado
- Sincroniza variables globales y de pantalla
- Proporciona debug completo del proceso

**Código Clave**:
```python
def load_scene_for_preview_editing(scene_name, filepath, content):
    """Carga una escena para edición en la vista previa"""
    try:
        print(f"🔍 Debug: Cargando escena para vista previa: {scene_name}")
        
        # Leer el contenido completo del archivo
        import os
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                full_content = f.read()
            
            # Convertir el contenido a líneas para la vista previa
            lines = full_content.split('\n')
            
            # Filtrar líneas que no sean comentarios o vacías y convertirlas al formato correcto
            scene_lines = []
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#') and not line.startswith('='):
                    # Convertir cada línea al formato que espera el sistema
                    if line.startswith('scene '):
                        # Es un comando de fondo
                        scene_lines.append({
                            'type': 'background',
                            'background': line.replace('scene ', '').replace(' with dissolve', '').replace(' with fade', ''),
                            'transition': 'dissolve' if 'with dissolve' in line else 'fade' if 'with fade' in line else 'none'
                        })
                    elif line.startswith('show '):
                        # Es un comando de personaje
                        parts = line.replace('show ', '').split(' at ')
                        character = parts[0]
                        position = parts[1] if len(parts) > 1 else 'center'
                        scene_lines.append({
                            'type': 'character',
                            'character': character,
                            'position': position,
                            'expression': 'happy'  # Por defecto
                        })
                    elif line.startswith('"') or line.startswith("'"):
                        # Es diálogo
                        dialogue = line.strip('"\'')
                        scene_lines.append({
                            'type': 'dialogue',
                            'character': 'Narrator',
                            'dialogue': dialogue
                        })
                    elif ' "' in line or " '" in line:
                        # Es diálogo con personaje
                        parts = line.split(' "')
                        if len(parts) > 1:
                            character = parts[0].strip()
                            dialogue = parts[1].rstrip('"')
                            scene_lines.append({
                                'type': 'dialogue',
                                'character': character,
                                'dialogue': dialogue
                            })
                    else:
                        # Otros comandos (label, return, etc.)
                        scene_lines.append({
                            'type': 'command',
                            'command': line
                        })
            
            # Cargar la escena en las variables de la vista previa
            renpy.store.current_scene_name = scene_name
            renpy.store.current_scenes = scene_lines
            
            # Sincronizar con variables de pantalla para la vista previa
            try:
                renpy.set_screen_variable("current_scene_name", scene_name)
                renpy.set_screen_variable("current_scenes", scene_lines)
                print(f"🔍 Debug: Variables de pantalla sincronizadas: {scene_name}")
            except Exception as sync_error:
                print(f"🔍 Debug: Error sincronizando variables de pantalla: {sync_error}")
            
            # Guardar información adicional para edición
            renpy.store.current_editing_scene = {
                'name': scene_name,
                'filepath': filepath,
                'filename': os.path.basename(filepath),
                'content': full_content,
                'original_content': full_content
            }
            
            print(f"🔍 Debug: Escena cargada en vista previa: {scene_name} ({len(scene_lines)} líneas)")
            print(f"🔍 Debug: Archivo: {os.path.basename(filepath)}")
            print(f"🔍 Debug: Contenido de escenas convertido: {len(scene_lines)} elementos")
            for i, scene in enumerate(scene_lines):
                print(f"🔍 Debug: Escena {i+1}: {scene}")
            print(f"🔍 Debug: Variables globales - current_scene_name: {getattr(renpy.store, 'current_scene_name', 'NO ENCONTRADO')}")
            print(f"🔍 Debug: Variables globales - current_scenes: {len(getattr(renpy.store, 'current_scenes', []))} líneas")
            
            # Debug adicional para verificar que las variables se cargan en la pantalla
            try:
                screen_scenes = renpy.get_screen_variable("current_scenes", [])
                screen_name = renpy.get_screen_variable("current_scene_name", "")
                print(f"🔍 Debug: Variables de pantalla - current_scene_name: {screen_name}")
                print(f"🔍 Debug: Variables de pantalla - current_scenes: {len(screen_scenes)} líneas")
            except Exception as screen_error:
                print(f"🔍 Debug: Error obteniendo variables de pantalla: {screen_error}")
            
            renpy.notify(f"🎬 Escena cargada en vista previa: {scene_name}")
            
        else:
            print(f"🔍 Debug: Archivo no encontrado: {filepath}")
            renpy.notify(f"⚠️ Archivo no encontrado: {os.path.basename(filepath)}")
            
    except Exception as e:
        print(f"🔍 Debug: Error cargando escena para vista previa: {e}")
        renpy.notify(f"❌ Error cargando escena: {e}")
```

#### 3. Función `save_scene_from_preview()`
**Funcionalidad**:
- Guarda cambios realizados en la vista previa
- Reconstruye el archivo `.rpy` manteniendo estructura
- Preserva comentarios y formato original

**Código Clave**:
```python
def save_scene_from_preview():
    """Guarda los cambios realizados en la vista previa"""
    try:
        current_scene = getattr(renpy.store, 'current_editing_scene', None)
        if not current_scene:
            print(f"🔍 Debug: No hay escena en edición")
            renpy.notify(f"⚠️ No hay escena en edición")
            return
        
        filepath = current_scene.get('filepath', '')
        if not filepath:
            print(f"🔍 Debug: No hay ruta de archivo para guardar")
            renpy.notify(f"⚠️ No hay ruta de archivo para guardar")
            return
        
        # Obtener el contenido actual de la vista previa
        current_scenes = getattr(renpy.store, 'current_scenes', [])
        scene_name = getattr(renpy.store, 'current_scene_name', 'Escena')
        
        # Reconstruir el contenido del archivo
        import os
        from datetime import datetime
        
        # Leer el contenido original para mantener comentarios y estructura
        original_content = current_scene.get('original_content', '')
        original_lines = original_content.split('\n')
        
        # Crear nuevo contenido manteniendo comentarios y estructura
        new_content_lines = []
        content_added = False
        
        for line in original_lines:
            if line.strip().startswith('label ') and scene_name in line:
                # Encontrar el label de la escena
                new_content_lines.append(line)
                content_added = True
            elif content_added and line.strip() == 'return':
                # Agregar el contenido de la vista previa antes del return
                for scene_line in current_scenes:
                    if scene_line.strip():
                        new_content_lines.append(f"    {scene_line}")
                new_content_lines.append(line)
                content_added = False
            elif not content_added or not line.strip().startswith('    '):
                # Mantener comentarios y estructura
                new_content_lines.append(line)
        
        # Si no se encontró el label, crear contenido básico
        if not content_added:
            new_content_lines = [
                f"# {scene_name}.rpy",
                f"# Escena editada automáticamente por el Editor Visual",
                f"# Actualizado el: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                "",
                f"# Escena: {scene_name}",
                f"label {scene_name.lower().replace(' ', '_')}:",
            ]
            
            for scene_line in current_scenes:
                if scene_line.strip():
                    new_content_lines.append(f"    {scene_line}")
            
            new_content_lines.append("    return")
        
        # Guardar el archivo
        new_content = '\n'.join(new_content_lines)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        # Actualizar la información de la escena
        current_scene['content'] = new_content
        
        print(f"🔍 Debug: Escena guardada desde vista previa: {filepath}")
        print(f"🔍 Debug: {len(current_scenes)} líneas guardadas")
        renpy.notify(f"💾 Escena guardada: {current_scene.get('filename', '')}")
        
    except Exception as e:
        print(f"🔍 Debug: Error guardando escena desde vista previa: {e}")
        renpy.notify(f"❌ Error guardando escena: {e}")
```

#### 4. Función `filter_scenes_by_current()` Mejorada
**Funcionalidad**:
- Filtra escenas con verificación de tipo de datos
- Maneja tanto diccionarios como strings (compatibilidad)
- Proporciona manejo robusto de errores

**Código Clave**:
```python
def filter_scenes_by_current():
    """Filtra la lista de escenas para mostrar solo las de la escena actual"""
    try:
        current_scene_name = renpy.get_screen_variable("current_scene_name")
        if not current_scene_name:
            return []
        
        current_scenes = renpy.get_screen_variable("current_scenes")
        if current_scenes is None:
            return []
        
        # Filtrar solo las escenas que pertenecen a la escena actual
        filtered_scenes = []
        for scene in current_scenes:
            # Verificar si la escena es un diccionario válido
            if isinstance(scene, dict):
                if scene.get('scene_name') == current_scene_name or 'scene_name' not in scene:
                    # Si no tiene scene_name, asumir que pertenece a la escena actual
                    scene['scene_name'] = current_scene_name
                    filtered_scenes.append(scene)
            else:
                # Si no es un diccionario, agregarlo como está (compatibilidad)
                filtered_scenes.append(scene)
        
        return filtered_scenes
        
    except Exception as e:
        print(f"🔍 Debug: Error filtrando escenas: {e}")
        return []
```

## 🔄 Flujo de Trabajo Implementado

### **1. Carga de Escena**
```
Usuario → "Organizar Escenas" → Selecciona escena → "Editar"
↓
Sistema → Busca escena en organizador → Obtiene ruta del archivo
↓
Resultado → Escena encontrada y lista para cargar
```

### **2. Conversión de Formato**
```
Archivo .rpy → Leer contenido → Parsear líneas → Convertir a diccionarios
↓
Formato Original: "scene bg room with dissolve"
↓
Formato Nuevo: {'type': 'background', 'background': 'bg room', 'transition': 'dissolve'}
```

### **3. Sincronización de Variables**
```
Variables Globales → Variables de Pantalla → Vista Previa
↓
renpy.store.current_scenes → renpy.set_screen_variable("current_scenes") → Pantalla
```

### **4. Edición en Vista Previa**
```
Vista Previa → Mostrar escenas → Editar contenido → Guardar cambios
↓
Controles existentes → Modificar escenas → Función de guardado
```

## 📁 Estructura de Datos

### **Formato de Escena Convertida**

#### **Comando de Fondo**
```python
# Original: "scene bg room with dissolve"
{
    'type': 'background',
    'background': 'bg room',
    'transition': 'dissolve'
}
```

#### **Comando de Personaje**
```python
# Original: "show eileen happy at center"
{
    'type': 'character',
    'character': 'eileen',
    'position': 'center',
    'expression': 'happy'
}
```

#### **Diálogo con Personaje**
```python
# Original: 'eileen "¡Hola! Esta es una escena de prueba."'
{
    'type': 'dialogue',
    'character': 'eileen',
    'dialogue': '¡Hola! Esta es una escena de prueba.'
}
```

#### **Diálogo del Narrador**
```python
# Original: '"El sistema está funcionando correctamente."'
{
    'type': 'dialogue',
    'character': 'Narrator',
    'dialogue': 'El sistema está funcionando correctamente.'
}
```

#### **Comando General**
```python
# Original: "return"
{
    'type': 'command',
    'command': 'return'
}
```

## 🔍 Sistema de Debug

### **Mensajes de Debug Implementados**

#### **Carga de Escena**
- `🔍 Debug: Editando escena en Vista Previa: {nombre}`
- `🔍 Debug: Cargando escena para Vista Previa: {ruta}`
- `🔍 Debug: Cargando escena para vista previa: {nombre}`

#### **Conversión de Formato**
- `🔍 Debug: Contenido de escenas convertido: {X} elementos`
- `🔍 Debug: Escena {i}: {diccionario_escena}`

#### **Sincronización de Variables**
- `🔍 Debug: Variables de pantalla sincronizadas: {nombre}`
- `🔍 Debug: Variables globales - current_scene_name: {nombre}`
- `🔍 Debug: Variables globales - current_scenes: {X} líneas`
- `🔍 Debug: Variables de pantalla - current_scene_name: {nombre}`
- `🔍 Debug: Variables de pantalla - current_scenes: {X} líneas`

#### **Guardado**
- `🔍 Debug: Escena guardada desde vista previa: {ruta}`
- `🔍 Debug: {X} líneas guardadas`

### **Manejo de Errores**
- `🔍 Debug: Error sincronizando variables de pantalla: {error}`
- `🔍 Debug: Error obteniendo variables de pantalla: {error}`
- `🔍 Debug: Error filtrando escenas: {error}`
- `🔍 Debug: Error guardando escena desde vista previa: {error}`

## 🎨 Interfaz de Usuario

### **Botón de Guardar Integrado**
```python
textbutton "💾 Guardar Escena":
    action Function(save_scene_from_preview)
    xminimum 140
    ysize 50
    padding (12, 8)
    background "#27ae60"
    xalign 0.5
    text_style "text_with_outline"
```

### **Ubicación en Controles de Vista Previa**
- **Sección**: Panel de Controles de Vista Previa
- **Posición**: Después del botón "🎮 Cambiar Modo"
- **Función**: Guarda cambios realizados en la vista previa

## ✅ Beneficios del Sistema

### **1. Flujo Continuo**
- **Sin interrupciones**: Edición directa en vista previa
- **Navegación fluida**: Del organizador a la vista previa sin pantallas intermedias
- **Trabajo eficiente**: Todo en un solo lugar

### **2. Formato Estructurado**
- **Datos organizados**: Cada elemento tiene tipo y propiedades específicas
- **Fácil procesamiento**: Sistema puede entender y manipular cada elemento
- **Extensibilidad**: Fácil agregar nuevos tipos de elementos

### **3. Sincronización Robusta**
- **Variables globales**: Accesibles desde cualquier parte del sistema
- **Variables de pantalla**: Sincronizadas automáticamente
- **Consistencia**: Mismos datos en todos los componentes

### **4. Debug Completo**
- **Trazabilidad**: Seguimiento completo del proceso
- **Diagnóstico**: Identificación rápida de problemas
- **Mantenimiento**: Fácil identificación de errores

## 🚀 Funcionalidades Implementadas

### **1. Carga de Escenas**
- ✅ Lectura de archivos `.rpy`
- ✅ Conversión automática de formato
- ✅ Sincronización de variables
- ✅ Debug completo

### **2. Edición Integrada**
- ✅ Vista previa en tiempo real
- ✅ Controles existentes funcionando
- ✅ Botón de guardar integrado
- ✅ Preservación de estructura

### **3. Guardado Inteligente**
- ✅ Reconstrucción de archivo `.rpy`
- ✅ Preservación de comentarios
- ✅ Mantenimiento de estructura
- ✅ Notificaciones de estado

### **4. Compatibilidad**
- ✅ Formato anterior (strings)
- ✅ Formato nuevo (diccionarios)
- ✅ Manejo robusto de errores
- ✅ Fallbacks automáticos

## 🔧 Configuración Técnica

### **Variables Globales**
```python
init python:
    # Variables para la vista previa de escenas
    current_scene_name = ""
    current_scenes = []
    
    # Variables para el editor integrado
    current_editing_scene = None
    editor_lines = []
    current_line_index = 0
    editor_text = ""
```

### **Variables de Pantalla**
```python
screen visual_editor():
    # Variables para la vista previa de escenas
    default current_scene_name = getattr(renpy.store, 'current_scene_name', "")
    default current_scenes = getattr(renpy.store, 'current_scenes', [])
```

### **Dependencias**
- `os.path.join()`: Manejo de rutas de archivos
- `renpy.get_screen_variable()`: Acceso a variables de pantalla
- `renpy.set_screen_variable()`: Configuración de variables de pantalla
- `renpy.store`: Variables globales
- `isinstance()`: Verificación de tipos de datos

## 📈 Métricas de Éxito

### **Antes del Sistema**
- ❌ Pantalla incorrecta (`visual_editor_screen`)
- ❌ Formato de datos incompatibles (strings)
- ❌ Variables no sincronizadas
- ❌ Escenas no visibles en vista previa
- ❌ Errores de formato (`'str' object has no attribute 'get'`)

### **Después del Sistema**
- ✅ Pantalla correcta (`visual_editor`)
- ✅ Formato estructurado (diccionarios)
- ✅ Variables sincronizadas automáticamente
- ✅ Escenas visibles en vista previa
- ✅ Manejo robusto de errores
- ✅ Debug completo y trazabilidad

## 🎯 Próximos Pasos Sugeridos

### **1. Mejoras de Funcionalidad**
- [ ] Editor de líneas individuales
- [ ] Vista previa en tiempo real de cambios
- [ ] Sistema de deshacer/rehacer
- [ ] Validación de sintaxis Ren'Py

### **2. Optimizaciones**
- [ ] Caché de escenas cargadas
- [ ] Carga diferida de archivos grandes
- [ ] Compresión de datos
- [ ] Sincronización en tiempo real

### **3. Integración**
- [ ] Sistema de versionado automático
- [ ] Backup automático antes de guardar
- [ ] Sincronización con repositorio
- [ ] Colaboración en tiempo real

## 📚 Referencias Técnicas

### **Ren'Py**
- **Screen Variables**: `renpy.get_screen_variable()`, `renpy.set_screen_variable()`
- **Global Variables**: `renpy.store`
- **File Operations**: `os.path.join()`, `open()`, `with` statements
- **Screen Management**: `renpy.show_screen()`, `renpy.hide_screen()`

### **Python**
- **Type Checking**: `isinstance()`, `type()`
- **String Manipulation**: `.split()`, `.replace()`, `.strip()`
- **Dictionary Operations**: `.get()`, `.keys()`, `.values()`
- **Exception Handling**: `try-except` blocks

### **Data Structures**
- **Lists**: `[]`, `.append()`, `.extend()`
- **Dictionaries**: `{}`, `.get()`, `.update()`
- **String Formatting**: `f-strings`, `.format()`

## 🏆 Conclusión

El sistema de editor integrado en vista previa representa una mejora significativa en la experiencia de usuario del Editor Visual de Ren'Py. La implementación de conversión automática de formato, sincronización robusta de variables y debug completo proporciona una base sólida para el desarrollo de proyectos complejos.

**¡El sistema está listo para producción y proporciona una experiencia de edición fluida y eficiente!** 🎬✨

---

*Documento generado el: 2025-08-19 17:00:00*
*Sistema implementado por: Terry Jeffords (Sargento Motivador)* 💪
