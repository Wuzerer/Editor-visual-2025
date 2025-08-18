# Instrucciones Finales: Editor Visual Directo

## ✅ Sistema Completamente Funcional

El proyecto ha sido configurado exitosamente para comportarse como un editor directo. Al abrir el proyecto, irá directamente al editor visual sin mostrar menús de juego.

## Archivos del Sistema

### Archivos Principales:
- `script.rpy` - Script principal con configuración del editor
- `simple_editor_screen.rpy` - Pantalla simple del editor
- `options.rpy` - Configuración básica de Ren'Py
- `screens.rpy` - Pantallas modificadas para redirigir al editor

### Archivos de Agradecimiento (Opcionales):
- `config_agradecimiento.rpy` - Configuración de la pantalla de agradecimiento
- `agradecimiento_screen.rpy` - Pantalla de agradecimiento avanzada
- `INSTRUCCIONES_AGRADECIMIENTO.md` - Instrucciones de personalización

## Flujo de Inicio

### 1. Inicio del Proyecto
```
Proyecto se abre → Inicio directo → Pantalla de agradecimiento → Inicialización → Editor visual
```

### 2. Secuencia Completa:
1. **Pantalla de agradecimiento** (7.5 segundos)
   - Título grande en blanco
   - Subtítulos en gris
   - Mensaje motivacional en amarillo
   
2. **Pantalla de inicialización** (3.5 segundos)
   - Mensaje "Inicializando Editor Visual..."
   - Mensaje "Por favor espera..."
   - Posicionado más abajo para no sobreponerse
   
3. **Editor Visual**
   - Pantalla simple del editor
   - Botón para salir

## Configuraciones Aplicadas

- ✅ **Menú principal desactivado** - No aparece el menú tradicional
- ✅ **Menú del juego desactivado** - No hay menús de pausa
- ✅ **Ventanas de diálogo ocultas** - No muestra ventanas de juego
- ✅ **Transiciones instantáneas** - Sin transiciones de menú
- ✅ **Salida directa** - Sale sin confirmaciones
- ✅ **Mensaje de inicialización separado** - No se sobrepone al agradecimiento

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
Edita `script.rpy` en la sección `agradecimiento_editor`:
```python
$ renpy.pause(6.0)  # En lugar de 4.0
```

#### Opción 3: Agregar imagen de fondo
Usa los archivos de agradecimiento avanzado:
1. Edita `config_agradecimiento.rpy`:
```python
AGRADECIMIENTO_CONFIG = {
    "usar_imagen_fondo": True,
    "imagen_fondo": "images/backgrounds/tu_imagen.png",
    # ... otras configuraciones
}
```

2. Cambia `script.rpy` para usar la pantalla avanzada:
```python
label agradecimiento_editor:
    $ renpy.show_screen("agradecimiento_screen")
    $ renpy.pause(6.0)
    $ renpy.hide_screen("agradecimiento_screen")
    jump visual_editor_start
```

### Desactivar Completamente la Pantalla de Agradecimiento

Si quieres ir directamente al editor sin pantalla de agradecimiento:

Edita `script.rpy`:
```python
label start:
    # Inicializar configuración básica
    if persistent.unlocked_gallery is None:
        $ persistent.unlocked_gallery = set()
    
    # Ir directamente al editor visual
    jump visual_editor_start
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
3. Elimina archivos `.rpyc` si es necesario: `del *.rpyc`

### Si la pantalla de agradecimiento no aparece:
1. Verifica que el label `agradecimiento_editor` esté definido en `script.rpy`
2. Asegúrate de que no haya errores de sintaxis

### Si el editor no se abre:
1. Verifica que `simple_editor_screen.rpy` esté presente
2. Asegúrate de que la pantalla `simple_editor_screen` esté definida

## Notas Importantes

- **El proyecto ahora es un editor, no un juego**: No tendrás menús tradicionales de juego
- **Inicio automático**: Al abrir el proyecto, irá directamente al editor
- **Salida directa**: Al cerrar, saldrá sin confirmaciones
- **Personalizable**: Puedes modificar la pantalla de agradecimiento según tus necesidades
- **Configuración centralizada**: Toda la configuración está en `script.rpy`
- **Mensaje de inicialización separado**: No se sobrepone al agradecimiento

## Comandos Útiles

### Para Desarrolladores
```python
# Forzar inicio al editor
renpy.jump("visual_editor_start")

# Mostrar pantalla de agradecimiento
renpy.jump("agradecimiento_editor")

# Salir del proyecto
renpy.quit()
```

## Estado Actual

✅ **Sistema completamente funcional**
✅ **Sin errores de sintaxis**
✅ **Mensaje de inicialización separado**
✅ **Configuración simplificada**
✅ **Fácil de personalizar**

¡El sistema está listo para usar!
