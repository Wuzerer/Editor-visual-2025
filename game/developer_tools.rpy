# developer_tools_optimized.rpy
# Versión optimizada del editor visual usando módulos separados

init -2 python:
    # ===== USAR LAYOUT DESDE LAYOUT_CONTROLLER =====
    # Verificar si las clases de layout ya están disponibles desde layout_controller.rpy
    
    # Importar las instancias globales desde layout_controller si están disponibles
    if hasattr(renpy.store, 'visual_layout') and hasattr(renpy.store, 'colors') and hasattr(renpy.store, 'text_sizes'):
        # Usar las instancias existentes desde layout_controller.rpy
        visual_layout = renpy.store.visual_layout
        colors = renpy.store.colors
        text_sizes = renpy.store.text_sizes
        print("✅ Usando layout desde layout_controller.rpy")
    else:
        # Fallback: crear instancias básicas si no están disponibles
        print("⚠️ Layout no disponible desde layout_controller.rpy, creando fallback básico")
        
        # Crear instancias mínimas para evitar errores
        class MinimalLayout:
            def __init__(self):
                # Dimensiones principales
                self.editor_width = 1600
                self.editor_height = 900
                self.top_area_height = 400
                self.bottom_area_height = 480
                
                # Áreas de vista previa y escenas
                self.preview_area_width = 800
                self.preview_area_height = 380
                self.scenes_area_width = 780
                self.scenes_area_height = 380
                
                # Paneles y elementos
                self.panel_width = 380
                self.panel_height = 220
                self.panel_spacing = 10
                self.line_height = 30
                self.content_width = 350
                self.action_button_size = 28
                self.panel_padding = 20
                self.content_spacing = 20
                
                # Fondos y colores
                self.editor_background = "#1a252f"
                self.preview_background = "#2c3e50"
                self.scenes_background = "#34495e"
                
                # Atributos adicionales que podrían faltar
                self.preview_area_x = 0
                self.preview_area_y = 0
                self.scenes_area_x = 820
                self.scenes_area_y = 0
                self.panel_area_x = 0
                self.panel_area_y = 420
                self.button_height = 40
                self.button_width = 120
                self.text_input_height = 30
                self.text_input_width = 300
        
        class MinimalColors:
            def __init__(self):
                self.background_panel = "#e74c3c"
                self.character_panel = "#3498db"
                self.expressions_panel = "#9b59b6"
                self.stage_panel = "#f39c12"
                self.dialogue_panel = "#27ae60"
                self.structure_panel = "#8e44ad"
                self.projects_panel = "#16a085"
                self.developer_panel = "#e74c3c"
        
        class MinimalTextSizes:
            def __init__(self):
                self.title_large = 28
                self.title_medium = 20
                self.title_small = 18
                self.text_large = 16
                self.text_medium = 14
                self.text_small = 12
        
        visual_layout = MinimalLayout()
        colors = MinimalColors()
        text_sizes = MinimalTextSizes()
        print("✅ Layout fallback básico creado")
    
    # Verificación específica para panel_padding
    if not hasattr(visual_layout, 'panel_padding'):
        print("⚠️ Agregando panel_padding faltante a visual_layout")
        visual_layout.panel_padding = 20
        print("✅ panel_padding agregado a visual_layout")
    
    # Verificación global para todas las instancias de VisualEditorLayout
    def ensure_panel_padding_global():
        """Asegura que todas las instancias de VisualEditorLayout tengan panel_padding"""
        try:
            # Verificar la instancia global
            if hasattr(renpy.store, 'visual_layout'):
                if not hasattr(renpy.store.visual_layout, 'panel_padding'):
                    print("⚠️ Agregando panel_padding a instancia global de visual_layout")
                    renpy.store.visual_layout.panel_padding = 20
                    print("✅ panel_padding agregado a instancia global")
            
            # Verificar la instancia local
            if 'visual_layout' in globals():
                if not hasattr(globals()['visual_layout'], 'panel_padding'):
                    print("⚠️ Agregando panel_padding a instancia local de visual_layout")
                    globals()['visual_layout'].panel_padding = 20
                    print("✅ panel_padding agregado a instancia local")
                    
        except Exception as e:
            print(f"⚠️ Error en verificación global de panel_padding: {e}")
    
    # Ejecutar verificación global
    ensure_panel_padding_global()
    
    # Función de seguridad para obtener panel_padding
    def get_panel_padding(layout_obj=None):
        """Obtiene el panel_padding de forma segura, con valor por defecto si no existe"""
        try:
            if layout_obj is None:
                layout_obj = visual_layout
            
            # Verificación adicional en tiempo de ejecución
            if not hasattr(layout_obj, 'panel_padding'):
                layout_obj.panel_padding = 20
                print(f"⚠️ Agregando panel_padding faltante a {type(layout_obj).__name__} en tiempo de ejecución")
                return 20
            
            return layout_obj.panel_padding
        except Exception as e:
            print(f"⚠️ Error obteniendo panel_padding: {e}")
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
            print(f"⚠️ Error obteniendo panel_padding_tuple: {e}")
            return (20, 20, 20, 20)  # Valor por defecto seguro
    
    # Verificación adicional: asegurar que visual_layout tenga panel_padding antes de cualquier uso
    def ensure_visual_layout_panel_padding():
        """Asegura que visual_layout tenga panel_padding antes de cualquier uso"""
        try:
            global visual_layout
            if not hasattr(visual_layout, 'panel_padding'):
                visual_layout.panel_padding = 20
                print("⚠️ Agregando panel_padding a visual_layout en verificación previa")
        except Exception as e:
            print(f"⚠️ Error en verificación previa de panel_padding: {e}")
    
    # Ejecutar verificación previa
    ensure_visual_layout_panel_padding()
    
    # Función para asegurar que visual_layout tenga todos los atributos necesarios
    def ensure_all_layout_attributes():
        """Asegura que visual_layout tenga todos los atributos necesarios"""
        try:
            global visual_layout
            
            # Lista de atributos requeridos con valores por defecto
            required_attributes = {
                'editor_width': 1600,
                'editor_height': 900,
                'top_area_height': 400,
                'bottom_area_height': 480,
                'preview_area_width': 800,
                'preview_area_height': 380,
                'scenes_area_width': 780,
                'scenes_area_height': 380,
                'panel_width': 380,
                'panel_height': 220,
                'panel_spacing': 10,
                'line_height': 30,
                'content_width': 350,
                'action_button_size': 28,
                'panel_padding': 20,
                'content_spacing': 20,
                'editor_background': "#1a252f",
                'preview_background': "#2c3e50",
                'scenes_background': "#34495e",
                'preview_area_x': 0,
                'preview_area_y': 0,
                'scenes_area_x': 820,
                'scenes_area_y': 0,
                'panel_area_x': 0,
                'panel_area_y': 420,
                'button_height': 40,
                'button_width': 120,
                'text_input_height': 30,
                'text_input_width': 300
            }
            
            # Verificar y agregar atributos faltantes
            for attr_name, default_value in required_attributes.items():
                if not hasattr(visual_layout, attr_name):
                    setattr(visual_layout, attr_name, default_value)
                    print(f"⚠️ Agregando atributo faltante: {attr_name} = {default_value}")
            
            print("✅ Todos los atributos de layout verificados")
            
        except Exception as e:
            print(f"⚠️ Error verificando atributos de layout: {e}")
    
    # Ejecutar verificación de atributos
    ensure_all_layout_attributes()
    
    # Clase wrapper para asegurar que siempre tengamos panel_padding
    class SafeVisualLayout:
        """Wrapper que asegura que siempre tengamos panel_padding"""
        def __init__(self, layout_obj):
            self._layout = layout_obj
            # Asegurar que tenga panel_padding
            if not hasattr(self._layout, 'panel_padding'):
                self._layout.panel_padding = 20
                print(f"⚠️ Agregando panel_padding a {type(self._layout).__name__} en SafeVisualLayout")
        
        def __getattr__(self, name):
            # Si el atributo no existe en el wrapper, buscarlo en el objeto original
            if name == 'panel_padding' and not hasattr(self._layout, 'panel_padding'):
                self._layout.panel_padding = 20
                print(f"⚠️ Agregando panel_padding a {type(self._layout).__name__} en __getattr__")
                return 20
            return getattr(self._layout, name)
        
        def __setattr__(self, name, value):
            if name == '_layout':
                super().__setattr__(name, value)
            else:
                setattr(self._layout, name, value)
    
    # Crear una instancia segura de visual_layout
    try:
        safe_visual_layout = SafeVisualLayout(visual_layout)
        # Reemplazar la referencia global con la versión segura
        visual_layout = safe_visual_layout._layout
        print("✅ Instancia segura de visual_layout creada")
    except Exception as e:
        print(f"⚠️ Error creando instancia segura: {e}")
    
    # ===== VARIABLES GLOBALES DEL EDITOR =====
    
    # Variables para el editor visual
    current_panel_page = "scene"  # Página actual del panel
    active_input_area = None  # Área de entrada activa
    
    # Variables para selección de elementos
    selected_background_global = None
    current_speaker = None
    selected_char_base = None
    selected_char_sprite = None
    pos_to_add = "center"
    dialogue_text = ""
    
    # Lista de escenas actual
    current_scenes = []
    
    # Lista de personajes del editor
    editor_character_list = ["Eileen", "Lucy", "Narrator"]
    
    # Posiciones de personajes
    character_positions = ["at center", "at left", "at right"]
    
    # Obtener sprites de personajes desde el módulo de recursos
    try:
        from resource_manager import get_character_sprites
        character_sprites = {}
        for char in editor_character_list:
            character_sprites[char.lower()] = get_character_sprites(char)
    except:
        character_sprites = {}
    
    print("✅ Editor visual optimizado inicializado")
