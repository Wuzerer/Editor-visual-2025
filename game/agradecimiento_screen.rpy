# Pantalla de Agradecimiento - Editor Visual
# Este archivo maneja la pantalla de bienvenida y agradecimiento

init python:
    # Configuración de la pantalla de agradecimiento
    AGRADECIMIENTO_DURACION = 6.0  # Duración total en segundos
    AGRADECIMIENTO_FADE_IN = 1.0   # Tiempo de fade in
    AGRADECIMIENTO_FADE_OUT = 1.0  # Tiempo de fade out

# Pantalla de agradecimiento
screen agradecimiento_screen():
    modal True
    
    # Fondo (negro o imagen según configuración)
    if AGRADECIMIENTO_CONFIG["usar_imagen_fondo"]:
        add AGRADECIMIENTO_CONFIG["imagen_fondo"]
    else:
        frame:
            background "#000000"
            xfill True
            yfill True
    
    # Contenido centrado
    vbox:
        align (0.5, 0.5)
        spacing 30
        
        # Título principal
        text AGRADECIMIENTO_MENSAJES["titulo"]:
            size AGRADECIMIENTO_CONFIG["tamano_titulo"]
            color AGRADECIMIENTO_CONFIG["color_titulo"]
            align (0.5, 0.5)
            font "DejaVuSans.ttf"
        
        # Mensaje secundario
        text AGRADECIMIENTO_MENSAJES["subtitulo_1"]:
            size AGRADECIMIENTO_CONFIG["tamano_subtitulo"]
            color AGRADECIMIENTO_CONFIG["color_subtitulo"]
            align (0.5, 0.5)
            font "DejaVuSans.ttf"
        
        text AGRADECIMIENTO_MENSAJES["subtitulo_2"]:
            size AGRADECIMIENTO_CONFIG["tamano_subtitulo"]
            color AGRADECIMIENTO_CONFIG["color_subtitulo"]
            align (0.5, 0.5)
            font "DejaVuSans.ttf"
        
        # Mensaje motivacional
        text AGRADECIMIENTO_MENSAJES["motivacional"]:
            size AGRADECIMIENTO_CONFIG["tamano_motivacional"]
            color AGRADECIMIENTO_CONFIG["color_motivacional"]
            align (0.5, 0.5)
            font "DejaVuSans.ttf"
    
    # Botón para saltar (opcional)
    if AGRADECIMIENTO_CONFIG["mostrar_boton_saltar"]:
        textbutton AGRADECIMIENTO_MENSAJES["boton_saltar"]:
            align (0.5, 0.9)
            text_size 16
            text_color "#ffffff"
            background "#333333"
            hover_background "#555555"
            action Jump("visual_editor_start")
            padding (20, 10)

# Función para mostrar la pantalla de agradecimiento
init python:
    def mostrar_agradecimiento():
        """Muestra la pantalla de agradecimiento y luego va al editor"""
        renpy.show_screen("agradecimiento_screen")
        renpy.pause(AGRADECIMIENTO_CONFIG["duracion_total"])
        renpy.hide_screen("agradecimiento_screen")
        renpy.jump("visual_editor_start")

# Label para mostrar agradecimiento con imagen opcional
label agradecimiento_con_imagen(imagen_fondo=None):
    if imagen_fondo:
        scene expression imagen_fondo with fade
    else:
        scene black with fade
    
    # Mostrar mensaje de agradecimiento con mejor formato
    centered "{size=+20}{color=#ffffff}¡GRACIAS POR USAR NUESTRO EDITOR VISUAL!{/color}{/size}"
    
    $ renpy.pause(1.5)
    
    centered "{size=+10}{color=#cccccc}Esperamos que disfrutes experimentando con esta herramienta{/color}{/size}"
    
    $ renpy.pause(1.0)
    
    centered "{size=+10}{color=#cccccc}para crear tus propias novelas visuales.{/color}{/size}"
    
    $ renpy.pause(1.0)
    
    centered "{size=+15}{color=#ffff00}¡Que tu creatividad no tenga límites!{/color}{/size}"
    
    # Pausa más larga para que el usuario lea
    $ renpy.pause(4.0)
    
    # Transición suave al editor visual
    scene black with fade
    
    # Ir directamente al editor visual
    jump visual_editor_start
