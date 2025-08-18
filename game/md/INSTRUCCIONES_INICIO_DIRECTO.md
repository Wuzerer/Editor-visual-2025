# Instrucciones: Inicio Directo al Editor Visual

## Descripción
El proyecto ha sido configurado para comportarse como un editor directo, no como un juego tradicional. Al abrir el proyecto, irá directamente al editor visual sin mostrar menús de juego.

## Archivos de Configuración

### Archivos Principales:
- `script.rpy` - Script principal con configuración del editor
- `options.rpy` - Configuración básica de Ren'Py
- `screens.rpy` - Pantallas modificadas para redirigir al editor

### Archivos de Agradecimiento:
- `config_agradecimiento.rpy` - Configuración de la pantalla de agradecimiento
- `agradecimiento_screen.rpy` - Pantalla de agradecimiento
- `INSTRUCCIONES_AGRADECIMIENTO.md` - Instrucciones de personalización

## Flujo de Inicio

### 1. Inicio del Proyecto
```
Proyecto se abre → Inicio directo → Pantalla de agradecimiento → Editor visual
```

### 2. Configuraciones Aplicadas
- ✅ Menú principal desactivado
- ✅ Menú del juego desactivado
- ✅ Ventanas de diálogo ocultas
- ✅ Transiciones instantáneas
- ✅ Salida directa sin confirmación

## Personalización

### Cambiar el Comportamiento de Inicio

#### Opción 1: Ir directamente al editor (sin agradecimiento)
Edita `script.rpy` y cambia:
```python
label start:
    # ... configuración ...
    jump visual_editor_start  # En lugar de agradecimiento_editor
```

#### Opción 2: Mostrar agradecimiento más largo
Edita `config_agradecimiento.rpy`:
```python
AGRADECIMIENTO_CONFIG = {
    "duracion_total": 10.0,  # Más tiempo
    # ... otras configuraciones
}
```

#### Opción 3: Agregar imagen de fondo
Edita `config_agradecimiento.rpy`:
```python
AGRADECIMIENTO_CONFIG = {
    "usar_imagen_fondo": True,
    "imagen_fondo": "images/backgrounds/tu_imagen.png",
    # ... otras configuraciones
}
```

### Desactivar Completamente la Pantalla de Agradecimiento

Si quieres ir directamente al editor sin pantalla de agradecimiento:

1. Edita `script.rpy`:
```python
label start:
    # Inicializamos la memoria del mundo la primera vez que se juega.
    if persistent.unlocked_gallery is None:
        $ persistent.unlocked_gallery = set()
    
    # Ir directamente al editor visual
    jump visual_editor_start
```

2. Elimina o comenta la línea:
```python
# jump agradecimiento_editor
```

## Funciones Disponibles

### Para Usar en el Código
```python
# Ir directamente al editor
renpy.jump("visual_editor_start")

# Ir a la pantalla de agradecimiento
renpy.jump("agradecimiento_editor")

# Salir directamente
renpy.quit()
```

## Solución de Problemas

### Si aún aparece el menú principal:
1. Verifica que `config.main_menu = False` esté en `script.rpy`
2. Reinicia Ren'Py completamente
3. Elimina archivos `.rpyc` si es necesario

### Si la pantalla de agradecimiento no aparece:
1. Verifica que `agradecimiento_screen.rpy` esté presente
2. Asegúrate de que `config_agradecimiento.rpy` esté presente
3. Verifica que el label `agradecimiento_editor` esté definido

### Si el editor no se abre:
1. Verifica que `visual_editor.rpy` esté presente
2. Asegúrate de que la pantalla `visual_editor_screen` esté definida
3. Verifica que todos los archivos del editor estén en su lugar

## Notas Importantes

- **El proyecto ahora es un editor, no un juego**: No tendrás menús tradicionales de juego
- **Inicio automático**: Al abrir el proyecto, irá directamente al editor
- **Salida directa**: Al cerrar, saldrá sin confirmaciones
- **Personalizable**: Puedes modificar la pantalla de agradecimiento según tus necesidades
- **Configuración centralizada**: Toda la configuración está en `script.rpy`

## Archivos de Respaldo

Si necesitas restaurar el comportamiento original:
- `script.rpy.original` - Script original (si existe)
- `options.rpy.original` - Opciones originales (si existe)
- `screens.rpy.original` - Pantallas originales (si existe)

## Comandos Útiles

### Para Desarrolladores
```python
# Forzar inicio al editor
renpy.jump("visual_editor_start")

# Mostrar pantalla de agradecimiento
renpy.show_screen("agradecimiento_screen")

# Ocultar pantalla de agradecimiento
renpy.hide_screen("agradecimiento_screen")

# Salir del proyecto
renpy.quit()
```
