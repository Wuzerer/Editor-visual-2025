# Panel de Diálogo Dinámico

## Descripción
Se ha implementado un sistema de altura dinámica para el panel de diálogo que se ajusta automáticamente según el número de personajes definidos.

## 🎯 Características Implementadas

### 📏 Altura Dinámica Automática
- **Cálculo inteligente**: La altura del panel se calcula automáticamente según el número de personajes
- **Fórmula dinámica**: `50 + (número_de_personajes × 35)` píxeles
- **Altura mínima**: 120 píxeles (incluso sin personajes)
- **Altura máxima**: 800 píxeles (para evitar paneles demasiado grandes)

### 🔄 Actualización Automática
- **Redimensionamiento instantáneo**: El panel se ajusta inmediatamente al agregar personajes
- **Forzar actualización**: Se usa `renpy.restart_interaction()` para recalcular dimensiones
- **Sincronización perfecta**: Los cambios se reflejan en tiempo real

### 📐 Viewport Adaptativo
- **Altura del viewport**: Se ajusta dinámicamente según el número de personajes
- **Fórmula del viewport**: `50 + (número_de_personajes × 30)` píxeles
- **Scroll automático**: Mantiene scroll vertical cuando hay muchos personajes

## 🔧 Código Implementado

### Cálculo de Altura Dinámica
```python
# Altura por sección - DINÁMICA SEGÚN PERSONAJES
$ defined_chars = defined_characters
$ character_count = len(defined_chars) if defined_chars else 0

# Altura del selector de personajes (dinámica)
if character_count > 0:
    character_selector_height = 50 + (character_count * 35)  # 50 base + 35 por personaje
    character_selector_height = max(120, character_selector_height)  # Mínimo 120
else:
    character_selector_height = 120  # Altura por defecto
```

### Viewport Dinámico
```python
viewport:
    xminimum 350
    ysize (50 + (len(defined_chars) * 30))  # Altura dinámica según personajes
    scrollbars "vertical"
    mousewheel True
    xalign 0.5
```

### Actualización Automática
```python
# Forzar actualización de la pantalla para redimensionar el panel
renpy.restart_interaction()
```

## 📊 Comportamiento por Número de Personajes

| Personajes | Altura Panel | Altura Viewport | Comportamiento |
|------------|--------------|-----------------|----------------|
| 0 | 300px | 120px | Altura mínima |
| 1 | 335px | 80px | Altura base + 1 personaje |
| 2 | 370px | 110px | Altura base + 2 personajes |
| 3 | 405px | 140px | Altura base + 3 personajes |
| 4 | 440px | 170px | Altura base + 4 personajes |
| 5 | 475px | 200px | Altura base + 5 personajes |
| 10+ | 800px | 350px+ | Altura máxima con scroll |

## 🎨 Ventajas del Sistema

### 1. **Experiencia de Usuario Mejorada**
- No hay espacios vacíos innecesarios
- El panel siempre se ajusta al contenido
- Interfaz más limpia y profesional

### 2. **Eficiencia de Espacio**
- Aprovecha mejor el espacio disponible
- Evita scroll innecesario en paneles pequeños
- Optimiza la distribución visual

### 3. **Escalabilidad**
- Funciona con cualquier número de personajes
- Se adapta automáticamente a proyectos grandes
- Mantiene la usabilidad independientemente del tamaño

### 4. **Consistencia Visual**
- Mantiene proporciones adecuadas
- Evita cambios bruscos en el layout
- Proporciona una experiencia visual coherente

## 🔄 Flujo de Funcionamiento

1. **Usuario define un personaje** → Función `define_character()`
2. **Se actualiza `defined_characters`** → Variable de pantalla modificada
3. **Se fuerza actualización** → `renpy.restart_interaction()`
4. **Se recalcula altura** → Cálculo dinámico ejecutado
5. **Panel se redimensiona** → Nueva altura aplicada automáticamente

## 🛠️ Mantenimiento y Personalización

### Ajustar Altura por Personaje
```python
# Cambiar el valor 35 para ajustar altura por personaje
character_selector_height = 50 + (character_count * 35)
```

### Ajustar Altura del Viewport
```python
# Cambiar el valor 30 para ajustar altura del viewport
ysize (50 + (len(defined_chars) * 30))
```

### Modificar Altura Máxima
```python
# Cambiar el valor 800 para ajustar altura máxima
max_height = 800
```

## 🎯 Casos de Uso

### Proyectos Pequeños (1-3 personajes)
- Panel compacto y eficiente
- Sin scroll innecesario
- Interfaz limpia y directa

### Proyectos Medianos (4-8 personajes)
- Panel que crece gradualmente
- Scroll suave cuando es necesario
- Balance entre espacio y funcionalidad

### Proyectos Grandes (9+ personajes)
- Panel con altura máxima
- Scroll optimizado para navegación
- Mantiene la usabilidad

## 🔮 Futuras Mejoras

- **Animación suave**: Transiciones animadas al redimensionar
- **Agrupación de personajes**: Categorías o filtros
- **Búsqueda de personajes**: Campo de búsqueda para proyectos grandes
- **Vista en cuadrícula**: Opción de mostrar personajes en grid
- **Personalización de altura**: Permitir al usuario ajustar parámetros

---

**Nota**: Este sistema proporciona una experiencia de usuario fluida y profesional, adaptándose automáticamente a las necesidades del proyecto sin requerir intervención manual.


