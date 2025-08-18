# design_tools.rpy
# Herramientas de diseño visual
# Sistema de presets, selector de colores y utilidades

init python:
    # Sistema de presets de diseño
    design_presets = {
        'default': {
            'name': 'Diseño Por Defecto',
            'description': 'Configuración estándar del editor',
            'colors': {
                'background_panel': "#27ae60",
                'dialogue_panel': "#3498db",
                'character_panel': "#8e44ad",
                'preview_panel': "#8e44ad",
                'structure_panel': "#f39c12",
                'developer_panel': "#e74c3c"
            },
            'sizes': {
                'panel_width': 500,
                'panel_height': 400,
                'button_height': 35,
                'text_size': 18
            }
        },
        'dark_pro': {
            'name': 'Tema Oscuro Profesional',
            'description': 'Diseño oscuro para uso profesional',
            'colors': {
                'background_panel': "#2c3e50",
                'dialogue_panel': "#34495e",
                'character_panel': "#2c3e50",
                'preview_panel': "#34495e",
                'structure_panel': "#2c3e50",
                'developer_panel': "#34495e"
            },
            'sizes': {
                'panel_width': 550,
                'panel_height': 450,
                'button_height': 40,
                'text_size': 20
            }
        },
        'colorful': {
            'name': 'Tema Colorido',
            'description': 'Diseño vibrante y colorido',
            'colors': {
                'background_panel': "#e74c3c",
                'dialogue_panel': "#f39c12",
                'character_panel': "#f1c40f",
                'preview_panel': "#2ecc71",
                'structure_panel': "#3498db",
                'developer_panel': "#9b59b6"
            },
            'sizes': {
                'panel_width': 480,
                'panel_height': 380,
                'button_height': 30,
                'text_size': 16
            }
        }
    }
    
    # Preset actual
    current_design_preset = 'default'
    
    # Paleta de colores predefinida
    color_palette = [
        "#e74c3c", "#f39c12", "#f1c40f", "#2ecc71", "#27ae60",
        "#3498db", "#2980b9", "#9b59b6", "#8e44ad", "#e67e22",
        "#2c3e50", "#34495e", "#95a5a6", "#7f8c8d", "#1a252f",
        "#ffffff", "#000000", "#c8ffc8", "#ffc8c8", "#c8c8ff"
    ]
    
    # Colores personalizados del usuario
    custom_colors = []
    new_color_hex = "#ffffff"

# Pantalla del selector de colores
screen color_picker_screen():
    modal True
    
    frame:
        xfill True
        yfill True
        background "#00000080"
        
        frame:
            xalign 0.5
            yalign 0.5
            background "#2c3e50"
            padding (20, 20)
            
            vbox:
                spacing 15
                
                text "🎨 Selector de Colores" color "#ffffff" size 24 bold True xalign 0.5
                
                # Paleta de colores predefinidos
                vbox:
                    spacing 10
                    
                    text "Paleta Predefinida:" color "#ffffff" size 18
                    
                    # Grid de colores (5x4)
                    grid 5 4:
                        spacing 5
                        
                        for color in color_palette:
                            frame:
                                xsize 50
                                ysize 50
                                background color
                                
                                textbutton "":
                                    xfill True
                                    yfill True
                                    action Function(select_color, color)
                                
                                # Indicador de selección
                                if color == selected_color:
                                    text "✓" color "#ffffff" size 20 xalign 0.5 yalign 0.5
                
                # Colores personalizados
                vbox:
                    spacing 10
                    
                    text "Colores Personalizados:" color "#ffffff" size 18
                    
                    if custom_colors:
                        grid 5 2:
                            spacing 5
                            
                            for color in custom_colors:
                                frame:
                                    xsize 50
                                    ysize 50
                                    background color
                                    
                                    textbutton "":
                                        xfill True
                                        yfill True
                                        action Function(select_color, color)
                    else:
                        text "No hay colores personalizados" color "#95a5a6" size 14
                
                # Agregar color personalizado
                hbox:
                    spacing 10
                    xalign 0.5
                    
                    text "Nuevo color:" color "#ffffff" size 16
                    input value ScreenVariableInputValue("new_color_hex", "#ffffff") length 7
                    textbutton "➕ Agregar":
                        action Function(add_custom_color)
                        background "#27ae60"
                        padding (10, 5)
                
                # Botones de acción
                hbox:
                    spacing 15
                    xalign 0.5
                    
                    textbutton "✅ Aplicar":
                        action [Function(apply_selected_color), Hide("color_picker_screen")]
                        background "#27ae60"
                        padding (15, 10)
                    
                    textbutton "❌ Cancelar":
                        action Hide("color_picker_screen")
                        background "#e74c3c"
                        padding (15, 10)

# Pantalla de gestión de presets
screen design_presets_screen():
    modal True
    
    frame:
        xfill True
        yfill True
        background "#00000080"
        
        frame:
            xalign 0.5
            yalign 0.5
            xsize 800
            ysize 600
            background "#2c3e50"
            padding (20, 20)
            
            vbox:
                spacing 20
                
                text "🎨 Gestión de Presets de Diseño" color "#ffffff" size 24 bold True xalign 0.5
                
                # Lista de presets disponibles
                viewport:
                    xfill True
                    yfill True
                    scrollbars "vertical"
                    
                    vbox:
                        spacing 15
                        
                        for preset_id, preset_data in design_presets.items():
                            frame:
                                xfill True
                                background (preset_id == current_design_preset and "#34495e" or "#1a252f")
                                padding (15, 15)
                                
                                vbox:
                                    spacing 10
                                    
                                    hbox:
                                        spacing 15
                                        xfill True
                                        
                                        vbox:
                                            spacing 5
                                            xfill True
                                            
                                            text preset_data['name'] color "#ffffff" size 18 bold True
                                            text preset_data['description'] color "#95a5a6" size 14
                                        
                                        # Vista previa de colores
                                        hbox:
                                            spacing 5
                                            
                                            for color_name, color_value in preset_data['colors'].items():
                                                frame:
                                                    xsize 30
                                                    ysize 30
                                                    background color_value
                                        
                                        # Botones de acción
                                        vbox:
                                            spacing 5
                                            
                                            textbutton "🎨 Aplicar":
                                                action Function(apply_design_preset, preset_id)
                                                background "#27ae60"
                                                padding (8, 5)
                                                text_size 12
                                            
                                            if preset_id != 'default':
                                                textbutton "🗑️ Eliminar":
                                                    action Function(delete_design_preset, preset_id)
                                                    background "#e74c3c"
                                                    padding (8, 5)
                                                    text_size 12
                
                # Botones de acción principales
                hbox:
                    spacing 15
                    xalign 0.5
                    
                    textbutton "💾 Guardar Preset Actual":
                        action Function(save_current_as_preset)
                        background "#3498db"
                        padding (15, 10)
                    
                    textbutton "📁 Importar Preset":
                        action Function(import_preset)
                        background "#f39c12"
                        padding (15, 10)
                    
                    textbutton "❌ Cerrar":
                        action Hide("design_presets_screen")
                        background "#e74c3c"
                        padding (15, 10)

# Funciones de utilidad para el diseño
init python:
    def select_color(color):
        """Selecciona un color del selector"""
        global selected_color
        selected_color = color
        renpy.notify(f"Color {color} seleccionado")
    
    def apply_selected_color():
        """Aplica el color seleccionado al elemento actual"""
        if selected_element and selected_color:
            # Aquí se aplicaría el color al elemento
            renpy.notify(f"Color {selected_color} aplicado")
    
    def add_custom_color():
        """Agrega un color personalizado a la paleta"""
        global custom_colors, new_color_hex
        if new_color_hex and new_color_hex not in custom_colors:
            custom_colors.append(new_color_hex)
            new_color_hex = "#ffffff"
            renpy.notify("Color personalizado agregado")
    
    def apply_design_preset(preset_id):
        """Aplica un preset de diseño"""
        global current_design_preset
        if preset_id in design_presets:
            current_design_preset = preset_id
            preset_data = design_presets[preset_id]
            
            # Aplicar colores (si existe el objeto colors)
            try:
                if hasattr(renpy.store, 'colors'):
                    colors = renpy.store.colors
                    for color_name, color_value in preset_data['colors'].items():
                        if hasattr(colors, color_name):
                            setattr(colors, color_name, color_value)
            except:
                pass
            
            # Aplicar tamaños (si existe el objeto visual_layout)
            try:
                if hasattr(renpy.store, 'visual_layout'):
                    visual_layout = renpy.store.visual_layout
                    for size_name, size_value in preset_data['sizes'].items():
                        if hasattr(visual_layout, size_name):
                            setattr(visual_layout, size_name, size_value)
            except:
                pass
            
            renpy.notify(f"Preset '{preset_data['name']}' aplicado")
    
    def save_current_as_preset():
        """Guarda la configuración actual como un nuevo preset"""
        # Aquí se implementaría el guardado del preset actual
        renpy.notify("Preset actual guardado")
    
    def delete_design_preset(preset_id):
        """Elimina un preset de diseño"""
        if preset_id in design_presets and preset_id != 'default':
            del design_presets[preset_id]
            if current_design_preset == preset_id:
                current_design_preset = 'default'
            renpy.notify("Preset eliminado")
    
    def import_preset():
        """Importa un preset desde archivo"""
        # Aquí se implementaría la importación de presets
        renpy.notify("Función de importación en desarrollo")
