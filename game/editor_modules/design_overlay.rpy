# design_overlay.rpy
# Sistema de overlay para diseño visual interactivo
# Se superpone al editor existente sin modificarlo

init python:
    # Variables para el modo de diseño
    design_mode_active = False
    selected_element = None
    selected_element_width = 500
    selected_element_height = 400
    selected_element_x = 0
    selected_element_y = 0
    selected_color = "#ffffff"
    drag_start_pos = None
    resize_handle = None
    
    # Configuraciones de diseño
    design_grid_size = 10
    design_snap_enabled = True
    design_show_guides = True
    
    # Colores para las herramientas de diseño
    design_colors = {
        'overlay_bg': "#00000080",  # Fondo semi-transparente
        'handle_color': "#3498db",   # Color de los controles de redimensionamiento
        'guide_color': "#e74c3c",    # Color de las guías
        'grid_color': "#95a5a680",   # Color de la cuadrícula
        'selected_color': "#f39c12", # Color del elemento seleccionado
    }

# Transform para efectos de diseño
transform design_fade_in:
    alpha 0.0
    ease 0.3 alpha 1.0

transform design_handle_pulse:
    alpha 0.7
    ease 0.5 alpha 1.0
    ease 0.5 alpha 0.7
    repeat

# Pantalla de overlay de diseño
screen design_overlay():
    if design_mode_active:
        # Fondo semi-transparente para el modo diseño
        frame:
            xfill True
            yfill True
            background design_colors['overlay_bg']
            
        # Barra de herramientas de diseño
        frame:
            xalign 0.5
            yalign 0.0
            yoffset 10
            background "#2c3e50"
            padding (15, 10)
            
            hbox:
                spacing 15
                
                # Botón para desactivar modo diseño
                textbutton "❌ Salir Modo Diseño":
                    action SetVariable("design_mode_active", False)
                    background "#e74c3c"
                    padding (10, 5)
                    text_size 16
                
                # Toggle para mostrar guías
                textbutton "📏 Guías":
                    action ToggleVariable("design_show_guides")
                    background (design_show_guides and "#27ae60" or "#95a5a6")
                    padding (10, 5)
                    text_size 16
                
                # Toggle para snap
                textbutton "🔗 Snap":
                    action ToggleVariable("design_snap_enabled")
                    background (design_snap_enabled and "#27ae60" or "#95a5a6")
                    padding (10, 5)
                    text_size 16
                
                # Selector de tamaño de grid
                textbutton "🔲 Grid":
                    action Function(toggle_grid_size)
                    background "#3498db"
                    padding (10, 5)
                    text_size 16
        
        # Controles de redimensionamiento para paneles
        if selected_element:
            # Controles de redimensionamiento
            frame:
                xalign 0.0
                yalign 0.0
                xoffset 50
                yoffset 100
                background "#34495e"
                padding (10, 10)
                
                vbox:
                    spacing 8
                    
                    text "🎨 Controles de Diseño" color "#ffffff" size 18 bold True
                    
                    # Controles de tamaño
                    hbox:
                        spacing 10
                        
                        text "Ancho:" color "#ffffff" size 14
                        bar value ScreenVariableValue("selected_element_width", range=1000) xsize 100
                        text "[selected_element_width]px" color "#bdc3c7" size 12
                    
                    hbox:
                        spacing 10
                        
                        text "Alto:" color "#ffffff" size 14
                        bar value ScreenVariableValue("selected_element_height", range=800) xsize 100
                        text "[selected_element_height]px" color "#bdc3c7" size 12
                    
                    # Controles de posición
                    hbox:
                        spacing 10
                        
                        text "X:" color "#ffffff" size 14
                        bar value ScreenVariableValue("selected_element_x", range=1600) xsize 100
                        text "[selected_element_x]px" color "#bdc3c7" size 12
                    
                    hbox:
                        spacing 10
                        
                        text "Y:" color "#ffffff" size 14
                        bar value ScreenVariableValue("selected_element_y", range=900) xsize 100
                        text "[selected_element_y]px" color "#bdc3c7" size 12
                    
                    # Botones de acción
                    hbox:
                        spacing 8
                        
                        textbutton "💾 Guardar":
                            action Function(save_element_config)
                            background "#27ae60"
                            padding (8, 5)
                            text_size 14
                        
                        textbutton "🔄 Reset":
                            action Function(reset_element_config)
                            background "#f39c12"
                            padding (8, 5)
                            text_size 14
                        
                        textbutton "❌ Cancelar":
                            action SetVariable("selected_element", None)
                            background "#e74c3c"
                            padding (8, 5)
                            text_size 14

# Funciones de utilidad para el diseño
init python:
    def toggle_grid_size():
        """Alterna entre diferentes tamaños de grid"""
        global design_grid_size
        if design_grid_size == 5:
            design_grid_size = 10
        elif design_grid_size == 10:
            design_grid_size = 20
        else:
            design_grid_size = 5
    
    def save_element_config():
        """Guarda la configuración del elemento seleccionado"""
        if selected_element:
            # Aquí se guardaría la configuración
            renpy.notify("Configuración guardada")
    
    def reset_element_config():
        """Resetea la configuración del elemento seleccionado"""
        if selected_element:
            # Aquí se resetearía la configuración
            renpy.notify("Configuración reseteada")
    
    def activate_design_mode():
        """Activa el modo de diseño"""
        global design_mode_active
        design_mode_active = True
        renpy.notify("Modo diseño activado")
    
    def deactivate_design_mode():
        """Desactiva el modo de diseño"""
        global design_mode_active, selected_element
        design_mode_active = False
        selected_element = None
        renpy.notify("Modo diseño desactivado")
