# layout_controller.rpy
# ===== SISTEMA CENTRAL DE CONTROL DE LAYOUT =====
# Este archivo es la FUENTE ÚNICA DE VERDAD para todas las configuraciones
# de layout del editor visual. Todos los demás archivos deben importar
# las clases e instancias desde aquí.

init -2 python:
    # ===== CONFIGURACIÓN GLOBAL DEL LAYOUT =====
    
    class VisualEditorLayout:
        """
        Clase principal para configurar el layout del editor visual.
        Contiene todas las dimensiones, espaciados y configuraciones visuales.
        """
        def __init__(self):
            # Dimensiones principales - Adaptativas a la resolución de la PC
            self.editor_width = 1800  # Más ancho para pantallas grandes
            self.editor_height = 1000  # Más alto para pantallas grandes
            self.editor_background = "#2c3e50"
            self.content_spacing = 15  # Más espacio
            
            # Layout optimizado: Vista previa y escenas más grandes
            self.top_area_height = 600  # Mucho más alto para mejor visualización
            self.bottom_area_height = 370  # Más pequeño para los paneles
            
            # Vista previa (izquierda del área superior)
            self.preview_area_width = 900  # Más ancho
            self.preview_area_height = 550  # Mucho más alto
            self.preview_background = "#1a252f"
            self.preview_textbox_ratio = 0.15
            self.preview_text_size = 20
            
            # Lista de escenas (derecha del área superior)
            self.scenes_area_width = 900  # Más ancho
            self.scenes_area_height = 550  # Mucho más alto
            self.scenes_background = "#2c3e50"
            
            # Paneles más compactos (área inferior)
            self.panel_width = 380  # Más compacto
            self.panel_height = 200  # Más compacto
            self.panel_spacing = 10  # Menos espacio entre paneles
            
            # Configuración de contenido
            self.line_height = 35  # Más alto
            self.content_width = 400  # Más ancho
            self.action_button_size = 32  # Botones más grandes
            
            # Configuración para viewports con scrollbars
            self.viewport_height = 300  # Altura para viewports de paneles
            self.scrollbar_width = 20  # Ancho de las scrollbars
            self.panel_padding = 20  # Padding interno de paneles
    
    class PanelColors:
        """
        Clase para definir los colores de todos los paneles del editor.
        Cada panel tiene su color distintivo para mejor identificación visual.
        """
        def __init__(self):
            self.background_panel = "#e74c3c"      # Rojo - Panel de fondos
            self.character_panel = "#3498db"       # Azul - Panel de personajes
            self.expressions_panel = "#9b59b6"     # Púrpura - Panel de expresiones
            self.stage_panel = "#f39c12"           # Naranja - Panel de escenario
            self.dialogue_panel = "#27ae60"        # Verde - Panel de diálogo
            self.structure_panel = "#8e44ad"       # Púrpura oscuro - Panel de estructura
            self.projects_panel = "#16a085"        # Verde azulado - Panel de proyectos
            self.developer_panel = "#e74c3c"       # Rojo - Panel de herramientas
            self.text_primary = "#ffffff"          # Blanco - Texto principal
            self.text_secondary = "#ecf0f1"        # Gris claro - Texto secundario
    
    class TextSizes:
        """
        Clase para definir los tamaños de texto utilizados en el editor.
        Mantiene consistencia visual en toda la interfaz.
        """
        def __init__(self):
            self.title_large = 28      # Títulos principales
            self.title_medium = 20     # Títulos de sección
            self.title_small = 18      # Subtítulos
            self.text_large = 16       # Texto grande
            self.text_medium = 14      # Texto normal
            self.text_small = 12       # Texto pequeño
    
    # ===== INSTANCIAS GLOBALES =====
    # Estas instancias son las que se usarán en todo el proyecto
    visual_layout = VisualEditorLayout()
    colors = PanelColors()
    text_sizes = TextSizes()
    
    print("✅ Layout central inicializado en layout_controller.rpy")
    
    # Verificación de atributos críticos
    if not hasattr(visual_layout, 'panel_padding'):
        print("⚠️ Agregando panel_padding faltante a visual_layout en layout_controller")
        visual_layout.panel_padding = 20
        print("✅ panel_padding agregado a visual_layout")
    
    # Verificación global para todas las instancias de VisualEditorLayout
    def ensure_panel_padding_global():
        """Asegura que todas las instancias de VisualEditorLayout tengan panel_padding"""
        try:
            # Verificar la instancia global
            if hasattr(renpy.store, 'visual_layout'):
                if not hasattr(renpy.store.visual_layout, 'panel_padding'):
                    print("⚠️ Agregando panel_padding a instancia global de visual_layout en layout_controller")
                    renpy.store.visual_layout.panel_padding = 20
                    print("✅ panel_padding agregado a instancia global en layout_controller")
            
            # Verificar la instancia local
            if 'visual_layout' in globals():
                if not hasattr(globals()['visual_layout'], 'panel_padding'):
                    print("⚠️ Agregando panel_padding a instancia local de visual_layout en layout_controller")
                    globals()['visual_layout'].panel_padding = 20
                    print("✅ panel_padding agregado a instancia local en layout_controller")
                    
        except Exception as e:
            print(f"⚠️ Error en verificación global de panel_padding en layout_controller: {e}")
    
    # Ejecutar verificación global
    ensure_panel_padding_global()
    
    # Función de seguridad para obtener panel_padding
    def get_panel_padding(layout_obj=None):
        """Obtiene el panel_padding de forma segura, con valor por defecto si no existe"""
        try:
            if layout_obj is None:
                layout_obj = visual_layout
            
            if hasattr(layout_obj, 'panel_padding'):
                return layout_obj.panel_padding
            else:
                # Agregar el atributo si no existe
                layout_obj.panel_padding = 20
                print(f"⚠️ Agregando panel_padding faltante a {type(layout_obj).__name__} en layout_controller")
                return 20
        except Exception as e:
            print(f"⚠️ Error obteniendo panel_padding en layout_controller: {e}")
            return 20  # Valor por defecto seguro
    
    # Función para obtener padding como tupla (compatible con Ren'Py)
    def get_panel_padding_tuple(layout_obj=None):
        """Obtiene el panel_padding como tupla para compatibilidad con Ren'Py"""
        try:
            padding_value = get_panel_padding(layout_obj)
            # Si es un entero, convertirlo a tupla de 4 elementos
            if isinstance(padding_value, int):
                return (padding_value, padding_value, padding_value, padding_value)
            # Si ya es una tupla, devolverla tal como está
            elif isinstance(padding_value, (tuple, list)):
                return tuple(padding_value)
            else:
                return (20, 20, 20, 20)  # Valor por defecto seguro
        except Exception as e:
            print(f"⚠️ Error obteniendo panel_padding_tuple en layout_controller: {e}")
            return (20, 20, 20, 20)  # Valor por defecto seguro

# ===== INICIALIZACIÓN DE CONFIGURACIÓN PERSISTENTE =====

init -1 python:
    # Cargar configuración persistente al inicio
    try:
        from persistent_config import persistent_config
        if persistent_config.load_config():
            # Aplicar configuración cargada a las variables globales
            config_data = persistent_config.config
            
            # Aplicar layout
            if 'layout' in config_data:
                layout_data = config_data['layout']
                for key, value in layout_data.items():
                    if hasattr(visual_layout, key):
                        setattr(visual_layout, key, value)
            
            # Aplicar colores
            if 'colors' in config_data:
                colors_data = config_data['colors']
                for key, value in colors_data.items():
                    if hasattr(colors, key):
                        setattr(colors, key, value)
            
            # Aplicar tamaños de texto
            if 'text_sizes' in config_data:
                text_data = config_data['text_sizes']
                for key, value in text_data.items():
                    if hasattr(text_sizes, key):
                        setattr(text_sizes, key, value)
            
            print("✅ Configuración persistente cargada al inicio")
        else:
            print("ℹ️ No se encontró configuración persistente, usando valores por defecto")
    except Exception as e:
        print(f"⚠️ Error al cargar configuración persistente: {e}")

# ===== VARIABLES GLOBALES PARA EL CONFIGURADOR =====

init -1 python:
    # Variables globales para almacenar los valores del configurador
    config_editor_width = 1800
    config_editor_height = 1000
    config_top_area_height = 600
    config_bottom_area_height = 370
    config_preview_area_width = 900
    config_preview_area_height = 550
    config_scenes_area_width = 900
    config_scenes_area_height = 550
    config_panel_width = 380
    config_panel_height = 200
    config_panel_spacing = 10
    config_preview_textbox_ratio = 0.15
    config_preview_text_size = 20
    config_line_height = 30
    config_content_width = 350
    config_action_button_size = 28
    
    # Variables globales para colores
    config_background_panel_color = "#e74c3c"
    config_character_panel_color = "#3498db"
    config_expressions_panel_color = "#9b59b6"
    config_stage_panel_color = "#f39c12"
    config_dialogue_panel_color = "#27ae60"
    config_structure_panel_color = "#8e44ad"
    config_projects_panel_color = "#16a085"
    config_developer_panel_color = "#e74c3c"
    
    # Variables globales para tamaños de texto
    config_title_large_size = 28
    config_title_medium_size = 20
    config_title_small_size = 18
    config_text_large_size = 16
    config_text_medium_size = 14
    config_text_small_size = 12

# ===== FUNCIONES DE SINCRONIZACIÓN =====

init -1 python:
    def force_screen_refresh():
        """Fuerza la actualización de todas las pantallas"""
        try:
            renpy.restart_interaction()
        except:
            pass
    
    def apply_all_changes():
        """Aplica todos los cambios de una vez usando variables globales"""
        try:
            global visual_layout, colors, text_sizes
            
            # Aplicar todos los cambios de layout usando variables globales
            visual_layout.editor_width = config_editor_width
            visual_layout.editor_height = config_editor_height
            visual_layout.top_area_height = config_top_area_height
            visual_layout.bottom_area_height = config_bottom_area_height
            visual_layout.preview_area_width = config_preview_area_width
            visual_layout.preview_area_height = config_preview_area_height
            visual_layout.scenes_area_width = config_scenes_area_width
            visual_layout.scenes_area_height = config_scenes_area_height
            visual_layout.panel_width = config_panel_width
            visual_layout.panel_height = config_panel_height
            visual_layout.panel_spacing = config_panel_spacing
            visual_layout.preview_textbox_ratio = config_preview_textbox_ratio
            visual_layout.preview_text_size = config_preview_text_size
            visual_layout.line_height = config_line_height
            visual_layout.content_width = config_content_width
            visual_layout.action_button_size = config_action_button_size
            
            # Aplicar todos los cambios de colores usando variables globales
            colors.background_panel = config_background_panel_color
            colors.character_panel = config_character_panel_color
            colors.expressions_panel = config_expressions_panel_color
            colors.stage_panel = config_stage_panel_color
            colors.dialogue_panel = config_dialogue_panel_color
            colors.structure_panel = config_structure_panel_color
            colors.projects_panel = config_projects_panel_color
            colors.developer_panel = config_developer_panel_color
            
            # Aplicar todos los cambios de tamaños de texto usando variables globales
            text_sizes.title_large = config_title_large_size
            text_sizes.title_medium = config_title_medium_size
            text_sizes.title_small = config_title_small_size
            text_sizes.text_large = config_text_large_size
            text_sizes.text_medium = config_text_medium_size
            text_sizes.text_small = config_text_small_size
            
            # Forzar actualización completa
            renpy.restart_interaction()
            renpy.notify("✅ Todos los cambios aplicados al editor")
        except Exception as e:
            renpy.notify(f"❌ Error: {str(e)}")
    
    def apply_single_change(var_name, new_value):
        """Aplica un cambio individual inmediatamente"""
        try:
            global visual_layout, colors, text_sizes
            
            # Aplicar cambio según el tipo de variable
            if var_name == "editor_width":
                visual_layout.editor_width = new_value
                config_editor_width = new_value
            elif var_name == "editor_height":
                visual_layout.editor_height = new_value
                config_editor_height = new_value
            elif var_name == "top_area_height":
                visual_layout.top_area_height = new_value
                config_top_area_height = new_value
            elif var_name == "bottom_area_height":
                visual_layout.bottom_area_height = new_value
                config_bottom_area_height = new_value
            elif var_name == "preview_area_width":
                visual_layout.preview_area_width = new_value
                config_preview_area_width = new_value
            elif var_name == "preview_area_height":
                visual_layout.preview_area_height = new_value
                config_preview_area_height = new_value
            elif var_name == "scenes_area_width":
                visual_layout.scenes_area_width = new_value
                config_scenes_area_width = new_value
            elif var_name == "scenes_area_height":
                visual_layout.scenes_area_height = new_value
                config_scenes_area_height = new_value
            elif var_name == "panel_width":
                visual_layout.panel_width = new_value
                config_panel_width = new_value
            elif var_name == "panel_height":
                visual_layout.panel_height = new_value
                config_panel_height = new_value
            elif var_name == "panel_spacing":
                visual_layout.panel_spacing = new_value
                config_panel_spacing = new_value
            elif var_name == "preview_textbox_ratio":
                visual_layout.preview_textbox_ratio = new_value
                config_preview_textbox_ratio = new_value
            elif var_name == "preview_text_size":
                visual_layout.preview_text_size = new_value
                config_preview_text_size = new_value
            elif var_name == "line_height":
                visual_layout.line_height = new_value
                config_line_height = new_value
            elif var_name == "content_width":
                visual_layout.content_width = new_value
                config_content_width = new_value
            elif var_name == "action_button_size":
                visual_layout.action_button_size = new_value
                config_action_button_size = new_value
            elif var_name == "title_large_size":
                text_sizes.title_large = new_value
                config_title_large_size = new_value
            elif var_name == "title_medium_size":
                text_sizes.title_medium = new_value
                config_title_medium_size = new_value
            elif var_name == "title_small_size":
                text_sizes.title_small = new_value
                config_title_small_size = new_value
            elif var_name == "text_large_size":
                text_sizes.text_large = new_value
                config_text_large_size = new_value
            elif var_name == "text_medium_size":
                text_sizes.text_medium = new_value
                config_text_medium_size = new_value
            elif var_name == "text_small_size":
                text_sizes.text_small = new_value
                config_text_small_size = new_value
            
            # Forzar actualización
            renpy.restart_interaction()
            renpy.notify(f"✅ {var_name} actualizado a {new_value}")
        except Exception as e:
            renpy.notify(f"❌ Error: {str(e)}")
    
    def apply_color_change(color_var, new_color):
        """Aplica un cambio de color inmediatamente"""
        try:
            global colors
            global config_background_panel_color, config_character_panel_color, config_expressions_panel_color
            global config_stage_panel_color, config_dialogue_panel_color, config_structure_panel_color
            global config_projects_panel_color, config_developer_panel_color
            
            # Extraer el nombre del panel del color_var (ej: "background_panel_color" -> "background_panel")
            panel_name = color_var.replace("_color", "")
            
            # Actualizar variable global correspondiente
            if panel_name == "background_panel":
                config_background_panel_color = new_color
            elif panel_name == "character_panel":
                config_character_panel_color = new_color
            elif panel_name == "expressions_panel":
                config_expressions_panel_color = new_color
            elif panel_name == "stage_panel":
                config_stage_panel_color = new_color
            elif panel_name == "dialogue_panel":
                config_dialogue_panel_color = new_color
            elif panel_name == "structure_panel":
                config_structure_panel_color = new_color
            elif panel_name == "projects_panel":
                config_projects_panel_color = new_color
            elif panel_name == "developer_panel":
                config_developer_panel_color = new_color
            
            # Aplicar cambio al objeto global
            setattr(colors, panel_name, new_color)
            force_screen_refresh()
            renpy.notify(f"✅ Color {panel_name} actualizado a {new_color}")
        except Exception as e:
            renpy.notify(f"❌ Error: {str(e)}")
    
    def test_color_temporarily(color_var, color_input):
        """Prueba un color temporalmente"""
        try:
            global colors
            # Extraer el nombre del panel del color_var (ej: "background_panel_color" -> "background_panel")
            panel_name = color_var.replace("_color", "")
            setattr(colors, panel_name, color_input)
            force_screen_refresh()
            renpy.notify("👁️ Color probado temporalmente")
        except Exception as e:
            renpy.notify(f"❌ Error: {str(e)}")
    
    def update_layout_variable(var_name, new_value):
        """Actualiza una variable de layout global"""
        try:
            global config_editor_width, config_editor_height, config_left_panel_width, config_right_panel_width
            global config_preview_area_ratio, config_scenes_area_ratio, config_preview_textbox_ratio, config_preview_text_size
            global config_line_height, config_content_width, config_action_button_size
            
            if var_name == "editor_width":
                config_editor_width = new_value
            elif var_name == "editor_height":
                config_editor_height = new_value
            elif var_name == "left_panel_width":
                config_left_panel_width = new_value
            elif var_name == "right_panel_width":
                config_right_panel_width = new_value
            elif var_name == "preview_area_ratio":
                config_preview_area_ratio = new_value
            elif var_name == "scenes_area_ratio":
                config_scenes_area_ratio = new_value
            elif var_name == "preview_textbox_ratio":
                config_preview_textbox_ratio = new_value
            elif var_name == "preview_text_size":
                config_preview_text_size = new_value
            elif var_name == "line_height":
                config_line_height = new_value
            elif var_name == "content_width":
                config_content_width = new_value
            elif var_name == "action_button_size":
                config_action_button_size = new_value
        except Exception as e:
            print(f"Error actualizando variable de layout: {e}")
    
    def update_text_size_variable(var_name, new_value):
        """Actualiza una variable de tamaño de texto global"""
        try:
            global config_title_large_size, config_title_medium_size, config_title_small_size
            global config_text_large_size, config_text_medium_size, config_text_small_size
            
            if var_name == "title_large_size":
                config_title_large_size = new_value
            elif var_name == "title_medium_size":
                config_title_medium_size = new_value
            elif var_name == "title_small_size":
                config_title_small_size = new_value
            elif var_name == "text_large_size":
                config_text_large_size = new_value
            elif var_name == "text_medium_size":
                config_text_medium_size = new_value
            elif var_name == "text_small_size":
                config_text_small_size = new_value
        except Exception as e:
            print(f"Error actualizando variable de texto: {e}")
    
    def save_from_screen_variables():
        """Guarda configuración desde variables globales del configurador"""
        try:
            # Aplicar cambios del configurador antes de guardar
            apply_all_changes()
            
            # Guardar configuración actual
            save_current_configuration()
            
            renpy.notify("✅ Cambios aplicados y guardados")
        except Exception as e:
            # Si hay error, usar configuración actual
            renpy.notify("⚠️ Guardando configuración actual")
            save_current_configuration()
    
    def save_current_configuration():
        """Guarda la configuración actual de forma robusta"""
        try:
            global visual_layout, colors, text_sizes
            
            # Guardar layout
            persistent_config.update_config('layout', 'editor_width', visual_layout.editor_width)
            persistent_config.update_config('layout', 'editor_height', visual_layout.editor_height)
            persistent_config.update_config('layout', 'left_panel_width', visual_layout.left_panel_width)
            persistent_config.update_config('layout', 'right_panel_width', visual_layout.right_panel_width)
            persistent_config.update_config('layout', 'preview_area_ratio', visual_layout.preview_area_ratio)
            persistent_config.update_config('layout', 'scenes_area_ratio', visual_layout.scenes_area_ratio)
            persistent_config.update_config('layout', 'preview_textbox_ratio', visual_layout.preview_textbox_ratio)
            persistent_config.update_config('layout', 'preview_text_size', visual_layout.preview_text_size)
            persistent_config.update_config('layout', 'line_height', visual_layout.line_height)
            persistent_config.update_config('layout', 'content_width', visual_layout.content_width)
            persistent_config.update_config('layout', 'action_button_size', visual_layout.action_button_size)
            
            # Guardar colores
            persistent_config.update_config('colors', 'background_panel', colors.background_panel)
            persistent_config.update_config('colors', 'character_panel', colors.character_panel)
            persistent_config.update_config('colors', 'expressions_panel', colors.expressions_panel)
            persistent_config.update_config('colors', 'stage_panel', colors.stage_panel)
            persistent_config.update_config('colors', 'dialogue_panel', colors.dialogue_panel)
            persistent_config.update_config('colors', 'structure_panel', colors.structure_panel)
            persistent_config.update_config('colors', 'projects_panel', colors.projects_panel)
            persistent_config.update_config('colors', 'developer_panel', colors.developer_panel)
            
            # Guardar tamaños de texto
            persistent_config.update_config('text_sizes', 'title_large', text_sizes.title_large)
            persistent_config.update_config('text_sizes', 'title_medium', text_sizes.title_medium)
            persistent_config.update_config('text_sizes', 'title_small', text_sizes.title_small)
            persistent_config.update_config('text_sizes', 'text_large', text_sizes.text_large)
            persistent_config.update_config('text_sizes', 'text_medium', text_sizes.text_medium)
            persistent_config.update_config('text_sizes', 'text_small', text_sizes.text_small)
            
            # Guardar archivo
            if persistent_config.save_config():
                renpy.notify("✅ Configuración guardada exitosamente")
            else:
                renpy.notify("❌ Error al guardar configuración")
        except Exception as e:
            renpy.notify(f"❌ Error: {str(e)}")
    
    def load_persistent_to_editor():
        """Carga configuración persistente al editor"""
        try:
            if persistent_config.load_config():
                # Aplicar configuración cargada a las variables globales
                config_data = persistent_config.config
                
                # Aplicar layout
                if 'layout' in config_data:
                    layout_data = config_data['layout']
                    for key, value in layout_data.items():
                        if hasattr(visual_layout, key):
                            setattr(visual_layout, key, value)
                
                # Aplicar colores
                if 'colors' in config_data:
                    colors_data = config_data['colors']
                    for key, value in colors_data.items():
                        if hasattr(colors, key):
                            setattr(colors, key, value)
                
                # Aplicar tamaños de texto
                if 'text_sizes' in config_data:
                    text_data = config_data['text_sizes']
                    for key, value in text_data.items():
                        if hasattr(text_sizes, key):
                            setattr(text_sizes, key, value)
                
                # Sincronizar variables globales
                sync_screen_variables_to_globals()
                
                # Forzar actualización completa
                renpy.restart_interaction()
                renpy.notify("✅ Configuración persistente cargada")
            else:
                renpy.notify("❌ No se encontró configuración persistente")
        except Exception as e:
            renpy.notify(f"❌ Error: {str(e)}")
    
    def reset_to_default_persistent():
        """Restaura configuración predeterminada"""
        try:
            global visual_layout, colors, text_sizes
            
            # Restaurar valores por defecto
            visual_layout = VisualEditorLayout()
            colors = PanelColors()
            text_sizes = TextSizes()
            
            # Verificación de atributos críticos después de crear nueva instancia
            if not hasattr(visual_layout, 'panel_padding'):
                print("⚠️ Agregando panel_padding faltante después de reset")
                visual_layout.panel_padding = 20
                print("✅ panel_padding agregado después de reset")
            
            # Sincronizar variables globales
            sync_screen_variables_to_globals()
            
            # Forzar actualización completa
            renpy.restart_interaction()
            renpy.notify("✅ Configuración restaurada a valores por defecto")
        except Exception as e:
            renpy.notify(f"❌ Error: {str(e)}")

    def sync_screen_variables_to_globals():
        """Sincroniza las variables de pantalla con las globales cuando se abre el configurador"""
        try:
            global visual_layout, colors, text_sizes
            global config_editor_width, config_editor_height, config_top_area_height, config_bottom_area_height
            global config_preview_area_width, config_preview_area_height, config_scenes_area_width, config_scenes_area_height
            global config_panel_width, config_panel_height, config_panel_spacing, config_preview_textbox_ratio, config_preview_text_size
            global config_line_height, config_content_width, config_action_button_size
            global config_background_panel_color, config_character_panel_color, config_expressions_panel_color
            global config_stage_panel_color, config_dialogue_panel_color, config_structure_panel_color
            global config_projects_panel_color, config_developer_panel_color
            global config_title_large_size, config_title_medium_size, config_title_small_size
            global config_text_large_size, config_text_medium_size, config_text_small_size
            
            # Sincronizar desde los objetos globales actuales
            config_editor_width = visual_layout.editor_width
            config_editor_height = visual_layout.editor_height
            config_top_area_height = visual_layout.top_area_height
            config_bottom_area_height = visual_layout.bottom_area_height
            config_preview_area_width = visual_layout.preview_area_width
            config_preview_area_height = visual_layout.preview_area_height
            config_scenes_area_width = visual_layout.scenes_area_width
            config_scenes_area_height = visual_layout.scenes_area_height
            config_panel_width = visual_layout.panel_width
            config_panel_height = visual_layout.panel_height
            config_panel_spacing = visual_layout.panel_spacing
            config_preview_textbox_ratio = visual_layout.preview_textbox_ratio
            config_preview_text_size = visual_layout.preview_text_size
            config_line_height = visual_layout.line_height
            config_content_width = visual_layout.content_width
            config_action_button_size = visual_layout.action_button_size
            
            config_background_panel_color = colors.background_panel
            config_character_panel_color = colors.character_panel
            config_expressions_panel_color = colors.expressions_panel
            config_stage_panel_color = colors.stage_panel
            config_dialogue_panel_color = colors.dialogue_panel
            config_structure_panel_color = colors.structure_panel
            config_projects_panel_color = colors.projects_panel
            config_developer_panel_color = colors.developer_panel
            
            config_title_large_size = text_sizes.title_large
            config_title_medium_size = text_sizes.title_medium
            config_title_small_size = text_sizes.title_small
            config_text_large_size = text_sizes.text_large
            config_text_medium_size = text_sizes.text_medium
            config_text_small_size = text_sizes.text_small
            
        except Exception as e:
            print(f"Error sincronizando variables: {e}")
    
    def update_screen_variables_from_globals():
        """Actualiza las variables de pantalla desde las globales"""
        try:
            # Esta función se llama cuando se muestra la pantalla del configurador
            sync_screen_variables_to_globals()
        except Exception as e:
            print(f"Error actualizando variables de pantalla: {e}")

# ===== PANTALLA DE CONFIGURACIÓN =====

screen layout_configurator():
    modal True
    
    default current_tab = "dimensions"
    
    # Variables de pantalla que se sincronizan con las globales
    default editor_width = config_editor_width
    default editor_height = config_editor_height
    default top_area_height = config_top_area_height
    default bottom_area_height = config_bottom_area_height
    default preview_area_width = config_preview_area_width
    default preview_area_height = config_preview_area_height
    default scenes_area_width = config_scenes_area_width
    default scenes_area_height = config_scenes_area_height
    default panel_width = config_panel_width
    default panel_height = config_panel_height
    default panel_spacing = config_panel_spacing
    default preview_textbox_ratio = config_preview_textbox_ratio
    default preview_text_size = config_preview_text_size
    default line_height = config_line_height
    default content_width = config_content_width
    default action_button_size = config_action_button_size
    
    # Variables de pantalla para colores
    default background_panel_color = config_background_panel_color
    default character_panel_color = config_character_panel_color
    default expressions_panel_color = config_expressions_panel_color
    default stage_panel_color = config_stage_panel_color
    default dialogue_panel_color = config_dialogue_panel_color
    default structure_panel_color = config_structure_panel_color
    default projects_panel_color = config_projects_panel_color
    default developer_panel_color = config_developer_panel_color
    
    # Variables de pantalla para tamaños de texto
    default title_large_size = config_title_large_size
    default title_medium_size = config_title_medium_size
    default title_small_size = config_title_small_size
    default text_large_size = config_text_large_size
    default text_medium_size = config_text_medium_size
    default text_small_size = config_text_small_size
    
    # Actualizar variables de pantalla cuando se muestra la pantalla
    on "show" action Function(update_screen_variables_from_globals)
    
    add Solid("#1a1a1a")
    
    frame:
        background "#2c3e50"
        padding (30, 30)
        xalign 0.5
        yalign 0.5
        xsize 1000
        ysize 700
        
        vbox:
            spacing 20
            
            text "🎨 Configurador de Layout" size 32 color "#ffffff" xalign 0.5
            
            # Pestañas
            hbox:
                spacing 10
                xalign 0.5
                
                textbutton "📏 Dimensiones" action SetScreenVariable("current_tab", "dimensions") style "config_tab_button"
                textbutton "🎨 Colores" action SetScreenVariable("current_tab", "colors") style "config_tab_button"
                textbutton "📝 Texto" action SetScreenVariable("current_tab", "text") style "config_tab_button"
                textbutton "💾 Guardar" action SetScreenVariable("current_tab", "save") style "config_tab_button"
            
            # Contenido de las pestañas
            viewport:
                scrollbars "vertical"
                mousewheel True
                xsize 940
                ysize 500
                
                if current_tab == "dimensions":
                    text "📏 Dimensiones del Editor Compacto" size 24 color "#ecf0f1" xalign 0.5
                    
                    text "🖥️ Dimensiones Principales" size 20 color "#ecf0f1" xalign 0.5
                    
                    grid 2 2:
                        spacing 20
                        
                        vbox:
                            text "Ancho del Editor:" color "#ecf0f1"
                            bar value ScreenVariableValue("editor_width", range=2000) xsize 200
                            textbutton "Aplicar" action Function(apply_single_change, "editor_width", editor_width) xalign 0.5
                            text "[editor_width]px" color "#bdc3c7" size 14
                        
                        vbox:
                            text "Alto del Editor:" color "#ecf0f1"
                            bar value ScreenVariableValue("editor_height", range=1200) xsize 200
                            textbutton "Aplicar" action Function(apply_single_change, "editor_height", editor_height) xalign 0.5
                            text "[editor_height]px" color "#bdc3c7" size 14
                    
                    text "📊 Áreas Superior e Inferior" size 20 color "#ecf0f1" xalign 0.5
                    
                    grid 2 2:
                        spacing 20
                        
                        vbox:
                            text "Altura Área Superior:" color "#ecf0f1"
                            bar value ScreenVariableValue("top_area_height", range=600) xsize 200
                            textbutton "Aplicar" action Function(apply_single_change, "top_area_height", top_area_height) xalign 0.5
                            text "[top_area_height]px" color "#bdc3c7" size 14
                        
                        vbox:
                            text "Altura Área Inferior:" color "#ecf0f1"
                            bar value ScreenVariableValue("bottom_area_height", range=600) xsize 200
                            textbutton "Aplicar" action Function(apply_single_change, "bottom_area_height", bottom_area_height) xalign 0.5
                            text "[bottom_area_height]px" color "#bdc3c7" size 14
                    
                    text "👁️ Vista Previa (Área Superior Izquierda)" size 20 color "#ecf0f1" xalign 0.5
                    
                    grid 2 2:
                        spacing 20
                        
                        vbox:
                            text "Ancho Vista Previa:" color "#ecf0f1"
                            bar value ScreenVariableValue("preview_area_width", range=1000) xsize 200
                            textbutton "Aplicar" action Function(apply_single_change, "preview_area_width", preview_area_width) xalign 0.5
                            text "[preview_area_width]px" color "#bdc3c7" size 14
                        
                        vbox:
                            text "Alto Vista Previa:" color "#ecf0f1"
                            bar value ScreenVariableValue("preview_area_height", range=500) xsize 200
                            textbutton "Aplicar" action Function(apply_single_change, "preview_area_height", preview_area_height) xalign 0.5
                            text "[preview_area_height]px" color "#bdc3c7" size 14
                    
                    text "📝 Lista de Escenas (Área Superior Derecha)" size 20 color "#ecf0f1" xalign 0.5
                    
                    grid 2 2:
                        spacing 20
                        
                        vbox:
                            text "Ancho Lista Escenas:" color "#ecf0f1"
                            bar value ScreenVariableValue("scenes_area_width", range=1000) xsize 200
                            textbutton "Aplicar" action Function(apply_single_change, "scenes_area_width", scenes_area_width) xalign 0.5
                            text "[scenes_area_width]px" color "#bdc3c7" size 14
                        
                        vbox:
                            text "Alto Lista Escenas:" color "#ecf0f1"
                            bar value ScreenVariableValue("scenes_area_height", range=500) xsize 200
                            textbutton "Aplicar" action Function(apply_single_change, "scenes_area_height", scenes_area_height) xalign 0.5
                            text "[scenes_area_height]px" color "#bdc3c7" size 14
                    
                    text "🎛️ Paneles (Área Inferior - 4 por Fila)" size 20 color "#ecf0f1" xalign 0.5
                    
                    grid 2 2:
                        spacing 20
                        
                        vbox:
                            text "Ancho de Panel:" color "#ecf0f1"
                            bar value ScreenVariableValue("panel_width", range=500) xsize 200
                            textbutton "Aplicar" action Function(apply_single_change, "panel_width", panel_width) xalign 0.5
                            text "[panel_width]px" color "#bdc3c7" size 14
                        
                        vbox:
                            text "Alto de Panel:" color "#ecf0f1"
                            bar value ScreenVariableValue("panel_height", range=300) xsize 200
                            textbutton "Aplicar" action Function(apply_single_change, "panel_height", panel_height) xalign 0.5
                            text "[panel_height]px" color "#bdc3c7" size 14
                        
                        vbox:
                            text "Espacio entre Paneles:" color "#ecf0f1"
                            bar value ScreenVariableValue("panel_spacing", range=30) xsize 200
                            textbutton "Aplicar" action Function(apply_single_change, "panel_spacing", panel_spacing) xalign 0.5
                            text "[panel_spacing]px" color "#bdc3c7" size 14
                        
                        vbox:
                            text "Ratio Textbox Previa:" color "#ecf0f1"
                            bar value ScreenVariableValue("preview_textbox_ratio", range=0.5) xsize 200
                            textbutton "Aplicar" action Function(apply_single_change, "preview_textbox_ratio", preview_textbox_ratio) xalign 0.5
                            text "[preview_textbox_ratio]" color "#bdc3c7" size 14
                    
                    text "🔧 Configuración de Contenido" size 20 color "#ecf0f1" xalign 0.5
                    
                    grid 2 2:
                        spacing 20
                        
                        vbox:
                            text "Tamaño Texto Previa:" color "#ecf0f1"
                            bar value ScreenVariableValue("preview_text_size", range=50) xsize 200
                            textbutton "Aplicar" action Function(apply_single_change, "preview_text_size", preview_text_size) xalign 0.5
                            text "[preview_text_size]px" color "#bdc3c7" size 14
                        
                        vbox:
                            text "Altura de Línea:" color "#ecf0f1"
                            bar value ScreenVariableValue("line_height", range=100) xsize 200
                            textbutton "Aplicar" action Function(apply_single_change, "line_height", line_height) xalign 0.5
                            text "[line_height]px" color "#bdc3c7" size 14
                        
                        vbox:
                            text "Ancho de Contenido:" color "#ecf0f1"
                            bar value ScreenVariableValue("content_width", range=800) xsize 200
                            textbutton "Aplicar" action Function(apply_single_change, "content_width", content_width) xalign 0.5
                            text "[content_width]px" color "#bdc3c7" size 14
                        
                        vbox:
                            text "Tamaño Botón Acción:" color "#ecf0f1"
                            bar value ScreenVariableValue("action_button_size", range=80) xsize 200
                            textbutton "Aplicar" action Function(apply_single_change, "action_button_size", action_button_size) xalign 0.5
                            text "[action_button_size]px" color "#bdc3c7" size 14
                
                elif current_tab == "colors":
                    vbox:
                        spacing 15
                        
                        frame:
                            background "#34495e"
                            padding (20, 20)
                            
                            vbox:
                                spacing 10
                                
                                text "🎨 Colores de Paneles" size 24 color "#ecf0f1" xalign 0.5
                                
                                grid 2 4:
                                    spacing 15
                                    
                                    vbox:
                                        text "Panel Fondo:" color "#ecf0f1"
                                        frame:
                                            background Solid(background_panel_color)
                                            padding (10, 5)
                                            text background_panel_color color "#ffffff" size 12
                                        textbutton "✏️ Editar" action Show("color_editor", color_var="background_panel_color", current_color=background_panel_color) style "config_edit_button"
                                    
                                    vbox:
                                        text "Panel Personajes:" color "#ecf0f1"
                                        frame:
                                            background Solid(character_panel_color)
                                            padding (10, 5)
                                            text character_panel_color color "#ffffff" size 12
                                        textbutton "✏️ Editar" action Show("color_editor", color_var="character_panel_color", current_color=character_panel_color) style "config_edit_button"
                                    
                                    vbox:
                                        text "Panel Expresiones:" color "#ecf0f1"
                                        frame:
                                            background Solid(expressions_panel_color)
                                            padding (10, 5)
                                            text expressions_panel_color color "#ffffff" size 12
                                        textbutton "✏️ Editar" action Show("color_editor", color_var="expressions_panel_color", current_color=expressions_panel_color) style "config_edit_button"
                                    
                                    vbox:
                                        text "Panel Escenario:" color "#ecf0f1"
                                        frame:
                                            background Solid(stage_panel_color)
                                            padding (10, 5)
                                            text stage_panel_color color "#ffffff" size 12
                                        textbutton "✏️ Editar" action Show("color_editor", color_var="stage_panel_color", current_color=stage_panel_color) style "config_edit_button"
                                    
                                    vbox:
                                        text "Panel Diálogo:" color "#ecf0f1"
                                        frame:
                                            background Solid(dialogue_panel_color)
                                            padding (10, 5)
                                            text dialogue_panel_color color "#ffffff" size 12
                                        textbutton "✏️ Editar" action Show("color_editor", color_var="dialogue_panel_color", current_color=dialogue_panel_color) style "config_edit_button"
                                    
                                    vbox:
                                        text "Panel Estructura:" color "#ecf0f1"
                                        frame:
                                            background Solid(structure_panel_color)
                                            padding (10, 5)
                                            text structure_panel_color color "#ffffff" size 12
                                        textbutton "✏️ Editar" action Show("color_editor", color_var="structure_panel_color", current_color=structure_panel_color) style "config_edit_button"
                                    
                                    vbox:
                                        text "Panel Proyectos:" color "#ecf0f1"
                                        frame:
                                            background Solid(projects_panel_color)
                                            padding (10, 5)
                                            text projects_panel_color color "#ffffff" size 12
                                        textbutton "✏️ Editar" action Show("color_editor", color_var="projects_panel_color", current_color=projects_panel_color) style "config_edit_button"
                                    
                                    vbox:
                                        text "Panel Desarrollador:" color "#ecf0f1"
                                        frame:
                                            background Solid(developer_panel_color)
                                            padding (10, 5)
                                            text developer_panel_color color "#ffffff" size 12
                                        textbutton "✏️ Editar" action Show("color_editor", color_var="developer_panel_color", current_color=developer_panel_color) style "config_edit_button"
                
                elif current_tab == "text":
                    vbox:
                        spacing 15
                        
                        frame:
                            background "#34495e"
                            padding (20, 20)
                            
                            vbox:
                                spacing 10
                                
                                text "📝 Tamaños de Texto" size 24 color "#ecf0f1" xalign 0.5
                                
                                grid 2 3:
                                    spacing 20
                                    
                                    vbox:
                                        text "Título Grande:" color "#ecf0f1"
                                        bar value ScreenVariableValue("title_large_size", range=50) xsize 200
                                        textbutton "Aplicar" action Function(apply_single_change, "title_large_size", title_large_size) xalign 0.5
                                        text "[title_large_size]px" color "#bdc3c7" size 14
                                    
                                    vbox:
                                        text "Título Mediano:" color "#ecf0f1"
                                        bar value ScreenVariableValue("title_medium_size", range=40) xsize 200
                                        textbutton "Aplicar" action Function(apply_single_change, "title_medium_size", title_medium_size) xalign 0.5
                                        text "[title_medium_size]px" color "#bdc3c7" size 14
                                    
                                    vbox:
                                        text "Título Pequeño:" color "#ecf0f1"
                                        bar value ScreenVariableValue("title_small_size", range=30) xsize 200
                                        textbutton "Aplicar" action Function(apply_single_change, "title_small_size", title_small_size) xalign 0.5
                                        text "[title_small_size]px" color "#bdc3c7" size 14
                                    
                                    vbox:
                                        text "Texto Grande:" color "#ecf0f1"
                                        bar value ScreenVariableValue("text_large_size", range=30) xsize 200
                                        textbutton "Aplicar" action Function(apply_single_change, "text_large_size", text_large_size) xalign 0.5
                                        text "[text_large_size]px" color "#bdc3c7" size 14
                                    
                                    vbox:
                                        text "Texto Mediano:" color "#ecf0f1"
                                        bar value ScreenVariableValue("text_medium_size", range=25) xsize 200
                                        textbutton "Aplicar" action Function(apply_single_change, "text_medium_size", text_medium_size) xalign 0.5
                                        text "[text_medium_size]px" color "#bdc3c7" size 14
                                    
                                    vbox:
                                        text "Texto Pequeño:" color "#ecf0f1"
                                        bar value ScreenVariableValue("text_small_size", range=20) xsize 200
                                        textbutton "Aplicar" action Function(apply_single_change, "text_small_size", text_small_size) xalign 0.5
                                        text "[text_small_size]px" color "#bdc3c7" size 14
                
                elif current_tab == "save":
                    vbox:
                        spacing 20
                        
                        frame:
                            background "#34495e"
                            padding (30, 30)
                            
                            vbox:
                                spacing 20
                                xalign 0.5
                                
                                text "💾 Gestión de Configuración" size 28 color "#ecf0f1" xalign 0.5
                                
                                textbutton "🔄 Aplicar Cambios" action Function(apply_all_changes) style "config_apply_button"
                                textbutton "💾 Guardar Persistente" action Function(save_from_screen_variables) style "config_save_button"
                                textbutton "📂 Cargar Persistente" action Function(load_persistent_to_editor) style "config_load_button"
                                textbutton "🔄 Restaurar Predeterminado" action Function(reset_to_default_persistent) style "config_reset_button"
            
            # Botones de control
            hbox:
                spacing 20
                xalign 0.5
                
                textbutton "❌ Cerrar" action Hide("layout_configurator") style "config_close_button"

# ===== PANTALLA EDITOR DE COLORES =====

screen color_editor(color_var, current_color):
    modal True
    
    default color_input = current_color
    
    add Solid("#1a1a1a")
    
    frame:
        background "#2c3e50"
        padding (30, 30)
        xalign 0.5
        yalign 0.5
        xsize 600
        ysize 500
        
        vbox:
            spacing 20
            
            text "🎨 Editor de Color" size 28 color "#ffffff" xalign 0.5
            
            vbox:
                spacing 10
                
                text "Color actual: [color_var]" color "#ecf0f1" size 16
                
                frame:
                    background Solid(current_color)
                    padding (20, 20)
                    text current_color color "#ffffff" size 18 xalign 0.5
            
            vbox:
                spacing 10
                
                text "Nuevo color (hex):" color "#ecf0f1"
                input value ScreenVariableInputValue("color_input") xsize 200
            
            frame:
                background Solid(color_input)
                padding (20, 20)
                text "Vista previa" color "#ffffff" size 16 xalign 0.5
            
            # Colores predefinidos
            vbox:
                spacing 10
                
                text "Colores predefinidos:" color "#ecf0f1" size 16
                
                grid 4 2:
                    spacing 10
                    
                    textbutton "" background Solid("#e74c3c") action SetScreenVariable("color_input", "#e74c3c") xsize 40 ysize 40
                    textbutton "" background Solid("#3498db") action SetScreenVariable("color_input", "#3498db") xsize 40 ysize 40
                    textbutton "" background Solid("#9b59b6") action SetScreenVariable("color_input", "#9b59b6") xsize 40 ysize 40
                    textbutton "" background Solid("#f39c12") action SetScreenVariable("color_input", "#f39c12") xsize 40 ysize 40
                    textbutton "" background Solid("#27ae60") action SetScreenVariable("color_input", "#27ae60") xsize 40 ysize 40
                    textbutton "" background Solid("#8e44ad") action SetScreenVariable("color_input", "#8e44ad") xsize 40 ysize 40
                    textbutton "" background Solid("#16a085") action SetScreenVariable("color_input", "#16a085") xsize 40 ysize 40
                    textbutton "" background Solid("#2c3e50") action SetScreenVariable("color_input", "#2c3e50") xsize 40 ysize 40
            
            # Botones de control
            hbox:
                spacing 20
                xalign 0.5
                
                textbutton "👁️ Probar" action Function(test_color_temporarily, color_var, color_input) style "config_test_button"
                textbutton "✅ Aplicar" action [Function(apply_color_change, color_var, color_input), Hide("color_editor")] style "config_save_button"
                textbutton "❌ Cancelar" action Hide("color_editor") style "config_close_button"

# ===== ESTILOS =====

style config_tab_button:
    background "#34495e"
    hover_background "#3498db"
    padding (20, 10)
    size 16

style config_apply_button:
    background "#27ae60"
    hover_background "#2ecc71"
    padding (20, 15)
    size 18
    xsize 300

style config_save_button:
    background "#3498db"
    hover_background "#5dade2"
    padding (20, 15)
    size 18
    xsize 300

style config_load_button:
    background "#f39c12"
    hover_background "#f7dc6f"
    padding (20, 15)
    size 18
    xsize 300

style config_reset_button:
    background "#e74c3c"
    hover_background "#ec7063"
    padding (20, 15)
    size 18
    xsize 300

style config_close_button:
    background "#95a5a6"
    hover_background "#bdc3c7"
    padding (20, 15)
    size 18
    xsize 200

style config_edit_button:
    background "#9b59b6"
    hover_background "#bb8fce"
    padding (10, 8)
    size 14
    xsize 100

style config_test_button:
    background "#f39c12"
    hover_background "#f7dc6f"
    padding (15, 10)
    size 16
    xsize 120
