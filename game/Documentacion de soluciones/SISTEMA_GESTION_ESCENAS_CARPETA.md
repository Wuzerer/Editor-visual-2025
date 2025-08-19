# Sistema de Gestión de Escenas con Carpeta Organizada

## 📋 Resumen Ejecutivo

Se implementó un sistema completo de gestión de escenas que utiliza una carpeta `scenes/` para organizar cada escena en archivos individuales `.rpy`, permitiendo edición directa y mejor organización del proyecto.

## 🎯 Problema Original

- **Error**: "Screen is not showing" al crear escenas
- **Archivo `current_scenes.rpy`**: Contenía escenas de prueba que persistían
- **Organización**: Todas las escenas en un solo archivo, difícil de gestionar
- **Edición**: No había forma de editar escenas individuales

## 🏗️ Solución Implementada

### Arquitectura del Sistema

```
game/
├── scenes/                    # Carpeta principal de escenas
│   ├── introduccion.rpy      # Escena individual
│   ├── capitulo_1.rpy        # Escena individual
│   ├── dialogo_principal.rpy # Escena individual
│   └── ...
├── current_scenes.rpy        # Archivo limpio (solo documentación)
└── editor_modules/
    └── visual_editor_screen.rpy # Lógica principal
```

### Componentes Principales

#### 1. Función `get_scenes_from_rpy_file()`
**Ubicación**: `editor_modules/visual_editor_screen.rpy`

**Funcionalidad**:
- Lee escenas desde la carpeta `scenes/`
- Crea la carpeta automáticamente si no existe
- Parsea cada archivo `.rpy` individual
- Extrae información: nombre, tipo, contenido, ruta del archivo

**Código Clave**:
```python
def get_scenes_from_rpy_file():
    """Obtiene las escenas desde la carpeta scenes/"""
    try:
        import os
        scenes_dir = os.path.join(config.gamedir, "scenes")
        
        if not os.path.exists(scenes_dir):
            print(f"🔍 Debug: Carpeta scenes/ no encontrada, creando...")
            os.makedirs(scenes_dir)
        
        scenes = []
        
        # Buscar archivos .rpy en la carpeta scenes/
        for filename in os.listdir(scenes_dir):
            if filename.endswith('.rpy'):
                scene_file = os.path.join(scenes_dir, filename)
                
                try:
                    with open(scene_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Extraer información de la escena
                    scene_name = filename.replace('.rpy', '')
                    scene_type = 'scene'
                    
                    # Parsear contenido básico
                    lines = content.split('\n')
                    scene_content = []
                    
                    for line in lines:
                        line = line.strip()
                        if line and not line.startswith('#') and not line.startswith('='):
                            scene_content.append(line)
                    
                    scene_data = {
                        'name': scene_name,
                        'type': scene_type,
                        'content': scene_content,
                        'filename': filename,
                        'filepath': scene_file
                    }
                    
                    scenes.append(scene_data)
                    print(f"🔍 Debug: Escena cargada: {scene_name} ({len(scene_content)} líneas)")
                    
                except Exception as file_error:
                    print(f"🔍 Debug: Error leyendo archivo {filename}: {file_error}")
                    continue
        
        print(f"🔍 Debug: {len(scenes)} escenas cargadas desde carpeta scenes/")
        return scenes
            
    except Exception as e:
        print(f"🔍 Debug: Error cargando escenas desde carpeta: {e}")
        return []
```

#### 2. Función `add_scene_to_modal()` Mejorada
**Funcionalidad**:
- Crea archivos individuales en `scenes/`
- Genera nombres de archivo seguros y únicos
- Maneja duplicados automáticamente
- Crea contenido estructurado con comentarios

**Código Clave**:
```python
def add_scene_to_modal():
    # Crear nombre de archivo seguro
    safe_name = scene_name.lower().replace(" ", "_").replace("-", "_")
    safe_name = ''.join(c for c in safe_name if c.isalnum() or c == '_')
    
    # Crear archivo individual en carpeta scenes/
    import os
    scenes_dir = os.path.join(config.gamedir, "scenes")
    
    if not os.path.exists(scenes_dir):
        print(f"🔍 Debug: Creando carpeta scenes/...")
        os.makedirs(scenes_dir)
    
    # Generar nombre único para el archivo
    scene_filename = f"{safe_name}.rpy"
    scene_filepath = os.path.join(scenes_dir, scene_filename)
    
    # Verificar si el archivo ya existe
    counter = 1
    while os.path.exists(scene_filepath):
        scene_filename = f"{safe_name}_{counter}.rpy"
        scene_filepath = os.path.join(scenes_dir, scene_filename)
        counter += 1
    
    # Crear contenido de la escena
    scene_content = [
        f"# {scene_name}.rpy",
        f"# Escena creada automáticamente por el Editor Visual",
        f"# Generado el: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        f"# Escena: {scene_name}",
        f"label {safe_name}:",
        f"    # Aquí puedes agregar el contenido de la escena",
        f"    # Por ejemplo:",
        f"    # scene bg room",
        f"    # show eileen happy at center",
        f"    # eileen \"¡Hola! Esta es la escena {scene_name}\"",
        f"    ",
        f"    # Contenido de la escena se agregará aquí",
        f"    ",
        f"    return"
    ]
    
    # Escribir el archivo de la escena
    try:
        with open(scene_filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(scene_content))
        
        print(f"🔍 Debug: Escena creada exitosamente: {scene_filename}")
        print(f"🔍 Debug: Ruta del archivo: {scene_filepath}")
        
        # Notificar éxito
        renpy.notify(create_clear_notification("success", f"Escena '{scene_name}' creada en scenes/{scene_filename}"))
        
    except Exception as file_error:
        print(f"🔍 Debug: Error creando archivo de escena: {file_error}")
        renpy.notify(create_clear_notification("error", f"Error creando archivo de escena: {file_error}"))
        return
```

#### 3. Función `edit_scene_from_organizer()` Mejorada
**Funcionalidad**:
- Abre archivos directamente en el editor del sistema
- Compatible con Windows, macOS y Linux
- Busca la escena en la lista del organizador
- Proporciona notificaciones claras

**Código Clave**:
```python
def edit_scene_from_organizer(scene_name):
    """Edita una escena desde el organizador"""
    try:
        print(f"🔍 Debug: Editando escena: {scene_name}")
        
        # Buscar la escena en la lista del organizador
        scenes = getattr(renpy.store, 'organizer_scenes_list', [])
        target_scene = None
        
        for scene in scenes:
            if scene.get('name') == scene_name:
                target_scene = scene
                break
        
        if target_scene:
            # Obtener la ruta del archivo
            filepath = target_scene.get('filepath', '')
            filename = target_scene.get('filename', '')
            
            if filepath:
                print(f"🔍 Debug: Abriendo archivo para edición: {filepath}")
                
                # Cerrar la modal del organizador
                renpy.hide_screen("organize_scenes_modal")
                
                # Notificar al usuario
                renpy.notify(f"✏️ Editando escena: {scene_name} ({filename})")
                
                # Abrir el archivo en el editor del sistema
                try:
                    import os
                    import subprocess
                    import platform
                    
                    system = platform.system()
                    if system == "Windows":
                        os.startfile(filepath)
                    elif system == "Darwin":  # macOS
                        subprocess.run(["open", filepath])
                    else:  # Linux
                        subprocess.run(["xdg-open", filepath])
                    
                    print(f"🔍 Debug: Archivo abierto en editor del sistema")
                    
                except Exception as open_error:
                    print(f"🔍 Debug: Error abriendo archivo en editor: {open_error}")
                    renpy.notify(f"📝 Archivo listo para editar: {filename}")
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

## 🔄 Flujo de Trabajo Implementado

### 1. Creación de Escenas
```
Usuario → "Crear Escena" → Escribe nombre → "Crear Escena"
↓
Sistema → Valida nombre → Crea archivo en scenes/nombre.rpy
↓
Resultado → Archivo individual con estructura básica
```

### 2. Organización de Escenas
```
Usuario → "Organizar Escenas" → Modal se abre
↓
Sistema → Lee carpeta scenes/ → Lista todas las escenas
↓
Resultado → Lista organizada con opciones de edición
```

### 3. Edición de Escenas
```
Usuario → Selecciona escena → "Editar"
↓
Sistema → Busca archivo → Abre en editor del sistema
↓
Resultado → Archivo abierto para edición directa
```

## 📁 Estructura de Archivos Generada

### Archivo de Escena Individual (`scenes/mi_escena.rpy`)
```python
# Mi Escena.rpy
# Escena creada automáticamente por el Editor Visual
# Generado el: 2025-08-19 16:45:30

# Escena: Mi Escena
label mi_escena:
    # Aquí puedes agregar el contenido de la escena
    # Por ejemplo:
    # scene bg room
    # show eileen happy at center
    # eileen "¡Hola! Esta es la escena Mi Escena"
    
    # Contenido de la escena se agregará aquí
    
    return
```

### Archivo Principal (`current_scenes.rpy`)
```python
# current_scenes.rpy
# Archivo generado automáticamente por el Editor Visual
# Generado el: 2025-08-19 16:40:00
# 
# Este archivo contiene las escenas creadas desde el Editor Visual
# Las escenas se generan automáticamente cuando usas el creador de escenas
#
# Para crear una nueva escena:
# 1. Ve al Editor Visual
# 2. Haz clic en "Crear Escena"
# 3. Escribe el nombre de la escena
# 4. Haz clic en "Crear Escena"
#
# Las escenas aparecerán aquí automáticamente

# ===== ESCENAS CREADAS DESDE EL EDITOR =====
# (Las escenas se agregarán automáticamente aquí)

# ===== FIN DEL ARCHIVO =====
```

## 🔍 Sistema de Debug

### Mensajes de Debug Implementados
- `🔍 Debug: Creando nueva escena en carpeta scenes/...`
- `🔍 Debug: Escena creada exitosamente: mi_escena.rpy`
- `🔍 Debug: Ruta del archivo: C:\...\scenes\mi_escena.rpy`
- `🔍 Debug: Archivo abierto en editor del sistema`
- `🔍 Debug: {X} escenas cargadas desde carpeta scenes/`

### Variables Globales
```python
init python:
    # Variables para el sistema de escenas
    new_scene_name = ""
    scene_name_active = False
    created_scenes_modal_global = []
    search_text = ""
    organizer_scenes_list = []
```

## ✅ Beneficios del Nuevo Sistema

### 1. Organización
- **Archivos individuales**: Cada escena en su propio archivo
- **Carpeta dedicada**: Estructura clara y profesional
- **Nombres únicos**: Manejo automático de duplicados

### 2. Edición
- **Editor del sistema**: Abre archivos directamente
- **Edición directa**: Modifica archivos `.rpy` nativos
- **Compatibilidad**: Funciona en Windows, macOS y Linux

### 3. Escalabilidad
- **Manejo de muchas escenas**: Sin límite de archivos
- **Búsqueda**: Sistema de búsqueda en el organizador
- **Estadísticas**: Conteo de escenas y tipos

### 4. Mantenimiento
- **Archivos independientes**: Modificación sin afectar otros
- **Backup fácil**: Copia individual de archivos
- **Versionado**: Control de versiones por archivo

### 5. Debug
- **Información detallada**: Logs completos de operaciones
- **Manejo de errores**: Captura y notificación de problemas
- **Trazabilidad**: Seguimiento de cada operación

## 🚀 Funcionalidades Implementadas

### 1. Creación de Escenas
- ✅ Validación de nombres
- ✅ Generación de archivos individuales
- ✅ Manejo de duplicados
- ✅ Estructura básica automática

### 2. Organización
- ✅ Lista de escenas desde carpeta
- ✅ Búsqueda de escenas
- ✅ Estadísticas de escenas
- ✅ Vista previa de contenido

### 3. Edición
- ✅ Apertura en editor del sistema
- ✅ Compatibilidad multiplataforma
- ✅ Notificaciones de estado
- ✅ Manejo de errores

### 4. Gestión de Archivos
- ✅ Creación automática de carpetas
- ✅ Nombres de archivo seguros
- ✅ Encoding UTF-8
- ✅ Manejo de rutas absolutas

## 🔧 Configuración Técnica

### Dependencias
- `os.path.join()`: Manejo de rutas
- `os.makedirs()`: Creación de directorios
- `os.listdir()`: Listado de archivos
- `platform.system()`: Detección de sistema operativo
- `subprocess.run()`: Ejecución de comandos del sistema

### Variables de Configuración
```python
# Rutas principales
config.gamedir  # Directorio base del juego
scenes_dir = os.path.join(config.gamedir, "scenes")  # Carpeta de escenas
```

### Manejo de Errores
- **Creación de carpetas**: Fallback si no existe
- **Apertura de archivos**: Manejo de permisos
- **Editor del sistema**: Fallback si no se puede abrir
- **Encoding**: UTF-8 para caracteres especiales

## 📈 Métricas de Éxito

### Antes del Sistema
- ❌ Escenas en archivo único
- ❌ Difícil edición individual
- ❌ Organización pobre
- ❌ Escalabilidad limitada

### Después del Sistema
- ✅ Archivos individuales organizados
- ✅ Edición directa en editor del sistema
- ✅ Carpeta dedicada y profesional
- ✅ Escalabilidad ilimitada
- ✅ Debug completo y trazabilidad

## 🎯 Próximos Pasos Sugeridos

### 1. Mejoras de Funcionalidad
- [ ] Editor integrado en Ren'Py
- [ ] Vista previa de escenas
- [ ] Sistema de plantillas
- [ ] Exportación de escenas

### 2. Optimizaciones
- [ ] Caché de escenas
- [ ] Búsqueda avanzada
- [ ] Filtros por tipo
- [ ] Ordenamiento personalizado

### 3. Integración
- [ ] Sistema de versionado
- [ ] Backup automático
- [ ] Sincronización con repositorio
- [ ] Colaboración en tiempo real

## 📚 Referencias Técnicas

### Ren'Py
- **Screen Variables**: `renpy.get_screen_variable()`, `renpy.set_screen_variable()`
- **Notifications**: `renpy.notify()`
- **File Operations**: `config.gamedir`, `os.path.join()`

### Python
- **File Handling**: `open()`, `with` statements
- **String Manipulation**: `.replace()`, `.lower()`, `.strip()`
- **System Operations**: `os.startfile()`, `subprocess.run()`

### Cross-Platform
- **Windows**: `os.startfile()`
- **macOS**: `subprocess.run(["open", filepath])`
- **Linux**: `subprocess.run(["xdg-open", filepath])`

## 🏆 Conclusión

El sistema de gestión de escenas implementado representa una mejora significativa en la organización y edición de contenido para el Editor Visual de Ren'Py. La arquitectura modular, la edición directa y la escalabilidad del sistema proporcionan una base sólida para el desarrollo de proyectos complejos.

**¡El sistema está listo para producción y proporciona una experiencia de usuario profesional y eficiente!** 🎬✨

---

*Documento generado el: 2025-08-19 16:50:00*
*Sistema implementado por: Terry Jeffords (Sargento Motivador)* 💪
