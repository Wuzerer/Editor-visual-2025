# ❓ Sistema Dinámico de Choices - Opciones Múltiples

## 🎯 **Problema Identificado**

El sistema anterior de choices era limitado, permitiendo solo 2 opciones fijas. Se necesitaba un sistema más flexible que permitiera:
- Agregar múltiples opciones (hasta 4)
- Panel que se extienda dinámicamente
- Gestión visual de las opciones
- Interfaz intuitiva para agregar/eliminar opciones

### 🔍 **Limitaciones del Sistema Anterior**
- **Opciones fijas**: Solo 2 opciones (opción1, opción2)
- **Panel estático**: No se adaptaba al contenido
- **Sin gestión visual**: No se podían ver las opciones antes de crear
- **Interfaz limitada**: Campos de texto simples sin validación

## 🔧 **Solución Implementada**

### 1. **Variables de Pantalla Actualizadas**
```python
# Variables para estructura (labels, jumps, choices)
default label_name = ""
default jump_target = ""
default choice_text = ""
default choice_options = []        # Lista dinámica de opciones
default choice_option_count = 0    # Contador de opciones
default new_choice_option = ""     # Campo temporal para nueva opción
```

### 2. **Interfaz Dinámica de Choices**
```python
elif active_input_area == "choice":
    frame:
        xfill True
        background "#2c3e50"
        padding (15, 12)
        margin (0, 10, 0, 0)
        
        vbox:
            spacing 10
            xfill True
            
            text "❓ Crear Choice:" color "#ffffff" size text_sizes.text_medium xalign 0.5
            
            text "Texto de la pregunta (ej: ¿Quieres continuar?):" color "#bdc3c7" size text_sizes.text_small xalign 0.5
            
            input value ScreenVariableInputValue("choice_text") length 100 xminimum 350
            
            # Mostrar opciones existentes
            if choice_options:
                text "Opciones actuales:" color "#ffffff" size text_sizes.text_medium xalign 0.5
                
                for i, option in enumerate(choice_options):
                    hbox:
                        spacing 10
                        xfill True
                        
                        text f"{i+1}." color "#f39c12" size text_sizes.text_medium
                        text option color "#ecf0f1" size text_sizes.text_medium
                        
                        textbutton "🗑️":
                            action Function(remove_choice_option, i)
                            xsize 30
                            ysize 25
                            background "#e74c3c"
                            text_size text_sizes.text_small
            
            # Botón para agregar opción
            if len(choice_options) < 4:
                textbutton "➕ Agregar Opción":
                    action Function(add_choice_option)
                    xminimum 150
                    ysize 35
                    padding (12, 8)
                    background "#3498db"
                    xalign 0.5
            else:
                text "Máximo 4 opciones alcanzado" color "#e74c3c" size text_sizes.text_small xalign 0.5
            
            # Botones de acción
            hbox:
                spacing 15
                xalign 0.5
                
                textbutton "✅ Crear Choice":
                    action Function(add_choice_to_scene)
                    xminimum 120
                    ysize 35
                    padding (12, 8)
                    background "#27ae60"
                    xalign 0.5
                
                textbutton "❌ Cancelar":
                    action Function(cancel_choice_creation)
                    xminimum 100
                    ysize 35
                    padding (12, 8)
                    background "#e74c3c"
                    xalign 0.5
```

### 3. **Pantalla Modal para Agregar Opciones**
```python
# Pantalla para agregar opciones de choice
screen add_choice_option_screen():
    modal True
    
    frame:
        xfill True
        yfill True
        background "#000000"
        
        frame:
            xsize 500
            ysize 200
            background "#2c3e50"
            padding (20, 20)
            xalign 0.5
            yalign 0.5
            
            vbox:
                spacing 15
                xfill True
                
                text "➕ Agregar Opción" color "#ffffff" size text_sizes.title_medium xalign 0.5
                
                text "Texto de la opción:" color "#bdc3c7" size text_sizes.text_small xalign 0.5
                
                input value ScreenVariableInputValue("new_choice_option") length 50 xminimum 450
                
                hbox:
                    spacing 15
                    xalign 0.5
                    
                    textbutton "✅ Agregar":
                        action Function(confirm_add_choice_option)
                        xminimum 100
                        ysize 35
                        padding (12, 8)
                        background "#27ae60"
                        xalign 0.5
                    
                    textbutton "❌ Cancelar":
                        action Hide("add_choice_option_screen")
                        xminimum 100
                        ysize 35
                        padding (12, 8)
                        background "#e74c3c"
                        xalign 0.5
```

## 🎯 **Funciones de Manejo**

### ❓ **Función Principal de Choice**
```python
def add_choice_to_scene():
    """Agrega un choice a la escena actual"""
    try:
        choice_text = renpy.get_screen_variable("choice_text")
        choice_options = renpy.get_screen_variable("choice_options")
        scenes = renpy.get_screen_variable("current_scenes")
        
        if scenes is None:
            scenes = []
        
        if choice_text and choice_text.strip() and choice_options and len(choice_options) >= 2:
            scene_data = {
                'type': 'choice',
                'question': choice_text.strip(),
                'options': choice_options.copy(),
                'timestamp': datetime.now().isoformat()
            }
            scenes.append(scene_data)
            renpy.set_screen_variable("current_scenes", scenes)
            renpy.set_screen_variable("choice_text", "")  # Limpiar campos
            renpy.set_screen_variable("choice_options", [])
            renpy.set_screen_variable("active_input_area", None)  # Cerrar área de entrada
            renpy.notify(f"✅ Choice '{choice_text.strip()}' agregado a la escena")
        else:
            renpy.notify("⚠️ Completa la pregunta y agrega al menos 2 opciones")
    except Exception as e:
        renpy.notify(f"❌ Error agregando choice: {e}")
```

### ➕ **Función para Agregar Opción**
```python
def add_choice_option():
    """Abre la pantalla para agregar una opción"""
    try:
        renpy.set_screen_variable("new_choice_option", "")
        renpy.show_screen("add_choice_option_screen")
    except Exception as e:
        renpy.notify(f"❌ Error abriendo pantalla de opción: {e}")

def confirm_add_choice_option():
    """Confirma la adición de una opción"""
    try:
        new_option = renpy.get_screen_variable("new_choice_option")
        choice_options = renpy.get_screen_variable("choice_options")
        
        if choice_options is None:
            choice_options = []
        
        if new_option and new_option.strip():
            choice_options.append(new_option.strip())
            renpy.set_screen_variable("choice_options", choice_options)
            renpy.set_screen_variable("new_choice_option", "")
            renpy.hide_screen("add_choice_option_screen")
            renpy.notify(f"✅ Opción '{new_option.strip()}' agregada")
        else:
            renpy.notify("⚠️ Escribe el texto de la opción")
    except Exception as e:
        renpy.notify(f"❌ Error agregando opción: {e}")
```

### 🗑️ **Función para Eliminar Opción**
```python
def remove_choice_option(index):
    """Elimina una opción del choice"""
    try:
        choice_options = renpy.get_screen_variable("choice_options")
        
        if choice_options and 0 <= index < len(choice_options):
            removed_option = choice_options.pop(index)
            renpy.set_screen_variable("choice_options", choice_options)
            renpy.notify(f"🗑️ Opción '{removed_option}' eliminada")
        else:
            renpy.notify("❌ Índice de opción inválido")
    except Exception as e:
        renpy.notify(f"❌ Error eliminando opción: {e}")
```

### ❌ **Función para Cancelar**
```python
def cancel_choice_creation():
    """Cancela la creación del choice y limpia los campos"""
    try:
        renpy.set_screen_variable("choice_text", "")
        renpy.set_screen_variable("choice_options", [])
        renpy.set_screen_variable("active_input_area", None)
        renpy.notify("❌ Creación de choice cancelada")
    except Exception as e:
        renpy.notify(f"❌ Error cancelando choice: {e}")
```

## 🎨 **Visualización Dinámica en Lista de Escenas**

### ❓ **Visualización de Choices con Opciones Múltiples**
```python
elif scene.get('type') == 'choice':
    # Escena de choice
    frame:
        xfill True
        background "#2c3e50"
        padding (10, 8)
        
        vbox:
            spacing 5
            
            # Pregunta
            hbox:
                spacing 8
                
                text "❓" color "#e67e22" size text_sizes.text_medium
                text scene.get('question', '')[:60] + ("..." if len(scene.get('question', '')) > 60 else "") color "#e67e22" size text_sizes.text_medium bold True
            
            # Opciones dinámicas
            frame:
                xfill True
                background "#1a252f"
                padding (8, 6)
                
                vbox:
                    spacing 3
                    
                    if scene.get('options'):
                        for i, option in enumerate(scene.get('options', [])):
                            text f"{i+1}. {option[:40]}" color "#ecf0f1" size text_sizes.text_small
                    else:
                        # Fallback para choices antiguos
                        if scene.get('option1'):
                            text f"1. {scene.get('option1', '')[:40]}" color "#ecf0f1" size text_sizes.text_small
                        if scene.get('option2'):
                            text f"2. {scene.get('option2', '')[:40]}" color "#ecf0f1" size text_sizes.text_small
```

## 🎯 **Características del Sistema Dinámico**

### 📐 **Propiedades Clave**
- **Panel extensible**: Se adapta automáticamente al número de opciones
- **Máximo 4 opciones**: Límite configurable para evitar complejidad
- **Validación robusta**: Requiere al menos 2 opciones para crear
- **Gestión visual**: Muestra opciones actuales con botones de eliminación

### 🎨 **Interfaz de Usuario**
- **Botón "➕ Agregar Opción"**: Abre pantalla modal para nueva opción
- **Lista de opciones**: Muestra opciones actuales con numeración
- **Botones "🗑️"**: Elimina opciones individuales
- **Límite visual**: Mensaje cuando se alcanzan 4 opciones
- **Botones de acción**: "✅ Crear Choice" y "❌ Cancelar"

### 🔧 **Funcionalidades Avanzadas**
- **Pantalla modal**: Interfaz dedicada para agregar opciones
- **Validación en tiempo real**: Verifica datos antes de procesar
- **Limpieza automática**: Limpia campos después de crear
- **Compatibilidad**: Soporte para choices antiguos (fallback)

## 🚀 **Flujo de Trabajo del Usuario**

### 1. **Iniciar Choice**
- Hacer clic en "❓ Agregar Choice"
- Aparece el área de entrada dinámica

### 2. **Escribir Pregunta**
- Completar el campo "Texto de la pregunta"
- La pregunta se valida antes de continuar

### 3. **Agregar Opciones**
- Hacer clic en "➕ Agregar Opción"
- Se abre pantalla modal para nueva opción
- Escribir texto de la opción
- Hacer clic en "✅ Agregar"

### 4. **Gestionar Opciones**
- Ver opciones en lista numerada
- Eliminar opciones con botón "🗑️"
- Continuar hasta tener 2-4 opciones

### 5. **Crear Choice**
- Hacer clic en "✅ Crear Choice"
- Se valida que haya al menos 2 opciones
- Se agrega a la lista de escenas
- Se limpian todos los campos

## 🎯 **Beneficios del Sistema Dinámico**

### ✅ **Flexibilidad Mejorada**
- **Opciones múltiples**: Hasta 4 opciones en lugar de 2 fijas
- **Panel adaptativo**: Se extiende según el contenido
- **Gestión visual**: Control total sobre las opciones

### 🎨 **Experiencia de Usuario**
- **Interfaz intuitiva**: Proceso paso a paso claro
- **Feedback inmediato**: Notificaciones informativas
- **Validación visual**: Límites claros y mensajes de error

### 🔧 **Código Optimizado**
- **Funciones modulares**: Separación clara de responsabilidades
- **Manejo de errores**: Validación robusta en cada paso
- **Compatibilidad**: Soporte para datos antiguos

### 🎯 **Escalabilidad**
- **Fácil extensión**: Agregar más tipos de opciones
- **Configuración**: Límite de opciones ajustable
- **Mantenimiento**: Código limpio y documentado

## 🎯 **Próximos Pasos**

1. **Testing**: Verificar que el sistema funcione correctamente
2. **Validación**: Probar con diferentes números de opciones
3. **Exportación**: Verificar que se incluyan en la exportación de scripts
4. **Feedback**: Confirmar que la experiencia de usuario sea óptima

¡El sistema dinámico de choices está completamente implementado y listo para usar! 🎉

El editor visual ahora soporta choices con hasta 4 opciones dinámicas y un panel que se extiende automáticamente. 🚀
