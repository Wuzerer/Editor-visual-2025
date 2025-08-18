# 🎛️ Sistema de Configuración del Layout para Desarrolladores

## 🎯 **Descripción General**

El sistema de configuración permite al desarrollador controlar exactamente la posición, tamaño y espaciado de todos los elementos del editor visual. Los valores se configuran directamente en el código `.rpy` y no aparecen en la interfaz del usuario final.

## 🔧 **Parámetros Ajustables**

### **1. Ancho del Contenido (`content_width`)**
- **Rango:** 200px - 800px
- **Por defecto:** 400px
- **Función:** Controla el ancho del área de texto en cada línea
- **Ajuste:** Botones "+" y "-" de 50px

### **2. Tamaño de Botones de Acción (`action_button_size`)**
- **Rango:** 20px - 60px
- **Por defecto:** 35px
- **Función:** Controla el tamaño de los botones "✏️", "📋", "🗑️", "➕"
- **Ajuste:** Botones "+" y "-" de 5px

### **3. Espaciado Entre Líneas (`line_spacing`)**
- **Rango:** 2px - 20px
- **Por defecto:** 6px
- **Función:** Controla el espacio vertical entre las líneas de escenas
- **Ajuste:** Botones "+" y "-" de 1px

### **4. Padding de Botones (`button_padding`)**
- **Rango:** 0px - 10px
- **Por defecto:** 2px
- **Función:** Referencia para el desarrollador (estilos usan valores fijos)
- **Nota:** Los estilos de botones están optimizados para compactación

### **5. Margen de Botones (`button_margin`)**
- **Rango:** 0px - 10px
- **Por defecto:** 1px
- **Función:** Referencia para el desarrollador (estilos usan valores fijos)
- **Nota:** Los estilos de botones están optimizados para compactación

### **6. Scrollbars Horizontales (`show_horizontal_scrollbars`)**
- **Valores:** True/False
- **Por defecto:** True
- **Función:** Habilita scrollbars horizontales para ver todas las opciones
- **Beneficio:** Permite ver botones que se extienden más allá del área visible

### **7. Límites de Texto por Tipo**

#### **Diálogos (`text_limit_dialogue`)**
- **Rango:** 20 - 100 caracteres
- **Por defecto:** 35 caracteres
- **Función:** Cuántos caracteres mostrar antes de "..."

#### **Escenas (`text_limit_stage`)**
- **Rango:** 10 - 50 caracteres
- **Por defecto:** 15 caracteres
- **Función:** Límite para nombres de fondos

#### **Labels (`text_limit_label`)**
- **Rango:** 10 - 50 caracteres
- **Por defecto:** 20 caracteres
- **Función:** Límite para nombres de labels

#### **Jumps (`text_limit_jump`)**
- **Rango:** 10 - 50 caracteres
- **Por defecto:** 20 caracteres
- **Función:** Límite para destinos de jump

#### **Decisiones (`text_limit_choice`)**
- **Rango:** 15 - 60 caracteres
- **Por defecto:** 25 caracteres
- **Función:** Límite para preguntas de decisiones

## 🔧 **Configuración en el Código**

### **Ubicación de las Variables:**
- Se encuentran en la sección `default` del archivo `developer_tools.rpy`
- Líneas 351-358 aproximadamente
- Fácil acceso para el desarrollador

### **Cómo Modificar:**
- **Editar directamente:** Cambiar los valores en las líneas `default`
- **Guardar el archivo:** Los cambios se aplican al reiniciar
- **Sin interfaz de usuario:** Los usuarios finales no ven estos controles

## 🔧 **Variables de Configuración**

### **Ubicación en el Código:**
```python
# Variables para ajuste manual del layout
default content_width = 400  # Ancho del contenido de las líneas
default action_button_size = 35  # Tamaño de los botones de acción
default line_spacing = 6  # Espaciado entre líneas
default button_padding = 2  # Padding interno de los botones
default button_margin = 1  # Margen externo de los botones
default show_horizontal_scrollbars = True  # Mostrar scrollbars horizontales
default text_limit_dialogue = 35  # Límite de caracteres para diálogos
default text_limit_stage = 15  # Límite de caracteres para escenas
default text_limit_label = 20  # Límite de caracteres para labels
default text_limit_jump = 20  # Límite de caracteres para jumps
default text_limit_choice = 25  # Límite de caracteres para decisiones
```

### **Cómo Modificar:**
- **Editar valores:** Cambiar directamente los números después del `=`
- **Guardar archivo:** Los cambios se aplican al reiniciar Ren'Py
- **Sin reinicio de juego:** Solo reiniciar Ren'Py para ver cambios

## 🎯 **Casos de Uso**

### **1. Botones Muy Separados**
- **Problema:** Los botones de acción están muy separados
- **Solución:** 
  - Cambiar `action_button_size = 35` a `action_button_size = 25`
  - Los estilos ya están optimizados para compactación
- **Resultado:** Botones más compactos y juntos

### **2. Texto Muy Corto**
- **Problema:** El texto se corta demasiado pronto
- **Solución:** Cambiar `text_limit_dialogue = 35` a `text_limit_dialogue = 50`
- **Resultado:** Más texto visible en cada línea

### **3. Contenido Muy Ancho**
- **Problema:** El área de texto ocupa demasiado espacio
- **Solución:** Cambiar `content_width = 400` a `content_width = 300`
- **Resultado:** Más espacio para los botones de acción

### **4. Líneas Muy Juntas**
- **Problema:** Las líneas están muy pegadas
- **Solución:** Cambiar `line_spacing = 6` a `line_spacing = 8`
- **Resultado:** Mejor separación visual entre líneas

### **5. Opciones Fuera de Vista**
- **Problema:** Los botones de acción se salen del área visible
- **Solución:** Mantener `show_horizontal_scrollbars = True`
- **Resultado:** Scroll horizontal para ver todas las opciones

## ✅ **Beneficios del Sistema**

### **Control del Desarrollador:**
- ✅ **Configuración directa** en el código fuente
- ✅ **Valores personalizados** según necesidades del proyecto
- ✅ **Sin interferencia** para usuarios finales
- ✅ **Fácil mantenimiento** y actualización

### **Flexibilidad:**
- ✅ **Adaptable** a diferentes tamaños de pantalla
- ✅ **Personalizable** según necesidades del proyecto
- ✅ **Optimizable** para diferentes tipos de contenido
- ✅ **Escalable** para proyectos grandes o pequeños

### **Simplicidad:**
- ✅ **Sin interfaz adicional** para usuarios
- ✅ **Configuración centralizada** en un lugar
- ✅ **Cambios inmediatos** al reiniciar
- ✅ **Código limpio** y mantenible

### **Navegación Mejorada:**
- ✅ **Scrollbars horizontales** para ver todas las opciones
- ✅ **Indicador visual** cuando hay contenido extendido
- ✅ **Navegación natural** con scrollbars estándar
- ✅ **Acceso completo** a todas las funciones

## 🚀 **Configuraciones Recomendadas**

### **Configuración Compacta:**
- **content_width:** 300px
- **action_button_size:** 25px
- **line_spacing:** 4px
- **text_limit_dialogue:** 30 caracteres

### **Configuración Estándar:**
- **content_width:** 400px
- **action_button_size:** 35px
- **line_spacing:** 6px
- **text_limit_dialogue:** 35 caracteres

### **Configuración Espaciosa:**
- **content_width:** 500px
- **action_button_size:** 45px
- **line_spacing:** 8px
- **text_limit_dialogue:** 50 caracteres

## 🎯 **Resultado Final**

El sistema de configuración proporciona:
- **Control total** del desarrollador sobre el layout
- **Flexibilidad máxima** para diferentes necesidades
- **Optimización personalizada** del espacio
- **Interfaz limpia** para usuarios finales

¡Ahora puedes configurar exactamente cómo se ve tu editor editando el código! 🎛️
