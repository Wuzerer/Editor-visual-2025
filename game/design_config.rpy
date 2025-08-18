# design_config.rpy
# Configuración del sistema de diseño visual

init python:
    # Configuraciones por defecto del modo diseño
    design_settings = {
        'enabled': False,
        'show_grid': True,
        'grid_size': 10,
        'snap_enabled': True,
        'show_guides': True,
        'auto_save': True,
        'undo_levels': 10
    }
    
    # Configuraciones de colores para el modo diseño
    design_color_scheme = {
        'primary': "#3498db",
        'secondary': "#2ecc71", 
        'accent': "#f39c12",
        'warning': "#e74c3c",
        'background': "#2c3e50",
        'text': "#ffffff",
        'text_secondary': "#95a5a6"
    }
    
    # Configuraciones de herramientas
    design_tools_config = {
        'resize_handles': True,
        'drag_enabled': True,
        'color_picker': True,
        'preset_manager': True,
        'grid_snap': True,
        'alignment_guides': True
    }
    
    # Configuraciones de presets
    design_preset_config = {
        'auto_save_presets': True,
        'max_presets': 20,
        'default_preset': 'default',
        'backup_presets': True
    }

# Estilos para el modo diseño
style design_button:
    background "#3498db"
    hover_background "#2980b9"
    padding (10, 5)
    size 16
    color "#ffffff"

style design_button_warning:
    background "#e74c3c"
    hover_background "#c0392b"
    padding (10, 5)
    size 16
    color "#ffffff"

style design_button_success:
    background "#27ae60"
    hover_background "#229954"
    padding (10, 5)
    size 16
    color "#ffffff"

style design_text:
    color "#ffffff"
    size 16
    outlines [(2, "#000000", 0, 0)]

style design_title:
    color "#ffffff"
    size 20
    bold True
    outlines [(2, "#000000", 0, 0)]

style design_panel:
    background "#2c3e50"
    padding (15, 15)
    margin (5, 5)
