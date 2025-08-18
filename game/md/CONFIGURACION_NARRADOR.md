# 📖 Configuración del Narrador

## 🎯 **Descripción**

Se ha implementado un **panel completo de configuración del narrador** en la sección de "Vista Previa" que permite personalizar completamente cómo se muestran los diálogos del narrador. Esto incluye diferentes estilos de presentación, posicionamiento, colores y tamaños de texto, dando mayor flexibilidad creativa a las historias.

## 🎮 **Panel de Configuración del Narrador**

### 📍 **Ubicación**
- **Sección**: "Vista Previa" (pestaña 🎮)
- **Posición**: Debajo del panel de transiciones
- **Tamaño**: 400px de ancho x 350px de alto
- **Color**: Fondo gris oscuro (#34495e)

### 🎯 **Estructura del Panel**
```
┌─────────────────────────────────────────┐
│ 📖 Configuración del Narrador           │
├─────────────────────────────────────────┤
│ 📝 Estilo de Narrador:                  │
│ [📋 Textbox] [💬 Flotante] [📜 Pantalla]│
│                                         │
│ 📍 Posición del Texto:                  │
│ [⬅️ Izquierda] [⬆️ Centro] [➡️ Derecha] │
│ [⬆️ Arriba] [⬇️ Abajo]                 │
│                                         │
│ 🎨 Color del Texto:                     │
│ [⚪ Blanco] [🟡 Amarillo] [🔵 Azul] [🟢 Verde]│
│                                         │
│ 📏 Tamaño del Texto:                    │
│ [📝 Pequeño] [📄 Mediano] [📰 Grande]   │
│                                         │
│ 📊 Configuración Actual:                │
│ 📝 Estilo: textbox                      │
│ 📍 Posición: center                     │
│ 🎨 Color: #ffffff                       │
│ 📏 Tamaño: medium                       │
└─────────────────────────────────────────┘
```

## 🎬 **Opciones de Configuración**

### 📝 **Estilos de Narrador**
- **📋 Textbox**: Texto en la caja de diálogo tradicional
- **💬 Flotante**: Texto libre posicionado en la pantalla
- **📜 Pantalla**: Texto como elemento de pantalla

### 📍 **Posiciones del Texto**
- **⬅️ Izquierda**: Texto alineado a la izquierda
- **⬆️ Centro**: Texto centrado horizontalmente
- **➡️ Derecha**: Texto alineado a la derecha
- **⬆️ Arriba**: Texto en la parte superior
- **⬇️ Abajo**: Texto en la parte inferior

### 🎨 **Colores del Texto**
- **⚪ Blanco**: Color blanco (#ffffff)
- **🟡 Amarillo**: Color amarillo (#f1c40f)
- **🔵 Azul**: Color azul (#3498db)
- **🟢 Verde**: Color verde (#27ae60)

### 📏 **Tamaños del Texto**
- **📝 Pequeño**: Tamaño de texto pequeño
- **📄 Mediano**: Tamaño de texto mediano
- **📰 Grande**: Tamaño de texto grande

## 🚀 **Funcionamiento**

### ✅ **Configuración Dinámica**
1. **Ir a "Vista Previa"** para ver el panel del narrador
2. **Seleccionar estilo** (📋 💬 📜)
3. **Configurar posición** (si no es textbox)
4. **Elegir color** del texto
5. **Seleccionar tamaño** del texto
6. **Ver configuración** actual en tiempo real

### ✅ **Aplicación Automática**
1. **Agregar diálogo del narrador**: Se aplica la configuración
2. **Configuración incluida**: En los datos de la escena
3. **Flexibilidad total**: Diferentes configuraciones por diálogo
4. **Notificaciones informativas**: Confirman cada cambio

## 🎯 **Variables del Sistema**

### 📝 **Configuración del Narrador**
- `narrator_style`: Controla el estilo de presentación
- **Valores**: "textbox", "floating", "screen"
- **Por defecto**: "textbox"

- `narrator_position`: Controla la posición del texto
- **Valores**: "left", "center", "right", "top", "bottom"
- **Por defecto**: "center"

- `narrator_color`: Controla el color del texto
- **Valores**: "#ffffff", "#f1c40f", "#3498db", "#27ae60"
- **Por defecto**: "#ffffff"

- `narrator_size`: Controla el tamaño del texto
- **Valores**: "small", "medium", "large"
- **Por defecto**: "medium"

## 🎬 **Funciones Implementadas**

### 📝 **set_narrator_style(style)**
```python
def set_narrator_style(style):
    """Establece el estilo del narrador"""
    try:
        renpy.set_screen_variable("narrator_style", style)
        
        # Mapear estilos a nombres descriptivos
        style_names = {
            "textbox": "Textbox (Caja de texto)",
            "floating": "Flotante (Texto libre)",
            "screen": "Pantalla (Texto en pantalla)"
        }
        
        style_name = style_names.get(style, style)
        renpy.notify(f"📝 Estilo de narrador cambiado a: {style_name}")
        
    except Exception as e:
        renpy.notify(f"❌ Error cambiando estilo de narrador: {e}")
```

### 📍 **set_narrator_position(position)**
```python
def set_narrator_position(position):
    """Establece la posición del texto del narrador"""
    try:
        renpy.set_screen_variable("narrator_position", position)
        
        # Mapear posiciones a nombres descriptivos
        position_names = {
            "left": "Izquierda",
            "center": "Centro",
            "right": "Derecha",
            "top": "Arriba",
            "bottom": "Abajo"
        }
        
        position_name = position_names.get(position, position)
        renpy.notify(f"📍 Posición del narrador cambiada a: {position_name}")
        
    except Exception as e:
        renpy.notify(f"❌ Error cambiando posición del narrador: {e}")
```

### 🎨 **set_narrator_color(color)**
```python
def set_narrator_color(color):
    """Establece el color del texto del narrador"""
    try:
        renpy.set_screen_variable("narrator_color", color)
        
        # Mapear colores a nombres descriptivos
        color_names = {
            "#ffffff": "Blanco",
            "#f1c40f": "Amarillo",
            "#3498db": "Azul",
            "#27ae60": "Verde"
        }
        
        color_name = color_names.get(color, color)
        renpy.notify(f"🎨 Color del narrador cambiado a: {color_name}")
        
    except Exception as e:
        renpy.notify(f"❌ Error cambiando color del narrador: {e}")
```

### 📏 **set_narrator_size(size)**
```python
def set_narrator_size(size):
    """Establece el tamaño del texto del narrador"""
    try:
        renpy.set_screen_variable("narrator_size", size)
        
        # Mapear tamaños a nombres descriptivos
        size_names = {
            "small": "Pequeño",
            "medium": "Mediano",
            "large": "Grande"
        }
        
        size_name = size_names.get(size, size)
        renpy.notify(f"📏 Tamaño del narrador cambiado a: {size_name}")
        
    except Exception as e:
        renpy.notify(f"❌ Error cambiando tamaño del narrador: {e}")
```

## 🎮 **Integración con Escenas**

### ✅ **Diálogos del Narrador con Configuración**
```python
def add_dialogue_to_scene():
    """Agrega un diálogo a la escena actual"""
    try:
        # Determinar si es narrador y aplicar configuración especial
        is_narrator = character_to_use == 'Narrator' or character_to_use == 'narrator'
        
        scene_data = {
            'type': 'dialogue',
            'character': character_to_use,
            'dialogue': dialogue.strip(),
            'transition': char_transition or 'dissolve',
            'timestamp': datetime.now().isoformat()
        }
        
        # Agregar configuración del narrador si es narrador
        if is_narrator:
            scene_data.update({
                'narrator_style': renpy.get_screen_variable("narrator_style") or 'textbox',
                'narrator_position': renpy.get_screen_variable("narrator_position") or 'center',
                'narrator_color': renpy.get_screen_variable("narrator_color") or '#ffffff',
                'narrator_size': renpy.get_screen_variable("narrator_size") or 'medium'
            })
```

## 🎮 **Experiencia de Usuario**

### ✅ **Configuración Intuitiva**
- **Botones visuales**: Iconos claros para cada opción
- **Selección visual**: Botón activo resaltado
- **Feedback inmediato**: Notificaciones descriptivas
- **Estado persistente**: Configuración mantenida

### ✅ **Aplicación Automática**
- **Detección automática**: Narrador identificado automáticamente
- **Configuración incluida**: En los datos de la escena
- **Flexibilidad total**: Diferentes configuraciones por diálogo
- **Notificaciones informativas**: Confirman la configuración aplicada

## 🎯 **Beneficios**

### ✅ **Creatividad Expandida**
- **Estilos variados**: Múltiples formas de presentar narración
- **Posicionamiento libre**: Texto en cualquier parte de la pantalla
- **Personalización visual**: Colores y tamaños configurables
- **Flexibilidad narrativa**: Adaptar el estilo a la historia

### ✅ **Desarrollo Eficiente**
- **Configuración centralizada**: Todas las opciones en un lugar
- **Aplicación automática**: Sin configuración manual por diálogo
- **Consistencia visual**: Configuración mantenida entre diálogos
- **Ahorro de tiempo**: No más configuración manual

## 🎮 **Casos de Uso**

### 📋 **Textbox Tradicional**
- **Uso**: Narración estándar en caja de diálogo
- **Aplicación**: Historias convencionales
- **Ventaja**: Familiar y legible

### 💬 **Texto Flotante**
- **Uso**: Narración posicionada libremente
- **Aplicación**: Efectos dramáticos, pensamientos
- **Ventaja**: Mayor control visual

### 📜 **Texto en Pantalla**
- **Uso**: Narración como elemento de pantalla
- **Aplicación**: Títulos, efectos especiales
- **Ventaja**: Integración completa con la pantalla

## 🎮 **Próximas Mejoras**

### 📝 **Estilos Avanzados**
1. **Animaciones de texto**: Efectos de aparición
2. **Estilos personalizados**: Configuraciones guardadas
3. **Efectos visuales**: Sombras, bordes, fondos
4. **Timing de texto**: Velocidad de aparición

### 🎯 **Controles Avanzados**
1. **Posiciones personalizadas**: Coordenadas exactas
2. **Colores personalizados**: Selector de color RGB
3. **Fuentes personalizadas**: Tipografías específicas
4. **Efectos de transición**: Entre diferentes configuraciones

¡La configuración del narrador ahora proporciona control total sobre la presentación de la narración, permitiendo crear experiencias narrativas únicas y personalizadas! 📖✨


