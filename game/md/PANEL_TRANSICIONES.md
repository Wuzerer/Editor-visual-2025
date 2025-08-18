# 🎬 Panel de Transiciones

## 🎯 **Descripción**

Se ha implementado un **panel completo de transiciones** en la sección de "Vista Previa" que permite configurar las transiciones para fondos y personajes. Estas transiciones se aplicarán automáticamente cuando se agreguen elementos a las escenas, proporcionando un control total sobre los efectos visuales.

## 🎮 **Panel de Transiciones**

### 📍 **Ubicación**
- **Sección**: "Vista Previa" (pestaña 🎮)
- **Posición**: Debajo del panel de controles de vista previa
- **Tamaño**: 400px de ancho x 300px de alto
- **Color**: Fondo gris oscuro (#2c3e50)

### 🎯 **Estructura del Panel**
```
┌─────────────────────────────────────────┐
│ 🎬 Panel de Transiciones                │
├─────────────────────────────────────────┤
│ 🖼️ Transiciones de Fondo:              │
│ [🌅 Dissolve] [⚡ Fade] [🔄 Move]       │
│                                         │
│ 👤 Transiciones de Personajes:          │
│ [🌅 Dissolve] [⚡ Fade] [🔄 Move]       │
│ [⬅️ MoveInLeft] [➡️ MoveInRight]       │
│ [⬆️ MoveInBottom]                      │
│                                         │
│ 📊 Transiciones Actuales:               │
│ 🖼️ Fondo: dissolve                     │
│ 👤 Personaje: dissolve                  │
└─────────────────────────────────────────┘
```

## 🎬 **Transiciones Disponibles**

### 🖼️ **Transiciones de Fondo**
- **🌅 Dissolve**: Desvanecimiento suave entre fondos
- **⚡ Fade**: Transición de desvanecimiento
- **🔄 Move**: Transición con movimiento

### 👤 **Transiciones de Personajes**
- **🌅 Dissolve**: Desvanecimiento suave del personaje
- **⚡ Fade**: Transición de desvanecimiento
- **🔄 Move**: Transición con movimiento
- **⬅️ MoveInLeft**: Personaje entra desde la izquierda
- **➡️ MoveInRight**: Personaje entra desde la derecha
- **⬆️ MoveInBottom**: Personaje entra desde abajo

## 🚀 **Funcionamiento**

### ✅ **Configuración de Transiciones**
1. **Ir a "Vista Previa"** para ver el panel de transiciones
2. **Seleccionar transición** para fondos (🖼️)
3. **Seleccionar transición** para personajes (👤)
4. **Ver confirmación** en notificaciones
5. **Transiciones se aplican** automáticamente

### ✅ **Aplicación Automática**
1. **Agregar fondo**: Se aplica la transición configurada
2. **Agregar personaje**: Se aplica la transición configurada
3. **Agregar diálogo**: Se aplica la transición del personaje
4. **Notificaciones**: Confirman la transición aplicada

## 🎯 **Variables del Sistema**

### 🖼️ **Transiciones de Fondo**
- `background_transition`: Controla la transición de fondos
- **Valores**: "dissolve", "fade", "move"
- **Por defecto**: "dissolve"

### 👤 **Transiciones de Personajes**
- `character_transition`: Controla la transición de personajes
- **Valores**: "dissolve", "fade", "move", "moveinleft", "moveinright", "moveinbottom"
- **Por defecto**: "dissolve"

## 🎬 **Funciones Implementadas**

### 🖼️ **set_background_transition(transition)**
```python
def set_background_transition(transition):
    """Establece la transición para fondos"""
    try:
        renpy.set_screen_variable("background_transition", transition)
        
        # Mapear transiciones a nombres descriptivos
        transition_names = {
            "dissolve": "Dissolve (Desvanecimiento)",
            "fade": "Fade (Desvanecimiento)",
            "move": "Move (Movimiento)"
        }
        
        transition_name = transition_names.get(transition, transition)
        renpy.notify(f"🖼️ Transición de fondo cambiada a: {transition_name}")
        
    except Exception as e:
        renpy.notify(f"❌ Error cambiando transición de fondo: {e}")
```

### 👤 **set_character_transition(transition)**
```python
def set_character_transition(transition):
    """Establece la transición para personajes"""
    try:
        renpy.set_screen_variable("character_transition", transition)
        
        # Mapear transiciones a nombres descriptivos
        transition_names = {
            "dissolve": "Dissolve (Desvanecimiento)",
            "fade": "Fade (Desvanecimiento)",
            "move": "Move (Movimiento)",
            "moveinleft": "MoveInLeft (Entrar desde la izquierda)",
            "moveinright": "MoveInRight (Entrar desde la derecha)",
            "moveinbottom": "MoveInBottom (Entrar desde abajo)"
        }
        
        transition_name = transition_names.get(transition, transition)
        renpy.notify(f"👤 Transición de personaje cambiada a: {transition_name}")
        
    except Exception as e:
        renpy.notify(f"❌ Error cambiando transición de personaje: {e}")
```

## 🎮 **Integración con Escenas**

### ✅ **Fondos con Transiciones**
```python
def add_background_to_scene():
    """Agrega un fondo a la escena actual"""
    try:
        bg_selected = renpy.get_screen_variable("selected_background_global")
        bg_transition = renpy.get_screen_variable("background_transition")
        
        scene_data = {
            'type': 'background',
            'background': bg_selected,
            'transition': bg_transition or 'dissolve',
            'timestamp': datetime.now().isoformat()
        }
        # Agregar a escena...
```

### ✅ **Personajes con Transiciones**
```python
def add_character_to_scene():
    """Agrega un personaje a la escena actual"""
    try:
        character = renpy.get_screen_variable("current_speaker")
        char_transition = renpy.get_screen_variable("character_transition")
        
        scene_data = {
            'type': 'character',
            'character': character,
            'expression': expression or 'happy',
            'position': position or 'center',
            'transition': char_transition or 'dissolve',
            'timestamp': datetime.now().isoformat()
        }
        # Agregar a escena...
```

### ✅ **Diálogos con Transiciones**
```python
def add_dialogue_to_scene():
    """Agrega un diálogo a la escena actual"""
    try:
        char_transition = renpy.get_screen_variable("character_transition")
        
        scene_data = {
            'type': 'dialogue',
            'character': character_to_use,
            'dialogue': dialogue.strip(),
            'transition': char_transition or 'dissolve',
            'timestamp': datetime.now().isoformat()
        }
        # Agregar a escena...
```

## 🎮 **Experiencia de Usuario**

### ✅ **Configuración Intuitiva**
- **Botones visuales**: Iconos claros para cada transición
- **Selección visual**: Botón activo resaltado
- **Feedback inmediato**: Notificaciones descriptivas
- **Estado persistente**: Configuración mantenida

### ✅ **Aplicación Automática**
- **Sin configuración manual**: Transiciones se aplican automáticamente
- **Consistencia**: Misma transición para elementos similares
- **Flexibilidad**: Diferentes transiciones para fondos y personajes
- **Notificaciones informativas**: Confirman la transición aplicada

## 🎯 **Beneficios**

### ✅ **Desarrollo Eficiente**
- **Configuración centralizada**: Todas las transiciones en un lugar
- **Aplicación automática**: Sin necesidad de configurar cada elemento
- **Consistencia visual**: Transiciones uniformes en toda la escena
- **Ahorro de tiempo**: No más configuración manual por elemento

### ✅ **Calidad Profesional**
- **Transiciones pulidas**: Efectos visuales profesionales
- **Variedad de opciones**: Múltiples tipos de transiciones
- **Control preciso**: Transiciones específicas por tipo de elemento
- **Experiencia inmersiva**: Efectos visuales que mejoran la narrativa

## 🎮 **Próximas Mejoras**

### 🎬 **Transiciones Avanzadas**
1. **Transiciones personalizadas**: Velocidad y duración configurables
2. **Transiciones combinadas**: Múltiples efectos simultáneos
3. **Transiciones por escena**: Diferentes configuraciones por escena
4. **Transiciones de salida**: Efectos cuando elementos desaparecen

### 🎯 **Controles Avanzados**
1. **Timing de transiciones**: Control de duración
2. **Easing de transiciones**: Tipos de interpolación
3. **Transiciones condicionales**: Basadas en contexto
4. **Templates de transiciones**: Configuraciones predefinidas

¡El panel de transiciones ahora proporciona control total sobre los efectos visuales, permitiendo crear escenas dinámicas y profesionales con transiciones automáticas y configurables! 🎬✨
