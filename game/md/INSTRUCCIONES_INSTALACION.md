# 📦 Instrucciones de Instalación del Editor Visual

## Instalación Automática (Recomendada)

### Paso 1: Preparar los Archivos

Asegúrate de tener todos estos archivos del editor visual:

```
📁 Archivos del Editor Visual:
├── auto_menu_integration.rpy          ← INTEGRACIÓN AUTOMÁTICA
├── visual_editor.rpy                  ← EDITOR PRINCIPAL
├── editor_modules/
│   ├── visual_editor_screen.rpy       ← PANTALLA PRINCIPAL
│   ├── design_tools.rpy               ← HERRAMIENTAS DE DISEÑO
│   ├── modal_windows.rpy              ← VENTANAS MODALES
│   ├── project_manager.rpy            ← GESTOR DE PROYECTOS
│   ├── resource_manager.rpy           ← GESTOR DE RECURSOS
│   └── scene_manager.rpy              ← GESTOR DE ESCENAS
├── custom_extras.rpy                  ← FUNCIONES EXTRA
├── custom_interface.rpy               ← INTERFAZ PERSONALIZADA
├── custom_menus.rpy                   ← MENÚS PERSONALIZADOS
├── custom_minigames.rpy               ← MINIJUEGOS
├── design_config.rpy                  ← CONFIGURACIÓN DE DISEÑO
├── developer_tools.rpy                ← HERRAMIENTAS DE DESARROLLO
├── editor_commands.rpy                ← COMANDOS DEL EDITOR
├── editor_operations.rpy              ← OPERACIONES DEL EDITOR
├── layout_controller.rpy              ← CONTROLADOR DE LAYOUT
├── persistent_config.rpy              ← CONFIGURACIÓN PERSISTENTE
└── save_system.rpy                    ← SISTEMA DE GUARDADO
```

### Paso 2: Copiar al Proyecto

1. **Copia TODOS los archivos** del editor visual a la carpeta `game/` de tu proyecto Ren'Py
2. **Mantén la estructura de carpetas** (especialmente `editor_modules/`)
3. **No modifiques ningún archivo existente** de tu proyecto

### Paso 3: Verificar la Instalación

1. **Ejecuta tu proyecto** Ren'Py
2. **Ve al menú principal**
3. **Busca el botón "Editor Visual"** - debería aparecer automáticamente
4. **Revisa la consola** - deberías ver el mensaje:
   ```
   🎨 Editor Visual detectado - Integrando botón en menú principal
   ✅ El botón 'Editor Visual' aparecerá automáticamente en el menú
   ```

## Solución de Problemas

### ❌ No aparece el botón "Editor Visual"

**Posibles causas:**
1. **Archivos faltantes** - Verifica que todos los archivos estén copiados
2. **Estructura incorrecta** - Asegúrate de que `editor_modules/` esté en la carpeta `game/`
3. **Archivos corruptos** - Revisa que los archivos se copiaron correctamente

**Solución:**
1. Revisa la consola para ver qué archivos faltan
2. Copia nuevamente todos los archivos
3. Reinicia Ren'Py

### ❌ Error al abrir el editor

**Posibles causas:**
1. **Dependencias faltantes** - Algunos módulos del editor no están presentes
2. **Conflicto de nombres** - Hay variables o funciones con nombres duplicados

**Solución:**
1. Asegúrate de que TODOS los archivos del editor estén presentes
2. Verifica que no haya conflictos con tu código existente
3. Revisa la consola para mensajes de error específicos

### ❌ El editor no funciona correctamente

**Posibles causas:**
1. **Versión de Ren'Py** - El editor requiere una versión específica
2. **Configuración incompatible** - Tu proyecto tiene configuraciones que interfieren

**Solución:**
1. Actualiza Ren'Py a la versión más reciente
2. Verifica que tu proyecto sea compatible
3. Revisa la documentación del editor para requisitos específicos

## Desinstalación

### Para remover el editor completamente:

1. **Borra todos los archivos del editor** de tu proyecto
2. **Reinicia Ren'Py**
3. **El botón desaparecerá automáticamente**

### Archivos a borrar:

```
📁 Archivos a eliminar:
├── auto_menu_integration.rpy
├── visual_editor.rpy
├── editor_modules/ (carpeta completa)
├── custom_extras.rpy
├── custom_interface.rpy
├── custom_menus.rpy
├── custom_minigames.rpy
├── design_config.rpy
├── developer_tools.rpy
├── editor_commands.rpy
├── editor_operations.rpy
├── layout_controller.rpy
├── persistent_config.rpy
└── save_system.rpy
```

## Verificación Final

Después de la instalación, deberías ver:

✅ **En el menú principal:** Botón "Editor Visual"
✅ **En la consola:** Mensaje de confirmación
✅ **Al hacer clic:** El editor se abre correctamente
✅ **Funcionalidad:** Todas las herramientas del editor funcionan

---

**¡Listo!** Tu editor visual está completamente integrado y listo para usar. 🎨✨
