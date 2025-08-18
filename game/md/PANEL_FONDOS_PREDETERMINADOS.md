# Panel de Fondos Predeterminados

## Descripción
Se ha agregado un nuevo panel en el sector de "Escena" que permite seleccionar fondos de colores predeterminados para las escenas del juego visual novel.

## Características

### 🎨 Colores Disponibles
El panel incluye 12 colores predeterminados organizados en una cuadrícula 4x3:

**Fila 1 - Colores Básicos:**
- ⚫ Negro (#000000)
- ⚪ Blanco (#ffffff)
- 🔴 Rojo (#e74c3c)
- 🔵 Azul (#3498db)

**Fila 2 - Colores Adicionales:**
- 🟣 Violeta (#9b59b6)
- 🟢 Verde (#27ae60)
- 🟡 Amarillo (#f1c40f)
- 🟠 Naranja (#e67e22)

**Fila 3 - Colores Neutros:**
- ⚫ Gris Oscuro (#2c3e50)
- ⚪ Gris Claro (#bdc3c7)
- 🟤 Marrón (#8b4513)
- 🩷 Rosa (#e91e63)

### 🔧 Funcionalidades

#### Selección de Color
- **Clic en color**: Selecciona el color como fondo predeterminado
- **Indicador visual**: El color seleccionado se resalta
- **Vista previa**: El color se muestra inmediatamente en la vista previa

#### Botones de Acción
- **➕ Agregar a Escena**: Añade el color seleccionado como escena de fondo
- **🎨 Color Personalizado**: Abre selector de color personalizado (en desarrollo)

### 🎮 Integración con el Sistema

#### Vista Previa en Tiempo Real
- Los colores se muestran inmediatamente en la vista previa
- Se indica el nombre del color seleccionado
- Compatible con el sistema de transiciones existente

#### Gestión de Escenas
- Los fondos de color se agregan como escenas de tipo 'background'
- Se almacenan con el código hexadecimal del color
- Compatible con el sistema de exportación de escenas

### 📁 Estructura de Datos
```python
# Escena de fondo de color
background_scene = {
    'type': 'background',
    'background': 'red',  # Nombre del color
    'color_code': '#e74c3c',  # Código hexadecimal
    'transition': 'dissolve'
}
```

### 🔄 Funciones Implementadas

#### `select_default_background(color_name)`
- Selecciona un color predeterminado
- Actualiza la variable `selected_background_global`
- Muestra notificación de confirmación

#### `add_default_background_to_scene()`
- Agrega el color seleccionado a la lista de escenas
- Crea una escena de fondo con metadatos del color
- Compatible con el sistema de escenas múltiples

#### `open_custom_color_picker()`
- Función placeholder para selector de color personalizado
- Preparada para futuras implementaciones

#### `clear_background_selection()`
- Limpia la selección de fondo actual
- Resetea la variable `selected_background_global`

### 🎯 Ventajas del Sistema

1. **Rapidez**: Selección instantánea de colores comunes
2. **Consistencia**: Colores estandarizados para el proyecto
3. **Simplicidad**: Interfaz intuitiva con botones de color
4. **Flexibilidad**: Compatible con fondos de imagen existentes
5. **Escalabilidad**: Fácil agregar nuevos colores predeterminados

### 🔮 Futuras Mejoras

- **Selector de color personalizado**: Implementar selector RGB/HSL
- **Paletas temáticas**: Conjuntos de colores para diferentes géneros
- **Gradientes**: Fondos con transiciones de color
- **Texturas**: Fondos con patrones y texturas
- **Animaciones**: Fondos con efectos de animación

### 📝 Uso Recomendado

1. **Escenas de transición**: Usar colores neutros para transiciones
2. **Estados emocionales**: Colores que reflejen el estado de ánimo
3. **Ambientación**: Colores que establezcan el ambiente de la escena
4. **Contraste**: Asegurar legibilidad del texto sobre el fondo

### 🛠️ Mantenimiento

Para agregar nuevos colores predeterminados:

1. Agregar el color al diccionario `color_map` en las funciones
2. Crear el botón correspondiente en la cuadrícula
3. Actualizar la documentación
4. Probar la integración con el sistema existente

---

**Nota**: Este panel complementa el sistema de fondos de imagen existente, proporcionando una alternativa rápida y eficiente para fondos de color sólido.


