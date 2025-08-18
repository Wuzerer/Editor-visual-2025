# 🖼️ Sistema de Fondos Organizados

## 📋 Descripción General

El sistema de fondos organizados permite una gestión más intuitiva y estructurada de las imágenes de fondo en el editor visual. Las imágenes se organizan automáticamente por su ubicación en el sistema de archivos, separando las que están directamente en la carpeta `images/` de las que están en subcarpetas.

## 🗂️ Estructura de Organización

### 📁 Fondos Principales
- **Ubicación**: `images/` (carpeta raíz)
- **Icono**: 📁
- **Color**: Naranja (#f39c12)
- **Descripción**: Imágenes que están directamente en la carpeta principal de imágenes

### 📂 Fondos por Carpetas
- **Ubicación**: `images/[nombre_carpeta]/`
- **Icono**: 📂
- **Color**: Azul (#3498db)
- **Descripción**: Imágenes organizadas en subcarpetas temáticas

### 🚫 Carpetas Excluidas
- **Carpetas**: `menus/`, `buttons/`, `character/`
- **Razón**: Contienen elementos de interfaz y sprites, no fondos
- **Configuración**: Fácilmente modificable en el código
- **Estado**: Excluidas pero preservadas para uso futuro

## 🔧 Funcionalidades Implementadas

### 1. **Escaneo Automático de Imágenes**
```python
def get_root_backgrounds():
    """Obtiene las imágenes de fondo que están directamente en la carpeta images/"""
    # Busca archivos .png, .jpg, .jpeg, .webp, .gif en images/
    # Retorna lista ordenada alfabéticamente
```

### 2. **Detección de Subcarpetas**
```python
def get_folder_backgrounds():
    """Obtiene las imágenes de fondo organizadas por subcarpetas"""
    # Escanea todas las subcarpetas en images/
    # Excluye carpetas específicas (menus, buttons, character)
    # Organiza por nombre de carpeta
    # Solo incluye carpetas que contengan imágenes
```

### 3. **Selección Inteligente de Fondos**
```python
def select_background(bg_name):
    """Selecciona un fondo por nombre"""
    # Verifica automáticamente diferentes extensiones
    # Maneja rutas con subcarpetas
    # Notifica el resultado de la selección
```

### 4. **Recarga Dinámica**
```python
def reload_backgrounds():
    """Recarga la lista de fondos"""
    # Actualiza la vista sin reiniciar el editor
    # Útil después de agregar nuevas imágenes
```

## 🎨 Interfaz de Usuario

### Panel de Fondos Organizados
- **Altura**: 420px (aumentada para mejor visibilidad)
- **Área de Lista**: 300px (más espacio para ver fondos)
- **Organización**: Vista previa con scroll vertical
- **Secciones**: Separadas visualmente por colores y iconos

### Indicadores Visuales
- **✅ Seleccionado**: Fondo verde cuando hay una imagen seleccionada
- **⚠️ Sin Selección**: Fondo rojo cuando no hay fondo seleccionado
- **🖼️ Botones**: Cada imagen es un botón clickeable
- **📁/📂 Iconos**: Distinguen entre carpetas principales y subcarpetas

### Botones de Acción
- **➕ Agregar Fondo**: Añade el fondo seleccionado a la escena
- **🔄 Recargar**: Actualiza la lista de fondos
- **🗑️ Limpiar**: Deselecciona el fondo actual

## 📁 Estructura de Archivos Soportada

### Extensiones Soportadas
- `.png` - Imágenes PNG
- `.jpg` - Imágenes JPEG
- `.jpeg` - Imágenes JPEG (alternativa)
- `.webp` - Imágenes WebP
- `.gif` - Imágenes GIF

### Ejemplo de Estructura
```
images/
├── fondo_principal.png          # 📁 Fondos Principales
├── menu_bg.jpg                  # 📁 Fondos Principales
├── backgrounds/                 # 📂 Subcarpeta (VISIBLE)
│   ├── casa.png
│   ├── escuela.jpg
│   └── parque.webp
├── menus/                       # 📂 Subcarpeta (EXCLUIDA)
│   ├── main_menu.png
│   └── options_menu.jpg
├── buttons/                     # 📂 Subcarpeta (EXCLUIDA)
│   ├── start_button.png
│   └── options_button.png
└── character/                   # 📂 Subcarpeta (EXCLUIDA)
    ├── eileen_happy.png
    └── lucy_sad.jpg
```

## 🚀 Ventajas del Sistema

### 1. **Organización Automática**
- No requiere configuración manual
- Se adapta automáticamente a la estructura de archivos
- Mantiene el orden alfabético

### 2. **Navegación Intuitiva**
- Separación visual clara entre tipos de fondos
- Iconos distintivos para cada categoría
- Scroll independiente para cada sección

### 3. **Flexibilidad**
- Soporta múltiples formatos de imagen
- Maneja rutas con subcarpetas automáticamente
- Recarga dinámica sin reiniciar

### 4. **Compatibilidad**
- Funciona con la estructura existente de Ren'Py
- No requiere cambios en el sistema de archivos
- Mantiene compatibilidad con proyectos existentes

## 🔍 Detalles Técnicos

### Manejo de Rutas
- **Fondos Principales**: `images/nombre.png`
- **Fondos en Subcarpetas**: `images/carpeta/nombre.png`
- **Comparación Inteligente**: Verifica múltiples extensiones

### Optimización de Rendimiento
- Escaneo bajo demanda
- Caché de resultados
- Recarga selectiva

### Manejo de Errores
- Verificación de existencia de archivos
- Notificaciones informativas
- Fallback graceful para archivos faltantes

## 📝 Uso Recomendado

### Organización de Proyectos
1. **Fondos Principales**: Para imágenes de uso frecuente
2. **Subcarpetas Temáticas**: Para organizar por contexto
   - `backgrounds/` - Fondos de escenas (VISIBLE)
   - `locations/` - Fondos por ubicación (VISIBLE)
   - `menus/` - Fondos de interfaz (EXCLUIDO)
   - `buttons/` - Botones de interfaz (EXCLUIDO)
   - `character/` - Sprites de personajes (EXCLUIDO)

### Flujo de Trabajo
1. Colocar imágenes en la estructura deseada
2. Usar "🔄 Recargar" si es necesario
3. Seleccionar fondo haciendo clic en el botón
4. Usar "➕ Agregar Fondo" para añadirlo a la escena

## 🎯 Resultado Final

El sistema proporciona una experiencia de usuario mejorada donde:
- **Los fondos están claramente organizados** por su ubicación
- **La navegación es intuitiva** con separación visual
- **La gestión es eficiente** con herramientas de recarga y limpieza
- **La compatibilidad se mantiene** con el sistema existente de Ren'Py

Este enfoque transforma la gestión de fondos de una tarea manual a una experiencia fluida y organizada, permitiendo a los creadores concentrarse en la narrativa en lugar de la organización de archivos.
