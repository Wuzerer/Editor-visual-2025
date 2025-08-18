# Configuración de la Pantalla de Agradecimiento
# Aquí puedes personalizar la pantalla de bienvenida

init python:
    # Configuración general
    AGRADECIMIENTO_CONFIG = {
        "usar_imagen_fondo": False,  # Cambiar a True para usar imagen
        "imagen_fondo": "images/backgrounds/main_menu_bg.png",  # Ruta de la imagen
        "duracion_total": 6.0,  # Duración en segundos
        "fade_in": 1.0,  # Tiempo de fade in
        "fade_out": 1.0,  # Tiempo de fade out
        "mostrar_boton_saltar": True,  # Mostrar botón para saltar
        "color_titulo": "#ffffff",  # Color del título principal
        "color_subtitulo": "#cccccc",  # Color del subtítulo
        "color_motivacional": "#ffff00",  # Color del mensaje motivacional
        "tamano_titulo": 32,  # Tamaño del título
        "tamano_subtitulo": 18,  # Tamaño del subtítulo
        "tamano_motivacional": 24,  # Tamaño del mensaje motivacional
    }
    
    # Mensajes personalizables
    AGRADECIMIENTO_MENSAJES = {
        "titulo": "¡GRACIAS POR USAR NUESTRO EDITOR VISUAL!",
        "subtitulo_1": "Esperamos que disfrutes experimentando con esta herramienta",
        "subtitulo_2": "para crear tus propias novelas visuales.",
        "motivacional": "¡Que tu creatividad no tenga límites!",
        "boton_saltar": "Comenzar ahora"
    }

# Función para obtener configuración
init python:
    def get_agradecimiento_config():
        """Retorna la configuración actual de agradecimiento"""
        return AGRADECIMIENTO_CONFIG
    
    def get_agradecimiento_mensajes():
        """Retorna los mensajes actuales de agradecimiento"""
        return AGRADECIMIENTO_MENSAJES
    
    def set_agradecimiento_imagen(ruta_imagen):
        """Establece una imagen de fondo para la pantalla de agradecimiento"""
        global AGRADECIMIENTO_CONFIG
        AGRADECIMIENTO_CONFIG["usar_imagen_fondo"] = True
        AGRADECIMIENTO_CONFIG["imagen_fondo"] = ruta_imagen
    
    def desactivar_agradecimiento_imagen():
        """Desactiva el uso de imagen de fondo"""
        global AGRADECIMIENTO_CONFIG
        AGRADECIMIENTO_CONFIG["usar_imagen_fondo"] = False
