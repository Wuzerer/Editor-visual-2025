# Script Directo para Editor Visual
# Versión con pantalla completa de agradecimiento

# Configuración para Editor Directo
init python:
    # Desactivar menús del juego
    config.main_menu = False
    config.game_menu = False
    
    # Configurar ventana de diálogo
    config.window = "hide"
    
    # Configurar transiciones instantáneas
    config.enter_transition = None
    config.exit_transition = None
    config.intra_transition = None
    config.after_load_transition = None
    config.end_game_transition = None
    
    # Configurar salida directa
    config.quit_action = Quit(confirm=False)
    
    # Ocultar título del juego
    gui.show_name = False

# El juego comienza aquí
label start:
    # Inicializar configuración básica
    if persistent.unlocked_gallery is None:
        $ persistent.unlocked_gallery = set()
    
    # Ir directamente al agradecimiento
    jump agradecimiento_editor

# Pantalla de agradecimiento completa
label agradecimiento_editor:
    scene black with fade
    
    # Mostrar pantalla completa de agradecimiento con mensajes de inicialización abajo
    $ renpy.show_screen("agradecimiento_completo")
    
    # Pausa para mostrar todo el contenido
    $ renpy.pause(7.5)
    
    # Ocultar pantalla de agradecimiento
    $ renpy.hide_screen("agradecimiento_completo")
    
    # Transición a la pantalla de inicialización dinámica
    scene black with fade
    
    # Mostrar pantalla de inicialización dinámica (mensajes se mueven al centro)
    $ renpy.show_screen("inicializacion_dinamica")
    
    # Pausa para mostrar la animación
    $ renpy.pause(4.0)
    
    # Ocultar pantalla de inicialización
    $ renpy.hide_screen("inicializacion_dinamica")
    
    # Ir directamente al editor visual real
    jump editor_directo

# Editor directo
label editor_directo:
    # Transición al editor
    scene black with fade
    
    # Mostrar el editor visual real directamente
    $ renpy.call_screen("visual_editor")
    
    return
