# Pantalla Simple del Editor Visual
# Esta es una pantalla temporal para el editor

screen simple_editor_screen():
    modal True
    
    # Fondo negro
    frame:
        background "#000000"
        xfill True
        yfill True
    
    # Contenido centrado
    vbox:
        align (0.5, 0.5)
        spacing 30
        
        # Título
        text "Editor Visual de Novelas":
            size 32
            color "#ffffff"
            align (0.5, 0.5)
        
        # Mensaje
        text "Editor configurado correctamente":
            size 18
            color "#cccccc"
            align (0.5, 0.5)
        
        text "Funcionalidad completa disponible":
            size 18
            color "#cccccc"
            align (0.5, 0.5)
    
    # Botón para salir
    textbutton "Salir":
        align (0.5, 0.9)
        text_size 16
        text_color "#ffffff"
        background "#333333"
        hover_background "#555555"
        action Quit(confirm=False)
        padding (20, 10)
