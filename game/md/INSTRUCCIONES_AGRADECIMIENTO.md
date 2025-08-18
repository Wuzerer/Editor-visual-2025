# Instrucciones para Personalizar la Pantalla de Agradecimiento

## Descripción
Al abrir el proyecto, ahora se muestra automáticamente una pantalla de agradecimiento antes de ir al editor visual. Esta pantalla es completamente personalizable.

## Archivos Involucrados
- `config_agradecimiento.rpy` - Configuración principal
- `agradecimiento_screen.rpy` - Pantalla de agradecimiento
- `script.rpy` - Script principal (modificado)

## Cómo Personalizar

### 1. Cambiar Mensajes
Edita el archivo `config_agradecimiento.rpy` y modifica la sección `AGRADECIMIENTO_MENSAJES`:

```python
AGRADECIMIENTO_MENSAJES = {
    "titulo": "¡TU MENSAJE PERSONALIZADO!",
    "subtitulo_1": "Tu primer subtítulo",
    "subtitulo_2": "Tu segundo subtítulo",
    "motivacional": "¡Tu mensaje motivacional!",
    "boton_saltar": "Texto del botón"
}
```

### 2. Cambiar Colores
Modifica la sección `AGRADECIMIENTO_CONFIG`:

```python
AGRADECIMIENTO_CONFIG = {
    "color_titulo": "#ffffff",        # Color del título
    "color_subtitulo": "#cccccc",     # Color del subtítulo
    "color_motivacional": "#ffff00",  # Color del mensaje motivacional
    # ... otras configuraciones
}
```

### 3. Cambiar Tamaños de Texto
```python
AGRADECIMIENTO_CONFIG = {
    "tamano_titulo": 32,        # Tamaño del título
    "tamano_subtitulo": 18,     # Tamaño del subtítulo
    "tamano_motivacional": 24,  # Tamaño del mensaje motivacional
    # ... otras configuraciones
}
```

### 4. Agregar Imagen de Fondo
Para usar una imagen de fondo:

1. Coloca tu imagen en la carpeta `images/backgrounds/`
2. Modifica la configuración:

```python
AGRADECIMIENTO_CONFIG = {
    "usar_imagen_fondo": True,  # Cambiar a True
    "imagen_fondo": "images/backgrounds/tu_imagen.png",  # Ruta de tu imagen
    # ... otras configuraciones
}
```

### 5. Cambiar Duración
```python
AGRADECIMIENTO_CONFIG = {
    "duracion_total": 8.0,  # Duración total en segundos
    "fade_in": 1.5,         # Tiempo de fade in
    "fade_out": 1.5,        # Tiempo de fade out
    # ... otras configuraciones
}
```

### 6. Mostrar/Ocultar Botón de Saltar
```python
AGRADECIMIENTO_CONFIG = {
    "mostrar_boton_saltar": False,  # False para ocultar el botón
    # ... otras configuraciones
}
```

## Funciones Disponibles

### Para Usar en el Código
```python
# Obtener configuración actual
config = get_agradecimiento_config()

# Obtener mensajes actuales
mensajes = get_agradecimiento_mensajes()

# Establecer imagen de fondo
set_agradecimiento_imagen("images/backgrounds/mi_imagen.png")

# Desactivar imagen de fondo
desactivar_agradecimiento_imagen()
```

## Ejemplo de Personalización Completa

```python
# En config_agradecimiento.rpy
AGRADECIMIENTO_CONFIG = {
    "usar_imagen_fondo": True,
    "imagen_fondo": "images/backgrounds/mi_fondo.jpg",
    "duracion_total": 10.0,
    "fade_in": 2.0,
    "fade_out": 2.0,
    "mostrar_boton_saltar": True,
    "color_titulo": "#ff6b6b",
    "color_subtitulo": "#4ecdc4",
    "color_motivacional": "#45b7d1",
    "tamano_titulo": 40,
    "tamano_subtitulo": 20,
    "tamano_motivacional": 28,
}

AGRADECIMIENTO_MENSAJES = {
    "titulo": "¡BIENVENIDO AL EDITOR VISUAL!",
    "subtitulo_1": "Una herramienta poderosa para crear",
    "subtitulo_2": "novelas visuales increíbles",
    "motivacional": "¡Tu historia está a punto de comenzar!",
    "boton_saltar": "¡Empezar a crear!"
}
```

## Notas Importantes
- La pantalla se muestra automáticamente al iniciar el juego
- Después de la pantalla de agradecimiento, va directamente al editor visual
- Si quieres desactivar completamente la pantalla, modifica `script.rpy` y cambia `jump agradecimiento_editor` por `jump visual_editor_start`
- Las imágenes deben estar en formato PNG, JPG o JPEG
- Los colores deben estar en formato hexadecimal (#RRGGBB)
