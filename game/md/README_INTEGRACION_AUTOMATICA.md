# 🎨 Integración Automática del Editor Visual

## ¿Cómo Funciona?

Este sistema permite que el **Editor Visual** se integre automáticamente en el menú principal de cualquier proyecto Ren'Py **sin modificar ningún archivo existente**.

### Archivos Requeridos

Para que la integración funcione, solo necesitas copiar estos archivos a tu proyecto:

1. **`auto_menu_integration.rpy`** - Este archivo
2. **`visual_editor.rpy`** - El editor principal
3. **`editor_modules/visual_editor_screen.rpy`** - La pantalla del editor
4. **Cualquier otro archivo del editor** (módulos, recursos, etc.)

### Proceso Automático

1. **Detección**: El archivo `auto_menu_integration.rpy` verifica automáticamente si los archivos del editor están presentes
2. **Integración**: Si los encuentra, sobrescribe la pantalla de navegación para incluir el botón "Editor Visual"
3. **Funcionamiento**: El botón aparece automáticamente en el menú principal sin necesidad de configuración

### Ventajas

✅ **No modifica archivos existentes** - No toca `screens.rpy`, `gui.rpy` ni ningún archivo por defecto de Ren'Py

✅ **Instalación simple** - Solo copia los archivos y listo

✅ **Desinstalación fácil** - Borra los archivos del editor y el botón desaparece automáticamente

✅ **Compatible** - Funciona con cualquier proyecto Ren'Py existente

✅ **No invasivo** - No interfiere con la funcionalidad existente del juego

### Mensajes de Consola

El sistema muestra mensajes informativos en la consola:

- 🎨 **"Editor Visual detectado - Integrando botón en menú principal"** - Cuando todo está correcto
- ⚠️ **"Editor Visual no encontrado - Botón no se agregará al menú"** - Si faltan archivos

### Estructura de Archivos

```
tu_proyecto/
├── auto_menu_integration.rpy          ← Este archivo (NUEVO)
├── visual_editor.rpy                  ← Editor principal
├── editor_modules/
│   └── visual_editor_screen.rpy       ← Pantalla del editor
├── screens.rpy                        ← NO SE MODIFICA
├── gui.rpy                           ← NO SE MODIFICA
└── ... (otros archivos del proyecto)
```

### Instalación

1. Copia todos los archivos del editor a tu proyecto
2. Incluye `auto_menu_integration.rpy` en la carpeta `game/`
3. Ejecuta tu proyecto
4. El botón "Editor Visual" aparecerá automáticamente en el menú principal

### Desinstalación

1. Borra todos los archivos del editor
2. El botón desaparecerá automáticamente en la próxima ejecución

---

**Nota**: Este sistema respeta completamente la filosofía de Ren'Py de no modificar archivos existentes, proporcionando una integración elegante y no invasiva.
