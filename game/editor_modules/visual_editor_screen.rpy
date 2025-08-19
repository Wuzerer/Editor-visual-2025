# visual_editor_screen.rpy
# Pantalla principal del editor visual

# Transforms para efectos visuales
transform sprite_fade_in:
    alpha 0.0
    ease 0.5 alpha 1.0

transform sprite_appear:
    alpha 0.0
    linear 0.3 alpha 1.0

# ===== TRANSFORMS PARA ANIMACIONES =====
transform enter_from_right:
    xalign 1.2  # Comienza fuera de la pantalla a la derecha
    yalign 1.0
    yoffset -80
    zoom 0.6
    ease 0.5 xalign 0.8  # Se mueve a la posición derecha

transform enter_from_left:
    xalign -0.2  # Comienza fuera de la pantalla a la izquierda
    yalign 1.0
    yoffset -80
    zoom 0.6
    ease 0.5 xalign 0.2  # Se mueve a la posición izquierda

transform enter_from_bottom:
    xalign 0.5  # Comienza en el centro
    yalign 1.2  # Comienza fuera de la pantalla abajo
    yoffset -80
    zoom 0.6
    ease 0.5 yalign 1.0  # Se mueve a la posición normal

# ===== CONFIGURACIÓN DE TEXTO =====

# Asegurar que visual_layout tenga todos los atributos necesarios antes de definir la pantalla
init python:
    from datetime import datetime
    
    # Variables globales para el editor de escenas
    new_scene_name = ""
    scene_name_active = False
    created_scenes_modal_global = []
    search_text = ""
    organizer_scenes_list = []
    
    # Variables para el editor integrado
    current_editing_scene = None
    editor_lines = []
    current_line_index = 0
    editor_text = ""
    
    # Variables para la vista previa de escenas
    current_scene_name = ""
    current_scenes = []
    
    # Variable para confirmación de eliminación
    pending_delete_scene = None
    
    # Variables para sistema de proyectos
    new_project_name = "Mi Proyecto"
    project_search_text = ""
    overwrite_search_text = ""
    delete_project_search_text = ""
    available_projects = []
    
    # Variables para control de limpieza automática
    project_saved = False
    scenes_created_since_last_save = []
    
    # Inicializar editor sin proyecto abierto
    def initialize_editor_without_project():
        """Inicializa el editor sin ningún proyecto abierto"""
        try:
            print(f"🔍 Debug: Inicializando editor sin proyecto...")
            
            import os
            
            # Limpiar escenas actuales
            current_scenes_dir = os.path.join(config.gamedir, "scenes")
            if os.path.exists(current_scenes_dir):
                for filename in os.listdir(current_scenes_dir):
                    if filename.endswith('.rpy'):
                        os.remove(os.path.join(current_scenes_dir, filename))
                        print(f"🔍 Debug: Escena eliminada al inicializar: {filename}")
            
            # Limpiar variables del editor
            renpy.store.current_scene_name = ""
            renpy.store.current_scenes = []
            renpy.store.organizer_scenes_list = []
            renpy.store.project_saved = False
            renpy.store.scenes_created_since_last_save = []
            
            # Recargar lista de escenas en el organizador
            load_all_scenes_for_organizer()
            
            print(f"🔍 Debug: Editor inicializado sin proyecto")
            
        except Exception as e:
            print(f"🔍 Debug: Error inicializando editor: {e}")
    
    # Ejecutar inicialización al cargar el módulo
    initialize_editor_without_project()
    
    def cleanup_unsaved_scenes():
        """Limpia las escenas no guardadas cuando se cierra el editor sin guardar proyecto"""
        try:
            print(f"🔍 Debug: Iniciando limpieza de escenas no guardadas...")
            
            import os
            
            # Solo limpiar si no se ha guardado el proyecto
            if not getattr(renpy.store, 'project_saved', False):
                current_scenes_dir = os.path.join(config.gamedir, "scenes")
                if os.path.exists(current_scenes_dir):
                    scenes_created = getattr(renpy.store, 'scenes_created_since_last_save', [])
                    
                    for scene_name in scenes_created:
                        scene_file = os.path.join(current_scenes_dir, f"{scene_name}.rpy")
                        scene_compiled = os.path.join(current_scenes_dir, f"{scene_name}.rpyc")
                        
                        # Eliminar archivo .rpy
                        if os.path.exists(scene_file):
                            os.remove(scene_file)
                            print(f"🔍 Debug: Escena no guardada eliminada: {scene_name}.rpy")
                        
                        # Eliminar archivo .rpyc si existe
                        if os.path.exists(scene_compiled):
                            os.remove(scene_compiled)
                            print(f"🔍 Debug: Archivo compilado eliminado: {scene_name}.rpyc")
                    
                    # Limpiar lista de escenas creadas
                    renpy.store.scenes_created_since_last_save = []
                    
                    # Recargar lista de escenas en el organizador
                    load_all_scenes_for_organizer()
                    
                    print(f"🔍 Debug: Limpieza de escenas no guardadas completada")
                else:
                    print(f"🔍 Debug: No hay directorio de escenas para limpiar")
            else:
                print(f"🔍 Debug: Proyecto guardado, no se requiere limpieza")
                
        except Exception as e:
            print(f"🔍 Debug: Error en limpieza de escenas no guardadas: {e}")
    
    def mark_scene_as_created(scene_name):
        """Marca una escena como creada para seguimiento de limpieza"""
        try:
            scenes_created = getattr(renpy.store, 'scenes_created_since_last_save', [])
            if scene_name not in scenes_created:
                scenes_created.append(scene_name)
                renpy.store.scenes_created_since_last_save = scenes_created
                print(f"🔍 Debug: Escena marcada como creada: {scene_name}")
        except Exception as e:
            print(f"🔍 Debug: Error marcando escena como creada: {e}")
    
    def mark_project_as_saved():
        """Marca el proyecto como guardado para evitar limpieza automática"""
        try:
            renpy.store.project_saved = True
            renpy.store.scenes_created_since_last_save = []
            print(f"🔍 Debug: Proyecto marcado como guardado")
        except Exception as e:
            print(f"🔍 Debug: Error marcando proyecto como guardado: {e}")
    
    def check_unsaved_changes():
        """Verifica si hay cambios no guardados en el editor"""
        try:
            # Verificar si hay escenas creadas sin guardar
            scenes_created = getattr(renpy.store, 'scenes_created_since_last_save', [])
            project_saved = getattr(renpy.store, 'project_saved', False)
            
            # Si hay escenas creadas y el proyecto no está guardado, hay cambios no guardados
            has_unsaved_changes = len(scenes_created) > 0 and not project_saved
            
            print(f"🔍 Debug: Verificación de cambios no guardados - Escenas: {len(scenes_created)}, Proyecto guardado: {project_saved}, Cambios no guardados: {has_unsaved_changes}")
            
            return has_unsaved_changes, scenes_created
            
        except Exception as e:
            print(f"🔍 Debug: Error verificando cambios no guardados: {e}")
            return False, []
    
    def confirm_exit_with_unsaved_changes():
        """Muestra confirmación de salida con cambios no guardados"""
        try:
            print(f"🔍 Debug: Mostrando confirmación de salida con cambios no guardados...")
            
            # Ocultar el editor temporalmente
            renpy.hide_screen("visual_editor")
            
            # Mostrar el modal de confirmación
            renpy.show_screen("confirm_exit_unsaved_modal")
            
        except Exception as e:
            print(f"🔍 Debug: Error mostrando confirmación de salida: {e}")
    
    def exit_editor_with_cleanup():
        """Sale del editor con limpieza automática de archivos no guardados"""
        try:
            print(f"🔍 Debug: Saliendo del editor con limpieza automática...")
            
            # Limpiar escenas no guardadas
            cleanup_unsaved_scenes()
            
            # Salir del editor
            renpy.hide_screen("visual_editor")
            
            # Notificar al usuario
            renpy.notify("🧹 Editor cerrado - Archivos temporales eliminados")
            
        except Exception as e:
            print(f"🔍 Debug: Error saliendo del editor: {e}")
            # Intentar salir de todas formas
            renpy.hide_screen("visual_editor")
    
    def exit_editor_without_cleanup():
        """Sale del editor sin limpiar archivos no guardados"""
        try:
            print(f"🔍 Debug: Saliendo del editor sin limpieza...")
            
            # Salir del editor
            renpy.hide_screen("visual_editor")
            
            # Notificar al usuario
            renpy.notify("👋 Editor cerrado - Archivos temporales conservados")
            
        except Exception as e:
            print(f"🔍 Debug: Error saliendo del editor: {e}")
            # Intentar salir de todas formas
            renpy.hide_screen("visual_editor")
    
    def smart_exit_editor():
        """Función inteligente para salir del editor con verificación de cambios"""
        try:
            print(f"🔍 Debug: Verificando cambios antes de salir...")
            
            # Verificar si hay cambios no guardados
            has_unsaved_changes, scenes_created = check_unsaved_changes()
            
            if has_unsaved_changes:
                print(f"🔍 Debug: Cambios no guardados detectados, mostrando confirmación...")
                # Mostrar modal de confirmación
                confirm_exit_with_unsaved_changes()
            else:
                print(f"🔍 Debug: No hay cambios no guardados, cerrando directamente...")
                # Cerrar directamente
                renpy.hide_screen("visual_editor")
                
        except Exception as e:
            print(f"🔍 Debug: Error en smart_exit_editor: {e}")
            # En caso de error, intentar cerrar directamente
            renpy.hide_screen("visual_editor")
    
    def clear_current_editor():
        """Limpia el editor actual sin abrir modal"""
        try:
            print(f"🔍 Debug: Limpiando editor actual...")
            
            # Limpiar escenas no guardadas si no se ha guardado el proyecto
            cleanup_unsaved_scenes()
            
            # Limpiar variables del editor
            renpy.store.current_scene_name = ""
            renpy.store.current_scenes = []
            renpy.store.organizer_scenes_list = []
            
            # Recargar lista de escenas en el organizador
            load_all_scenes_for_organizer()
            
            # Notificar éxito
            renpy.notify("🧹 Editor limpiado")
            print(f"🔍 Debug: Editor limpiado exitosamente")
            
        except Exception as e:
            print(f"🔍 Debug: Error limpiando editor: {e}")
            renpy.notify(f"❌ Error limpiando editor: {e}")
    
    def ensure_visual_layout_attributes():
        """Asegura que visual_layout tenga todos los atributos necesarios para la pantalla"""
        try:
            # Verificar si visual_layout existe
            if not hasattr(renpy.store, 'visual_layout'):
                print("⚠️ visual_layout no encontrado, creando instancia básica")
                # Crear una instancia básica si no existe
                class BasicLayout:
                    def __init__(self):
                        # Dimensiones principales
                        self.editor_width = 1600
                        self.editor_height = 900
                        self.top_area_height = 600
                        self.bottom_area_height = 370
                        
                        # Áreas de vista previa y escenas
                        self.preview_area_width = 900
                        self.preview_area_height = 550
                        self.scenes_area_width = 900
                        self.scenes_area_height = 550
                        
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
                        
                        # Posiciones
                        self.preview_area_x = 0
                        self.preview_area_y = 0
                        self.scenes_area_x = 820
                        self.scenes_area_y = 0
                        self.panel_area_x = 0
                        self.panel_area_y = 420
                        
                        # Elementos de interfaz
                        self.button_height = 40
                        self.button_width = 120
                        self.text_input_height = 30
                        self.text_input_width = 300
                
                renpy.store.visual_layout = BasicLayout()
                print("✅ Instancia básica de visual_layout creada")
            
            # Obtener la referencia a visual_layout
            visual_layout = renpy.store.visual_layout
            
            # Lista de atributos requeridos con valores por defecto
            required_attributes = {
                'editor_width': 1600,
                'editor_height': 900,
                'top_area_height': 600,
                'bottom_area_height': 370,
                'preview_area_width': 900,
                'preview_area_height': 550,
                'scenes_area_width': 900,
                'scenes_area_height': 550,
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
                    print(f"⚠️ Agregando atributo faltante a visual_layout: {attr_name} = {default_value}")
            
            print("✅ Todos los atributos de visual_layout verificados para la pantalla")
            
        except Exception as e:
            print(f"⚠️ Error verificando atributos de visual_layout: {e}")
    
    # Ejecutar verificación antes de definir la pantalla
    ensure_visual_layout_attributes()
    
    # Asegurar que text_sizes esté disponible
    def ensure_text_sizes_available():
        """Asegura que text_sizes esté disponible para la pantalla"""
        try:
            if not hasattr(renpy.store, 'text_sizes'):
                print("⚠️ text_sizes no encontrado, creando instancia básica")
                # Crear una instancia básica si no existe
                class BasicTextSizes:
                    def __init__(self):
                        self.title_large = 28
                        self.title_medium = 20
                        self.title_small = 18
                        self.text_large = 16
                        self.text_medium = 14
                        self.text_small = 12
                
                renpy.store.text_sizes = BasicTextSizes()
                print("✅ Instancia básica de text_sizes creada")
            
            print("✅ text_sizes verificado para la pantalla")
            
        except Exception as e:
            print(f"⚠️ Error verificando text_sizes: {e}")
    
    # Ejecutar verificación de text_sizes
    ensure_text_sizes_available()
    
    # Funciones para gestión de fondos organizados
    def get_root_backgrounds():
        """Obtiene las imágenes de fondo que están directamente en la carpeta images/"""
        try:
            import os
            import glob
            
            # Ruta a la carpeta images
            images_path = os.path.join(config.gamedir, "images")
            
            if not os.path.exists(images_path):
                return []
            
            # Extensiones de imagen soportadas
            image_extensions = ['*.png', '*.jpg', '*.jpeg', '*.webp', '*.gif']
            backgrounds = []
            
            # Buscar imágenes en la carpeta raíz de images
            for ext in image_extensions:
                pattern = os.path.join(images_path, ext)
                files = glob.glob(pattern)
                for file in files:
                    # Obtener solo el nombre del archivo sin extensión
                    filename = os.path.basename(file)
                    name_without_ext = os.path.splitext(filename)[0]
                    backgrounds.append(name_without_ext)
            
            # Ordenar alfabéticamente
            backgrounds.sort()
            return backgrounds
            
        except Exception as e:
            print(f"⚠️ Error obteniendo fondos raíz: {e}")
            return []
    
    def get_folder_backgrounds():
        """Obtiene las imágenes de fondo organizadas por subcarpetas"""
        try:
            import os
            import glob
            
            # Ruta a la carpeta images
            images_path = os.path.join(config.gamedir, "images")
            
            if not os.path.exists(images_path):
                return {}
            
            # Extensiones de imagen soportadas
            image_extensions = ['*.png', '*.jpg', '*.jpeg', '*.webp', '*.gif']
            folder_backgrounds = {}
            
            # Carpetas excluidas (no se mostrarán como fondos)
            excluded_folders = ['menus', 'buttons', 'character']
            
            # Buscar subcarpetas en images
            for item in os.listdir(images_path):
                item_path = os.path.join(images_path, item)
                if os.path.isdir(item_path):
                    folder_name = item
                    
                    # Saltar carpetas excluidas
                    if folder_name.lower() in [f.lower() for f in excluded_folders]:
                        continue
                    
                    backgrounds = []
                    
                    # Buscar imágenes en esta subcarpeta
                    for ext in image_extensions:
                        pattern = os.path.join(item_path, ext)
                        files = glob.glob(pattern)
                        for file in files:
                            # Obtener solo el nombre del archivo sin extensión
                            filename = os.path.basename(file)
                            name_without_ext = os.path.splitext(filename)[0]
                            backgrounds.append(name_without_ext)
                    
                    # Solo agregar carpetas que contengan imágenes
                    if backgrounds:
                        backgrounds.sort()  # Ordenar alfabéticamente
                        folder_backgrounds[folder_name] = backgrounds
            
            return folder_backgrounds
            
        except Exception as e:
            print(f"⚠️ Error obteniendo fondos por carpetas: {e}")
            return {}
    
    def select_background(bg_name):
        """Selecciona un fondo por nombre"""
        try:
            # Verificar si la imagen existe
            if renpy.loadable(f"images/{bg_name}.png"):
                renpy.set_screen_variable("selected_background_global", f"images/{bg_name}.png")
                renpy.notify(f"✅ Fondo seleccionado: {bg_name}")
            elif renpy.loadable(f"images/{bg_name}.jpg"):
                renpy.set_screen_variable("selected_background_global", f"images/{bg_name}.jpg")
                renpy.notify(f"✅ Fondo seleccionado: {bg_name}")
            elif renpy.loadable(f"images/{bg_name}.jpeg"):
                renpy.set_screen_variable("selected_background_global", f"images/{bg_name}.jpeg")
                renpy.notify(f"✅ Fondo seleccionado: {bg_name}")
            elif renpy.loadable(f"images/{bg_name}.webp"):
                renpy.set_screen_variable("selected_background_global", f"images/{bg_name}.webp")
                renpy.notify(f"✅ Fondo seleccionado: {bg_name}")
            else:
                renpy.notify(f"❌ No se encontró la imagen: {bg_name}")
        except Exception as e:
            renpy.notify(f"❌ Error seleccionando fondo: {e}")
    
    def reload_backgrounds():
        """Recarga la lista de fondos"""
        try:
            # Forzar recarga de la pantalla
            renpy.restart_interaction()
            renpy.notify("🔄 Fondos recargados")
        except Exception as e:
            renpy.notify(f"❌ Error recargando fondos: {e}")
    
    def select_default_background(color_name):
        """Selecciona un fondo de color predeterminado"""
        try:
            # Mapeo de nombres de colores a códigos hexadecimales
            color_map = {
                "black": "#000000",
                "white": "#ffffff", 
                "red": "#e74c3c",
                "blue": "#3498db",
                "purple": "#9b59b6",
                "green": "#27ae60",
                "yellow": "#f1c40f",
                "orange": "#e67e22",
                "dark_gray": "#2c3e50",
                "light_gray": "#bdc3c7",
                "brown": "#8b4513",
                "pink": "#e91e63"
            }
            
            if color_name in color_map:
                # Establecer el color como fondo predeterminado
                renpy.set_screen_variable("selected_background_global", color_name)
                renpy.notify(f"✅ Fondo de color seleccionado: {color_name}")
            else:
                renpy.notify(f"❌ Color no reconocido: {color_name}")
        except Exception as e:
            renpy.notify(f"❌ Error seleccionando fondo de color: {e}")
    
    def add_default_background_to_scene():
        """Agrega el fondo predeterminado seleccionado a la escena actual"""
        try:
            selected_bg = renpy.get_screen_variable("selected_background_global")
            
            if not selected_bg:
                renpy.notify("⚠️ No hay fondo seleccionado")
                return
            
            # Verificar que haya una escena actual seleccionada
            current_scene_name = renpy.get_screen_variable("current_scene_name")
            if not current_scene_name:
                renpy.notify("⚠️ Primero crea o selecciona una escena")
                return
            
            # Mapeo de nombres de colores a códigos hexadecimales
            color_map = {
                "black": "#000000",
                "white": "#ffffff", 
                "red": "#e74c3c",
                "blue": "#3498db",
                "purple": "#9b59b6",
                "green": "#27ae60",
                "yellow": "#f1c40f",
                "orange": "#e67e22",
                "dark_gray": "#2c3e50",
                "light_gray": "#bdc3c7",
                "brown": "#8b4513",
                "pink": "#e91e63"
            }
            
            # Verificar si es un color predeterminado
            if selected_bg in color_map:
                # Crear escena de fondo con color
                background_scene = {
                    'type': 'background',
                    'background': selected_bg,
                    'color_code': color_map[selected_bg],
                    'transition': 'dissolve',
                    'scene_name': current_scene_name  # Agregar referencia a la escena
                }
                
                # Agregar a la lista de escenas actuales
                current_scenes = renpy.get_screen_variable("current_scenes")
                if current_scenes is None:
                    current_scenes = []
                
                current_scenes.append(background_scene)
                renpy.set_screen_variable("current_scenes", current_scenes)
                
                # Actualizar la escena en el diccionario de todas las escenas
                all_scenes = get_all_scenes_safe()
                all_scenes[current_scene_name] = current_scenes.copy()
                renpy.set_screen_variable("all_scenes", all_scenes)
                
                renpy.notify(f"✅ Fondo de color agregado a escena '{current_scene_name}': {selected_bg}")
            else:
                # Si no es un color predeterminado, usar la función normal
                add_background_to_scene()
                
        except Exception as e:
            renpy.notify(f"❌ Error agregando fondo predeterminado: {e}")
    
    def organize_scenes_by_current():
        """Abre la ventana modal para organizar escenas"""
        try:
            print(f"🔍 Debug: Abriendo organizador de escenas...")
            
            # Cargar todas las escenas disponibles
            load_all_scenes_for_organizer()
            
            # Mostrar la ventana modal
            renpy.show_screen("organize_scenes_modal")
            print(f"🔍 Debug: Modal de organizador mostrada")
            
        except Exception as e:
            print(f"🔍 Debug: Error abriendo organizador: {e}")
            renpy.notify(f"❌ Error abriendo organizador de escenas: {e}")
    
    def load_all_scenes_for_organizer():
        """Carga todas las escenas para el organizador"""
        try:
            print(f"🔍 Debug: Cargando escenas para organizador...")
            
            # Obtener escenas desde el archivo RPY
            scenes_from_file = get_scenes_from_rpy_file()
            print(f"🔍 Debug: Escenas cargadas desde archivo: {len(scenes_from_file)}")
            
            # Guardar en variable global para el organizador
            renpy.store.organizer_scenes_list = scenes_from_file
            print(f"🔍 Debug: Escenas guardadas en organizador")
            
        except Exception as e:
            print(f"🔍 Debug: Error cargando escenas: {e}")
            renpy.store.organizer_scenes_list = []
    
    def get_scenes_from_rpy_file():
        """Obtiene las escenas desde la carpeta scenes/"""
        try:
            import os
            scenes_dir = os.path.join(config.gamedir, "scenes")
            
            if not os.path.exists(scenes_dir):
                print(f"🔍 Debug: Carpeta scenes/ no encontrada, creando...")
                os.makedirs(scenes_dir)
            
            scenes = []
            
            # Buscar archivos .rpy en la carpeta scenes/
            for filename in os.listdir(scenes_dir):
                if filename.endswith('.rpy'):
                    scene_file = os.path.join(scenes_dir, filename)
                    
                    try:
                        with open(scene_file, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        # Extraer información de la escena
                        scene_name = filename.replace('.rpy', '')
                        scene_type = 'scene'
                        
                        # Parsear contenido básico
                        lines = content.split('\n')
                        scene_content = []
                        
                        for line in lines:
                            line = line.strip()
                            if line and not line.startswith('#') and not line.startswith('='):
                                scene_content.append(line)
                        
                        scene_data = {
                            'name': scene_name,
                            'type': scene_type,
                            'content': scene_content,
                            'filename': filename,
                            'filepath': scene_file
                        }
                        
                        scenes.append(scene_data)
                        print(f"🔍 Debug: Escena cargada: {scene_name} ({len(scene_content)} líneas)")
                        
                    except Exception as file_error:
                        print(f"🔍 Debug: Error leyendo archivo {filename}: {file_error}")
                        continue
            
            print(f"🔍 Debug: {len(scenes)} escenas cargadas desde carpeta scenes/")
            return scenes
                
        except Exception as e:
            print(f"🔍 Debug: Error cargando escenas desde carpeta: {e}")
            return []
    
    def edit_scene_from_organizer(scene_name):
        """Edita una escena desde el organizador en la Vista Previa"""
        try:
            print(f"🔍 Debug: Editando escena en Vista Previa: {scene_name}")
            
            # Buscar la escena en la lista del organizador
            scenes = getattr(renpy.store, 'organizer_scenes_list', [])
            target_scene = None
            
            for scene in scenes:
                if scene.get('name') == scene_name:
                    target_scene = scene
                    break
            
            if target_scene:
                # Obtener la ruta del archivo y contenido
                filepath = target_scene.get('filepath', '')
                filename = target_scene.get('filename', '')
                content = target_scene.get('content', [])
                
                if filepath:
                    print(f"🔍 Debug: Cargando escena para Vista Previa: {filepath}")
                    
                    # Cerrar la modal del organizador
                    renpy.hide_screen("organize_scenes_modal")
                    
                    # Cargar el contenido de la escena para la vista previa
                    load_scene_for_preview_editing(scene_name, filepath, content)
                    
                    # Mostrar la pantalla principal del editor visual
                    renpy.show_screen("visual_editor")
                    
                    # Notificar al usuario
                    renpy.notify(f"🎬 Editando escena: {scene_name} en Vista Previa")
                    
                else:
                    print(f"🔍 Debug: No se encontró ruta del archivo para: {scene_name}")
                    renpy.notify(f"⚠️ No se encontró archivo para editar: {scene_name}")
            else:
                print(f"🔍 Debug: Escena no encontrada en organizador: {scene_name}")
                renpy.notify(f"⚠️ Escena no encontrada: {scene_name}")
            
        except Exception as e:
            print(f"🔍 Debug: Error editando escena: {e}")
            renpy.notify(f"❌ Error editando escena: {e}")
    
    def load_scene_content_for_editing(scene_name, filepath, content):
        """Carga el contenido de una escena para edición"""
        try:
            print(f"🔍 Debug: Cargando contenido para edición: {scene_name}")
            
            # Leer el contenido completo del archivo
            import os
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    full_content = f.read()
                
                # Guardar información de la escena en edición
                renpy.store.current_editing_scene = {
                    'name': scene_name,
                    'filepath': filepath,
                    'filename': os.path.basename(filepath),
                    'content': full_content,
                    'original_content': full_content
                }
                
                # Convertir el contenido a líneas para el editor
                lines = full_content.split('\n')
                renpy.store.editor_lines = lines
                renpy.store.current_line_index = 0
                
                # Crear variables dinámicas para cada línea del editor
                for i, line in enumerate(lines):
                    setattr(renpy.store, f'editor_line_{i}', line)
                
                print(f"🔍 Debug: Contenido cargado: {len(lines)} líneas")
                print(f"🔍 Debug: Variables de líneas creadas: editor_line_0 a editor_line_{len(lines)-1}")
                renpy.notify(f"📝 Contenido cargado: {len(lines)} líneas")
                
            else:
                print(f"🔍 Debug: Archivo no encontrado: {filepath}")
                renpy.notify(f"⚠️ Archivo no encontrado: {os.path.basename(filepath)}")
                
        except Exception as e:
            print(f"🔍 Debug: Error cargando contenido: {e}")
            renpy.notify(f"❌ Error cargando contenido: {e}")
    
    def save_scene_edits():
        """Guarda los cambios realizados en la escena"""
        try:
            current_scene = getattr(renpy.store, 'current_editing_scene', None)
            if not current_scene:
                print(f"🔍 Debug: No hay escena en edición")
                renpy.notify(f"⚠️ No hay escena en edición")
                return
            
            filepath = current_scene.get('filepath', '')
            if not filepath:
                print(f"🔍 Debug: No hay ruta de archivo para guardar")
                renpy.notify(f"⚠️ No hay ruta de archivo para guardar")
                return
            
            # Recolectar todas las líneas del editor
            lines = getattr(renpy.store, 'editor_lines', [])
            updated_lines = []
            
            for i in range(len(lines)):
                line_value = getattr(renpy.store, f'editor_line_{i}', '')
                updated_lines.append(line_value)
            
            # Crear el contenido actualizado
            current_content = '\n'.join(updated_lines)
            
            # Guardar el archivo
            import os
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(current_content)
            
            # Actualizar la información de la escena
            current_scene['content'] = current_content
            renpy.store.editor_lines = updated_lines
            
            print(f"🔍 Debug: Escena guardada exitosamente: {filepath}")
            print(f"🔍 Debug: {len(updated_lines)} líneas guardadas")
            renpy.notify(f"💾 Escena guardada: {current_scene.get('filename', '')}")
            
        except Exception as e:
            print(f"🔍 Debug: Error guardando escena: {e}")
            renpy.notify(f"❌ Error guardando escena: {e}")
    
    def cancel_scene_edits():
        """Cancela la edición sin guardar cambios"""
        try:
            current_scene = getattr(renpy.store, 'current_editing_scene', None)
            if current_scene:
                scene_name = current_scene.get('name', 'Escena')
                print(f"🔍 Debug: Edición cancelada para: {scene_name}")
                renpy.notify(f"❌ Edición cancelada: {scene_name}")
            
            # Limpiar variables de edición
            renpy.store.current_editing_scene = None
            renpy.store.editor_lines = []
            renpy.store.current_line_index = 0
            
        except Exception as e:
            print(f"🔍 Debug: Error cancelando edición: {e}")
            renpy.notify(f"❌ Error cancelando edición: {e}")
    
    def load_scene_for_editing(scene_name):
        """Carga una escena específica para edición"""
        try:
            print(f"🔍 Debug: Cargando escena para edición: {scene_name}")
            
            # Buscar la escena en la lista del organizador
            scenes = getattr(renpy.store, 'organizer_scenes_list', [])
            target_scene = None
            
            for scene in scenes:
                if scene.get('name') == scene_name:
                    target_scene = scene
                    break
            
            if target_scene:
                # Cargar la escena en el editor
                renpy.set_screen_variable("current_scene_name", scene_name)
                renpy.set_screen_variable("current_scenes", target_scene.get('content', []))
                print(f"🔍 Debug: Escena cargada exitosamente")
            else:
                print(f"🔍 Debug: Escena no encontrada: {scene_name}")
                renpy.notify(f"⚠️ Escena no encontrada: {scene_name}")
                
        except Exception as e:
            print(f"🔍 Debug: Error cargando escena: {e}")
            renpy.notify(f"❌ Error cargando escena: {e}")
    
    def load_scene_for_preview_editing(scene_name, filepath, content):
        """Carga una escena para edición en la vista previa"""
        try:
            print(f"🔍 Debug: Cargando escena para vista previa: {scene_name}")
            
            # Leer el contenido completo del archivo
            import os
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    full_content = f.read()
                
                # Convertir el contenido a líneas para la vista previa
                lines = full_content.split('\n')
                
                # Filtrar líneas que no sean comentarios o vacías y convertirlas al formato correcto
                scene_lines = []
                in_content_area = False  # Flag para saber si estamos en el área de contenido
                
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith('#') and not line.startswith('='):
                        # Verificar si estamos en el área de contenido (entre label y return)
                        if line.startswith('label '):
                            # Inicio de la escena - no incluir en la vista previa
                            continue
                        elif line == 'return':
                            # Fin de la escena - no incluir en la vista previa
                            break
                        else:
                            # Estamos en el área de contenido - procesar la línea
                            if line.startswith('scene '):
                                # Es un comando de fondo
                                scene_lines.append({
                                    'type': 'background',
                                    'background': line.replace('scene ', '').replace(' with dissolve', '').replace(' with fade', ''),
                                    'transition': 'dissolve' if 'with dissolve' in line else 'fade' if 'with fade' in line else 'none'
                                })
                            elif line.startswith('show '):
                                # Es un comando de personaje
                                parts = line.replace('show ', '').split(' at ')
                                character = parts[0]
                                position = parts[1] if len(parts) > 1 else 'center'
                                scene_lines.append({
                                    'type': 'character',
                                    'character': character,
                                    'position': position,
                                    'expression': 'happy'  # Por defecto
                                })
                            elif line.startswith('"') or line.startswith("'"):
                                # Es diálogo
                                dialogue = line.strip('"\'')
                                scene_lines.append({
                                    'type': 'dialogue',
                                    'character': 'Narrator',
                                    'dialogue': dialogue
                                })
                            elif ' "' in line or " '" in line:
                                # Es diálogo con personaje
                                parts = line.split(' "')
                                if len(parts) > 1:
                                    character = parts[0].strip()
                                    dialogue = parts[1].rstrip('"')
                                    scene_lines.append({
                                        'type': 'dialogue',
                                        'character': character,
                                        'dialogue': dialogue
                                    })
                            else:
                                # Otros comandos (pero no label ni return)
                                scene_lines.append({
                                    'type': 'command',
                                    'command': line
                                })
                
                # Cargar la escena en las variables de la vista previa
                renpy.store.current_scene_name = scene_name
                renpy.store.current_scenes = scene_lines
                
                # Sincronizar con variables de pantalla para la vista previa
                try:
                    renpy.set_screen_variable("current_scene_name", scene_name)
                    renpy.set_screen_variable("current_scenes", scene_lines)
                    print(f"🔍 Debug: Variables de pantalla sincronizadas: {scene_name}")
                except Exception as sync_error:
                    print(f"🔍 Debug: Error sincronizando variables de pantalla: {sync_error}")
                
                # Guardar información adicional para edición
                renpy.store.current_editing_scene = {
                    'name': scene_name,
                    'filepath': filepath,
                    'filename': os.path.basename(filepath),
                    'content': full_content,
                    'original_content': full_content
                }
                
                print(f"🔍 Debug: Escena cargada en vista previa: {scene_name} ({len(scene_lines)} líneas)")
                print(f"🔍 Debug: Archivo: {os.path.basename(filepath)}")
                print(f"🔍 Debug: Contenido de escenas convertido: {len(scene_lines)} elementos")
                for i, scene in enumerate(scene_lines):
                    print(f"🔍 Debug: Escena {i+1}: {scene}")
                print(f"🔍 Debug: Variables globales - current_scene_name: {getattr(renpy.store, 'current_scene_name', 'NO ENCONTRADO')}")
                print(f"🔍 Debug: Variables globales - current_scenes: {len(getattr(renpy.store, 'current_scenes', []))} líneas")
                
                # Debug adicional para verificar que las variables se cargan en la pantalla
                try:
                    screen_scenes = renpy.get_screen_variable("current_scenes", [])
                    screen_name = renpy.get_screen_variable("current_scene_name", "")
                    print(f"🔍 Debug: Variables de pantalla - current_scene_name: {screen_name}")
                    print(f"🔍 Debug: Variables de pantalla - current_scenes: {len(screen_scenes)} líneas")
                except Exception as screen_error:
                    print(f"🔍 Debug: Error obteniendo variables de pantalla: {screen_error}")
                
                renpy.notify(f"🎬 Escena cargada en vista previa: {scene_name}")
                
            else:
                print(f"🔍 Debug: Archivo no encontrado: {filepath}")
                renpy.notify(f"⚠️ Archivo no encontrado: {os.path.basename(filepath)}")
                
        except Exception as e:
            print(f"🔍 Debug: Error cargando escena para vista previa: {e}")
            renpy.notify(f"❌ Error cargando escena: {e}")
    
    def convert_scene_item_to_rpy_line(scene_item):
        """Convierte un diccionario de elemento de escena de vuelta a línea de Ren'Py"""
        try:
            if not isinstance(scene_item, dict):
                return None
            
            scene_type = scene_item.get('type', '')
            
            if scene_type == 'background':
                background = scene_item.get('background', '')
                transition = scene_item.get('transition', 'none')
                if transition and transition != 'none':
                    return f"scene {background} with {transition}"
                else:
                    return f"scene {background}"
                    
            elif scene_type == 'character':
                character = scene_item.get('character', '')
                position = scene_item.get('position', 'center')
                expression = scene_item.get('expression', '')
                
                if expression:
                    return f"show {character} {expression} at {position}"
                else:
                    return f"show {character} at {position}"
                    
            elif scene_type == 'dialogue':
                character = scene_item.get('character', 'Narrator')
                dialogue = scene_item.get('dialogue', '')
                
                if character == 'Narrator':
                    return f'"{dialogue}"'
                else:
                    return f'{character} "{dialogue}"'
                    
            elif scene_type == 'command':
                return scene_item.get('command', '')
                
            else:
                return None
                
        except Exception as e:
            print(f"🔍 Debug: Error convirtiendo elemento de escena: {e}")
            return None
    
    def save_scene_from_preview():
        """Guarda los cambios realizados en la vista previa"""
        try:
            current_scene = getattr(renpy.store, 'current_editing_scene', None)
            if not current_scene:
                print(f"🔍 Debug: No hay escena en edición")
                renpy.notify(f"⚠️ No hay escena en edición")
                return
            
            filepath = current_scene.get('filepath', '')
            if not filepath:
                print(f"🔍 Debug: No hay ruta de archivo para guardar")
                renpy.notify(f"⚠️ No hay ruta de archivo para guardar")
                return
            
            # Obtener el contenido actual de la vista previa
            current_scenes = getattr(renpy.store, 'current_scenes', [])
            scene_name = getattr(renpy.store, 'current_scene_name', 'Escena')
            
            # Reconstruir el contenido del archivo
            import os
            from datetime import datetime
            
            # Leer el contenido original para mantener comentarios y estructura
            original_content = current_scene.get('original_content', '')
            original_lines = original_content.split('\n')
            
            # Crear nuevo contenido manteniendo comentarios y estructura
            new_content_lines = []
            content_added = False
            
            for line in original_lines:
                if line.strip().startswith('label ') and scene_name in line:
                    # Encontrar el label de la escena
                    new_content_lines.append(line)
                    content_added = True
                elif content_added and line.strip() == 'return':
                    # Agregar el contenido de la vista previa antes del return
                    for scene_item in current_scenes:
                        if isinstance(scene_item, dict):
                            # Convertir el diccionario de vuelta a línea de Ren'Py
                            scene_line = convert_scene_item_to_rpy_line(scene_item)
                            if scene_line:
                                new_content_lines.append(f"    {scene_line}")
                        elif isinstance(scene_item, str) and scene_item.strip():
                            new_content_lines.append(f"    {scene_item}")
                    new_content_lines.append(line)
                    content_added = False
                elif not content_added or not line.strip().startswith('    '):
                    # Mantener comentarios y estructura
                    new_content_lines.append(line)
            
            # Si no se encontró el label, crear contenido básico
            if not content_added:
                new_content_lines = [
                    f"# {scene_name}.rpy",
                    f"# Escena editada automáticamente por el Editor Visual",
                    f"# Actualizado el: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                    "",
                    f"# Escena: {scene_name}",
                    f"label {scene_name.lower().replace(' ', '_')}:",
                ]
                
                for scene_item in current_scenes:
                    if isinstance(scene_item, dict):
                        # Convertir el diccionario de vuelta a línea de Ren'Py
                        scene_line = convert_scene_item_to_rpy_line(scene_item)
                        if scene_line:
                            new_content_lines.append(f"    {scene_line}")
                    elif isinstance(scene_item, str) and scene_item.strip():
                        new_content_lines.append(f"    {scene_item}")
                
                new_content_lines.append("    return")
            
            # Guardar el archivo
            new_content = '\n'.join(new_content_lines)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            # Actualizar la información de la escena
            current_scene['content'] = new_content
            
            print(f"🔍 Debug: Escena guardada desde vista previa: {filepath}")
            print(f"🔍 Debug: {len(current_scenes)} líneas guardadas")
            renpy.notify(f"💾 Escena guardada: {current_scene.get('filename', '')}")
            
        except Exception as e:
            print(f"🔍 Debug: Error guardando escena desde vista previa: {e}")
            renpy.notify(f"❌ Error guardando escena: {e}")
    
    def view_scene_from_organizer(scene_name):
        """Muestra una vista previa de la escena desde el organizador"""
        try:
            print(f"🔍 Debug: Vista previa de escena: {scene_name}")
            
            # Buscar la escena en la lista del organizador
            scenes = getattr(renpy.store, 'organizer_scenes_list', [])
            target_scene = None
            
            for scene in scenes:
                if scene.get('name') == scene_name:
                    target_scene = scene
                    break
            
            if target_scene:
                # Mostrar información de la escena
                content = target_scene.get('content', [])
                scene_type = target_scene.get('type', 'scene')
                
                # Crear mensaje informativo
                info_message = f"📋 Escena: {scene_name}\n"
                info_message += f"🎬 Tipo: {scene_type}\n"
                info_message += f"📊 Elementos: {len(content)}\n\n"
                
                if content:
                    info_message += "📝 Contenido:\n"
                    for i, line in enumerate(content[:5]):  # Mostrar solo las primeras 5 líneas
                        info_message += f"  {i+1}. {line}\n"
                    
                    if len(content) > 5:
                        info_message += f"  ... y {len(content) - 5} líneas más"
                else:
                    info_message += "📭 Escena vacía"
                
                # Mostrar notificación con la información
                renpy.notify(info_message)
                print(f"🔍 Debug: Vista previa mostrada para: {scene_name}")
            else:
                print(f"🔍 Debug: Escena no encontrada para vista previa: {scene_name}")
                renpy.notify(f"⚠️ Escena no encontrada: {scene_name}")
                
        except Exception as e:
            print(f"🔍 Debug: Error en vista previa: {e}")
            renpy.notify(f"❌ Error mostrando vista previa: {e}")
    
    def delete_scene_from_organizer(scene_name):
        """Elimina una escena desde el organizador y sus archivos"""
        try:
            print(f"🔍 Debug: Eliminando escena: {scene_name}")
            
            # Mostrar modal de confirmación
            confirm_delete_scene(scene_name)
            return
            
            # Buscar la escena en la lista del organizador
            scenes = getattr(renpy.store, 'organizer_scenes_list', [])
            target_scene = None
            scene_index = -1
            
            for i, scene in enumerate(scenes):
                if scene.get('name') == scene_name:
                    target_scene = scene
                    scene_index = i
                    break
            
            if target_scene:
                # Obtener la ruta del archivo
                filepath = target_scene.get('filepath', '')
                filename = target_scene.get('filename', '')
                
                if filepath:
                    print(f"🔍 Debug: Eliminando archivo: {filepath}")
                    
                    # Eliminar archivo .rpy
                    import os
                    if os.path.exists(filepath):
                        try:
                            os.remove(filepath)
                            print(f"🔍 Debug: Archivo .rpy eliminado: {filename}")
                        except Exception as file_error:
                            print(f"🔍 Debug: Error eliminando archivo .rpy: {file_error}")
                            renpy.notify(f"⚠️ Error eliminando archivo: {filename}")
                            return
                    else:
                        print(f"🔍 Debug: Archivo .rpy no encontrado: {filepath}")
                    
                    # Eliminar archivo .rpyc si existe
                    rpyc_filepath = filepath.replace('.rpy', '.rpyc')
                    if os.path.exists(rpyc_filepath):
                        try:
                            os.remove(rpyc_filepath)
                            print(f"🔍 Debug: Archivo .rpyc eliminado: {filename.replace('.rpy', '.rpyc')}")
                        except Exception as rpyc_error:
                            print(f"🔍 Debug: Error eliminando archivo .rpyc: {rpyc_error}")
                            # No es crítico si no se puede eliminar el .rpyc
                    
                    # Eliminar de la lista del organizador
                    if scene_index >= 0:
                        scenes.pop(scene_index)
                        renpy.store.organizer_scenes_list = scenes
                        print(f"🔍 Debug: Escena eliminada de la lista: {scene_name}")
                    
                    # Notificar éxito
                    renpy.notify(f"🗑️ Escena eliminada: {scene_name}")
                    print(f"🔍 Debug: Escena eliminada completamente: {scene_name}")
                    
                else:
                    print(f"🔍 Debug: No se encontró ruta del archivo para: {scene_name}")
                    renpy.notify(f"⚠️ No se encontró archivo para eliminar: {scene_name}")
            else:
                print(f"🔍 Debug: Escena no encontrada para eliminar: {scene_name}")
                renpy.notify(f"⚠️ Escena no encontrada: {scene_name}")
                
        except Exception as e:
            print(f"🔍 Debug: Error eliminando escena: {e}")
            renpy.notify(f"❌ Error eliminando escena: {e}")
    
    def execute_scene_deletion(scene_name):
        """Ejecuta la eliminación real de una escena"""
        try:
            print(f"🔍 Debug: Ejecutando eliminación de escena: {scene_name}")
            
            # Buscar la escena en la lista del organizador
            scenes = getattr(renpy.store, 'organizer_scenes_list', [])
            target_scene = None
            scene_index = -1
            
            for i, scene in enumerate(scenes):
                if scene.get('name') == scene_name:
                    target_scene = scene
                    scene_index = i
                    break
            
            if target_scene:
                # Obtener la ruta del archivo
                filepath = target_scene.get('filepath', '')
                filename = target_scene.get('filename', '')
                
                if filepath:
                    print(f"🔍 Debug: Eliminando archivo: {filepath}")
                    
                    # Eliminar archivo .rpy
                    import os
                    if os.path.exists(filepath):
                        try:
                            os.remove(filepath)
                            print(f"🔍 Debug: Archivo .rpy eliminado: {filename}")
                        except Exception as file_error:
                            print(f"🔍 Debug: Error eliminando archivo .rpy: {file_error}")
                            renpy.notify(f"⚠️ Error eliminando archivo: {filename}")
                            return
                    else:
                        print(f"🔍 Debug: Archivo .rpy no encontrado: {filepath}")
                    
                    # Eliminar archivo .rpyc si existe
                    rpyc_filepath = filepath.replace('.rpy', '.rpyc')
                    if os.path.exists(rpyc_filepath):
                        try:
                            os.remove(rpyc_filepath)
                            print(f"🔍 Debug: Archivo .rpyc eliminado: {filename.replace('.rpy', '.rpyc')}")
                        except Exception as rpyc_error:
                            print(f"🔍 Debug: Error eliminando archivo .rpyc: {rpyc_error}")
                            # No es crítico si no se puede eliminar el .rpyc
                    
                    # Eliminar de la lista del organizador
                    if scene_index >= 0:
                        scenes.pop(scene_index)
                        renpy.store.organizer_scenes_list = scenes
                        print(f"🔍 Debug: Escena eliminada de la lista: {scene_name}")
                    
                    # Notificar éxito
                    renpy.notify(f"🗑️ Escena eliminada: {scene_name}")
                    print(f"🔍 Debug: Escena eliminada completamente: {scene_name}")
                    
                    # Volver al organizador
                    renpy.hide_screen("confirm_delete_scene_modal")
                    renpy.show_screen("organize_scenes_modal")
                    
                else:
                    print(f"🔍 Debug: No se encontró ruta del archivo para: {scene_name}")
                    renpy.notify(f"⚠️ No se encontró archivo para eliminar: {scene_name}")
            else:
                print(f"🔍 Debug: Escena no encontrada para eliminar: {scene_name}")
                renpy.notify(f"⚠️ Escena no encontrada: {scene_name}")
                
        except Exception as e:
            print(f"🔍 Debug: Error ejecutando eliminación: {e}")
            renpy.notify(f"❌ Error eliminando escena: {e}")
    
    # ===== SISTEMA DE GESTIÓN DE PROYECTOS =====
    
    def save_project_modal():
        """Abre el modal para guardar el proyecto actual"""
        try:
            print(f"🔍 Debug: Abriendo modal de guardar proyecto...")
            
            # Ocultar el editor temporalmente
            renpy.hide_screen("visual_editor")
            
            # Mostrar el modal de guardar proyecto
            renpy.show_screen("save_project_modal")
            
        except Exception as e:
            print(f"🔍 Debug: Error abriendo modal de guardar proyecto: {e}")
            renpy.notify(f"❌ Error abriendo modal de guardar: {e}")
    
    def execute_save_project(project_name):
        """Ejecuta el guardado del proyecto actual"""
        try:
            print(f"🔍 Debug: Guardando proyecto: {project_name}")
            
            # Validar nombre del proyecto
            if not project_name or not project_name.strip():
                renpy.notify("⚠️ Ingresa un nombre para el proyecto")
                return
            
            project_name = project_name.strip()
            
            # Crear nombre de carpeta seguro
            safe_folder_name = project_name.lower().replace(" ", "_").replace("-", "_")
            safe_folder_name = ''.join(c for c in safe_folder_name if c.isalnum() or c == '_')
            
            # Crear carpeta del proyecto
            import os
            projects_dir = os.path.join(config.gamedir, "projects")
            
            if not os.path.exists(projects_dir):
                print(f"🔍 Debug: Creando carpeta projects/...")
                os.makedirs(projects_dir)
            
            project_folder = os.path.join(projects_dir, safe_folder_name)
            
            # Verificar si ya existe
            counter = 1
            original_folder = project_folder
            while os.path.exists(project_folder):
                safe_folder_name = f"{safe_folder_name}_{counter}"
                project_folder = os.path.join(projects_dir, safe_folder_name)
                counter += 1
            
            # Crear carpeta del proyecto
            os.makedirs(project_folder)
            print(f"🔍 Debug: Carpeta del proyecto creada: {project_folder}")
            
            # Copiar escenas actuales al proyecto
            scenes_dir = os.path.join(project_folder, "scenes")
            os.makedirs(scenes_dir)
            
            # Obtener escenas actuales
            current_scenes = getattr(renpy.store, 'current_scenes', [])
            current_scene_name = getattr(renpy.store, 'current_scene_name', "")
            
            # Guardar información del proyecto
            project_info = {
                "name": project_name,
                "created_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "current_scene": current_scene_name,
                "total_scenes": len(current_scenes),
                "scenes": []
            }
            
            # Copiar archivos de escenas con nombres únicos
            import shutil
            source_scenes_dir = os.path.join(config.gamedir, "scenes")
            if os.path.exists(source_scenes_dir):
                for filename in os.listdir(source_scenes_dir):
                    if filename.endswith('.rpy'):
                        # Crear nombre único para la escena
                        base_name = filename[:-4]  # Sin .rpy
                        unique_filename = f"{base_name}_{safe_folder_name}.rpy"
                        
                        source_file = os.path.join(source_scenes_dir, filename)
                        dest_file = os.path.join(scenes_dir, unique_filename)
                        shutil.copy2(source_file, dest_file)
                        project_info["scenes"].append(unique_filename)
                        print(f"🔍 Debug: Escena copiada con nombre único: {unique_filename}")
            
            # Guardar información del proyecto
            import json
            project_info_file = os.path.join(project_folder, "project_info.json")
            with open(project_info_file, 'w', encoding='utf-8') as f:
                json.dump(project_info, f, indent=2, ensure_ascii=False)
            
            # Marcar el proyecto como guardado para evitar limpieza automática
            mark_project_as_saved()
            
            # Notificar éxito
            renpy.notify(f"💾 Proyecto guardado: {project_name}")
            print(f"🔍 Debug: Proyecto guardado exitosamente: {project_name}")
            
            # Volver al editor
            renpy.hide_screen("save_project_modal")
            renpy.show_screen("visual_editor")
            
        except Exception as e:
            print(f"🔍 Debug: Error guardando proyecto: {e}")
            renpy.notify(f"❌ Error guardando proyecto: {e}")
    
    def load_project_modal():
        """Abre el modal para cargar un proyecto"""
        try:
            print(f"🔍 Debug: Abriendo modal de cargar proyecto...")
            
            # Cargar lista de proyectos
            load_projects_list()
            
            # Ocultar el editor temporalmente
            renpy.hide_screen("visual_editor")
            
            # Mostrar el modal de cargar proyecto
            renpy.show_screen("load_project_modal")
            
        except Exception as e:
            print(f"🔍 Debug: Error abriendo modal de cargar proyecto: {e}")
            renpy.notify(f"❌ Error abriendo modal de cargar: {e}")
    
    def load_projects_list():
        """Carga la lista de proyectos disponibles"""
        try:
            print(f"🔍 Debug: Cargando lista de proyectos...")
            
            import os
            projects_dir = os.path.join(config.gamedir, "projects")
            
            if not os.path.exists(projects_dir):
                print(f"🔍 Debug: Carpeta projects/ no existe")
                renpy.store.available_projects = []
                return
            
            projects = []
            for folder_name in os.listdir(projects_dir):
                project_folder = os.path.join(projects_dir, folder_name)
                if os.path.isdir(project_folder):
                    project_info_file = os.path.join(project_folder, "project_info.json")
                    
                    if os.path.exists(project_info_file):
                        try:
                            import json
                            with open(project_info_file, 'r', encoding='utf-8') as f:
                                project_info = json.load(f)
                            
                            projects.append({
                                'folder': folder_name,
                                'name': project_info.get('name', folder_name),
                                'created_date': project_info.get('created_date', 'Desconocida'),
                                'total_scenes': project_info.get('total_scenes', 0),
                                'current_scene': project_info.get('current_scene', ''),
                                'scenes': project_info.get('scenes', [])
                            })
                            print(f"🔍 Debug: Proyecto encontrado: {project_info.get('name', folder_name)}")
                        except Exception as e:
                            print(f"🔍 Debug: Error leyendo proyecto {folder_name}: {e}")
                            continue
            
            renpy.store.available_projects = projects
            print(f"🔍 Debug: {len(projects)} proyectos cargados")
            
        except Exception as e:
            print(f"🔍 Debug: Error cargando lista de proyectos: {e}")
            renpy.store.available_projects = []
    
    def execute_load_project(project_folder):
        """Ejecuta la carga de un proyecto específico"""
        try:
            print(f"🔍 Debug: Cargando proyecto: {project_folder}")
            
            import os
            import shutil
            
            # Ruta del proyecto
            projects_dir = os.path.join(config.gamedir, "projects")
            project_path = os.path.join(projects_dir, project_folder)
            
            if not os.path.exists(project_path):
                renpy.notify(f"⚠️ Proyecto no encontrado: {project_folder}")
                return
            
            # Limpiar escenas actuales
            current_scenes_dir = os.path.join(config.gamedir, "scenes")
            if os.path.exists(current_scenes_dir):
                for filename in os.listdir(current_scenes_dir):
                    if filename.endswith('.rpy'):
                        os.remove(os.path.join(current_scenes_dir, filename))
                        print(f"🔍 Debug: Escena eliminada: {filename}")
            
            # Copiar escenas del proyecto
            project_scenes_dir = os.path.join(project_path, "scenes")
            if os.path.exists(project_scenes_dir):
                for filename in os.listdir(project_scenes_dir):
                    if filename.endswith('.rpy'):
                        # Extraer nombre base de la escena (sin sufijo del proyecto)
                        if '_' in filename and filename.endswith('.rpy'):
                            parts = filename[:-4].split('_')  # Sin .rpy
                            if len(parts) > 1:
                                # Reconstruir nombre original sin sufijo del proyecto
                                original_name = '_'.join(parts[:-1]) + '.rpy'
                            else:
                                original_name = filename
                        else:
                            original_name = filename
                        
                        source_file = os.path.join(project_scenes_dir, filename)
                        dest_file = os.path.join(current_scenes_dir, original_name)
                        shutil.copy2(source_file, dest_file)
                        print(f"🔍 Debug: Escena copiada: {filename} -> {original_name}")
            
            # Cargar información del proyecto
            project_info_file = os.path.join(project_path, "project_info.json")
            if os.path.exists(project_info_file):
                import json
                with open(project_info_file, 'r', encoding='utf-8') as f:
                    project_info = json.load(f)
                
                # Actualizar variables del editor
                renpy.store.current_scene_name = project_info.get('current_scene', '')
                renpy.store.current_scenes = []
                
                # Recargar lista de escenas en el organizador
                load_all_scenes_for_organizer()
            
            # Notificar éxito
            project_name = project_info.get('name', project_folder) if 'project_info' in locals() else project_folder
            renpy.notify(f"📁 Proyecto cargado: {project_name}")
            print(f"🔍 Debug: Proyecto cargado exitosamente: {project_name}")
            
            # Volver al editor
            renpy.hide_screen("load_project_modal")
            renpy.show_screen("visual_editor")
            
        except Exception as e:
            print(f"🔍 Debug: Error cargando proyecto: {e}")
            renpy.notify(f"❌ Error cargando proyecto: {e}")
    
    def clear_project():
        """Abre el modal para eliminar proyectos completos"""
        try:
            print(f"🔍 Debug: Abriendo modal de eliminación de proyectos...")
            load_projects_list() # Cargar lista de proyectos para seleccionar cuál eliminar
            renpy.hide_screen("visual_editor") # Ocultar el editor temporalmente
            renpy.show_screen("delete_project_modal") # Mostrar el modal de eliminación
        except Exception as e:
            print(f"🔍 Debug: Error abriendo modal de eliminación: {e}")
            renpy.notify(f"❌ Error abriendo modal de eliminación: {e}")
    
    def execute_delete_project(project_folder):
        """Ejecuta la eliminación completa de un proyecto"""
        try:
            print(f"🔍 Debug: Eliminando proyecto completo: {project_folder}")
            
            import os
            import shutil
            
            # Ruta del proyecto
            projects_dir = os.path.join(config.gamedir, "projects")
            project_path = os.path.join(projects_dir, project_folder)
            
            if not os.path.exists(project_path):
                renpy.notify(f"⚠️ Proyecto no encontrado: {project_folder}")
                return
            
            # Eliminar toda la carpeta del proyecto
            shutil.rmtree(project_path)
            print(f"🔍 Debug: Carpeta del proyecto eliminada: {project_path}")
            
            # Recargar lista de proyectos
            load_projects_list()
            
            # Notificar éxito
            renpy.notify(f"🗑️ Proyecto eliminado: {project_folder}")
            print(f"🔍 Debug: Proyecto eliminado exitosamente: {project_folder}")
            
            # Volver al editor
            renpy.hide_screen("delete_project_modal")
            renpy.show_screen("visual_editor")
            
        except Exception as e:
            print(f"🔍 Debug: Error eliminando proyecto: {e}")
            renpy.notify(f"❌ Error eliminando proyecto: {e}")
    
    def fix_duplicate_labels():
        """Arregla conflictos de labels duplicados"""
        try:
            print(f"🔍 Debug: Arreglando conflictos de labels duplicados...")
            
            import os
            
            # Limpiar escenas actuales para evitar conflictos
            current_scenes_dir = os.path.join(config.gamedir, "scenes")
            if os.path.exists(current_scenes_dir):
                for filename in os.listdir(current_scenes_dir):
                    if filename.endswith('.rpy'):
                        os.remove(os.path.join(current_scenes_dir, filename))
                        print(f"🔍 Debug: Escena conflictiva eliminada: {filename}")
            
            # Limpiar variables del editor
            renpy.store.current_scene_name = ""
            renpy.store.current_scenes = []
            renpy.store.organizer_scenes_list = []
            
            # Recargar lista de escenas en el organizador
            load_all_scenes_for_organizer()
            
            # Notificar éxito
            renpy.notify("🔧 Conflictos de labels arreglados")
            print(f"🔍 Debug: Conflictos de labels arreglados exitosamente")
            
        except Exception as e:
            print(f"🔍 Debug: Error arreglando conflictos: {e}")
            renpy.notify(f"❌ Error arreglando conflictos: {e}")
    
    def overwrite_project_modal():
        """Abre el modal para sobrescribir un proyecto existente"""
        try:
            print(f"🔍 Debug: Abriendo modal de sobrescribir proyecto...")
            
            # Cargar lista de proyectos para seleccionar cuál sobrescribir
            load_projects_list()
            
            # Ocultar el editor temporalmente
            renpy.hide_screen("visual_editor")
            
            # Mostrar el modal de sobrescribir proyecto
            renpy.show_screen("overwrite_project_modal")
            
        except Exception as e:
            print(f"🔍 Debug: Error abriendo modal de sobrescribir proyecto: {e}")
            renpy.notify(f"❌ Error abriendo modal de sobrescribir: {e}")
    
    def execute_overwrite_project(project_folder):
        """Ejecuta la sobrescritura de un proyecto específico"""
        try:
            print(f"🔍 Debug: Sobrescribiendo proyecto: {project_folder}")
            
            import os
            import shutil
            
            # Ruta del proyecto
            projects_dir = os.path.join(config.gamedir, "projects")
            project_path = os.path.join(projects_dir, project_folder)
            
            if not os.path.exists(project_path):
                renpy.notify(f"⚠️ Proyecto no encontrado: {project_folder}")
                return
            
            # Obtener información del proyecto original
            project_info_file = os.path.join(project_path, "project_info.json")
            original_project_name = project_folder
            
            if os.path.exists(project_info_file):
                import json
                with open(project_info_file, 'r', encoding='utf-8') as f:
                    original_info = json.load(f)
                    original_project_name = original_info.get('name', project_folder)
            
            # Limpiar escenas del proyecto existente
            project_scenes_dir = os.path.join(project_path, "scenes")
            if os.path.exists(project_scenes_dir):
                for filename in os.listdir(project_scenes_dir):
                    if filename.endswith('.rpy'):
                        os.remove(os.path.join(project_scenes_dir, filename))
                        print(f"🔍 Debug: Escena eliminada del proyecto: {filename}")
            
            # Copiar escenas actuales al proyecto con nombres únicos
            current_scenes_dir = os.path.join(config.gamedir, "scenes")
            if os.path.exists(current_scenes_dir):
                for filename in os.listdir(current_scenes_dir):
                    if filename.endswith('.rpy'):
                        # Crear nombre único para la escena
                        base_name = filename[:-4]  # Sin .rpy
                        unique_filename = f"{base_name}_{project_folder}.rpy"
                        
                        source_file = os.path.join(current_scenes_dir, filename)
                        dest_file = os.path.join(project_scenes_dir, unique_filename)
                        shutil.copy2(source_file, dest_file)
                        print(f"🔍 Debug: Escena copiada al proyecto con nombre único: {unique_filename}")
            
            # Obtener escenas actuales
            current_scenes = getattr(renpy.store, 'current_scenes', [])
            current_scene_name = getattr(renpy.store, 'current_scene_name', "")
            
            # Actualizar información del proyecto
            updated_project_info = {
                "name": original_project_name,
                "created_date": original_info.get('created_date', 'Desconocida') if 'original_info' in locals() else 'Desconocida',
                "updated_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "current_scene": current_scene_name,
                "total_scenes": len(current_scenes),
                "scenes": []
            }
            
            # Listar archivos de escenas actualizados (con nombres únicos)
            if os.path.exists(current_scenes_dir):
                for filename in os.listdir(current_scenes_dir):
                    if filename.endswith('.rpy'):
                        # Crear nombre único para la escena
                        base_name = filename[:-4]  # Sin .rpy
                        unique_filename = f"{base_name}_{project_folder}.rpy"
                        updated_project_info["scenes"].append(unique_filename)
            
            # Guardar información actualizada del proyecto
            with open(project_info_file, 'w', encoding='utf-8') as f:
                json.dump(updated_project_info, f, indent=2, ensure_ascii=False)
            
            # Marcar el proyecto como guardado para evitar limpieza automática
            mark_project_as_saved()
            
            # Notificar éxito
            renpy.notify(f"💾 Proyecto sobrescrito: {original_project_name}")
            print(f"🔍 Debug: Proyecto sobrescrito exitosamente: {original_project_name}")
            
            # Volver al editor
            renpy.hide_screen("overwrite_project_modal")
            renpy.show_screen("visual_editor")
            
        except Exception as e:
            print(f"🔍 Debug: Error sobrescribiendo proyecto: {e}")
            renpy.notify(f"❌ Error sobrescribiendo proyecto: {e}")
    
    def confirm_delete_scene(scene_name):
        """Confirma la eliminación de una escena usando modal seguro"""
        try:
            print(f"🔍 Debug: Mostrando modal de confirmación para: {scene_name}")
            
            # Ocultar el organizador temporalmente para evitar conflictos
            renpy.hide_screen("organize_scenes_modal")
            
            # Mostrar el modal de confirmación
            renpy.show_screen("confirm_delete_scene_modal", scene_name=scene_name)
            
        except Exception as e:
            print(f"🔍 Debug: Error mostrando modal de confirmación: {e}")
            renpy.notify(f"❌ Error mostrando confirmación: {e}")
    
    def debug_delete_state(scene_name):
        """Función de debug para verificar el estado de eliminación"""
        try:
            pending_delete = getattr(renpy.store, 'pending_delete_scene', None)
            scenes = getattr(renpy.store, 'organizer_scenes_list', [])
            
            print("🔍 === DEBUG ESTADO DE ELIMINACIÓN ===")
            print(f"🎯 Escena solicitada: {scene_name}")
            print(f"⏳ Escena pendiente: {pending_delete}")
            print(f"✅ ¿Coinciden?: {pending_delete == scene_name}")
            print(f"📋 Total de escenas en lista: {len(scenes)}")
            print(f"📝 Escenas disponibles: {[s.get('name', '') for s in scenes]}")
            print("=====================================")
            
            return True
        except Exception as e:
            print(f"🔍 Error en debug de eliminación: {e}")
            return False
    
    def filter_scenes_by_current():
        """Filtra la lista de escenas para mostrar solo las de la escena actual"""
        try:
            current_scene_name = renpy.get_screen_variable("current_scene_name")
            if not current_scene_name:
                return []
            
            current_scenes = renpy.get_screen_variable("current_scenes")
            if current_scenes is None:
                return []
            
            # Filtrar solo las escenas que pertenecen a la escena actual
            filtered_scenes = []
            for scene in current_scenes:
                # Verificar si la escena es un diccionario válido
                if isinstance(scene, dict):
                    if scene.get('scene_name') == current_scene_name or 'scene_name' not in scene:
                        # Si no tiene scene_name, asumir que pertenece a la escena actual
                        scene['scene_name'] = current_scene_name
                    filtered_scenes.append(scene)
                else:
                    # Si no es un diccionario, agregarlo como está (compatibilidad)
                    filtered_scenes.append(scene)
            
            return filtered_scenes
            
        except Exception as e:
            print(f"🔍 Debug: Error filtrando escenas: {e}")
            return []
    
    def open_custom_color_picker():
        """Abre el selector de color personalizado"""
        try:
            # Por ahora, mostrar una notificación
            renpy.notify("🎨 Selector de color personalizado - Funcionalidad en desarrollo")
            
            # Aquí se podría implementar un selector de color más avanzado
            # Por ejemplo, usando una pantalla modal con sliders RGB
            
        except Exception as e:
            renpy.notify(f"❌ Error abriendo selector de color: {e}")
    
    def clear_background_selection():
        """Limpia la selección de fondo actual"""
        try:
            renpy.set_screen_variable("selected_background_global", None)
            renpy.notify("🗑️ Selección de fondo limpiada")
        except Exception as e:
            renpy.notify(f"❌ Error limpiando selección: {e}")

screen visual_editor():
    modal True
    
    # Variables de pantalla
    default current_panel_page = "scene"
    default active_input_area = None
    default selected_background_global = None
    default current_speaker = None
    default selected_char_base = None
    default selected_char_sprite = None
    default pos_to_add = "center"
    default dialogue_text = ""
    default current_scenes = getattr(renpy.store, 'current_scenes', [])
    # Variables para gestión de escenas múltiples
    default all_scenes = {}  # Diccionario de todas las escenas {nombre: escenas}
    default current_scene_name = getattr(renpy.store, 'current_scene_name', "")  # Nombre de la escena actual
    default scene_creation_mode = False  # Modo de creación de escena
    default new_scene_name = ""  # Nombre para nueva escena
    default new_scene_name_active = False  # Control para activar edición del nombre
    default selected_scene_to_edit = ""  # Escena seleccionada para editar
    default modal_mode = "create"  # Modo de la ventana modal (create/list)
    default simple_scene_name = ""  # Nombre para nueva escena (ventana simple)
    default show_scene_input = False  # Mostrar campo de entrada para nueva escena
    default editor_character_list = ["Eileen", "Lucy", "Narrator"]
    default character_positions = ["at center", "at left", "at right"]
    default character_sprites = {}
    
    # Variables para vista previa en tiempo real
    default current_expression = "happy"
    default preview_mode = "game"
    default preview_zoom = 1.0
    default preview_effects = True
    
    # Variables para estructura (labels, jumps, choices)
    default label_name = ""
    default jump_target = ""
    default choice_text = ""
    default choice_text_active = False  # Control para activar edición de la pregunta
    default choice_question_confirmed = False  # Control para confirmar la pregunta
    default choice_options = []
    default choice_option_count = 0
    default new_choice_option = ""
    default new_choice_jump = ""
    default choice_option_active = False  # Control para activar edición del texto de opción
    default choice_jump_active = False    # Control para activar edición del jump
    default show_choice_add_panel = False  # Control para mostrar/ocultar panel de agregar opciones
    
    # Variables para definición de personajes
    default character_display_name = ""
    default character_color = "#c8ffc8"
    default character_type = "normal"
    default defined_characters = {}
    default dialogue_character = ""
    default sprite_position = "center"
    default sprite_animation = "none"
    default force_animation_update = False
    
    # Variables para transiciones
    default background_transition = "dissolve"
    default character_transition = "dissolve"
    
    # Variables para configuración del narrador
    default narrator_position = "center"
    default narrator_style = "textbox"
    default narrator_color = "#ffffff"
    default narrator_size = "medium"
    default narrator_text = ""
    default narrator_text_active = False
    default narrator_pos_x = 0.5  # Posición X (0.0 = izquierda, 1.0 = derecha)
    default narrator_pos_y = 0.5  # Posición Y (0.0 = arriba, 1.0 = abajo)
    default narrator_name = "Narrador"  # Nombre personalizable del narrador
    default narrator_name_active = False  # Control para activar edición del nombre
    default narrator_date_time = ""  # Campo para fecha y hora
    default narrator_location = ""  # Campo para ubicación
    default narrator_transition = "dissolve"  # Transición del narrador
    
    # Obtener sprites de personajes
    python:
        try:
            from resource_manager import get_character_sprites
            character_sprites = {}
            for char in editor_character_list:
                character_sprites[char.lower()] = get_character_sprites(char)
        except:
            character_sprites = {}
    
    # Marco principal
    frame:
        xfill True
        yfill True
        background visual_layout.editor_background
        
        # Layout principal
        fixed:
            xfill True
            yfill True
            
            # ÁREA SUPERIOR: Vista previa y lista de escenas
            frame:
                xsize visual_layout.editor_width
                ysize visual_layout.top_area_height
                background "#1a252f"
                xalign 0.5
                ypos 0
                
                hbox:
                    spacing visual_layout.content_spacing
                    xfill True
                    yfill True
                    
                    # Vista previa en tiempo real (izquierda)
                    frame:
                        xsize visual_layout.preview_area_width
                        ysize visual_layout.preview_area_height
                        background visual_layout.preview_background
                        
                        vbox:
                            xfill True
                            yfill True
                            
                            # Título de vista previa
                            text "🎮 Vista Previa en Tiempo Real" color "#ffffff" size text_sizes.title_medium xalign 0.5
                            
                            # Área de vista previa del juego
                            frame:
                                xfill True
                                yfill True
                                background "#000000"
                                margin (10, 10)
                                
                                # Contenedor principal del juego
                                fixed:
                                    xfill True
                                    yfill True
                                    
                                    # ===== FONDO =====
                                    if selected_background_global:
                                        # Verificar si es un color predeterminado
                                        $ color_map = {
                                            "black": "#000000",
                                            "white": "#ffffff", 
                                            "red": "#e74c3c",
                                            "blue": "#3498db",
                                            "purple": "#9b59b6",
                                            "green": "#27ae60",
                                            "yellow": "#f1c40f",
                                            "orange": "#e67e22",
                                            "dark_gray": "#2c3e50",
                                            "light_gray": "#bdc3c7",
                                            "brown": "#8b4513",
                                            "pink": "#e91e63"
                                        }
                                        
                                        if selected_background_global in color_map:
                                            # Mostrar fondo de color predeterminado
                                            frame:
                                                xfill True
                                                yfill True
                                                background color_map[selected_background_global]
                                                
                                                # Mostrar nombre del color
                                                text f"Fondo: {selected_background_global}" color "#ffffff" size text_sizes.text_small xalign 0.5 yalign 0.1
                                        else:
                                            # Mostrar el fondo de imagen ajustado perfectamente
                                            add selected_background_global:
                                                xalign 0.5
                                                yalign 0.5
                                                xsize visual_layout.preview_area_width - 45
                                                ysize visual_layout.preview_area_height - 80
                                    else:
                                        # Fondo por defecto
                                        frame:
                                            xfill True
                                            yfill True
                                            background "#2c3e50"
                                            
                                            text "Sin fondo seleccionado" color "#e74c3c" size text_sizes.text_medium xalign 0.5 yalign 0.5
                                    
                                    # ===== NARRADOR FLOTANTE/PANTALLA =====
                                    if narrator_text and narrator_text.strip():
                                        $ narrator_style_value = get_narrator_style()
                                        $ narrator_position_value = get_narrator_position()
                                        
                                        if narrator_style_value in ["floating", "screen"]:
                                            # Narrador flotante o de pantalla
                                            $ current_pos_x = renpy.get_screen_variable("narrator_pos_x") or 0.5
                                            $ current_pos_y = renpy.get_screen_variable("narrator_pos_y") or 0.5
                                            
                                            # Contenedor posicionado
                                            frame:
                                                background None
                                                xalign current_pos_x
                                                yalign current_pos_y
                                                
                                                vbox:
                                                    spacing 10
                                                    
                                                    # Nombre del narrador (solo para pantalla)
                                                    if narrator_style_value == "screen":
                                                        $ narrator_display_name = renpy.get_screen_variable("narrator_name") or "Narrador"
                                                        $ narrator_color_hex = get_narrator_color()
                                                        $ narrator_size_value = get_narrator_size()
                                                        text narrator_display_name color narrator_color_hex size narrator_size_value bold True xalign 0.5
                                                    
                                                    # Texto del narrador
                                                    $ narrator_color_hex = get_narrator_color()
                                                    $ narrator_size_value = get_narrator_size()
                                                    text narrator_text color narrator_color_hex size narrator_size_value xalign 0.5 text_align 0.5
                                    
                                    # ===== SPRITES DE PERSONAJES =====
                                    if current_speaker and current_speaker in editor_character_list:
                                        # Mostrar sprite del personaje actual con expresión
                                        $ current_sprite = get_current_character_sprite()
                                        if current_sprite:
                                            # Obtener posición y animación actual
                                            $ current_position = sprite_position or "center"
                                            $ current_animation = sprite_animation or "none"
                                            $ force_update = force_animation_update
                                            
                                            # Aplicar transform según la posición y animación
                                            if force_update and current_animation == "enter_right":
                                                add current_sprite at enter_from_right:
                                                    fit "contain"
                                                    xsize visual_layout.preview_area_width - 60
                                                    ysize visual_layout.preview_area_height - 120
                                                $ renpy.set_screen_variable("force_animation_update", False)
                                            elif force_update and current_animation == "enter_left":
                                                add current_sprite at enter_from_left:
                                                    fit "contain"
                                                    xsize visual_layout.preview_area_width - 60
                                                    ysize visual_layout.preview_area_height - 120
                                                $ renpy.set_screen_variable("force_animation_update", False)
                                            elif force_update and current_animation == "enter_center":
                                                add current_sprite at enter_from_bottom:
                                                    fit "contain"
                                                    xsize visual_layout.preview_area_width - 60
                                                    ysize visual_layout.preview_area_height - 120
                                                $ renpy.set_screen_variable("force_animation_update", False)
                                            else:
                                                # Sin animación - usar posición estática
                                                if current_position == "left":
                                                    $ sprite_transform = Transform(xalign=0.2, yalign=1.0, yoffset=-80, zoom=0.6)
                                                elif current_position == "center":
                                                    $ sprite_transform = Transform(xalign=0.5, yalign=1.0, yoffset=-80, zoom=0.6)
                                                elif current_position == "right":
                                                    $ sprite_transform = Transform(xalign=0.8, yalign=1.0, yoffset=-80, zoom=0.6)
                                                else:
                                                    $ sprite_transform = Transform(xalign=0.5, yalign=1.0, yoffset=-80, zoom=0.6)
                                                
                                                add current_sprite at sprite_transform:
                                                    fit "contain"
                                                    xsize visual_layout.preview_area_width - 60
                                                    ysize visual_layout.preview_area_height - 120
                                        else:
                                            # Placeholder si no hay sprite
                                            frame:
                                                xalign 0.5
                                                yalign 1.0
                                                yoffset -80
                                                xsize 180
                                                ysize 250
                                                background "#34495e"
                                                
                                                text current_speaker color "#ffffff" size text_sizes.text_medium xalign 0.5 yalign 0.5
                                    
                                    # ===== BARRA DE DIÁLOGO =====
                                    # Barra de diálogo en la parte inferior (solo para personajes y textbox)
                                    if not (narrator_text and narrator_text.strip() and get_narrator_style() in ["floating", "screen"]):
                                        frame:
                                            xfill True
                                            ysize 120
                                            yalign 1.0
                                            background "#000000"
                                            padding (15, 15)
                                            
                                            vbox:
                                                xfill True
                                                yfill True
                                                
                                                # Mostrar narrador o personaje
                                            if narrator_text and narrator_text.strip() and get_narrator_style() == "textbox":
                                                # ===== NARRADOR TEXTBOX =====
                                                # Solo mostrar en barra inferior si es estilo textbox
                                                $ narrator_display_name = renpy.get_screen_variable("narrator_name") or "Narrador"
                                                $ narrator_color_hex = get_narrator_color()
                                                $ narrator_size_value = get_narrator_size()
                                                
                                                vbox:
                                                    spacing 10
                                                    xfill True
                                                    yfill True
                                                    
                                                    # Nombre del narrador
                                                    text narrator_display_name color narrator_color_hex size text_sizes.text_large bold True
                                                    
                                                    # Texto del narrador
                                                    text narrator_text color narrator_color_hex size narrator_size_value xfill True
                                                
                                            elif current_speaker:
                                                # ===== PERSONAJE NORMAL =====
                                                vbox:
                                                    spacing 10
                                                    xfill True
                                                    yfill True
                                                    
                                                    # Nombre del personaje
                                                    $ name_color = get_current_character_color()
                                                    text current_speaker color name_color size text_sizes.text_large bold True
                                                    
                                                    # Texto del diálogo
                                                    if dialogue_text:
                                                        text dialogue_text color "#ffffff" size text_sizes.text_medium xfill True
                                                    else:
                                                        text "Escribe un diálogo..." color "#95a5a6" size text_sizes.text_medium italic True
                                            else:
                                                # ===== ESTADO VACÍO =====
                                                vbox:
                                                    spacing 10
                                                    xfill True
                                                    yfill True
                                                    
                                                    text "Escribe un diálogo..." color "#95a5a6" size text_sizes.text_medium italic True xalign 0.5 yalign 0.5
                                    
                                    # ===== INDICADORES DE ESTADO =====
                                    # Indicadores en la esquina superior derecha
                                    frame:
                                        xalign 1.0
                                        yalign 0.0
                                        xoffset -5
                                        yoffset 5
                                        background "#000000"
                                        padding (8, 4)
                                        
                                        vbox:
                                            spacing 5
                                            
                                            # Contador de escenas
                                            $ current_scene_name = renpy.get_screen_variable("current_scene_name")
                                            $ filtered_scenes = filter_scenes_by_current()
                                            
                                            if current_scene_name:
                                                text f"🎬 {current_scene_name}" color "#f39c12" size text_sizes.text_small bold True
                                                if filtered_scenes:
                                                    text f"📋 {len(filtered_scenes)} elementos" color "#27ae60" size text_sizes.text_small
                                                else:
                                                    text "📋 Sin elementos" color "#95a5a6" size text_sizes.text_small
                                            else:
                                                text "⚠️ Sin escena seleccionada" color "#e74c3c" size text_sizes.text_small
                                            
                                            # Estado del fondo
                                            if selected_background_global:
                                                text f"🖼️ {selected_background_global}" color "#27ae60" size text_sizes.text_small
                                            
                                            # Estado del personaje o narrador
                                            if narrator_text and narrator_text.strip():
                                                $ narrator_style_value = get_narrator_style()
                                                $ narrator_pos_x_value = renpy.get_screen_variable("narrator_pos_x") or 0.5
                                                $ narrator_pos_y_value = renpy.get_screen_variable("narrator_pos_y") or 0.5
                                                $ narrator_size_name = get_narrator_size_name()
                                                $ narrator_name_value = renpy.get_screen_variable("narrator_name") or "Narrador"
                                                # Variables para fecha y ubicación (DESACTIVADAS)
                                                # $ narrator_date_time_value = renpy.get_screen_variable("narrator_date_time") or ""
                                                # $ narrator_location_value = renpy.get_screen_variable("narrator_location") or ""
                                                
                                                text f"📖 {narrator_name_value} ({narrator_style_value})" color "#e74c3c" size text_sizes.text_small
                                                text f"📍 X:{narrator_pos_x_value:.2f} Y:{narrator_pos_y_value:.2f} | 📏 {narrator_size_name}" color "#e74c3c" size text_sizes.text_small
                                                
                                                # Información adicional si está disponible (DESACTIVADA)
                                                # if narrator_date_time_value:
                                                #     text f"🕐 {narrator_date_time_value}" color "#f39c12" size text_sizes.text_small
                                                # if narrator_location_value:
                                                #     text f"📍 {narrator_location_value}" color "#27ae60" size text_sizes.text_small
                                                
                                                # Indicador de posición en tiempo real
                                                if narrator_style_value in ["floating", "screen"]:
                                                    text f"🎯 Posición: ({narrator_pos_x_value:.2f}, {narrator_pos_y_value:.2f})" color "#f39c12" size text_sizes.text_small
                                            elif current_speaker:
                                                text f"👤 {current_speaker}" color "#3498db" size text_sizes.text_small
                    
                    # Lista de escenas mejorada (derecha)
                    frame:
                        xsize visual_layout.scenes_area_width
                        ysize visual_layout.scenes_area_height
                        background visual_layout.scenes_background
                        
                        vbox:
                            xfill True
                            yfill True
                            
                            # Título mejorado de lista de escenas
                            frame:
                                xfill True
                                ysize 50
                                background "#2c3e50"
                                padding (15, 10)
                                
                                hbox:
                                    xfill True
                                    spacing 15
                                    
                                    text "📋 Lista de Escenas" color "#ffffff" size text_sizes.title_medium
                                    
                                    # Contador de escenas
                                    $ current_scene_name = renpy.get_screen_variable("current_scene_name")
                                    $ filtered_scenes = filter_scenes_by_current()
                                    
                                    if current_scene_name:
                                        text f"({current_scene_name}: {len(filtered_scenes)} elementos)" color "#f39c12" size text_sizes.text_medium
                                    else:
                                        text "(Sin escena seleccionada)" color "#e74c3c" size text_sizes.text_medium
                                    
                                    # Botones de gestión de escenas
                                    hbox:
                                        spacing 10
                                        xfill True
                                        
                                        # Botón para crear nueva escena - USANDO INPUT DIRECTO CONFIABLE
                                        textbutton "➕ Nueva Escena" action Show("new_scene_modal") background "#27ae60" hover_background "#2ecc71" text_color "#ffffff" text_hover_color "#ffffff" text_size text_sizes.text_small
                                        
                                        # Botón para organizar escenas por escena actual
                                        textbutton "📋 Organizar Escenas" action Function(organize_scenes_by_current) background "#f39c12" hover_background "#e67e22" text_color "#ffffff" text_hover_color "#ffffff" text_size text_sizes.text_small
                                        
                                        # Botón alternativo con modal (para probar)
                                        # textbutton "🎭 Nueva Escena (Modal)" action Show("simple_create_scene") background "#8e44ad" hover_background "#9b59b6" text_color "#ffffff" text_hover_color "#ffffff" text_size text_sizes.text_small
                            

                            
                            # Panel de gestión de escenas múltiples
                            if all_scenes:
                                frame:
                                    xfill True
                                    ysize 80
                                    background "#34495e"
                                    margin (10, 5)
                                    padding (15, 10)
                                    
                                    vbox:
                                        spacing 8
                                        xfill True
                                        
                                        # Título del panel
                                        text "🎬 Gestión de Escenas" color "#ffffff" size text_sizes.text_medium bold True
                                        
                                        # Lista de escenas existentes
                                        hbox:
                                            spacing 10
                                            xfill True
                                            
                                            # Selector de escena
                                            frame:
                                                xfill True
                                                background "#2c3e50"
                                                padding (8, 5)
                                                
                                                textbutton "📝 Seleccionar Escena..." action [ShowMenu("scene_selector")] background "#34495e" hover_background "#2c3e50" text_color "#ffffff" text_hover_color "#f39c12" text_size text_sizes.text_small
                                            
                                            # Botones de acción
                                            textbutton "💾 Guardar" action Function(save_current_scene) background "#3498db" hover_background "#2980b9" text_color "#ffffff" text_hover_color "#ffffff" text_size text_sizes.text_small
                                            textbutton "🗑️ Eliminar" action Function(delete_scene_by_name) background "#e74c3c" hover_background "#c0392b" text_color "#ffffff" text_hover_color "#ffffff" text_size text_sizes.text_small
                                        
                                        # Escena actual
                                        if current_scene_name:
                                            frame:
                                                xfill True
                                                background "#2c3e50"
                                                padding (8, 5)
                                                
                                                text f"🎭 Escena actual: {current_scene_name}" color "#f39c12" size text_sizes.text_small bold True
                                        
                                        # Botones adicionales
                                        hbox:
                                            spacing 10
                                            xfill True
                                            
                                            # Botón exportar todas las escenas
                                            if len(all_scenes) > 1:
                                                textbutton "📄 Exportar Todas las Escenas" action Function(export_all_scenes) background "#8e44ad" hover_background "#9b59b6" text_color "#ffffff" text_hover_color "#ffffff" text_size text_sizes.text_small
                                            
                                            # Botón de debug (temporal)
                                            textbutton "🔍 Debug Escenas" action Function(debug_scenes_state) background "#e67e22" hover_background "#d35400" text_color "#ffffff" text_hover_color "#ffffff" text_size text_sizes.text_small
                            
                            # Área de contenido de escenas
                            frame:
                                xfill True
                                yfill True
                                background "#1a252f"
                                margin (10, 10)
                                
                                # Lista de escenas mejorada
                                viewport:
                                    id "scenes_list_viewport"
                                    xfill True
                                    yfill True
                                    scrollbars "vertical"
                                    mousewheel True
                                    # Configuración para scroll automático más efectivo
                                    child_size (None, None)
                                    # Configuración adicional para scroll automático
                                    draggable True
                                    
                                    vbox:
                                        spacing 8
                                        xfill True
                                        
                                        # Obtener las escenas filtradas de la escena actual
                                        $ filtered_scenes = filter_scenes_by_current()
                                        if filtered_scenes:
                                            for i, scene in enumerate(filtered_scenes):
                                                # Tarjeta de escena mejorada
                                                frame:
                                                    xfill True
                                                    background "#34495e"
                                                    padding (15, 12)
                                                    margin (0, 0, 0, 8)
                                                    
                                                    vbox:
                                                        spacing 8
                                                        
                                                        # Encabezado de la escena
                                                        hbox:
                                                            xfill True
                                                            spacing 10
                                                            
                                                            # Número y tipo de escena
                                                            frame:
                                                                xsize 80
                                                                ysize 30
                                                                background "#2c3e50"
                                                                padding (5, 5)
                                                                
                                                                text f"#{i+1}" color "#f39c12" size text_sizes.text_medium bold True xalign 0.5 yalign 0.5
                                                            
                                                            # Tipo de escena con icono
                                                            frame:
                                                                xsize 120
                                                                ysize 30
                                                                background (scene.get('type') == 'dialogue' and "#3498db" or scene.get('type') == 'background' and "#27ae60" or scene.get('type') == 'label' and "#8e44ad" or scene.get('type') == 'jump' and "#f39c12" or scene.get('type') == 'choice' and "#e67e22" or "#95a5a6")
                                                                padding (5, 5)
                                                                
                                                                text (scene.get('type') == 'dialogue' and "💬 Diálogo" or scene.get('type') == 'background' and "🖼️ Fondo" or scene.get('type') == 'label' and "🏷️ Label" or scene.get('type') == 'jump' and "🔄 Jump" or scene.get('type') == 'choice' and "❓ Choice" or "❓ Otro") color "#ffffff" size text_sizes.text_small bold True xalign 0.5 yalign 0.5
                                                        
                                                        # Contenido de la escena
                                                        if scene.get('type') == 'dialogue':
                                                            # Escena de diálogo
                                                            frame:
                                                                xfill True
                                                                background "#2c3e50"
                                                                padding (10, 8)
                                                                
                                                                vbox:
                                                                    spacing 5
                                                                    
                                                                    # Personaje
                                                                    hbox:
                                                                        spacing 8
                                                                        
                                                                        text "👤" color "#3498db" size text_sizes.text_medium
                                                                        text scene.get('character', 'Narrator') color "#3498db" size text_sizes.text_medium bold True
                                                                    
                                                                    # Diálogo
                                                                    frame:
                                                                        xfill True
                                                                        background "#1a252f"
                                                                        padding (8, 6)
                                                                        
                                                                        text scene.get('dialogue', '')[:80] + ("..." if len(scene.get('dialogue', '')) > 80 else "") color "#ecf0f1" size text_sizes.text_small
                                                                        
                                                        elif scene.get('type') == 'background':
                                                            # Escena de fondo
                                                            frame:
                                                                xfill True
                                                                background "#2c3e50"
                                                                padding (10, 8)
                                                                
                                                                hbox:
                                                                    spacing 8
                                                                    
                                                                    text "🖼️" color "#27ae60" size text_sizes.text_medium
                                                                    text scene.get('background', '') color "#27ae60" size text_sizes.text_medium bold True
                                                        
                                                        elif scene.get('type') == 'label':
                                                            # Escena de label
                                                            frame:
                                                                xfill True
                                                                background "#2c3e50"
                                                                padding (10, 8)
                                                                
                                                                hbox:
                                                                    spacing 8
                                                                    
                                                                    text "🏷️" color "#8e44ad" size text_sizes.text_medium
                                                                    text scene.get('label_name', '') color "#8e44ad" size text_sizes.text_medium bold True
                                                        
                                                        elif scene.get('type') == 'jump':
                                                            # Escena de jump
                                                            frame:
                                                                xfill True
                                                                background "#2c3e50"
                                                                padding (10, 8)
                                                                
                                                                hbox:
                                                                    spacing 8
                                                                    
                                                                    text "🔄" color "#f39c12" size text_sizes.text_medium
                                                                    text f"Jump a: {scene.get('jump_target', '')}" color "#f39c12" size text_sizes.text_medium bold True
                                                        
                                                        elif scene.get('type') == 'choice':
                                                            # Escena de choice
                                                            frame:
                                                                xfill True
                                                                background "#2c3e50"
                                                                padding (10, 8)
                                                                
                                                                vbox:
                                                                    spacing 5
                                                                    
                                                                    # Pregunta
                                                                    hbox:
                                                                        spacing 8
                                                                        
                                                                        text "❓" color "#e67e22" size text_sizes.text_medium
                                                                        text scene.get('question', '')[:60] + ("..." if len(scene.get('question', '')) > 60 else "") color "#e67e22" size text_sizes.text_medium bold True
                                                                    
                                                                    # Opciones dinámicas
                                                                    frame:
                                                                        xfill True
                                                                        background "#1a252f"
                                                                        padding (8, 6)
                                                                        
                                                                        vbox:
                                                                            spacing 3
                                                                            
                                                                            if scene.get('options'):
                                                                                for i, option in enumerate(scene.get('options', [])):
                                                                                    if isinstance(option, dict):
                                                                                        $ option_text = option.get('text', 'Opción')[:40]
                                                                                        $ option_jump = option.get('jump')
                                                                                        if option_jump:
                                                                                            text f"{i+1}. {option_text} → {option_jump}" color "#ecf0f1" size text_sizes.text_small
                                                                                        else:
                                                                                            text f"{i+1}. {option_text}" color "#ecf0f1" size text_sizes.text_small
                                                                                    else:
                                                                                        # Fallback para opciones antiguas (strings)
                                                                                        text f"{i+1}. {option[:40]}" color "#ecf0f1" size text_sizes.text_small
                                                                            else:
                                                                                # Fallback para choices antiguos
                                                                                if scene.get('option1'):
                                                                                    text f"1. {scene.get('option1', '')[:40]}" color "#ecf0f1" size text_sizes.text_small
                                                                                if scene.get('option2'):
                                                                                    text f"2. {scene.get('option2', '')[:40]}" color "#ecf0f1" size text_sizes.text_small
                                                        
                                                        # Botones de acción mejorados
                                                        hbox:
                                                            xfill True
                                                            spacing 8
                                                            xalign 1.0
                                                            
                                                            textbutton "✏️ Editar":
                                                                action Function(lambda x=i: edit_scene(x))
                                                                xsize 80
                                                                ysize 28
                                                                background "#f39c12"
                                                                text_size text_sizes.text_small
                                                            
                                                            textbutton "🗑️ Eliminar":
                                                                action Function(lambda x=i: delete_scene(x))
                                                                xsize 80
                                                                ysize 28
                                                                background "#e74c3c"
                                                                text_size text_sizes.text_small
                                        else:
                                            # Mensaje cuando no hay escenas
                                            frame:
                                                xfill True
                                                yfill True
                                                background "#2c3e50"
                                                
                                                vbox:
                                                    xalign 0.5
                                                    yalign 0.5
                                                    spacing 15
                                                    
                                                    text "📝" color "#95a5a6" size 48 xalign 0.5
                                                    text "No hay escenas creadas" color "#95a5a6" size text_sizes.title_small xalign 0.5
                                                    text "Agrega fondos y diálogos para crear tu historia" color "#7f8c8d" size text_sizes.text_small xalign 0.5
            
            # ÁREA INFERIOR: Paneles de herramientas
            frame:
                xsize visual_layout.editor_width
                ysize visual_layout.bottom_area_height
                background "#34495e"
                xalign 0.5
                ypos visual_layout.top_area_height
                
                vbox:
                    xfill True
                    yfill True
                    spacing visual_layout.content_spacing
                    
                    # Barra de navegación de paneles
                    frame:
                        xfill True
                        ysize 50
                        background "#2c3e50"
                        
                        hbox:
                            xfill True
                            spacing 15
                            xalign 0.5
                            
                            textbutton "🎬 Escena":
                                action SetScreenVariable("current_panel_page", "scene")
                                selected (current_panel_page == "scene")
                                xminimum 100
                                ysize 40
                                padding (15, 8)
                                background colors.background_panel
                                xalign 0.5
                            
                            textbutton "👤 Personajes":
                                action SetScreenVariable("current_panel_page", "characters")
                                selected (current_panel_page == "characters")
                                xminimum 100
                                ysize 40
                                padding (15, 8)
                                background colors.character_panel
                                xalign 0.5
                            
                            textbutton "🎮 Vista Previa":
                                action SetScreenVariable("current_panel_page", "preview")
                                selected (current_panel_page == "preview")
                                xminimum 100
                                ysize 40
                                padding (15, 8)
                                background "#8e44ad"
                                xalign 0.5
                            
                            textbutton "🏗️ Estructura":
                                action SetScreenVariable("current_panel_page", "structure")
                                selected (current_panel_page == "structure")
                                xminimum 100
                                ysize 40
                                padding (15, 8)
                                background colors.structure_panel
                                xalign 0.5
                            
                            textbutton "⚙️ Herramientas":
                                action SetScreenVariable("current_panel_page", "tools")
                                selected (current_panel_page == "tools")
                                xminimum 100
                                ysize 40
                                padding (15, 8)
                                background colors.developer_panel
                                xalign 0.5
                            
                            # textbutton "🎨 Modo Diseño":
                            #     action Function(activate_design_mode)
                            #     selected design_mode_active
                            #     xminimum 100
                            #     ysize 40
                            #     padding (15, 8)
                            #     background (design_mode_active and "#f39c12" or "#95a5a6")
                            #     xalign 0.5
                    
                    # Contenido de paneles
                    frame:
                        xfill True
                        yfill True
                        background "#2c3e50"
                        
                        # PÁGINA 1: ESCENA
                        if current_panel_page == "scene":
                            viewport:
                                xsize visual_layout.editor_width - 60
                                ysize visual_layout.bottom_area_height - 70
                                scrollbars "vertical"
                                mousewheel True
                                xalign 0.5
                                
                                vbox:
                                    spacing 20
                                    xalign 0.5
                                    
                                                                        # Panel de Fondos Predeterminados
                                    python:
                                        try:
                                            # Calcular ancho dinámico según el contenido
                                            default_bg_panel_width = 700  # Ancho optimizado para este panel
                                            
                                            # Calcular altura dinámica según el contenido
                                            # Altura base: título + espaciado
                                            base_height = 80
                                            
                                            # Altura por sección
                                            colors_grid_height = 200  # Grid de colores
                                            action_buttons_height = 60 # Botones de acción
                                            
                                            # Calcular altura total
                                            default_bg_panel_height = (base_height + colors_grid_height + action_buttons_height)
                                            
                                            # Altura mínima y máxima
                                            min_height = 400
                                            max_height = 500
                                            default_bg_panel_height = max(min_height, min(default_bg_panel_height, max_height))
                                            
                                        except:
                                            default_bg_panel_width = 500
                                            default_bg_panel_height = 350
                                    frame:
                                        xsize default_bg_panel_width
                                        ysize default_bg_panel_height
                                        background "#8e44ad"
                                        padding (20, 15)
                                        xalign 0.5
                                        yalign 0.0
                                        xoffset 730
                                        yoffset 0
                                        
                                        vbox:
                                            spacing 15
                                            xfill True
                                            xalign 0.5
                                            
                                            # Título centrado
                                            text "🎨 Fondos Predeterminados" color "#ffffff" size text_sizes.title_medium xalign 0.5 style "title_with_outline"
                                            
                                            # Contenido del panel
                                            vbox:
                                                spacing 12
                                                xfill True
                                                xalign 0.5
                                                
                                                # Grid de colores predeterminados
                                                frame:
                                                    xfill True
                                                    ysize 200
                                                    background "#2c3e50"
                                                    padding (10, 10)
                                                    
                                                    grid 4 3:
                                                        xfill True
                                                        yfill True
                                                        spacing 10
                                                        
                                                        # Fila 1: Colores básicos
                                                        textbutton "⚫ Negro":
                                                            action Function(select_default_background, "black")
                                                            selected (selected_background_global == "black")
                                                            xfill True
                                                            yfill True
                                                            background "#000000"
                                                            text_color "#ffffff"
                                                            text_size 16
                                                            text_style "text_with_outline"
                                                        
                                                        textbutton "⚪ Blanco":
                                                            action Function(select_default_background, "white")
                                                            selected (selected_background_global == "white")
                                                            xfill True
                                                            yfill True
                                                            background "#ffffff"
                                                            text_color "#000000"
                                                            text_size 16
                                                            text_style "text_with_outline"
                                                        
                                                        textbutton "🔴 Rojo":
                                                            action Function(select_default_background, "red")
                                                            selected (selected_background_global == "red")
                                                            xfill True
                                                            yfill True
                                                            background "#e74c3c"
                                                            text_color "#ffffff"
                                                            text_size 16
                                                            text_style "text_with_outline"
                                                        
                                                        textbutton "🔵 Azul":
                                                            action Function(select_default_background, "blue")
                                                            selected (selected_background_global == "blue")
                                                            xfill True
                                                            yfill True
                                                            background "#3498db"
                                                            text_color "#ffffff"
                                                            text_size 16
                                                            text_style "text_with_outline"
                                                        
                                                        # Fila 2: Colores adicionales
                                                        textbutton "🟣 Violeta":
                                                            action Function(select_default_background, "purple")
                                                            selected (selected_background_global == "purple")
                                                            xfill True
                                                            yfill True
                                                            background "#9b59b6"
                                                            text_color "#ffffff"
                                                            text_size 16
                                                            text_style "text_with_outline"
                                                        
                                                        textbutton "🟢 Verde":
                                                            action Function(select_default_background, "green")
                                                            selected (selected_background_global == "green")
                                                            xfill True
                                                            yfill True
                                                            background "#27ae60"
                                                            text_color "#ffffff"
                                                            text_size 16
                                                            text_style "text_with_outline"
                                                        
                                                        textbutton "🟡 Amarillo":
                                                            action Function(select_default_background, "yellow")
                                                            selected (selected_background_global == "yellow")
                                                            xfill True
                                                            yfill True
                                                            background "#f1c40f"
                                                            text_color "#000000"
                                                            text_size 16
                                                            text_style "text_with_outline"
                                                        
                                                        textbutton "🟠 Naranja":
                                                            action Function(select_default_background, "orange")
                                                            selected (selected_background_global == "orange")
                                                            xfill True
                                                            yfill True
                                                            background "#e67e22"
                                                            text_color "#ffffff"
                                                            text_size 16
                                                            text_style "text_with_outline"
                                                        
                                                        # Fila 3: Colores neutros
                                                        textbutton "⚫ Gris Oscuro":
                                                            action Function(select_default_background, "dark_gray")
                                                            selected (selected_background_global == "dark_gray")
                                                            xfill True
                                                            yfill True
                                                            background "#2c3e50"
                                                            text_color "#ffffff"
                                                            text_size 14
                                                            text_style "text_with_outline"
                                                        
                                                        textbutton "⚪ Gris Claro":
                                                            action Function(select_default_background, "light_gray")
                                                            selected (selected_background_global == "light_gray")
                                                            xfill True
                                                            yfill True
                                                            background "#bdc3c7"
                                                            text_color "#000000"
                                                            text_size 14
                                                            text_style "text_with_outline"
                                                        
                                                        textbutton "🟤 Marrón":
                                                            action Function(select_default_background, "brown")
                                                            selected (selected_background_global == "brown")
                                                            xfill True
                                                            yfill True
                                                            background "#8b4513"
                                                            text_color "#ffffff"
                                                            text_size 16
                                                            text_style "text_with_outline"
                                                        
                                                        textbutton "🩷 Rosa":
                                                            action Function(select_default_background, "pink")
                                                            selected (selected_background_global == "pink")
                                                            xfill True
                                                            yfill True
                                                            background "#e91e63"
                                                            text_color "#ffffff"
                                                            text_size 16
                                                            text_style "text_with_outline"
                                                
                                                # Botones de acción
                                                hbox:
                                                    spacing 15
                                                    xalign 0.5
                                                    
                                                    textbutton "➕ Agregar a Escena":
                                                        action Function(add_default_background_to_scene)
                                                        xminimum 120
                                                        ysize 50
                                                        padding (12, 8)
                                                        background "#2c3e50"
                                                        xalign 0.5
                                                        text_style "text_with_outline"
                                                    
                                                    textbutton "🎨 Color Personalizado":
                                                        action Function(open_custom_color_picker)
                                                        xminimum 120
                                                        ysize 85
                                                        padding (12, 8)
                                                        background "#e67e22"
                                                        xalign 0.5
                                                        text_style "text_with_outline"
                                    
                                    # Panel de Fondo - Organizado por carpetas
                                    python:
                                        try:
                                            # Calcular ancho dinámico según el contenido
                                            background_panel_width = 800  # Ancho optimizado para este panel
                                            
                                            # Calcular altura dinámica según el contenido
                                            # Altura base: título + espaciado
                                            base_height = 80
                                            
                                            # Altura por sección
                                            status_height = 30        # Estado del fondo
                                            backgrounds_height = 200  # Lista de fondos
                                            action_buttons_height = 60 # Botones de acción
                                            
                                            # Calcular altura total
                                            background_panel_height = (base_height + status_height + 
                                                                      backgrounds_height + action_buttons_height)
                                            
                                            # Altura mínima y máxima
                                            min_height = 400
                                            max_height = 400
                                            background_panel_height = max(min_height, min(background_panel_height, max_height))
                                            
                                        except:
                                            background_panel_width = 500
                                            background_panel_height = 400
                                    frame:
                                        xsize background_panel_width
                                        ysize background_panel_height
                                        background "#27ae60"
                                        padding (20, 15)
                                        xalign 0.5
                                        xoffset -10
                                        yoffset -420
                                        
                                        vbox:
                                            spacing 15
                                            xfill True
                                            xalign 0.5
                                            
                                            # Título centrado
                                            text "🖼️ Fondos Organizados" color "#ffffff" size text_sizes.title_medium xalign 0.5 style "title_with_outline"
                                            
                                            # Contenido del panel
                                            vbox:
                                                spacing 12
                                                xfill True
                                                xalign 0.5
                                                
                                                # Estado del fondo seleccionado
                                                if selected_background_global:
                                                    frame:
                                                        xfill True
                                                        background "#2c3e50"
                                                        padding (8, 6)
                                                        
                                                        text f"✅ Seleccionado: {selected_background_global}" color "#ffffff" size 18 xalign 0.5 style "text_with_outline"
                                                else:
                                                    frame:
                                                        xfill True
                                                        background "#e74c3c"
                                                        padding (8, 6)
                                                        
                                                        text "⚠️ Ningún fondo seleccionado" color "#ffffff" size 18 xalign 0.5 style "text_with_outline"
                                                
                                                # Área de fondos organizados
                                                frame:
                                                    xfill True
                                                    ysize 200
                                                    background "#2c3e50"
                                                    padding (10, 10)
                                                    
                                                    viewport:
                                                        xfill True
                                                        yfill True
                                                        scrollbars "vertical"
                                                        mousewheel True
                                                        
                                                        vbox:
                                                            spacing 10
                                                            xfill True
                                                            
                                                            # Fondos en carpeta raíz (images/)
                                                            frame:
                                                                xfill True
                                                                background "#34495e"
                                                                padding (10, 8)
                                                                
                                                                vbox:
                                                                    spacing 8
                                                                    xfill True
                                                                    
                                                                    # Título de sección
                                                                    hbox:
                                                                        spacing 8
                                                                        xfill True
                                                                        
                                                                        text "📁" color "#f39c12" size 20
                                                                        text "Fondos Principales" color "#ffffff" size 20 bold True
                                                                    
                                                                    # Lista de fondos en raíz
                                                                    $ root_backgrounds = get_root_backgrounds()
                                                                    if root_backgrounds:
                                                                        for bg in root_backgrounds:
                                                                            textbutton f"🖼️ {bg}":
                                                                                action Function(select_background, bg)
                                                                                selected (selected_background_global and (selected_background_global.endswith(f"/{bg}.png") or selected_background_global.endswith(f"/{bg}.jpg") or selected_background_global.endswith(f"/{bg}.jpeg") or selected_background_global.endswith(f"/{bg}.webp")))
                                                                                xfill True
                                                                                ysize 25
                                                                                padding (5, 2)
                                                                                background "#1a252f"
                                                                                text_size 18
                                                                                xalign 0.0
                                                                    else:
                                                                        text "No hay fondos en la carpeta principal" color "#95a5a6" size 18 xalign 0.5
                                                            
                                                            # Fondos en subcarpetas
                                                            $ folder_backgrounds = get_folder_backgrounds()
                                                            if folder_backgrounds:
                                                                for folder_name, backgrounds in folder_backgrounds.items():
                                                                    frame:
                                                                        xfill True
                                                                        background "#34495e"
                                                                        padding (10, 8)
                                                                        
                                                                        vbox:
                                                                            spacing 8
                                                                            xfill True
                                                                            
                                                                            # Título de carpeta
                                                                            hbox:
                                                                                spacing 8
                                                                                xfill True
                                                                                
                                                                                text "📂" color "#3498db" size 18
                                                                                text folder_name color "#ffffff" size 18 bold True
                                                                            
                                                                            # Lista de fondos en esta carpeta
                                                                            for bg in backgrounds:
                                                                                textbutton f"🖼️ {bg}":
                                                                                    action Function(select_background, f"{folder_name}/{bg}")
                                                                                    selected (selected_background_global and (selected_background_global.endswith(f"/{folder_name}/{bg}.png") or selected_background_global.endswith(f"/{folder_name}/{bg}.jpg") or selected_background_global.endswith(f"/{folder_name}/{bg}.jpeg") or selected_background_global.endswith(f"/{folder_name}/{bg}.webp")))
                                                                                    xfill True
                                                                                    ysize 25
                                                                                    padding (5, 2)
                                                                                    background "#1a252f"
                                                                                    text_size 18
                                                                                    xalign 0.0
                                                            else:
                                                                text "No hay fondos en subcarpetas" color "#95a5a6" size 18 xalign 0.5
                                                
                                                # Botones de acción
                                                hbox:
                                                    spacing 15
                                                    xalign 0.5
                                                    
                                                    textbutton "➕ Agregar Fondo":
                                                        action Function(add_background_to_scene)
                                                        xminimum 120
                                                        ysize 50
                                                        padding (12, 8)
                                                        background "#2c3e50"
                                                        xalign 0.5
                                                        text_style "text_with_outline"
                                                    
                                                    textbutton "🔄 Recargar":
                                                        action Function(reload_backgrounds)
                                                        xminimum 100
                                                        ysize 50
                                                        padding (12, 8)
                                                        background "#3498db"
                                                        xalign 0.5
                                                        text_style "text_with_outline"
                                                    
                                                    textbutton "🗑️ Limpiar":
                                                        action Function(clear_background_selection)
                                                        xminimum 150
                                                        ysize 50
                                                        padding (8, 5)
                                                        background "#e74c3c"
                                                        xalign 0.5
                                                        text_size 30
                                                        text_style "text_with_outline"
                                    
                                    # Panel de Diálogo
                                    python:
                                        try:
                                            # Calcular ancho dinámico según el contenido
                                            dialogue_panel_width = 350  # Ancho optimizado para este panel
                                            
                                            # Calcular altura dinámica según el contenido
                                            # Altura base: título + espaciado
                                            base_height = 80
                                            
                                            # Altura por sección - DINÁMICA SEGÚN PERSONAJES
                                            defined_chars = defined_characters
                                            character_count = len(defined_chars) if defined_chars else 0
                                            
                                            # Altura del selector de personajes (dinámica)
                                            if character_count > 0:
                                                character_selector_height = 50 + (character_count * 35)  # 50 base + 35 por personaje
                                                character_selector_height = max(120, character_selector_height)  # Mínimo 120
                                            else:
                                                character_selector_height = 120  # Altura por defecto
                                            
                                            # Altura por sección
                                            input_field_height = 40          # Campo de entrada
                                            info_height = 30                 # Información del personaje
                                            action_button_height = 50        # Botón de acción
                                            
                                            # Calcular altura total
                                            dialogue_panel_height = (base_height + character_selector_height + 
                                                                   input_field_height + info_height + action_button_height)
                                            
                                            # Altura mínima y máxima - FLEXIBLE
                                            min_height = 400
                                            max_height = 850 # Permitir hasta 800px de altura
                                            dialogue_panel_height = max(min_height, min(dialogue_panel_height, max_height))
                                            
                                        except:
                                            dialogue_panel_width = 500
                                            dialogue_panel_height = 350
                                    frame:
                                        xsize dialogue_panel_width
                                        ysize dialogue_panel_height
                                        background "#3498db"
                                        padding (20, 15)
                                        xalign 0.5
                                        yalign 0.5
                                        xoffset 1250
                                        yoffset -840
                                        
                                        vbox:
                                            spacing 15
                                            xfill True
                                            xalign 0.5
                                            
                                            # Título centrado
                                            text "💬 Diálogo" color "#ffffff" size text_sizes.title_medium xalign 0.5 style "title_with_outline"
                                            
                                            # Contenido del panel
                                            vbox:
                                                spacing 12
                                                xfill True
                                                xalign 0.5
                                                
                                                # Selector de personaje definido
                                                vbox:
                                                    spacing 8
                                                    xfill True
                                                    xalign 0.5
                                                    
                                                    text "👤 Personaje:" color "#ffffff" size 19 xalign 0.5 style "text_with_outline"
                                                    
                                                    # Lista de personajes definidos
                                                    $ defined_chars = defined_characters
                                                    if defined_chars:
                                                        viewport:
                                                            xminimum 350
                                                            ysize (50 + (len(defined_chars) * 30))  # Altura dinámica según personajes
                                                            scrollbars "vertical"
                                                            mousewheel True
                                                            xalign 0.5
                                                            
                                                            
                                                            vbox:
                                                                spacing 5
                                                                xfill True
                                                                
                                                                for char_name, char_def in defined_chars.items():
                                                                    $ display_name = char_def.get('display_name', char_name)
                                                                    $ char_color = char_def.get('color', '#3498db')
                                                                    $ char_type = char_def.get('type', 'normal')
                                                                    
                                                                    textbutton display_name:
                                                                        action [
                                                                            SetScreenVariable("dialogue_character", char_name),
                                                                            SetScreenVariable("current_speaker", char_name)
                                                                        ]
                                                                        selected (dialogue_character == char_name)
                                                                        xminimum 120
                                                                        ysize 25
                                                                        padding (8, 3)
                                                                        background char_color
                                                                        text_color "#000000"
                                                                        xalign 0.5
                                                    else:
                                                        text "No hay personajes definidos" color "#95a5a6" size 18 xalign 0.5 style "title_with_outline"
                                                
                                                # Campo de entrada
                                                input value ScreenVariableInputValue("dialogue_text") length 100 xminimum 500
                                                
                                                # Información del personaje seleccionado
                                                if dialogue_character:
                                                    $ char_def = get_character_definition(dialogue_character)
                                                    if char_def:
                                                        $ display_name = char_def.get('display_name', dialogue_character)
                                                        $ char_color = char_def.get('color', '#3498db')
                                                        text f"💬 {display_name}:" color char_color size text_sizes.text_medium xalign 0.5
                                                
                                                # Botón de acción
                                                textbutton "➕ Agregar Diálogo":
                                                    action Function(add_dialogue_to_scene)
                                                    xminimum 150
                                                    ysize 90
                                                    padding (15, 10)
                                                    background "#2c3e50"
                                                    xalign 0.5
                                                    text_style "text_with_outline"
                        
                        # PÁGINA 2: PERSONAJES
                        elif current_panel_page == "characters":
                            viewport:
                                xsize visual_layout.editor_width - 60
                                ysize visual_layout.bottom_area_height - 70
                                scrollbars "vertical"
                                mousewheel True
                                xalign 0.5
                                
                                vbox:
                                    spacing 20
                                    xalign 0.5
                                    
                                    # Panel de Personajes
                                    python:
                                        try:
                                            # Calcular ancho dinámico según el contenido
                                            characters_panel_width = 700  # Ancho optimizado para este panel
                                            
                                            # Calcular altura dinámica según el contenido
                                            # Altura base: título + espaciado
                                            base_height = 80
                                            
                                            # Altura por sección
                                            characters_list_height = 150   # Lista de personajes
                                            action_buttons_height = 60     # Botones de acción
                                            
                                            # Calcular altura total
                                            characters_panel_height = (base_height + characters_list_height + action_buttons_height)
                                            
                                            # Altura mínima y máxima
                                            min_height = 450
                                            max_height = 450
                                            characters_panel_height = max(min_height, min(characters_panel_height, max_height))
                                            
                                        except:
                                            characters_panel_width = 500
                                            characters_panel_height = 300
                                    frame:
                                        xsize characters_panel_width
                                        ysize characters_panel_height
                                        background colors.character_panel
                                        padding (20, 15)
                                        xalign 0.5
                                        
                                        vbox:
                                            spacing 15
                                            xfill True
                                            
                                            # Título centrado
                                            text "👤 Personajes" color "#ffffff" size text_sizes.title_medium xalign 0.5 style "title_with_outline"
                                            
                                            # Contenido del panel
                                            vbox:
                                                spacing 12
                                                xfill True
                                                
                                                # Lista de personajes
                                                viewport:
                                                    xminimum 350
                                                    ysize 250
                                                    scrollbars "vertical"
                                                    mousewheel True
                                                    xalign 0.5
                                                    
                                                    vbox:
                                                        spacing 8
                                                        xfill True
                                                        for c in editor_character_list:
                                                            textbutton c:
                                                                action [
                                                                    SetScreenVariable("current_speaker", c),
                                                                    SetScreenVariable("selected_char_base", c),
                                                                    Function(load_character_definition, c)
                                                                ]
                                                                selected (current_speaker == c)
                                                                xminimum 120
                                                                ysize 50
                                                                padding (10, 5)
                                                                background "#34495e"
                                                                xalign 0.5
                                                                text_style "text_with_outline"
                                            
                                            # Botones de gestión de personajes
                                            hbox:
                                                spacing 10
                                                xalign 0.5
                                                
                                                textbutton "➕ Añadir Personaje":
                                                    action SetScreenVariable("active_input_area", "character")
                                                    xminimum 150
                                                    ysize 90
                                                    padding (12, 8)
                                                    background "#27ae60"
                                                    text_style "text_with_outline"
                                                
                                                textbutton "🎬 Agregar a Escena":
                                                    action Function(add_character_to_scene)
                                                    xminimum 150
                                                    ysize 90
                                                    padding (12, 8)
                                                    background "#8e44ad"
                                                    text_style "text_with_outline"
                                    
                                    # Panel de Sprites del Personaje Seleccionado
                                    if current_speaker:
                                        python:
                                            try:
                                                # Calcular ancho dinámico según el contenido
                                                sprites_panel_width = 500  # Ancho optimizado para este panel
                                                
                                                # Calcular altura dinámica según el contenido
                                                # Altura base: título + espaciado
                                                base_height = 80
                                                
                                                # Altura por sección
                                                preview_height = 80        # Vista previa del sprite
                                                action_buttons_height = 60 # Botones de gestión
                                                sprites_list_height = 120  # Lista de sprites
                                                
                                                # Calcular altura total
                                                sprites_panel_height = (base_height + preview_height + action_buttons_height + sprites_list_height)
                                                
                                                # Altura mínima y máxima
                                                min_height = 500
                                                max_height = 400
                                                sprites_panel_height = max(min_height, min(sprites_panel_height, max_height))
                                                
                                            except:
                                                sprites_panel_width = 500
                                                sprites_panel_height = 300
                                        frame:
                                            xsize sprites_panel_width
                                            ysize sprites_panel_height
                                            background "#2c3e50"
                                            padding (20, 15)
                                            xalign 0.5
                                            xoffset 600
                                            yoffset -480
                                            
                                            vbox:
                                                spacing 15
                                                xfill True
                                                
                                                # Título del panel de sprites
                                                text f"🎭 Sprites de {current_speaker}" color "#ffffff" size text_sizes.title_medium xalign 0.5 style "title_with_outline"
                                                
                                                # Obtener sprites del personaje
                                                $ character_sprites = get_character_sprites(current_speaker)
                                                
                                                if character_sprites:
                                                    # Vista previa del sprite actual
                                                    frame:
                                                        xfill True
                                                        ysize 80
                                                        background "#34495e"
                                                        padding (10, 10)
                                                        xalign 0.5
                                                        
                                                        hbox:
                                                            spacing 15
                                                            xfill True
                                                            yalign 0.5
                                                            
                                                            # Imagen del sprite actual
                                                            if current_expression:
                                                                $ current_sprite_path = f"images/character/{current_speaker.lower()}/{current_expression}.png"
                                                                if renpy.loadable(current_sprite_path):
                                                                    add current_sprite_path:
                                                                        xsize 60
                                                                        ysize 60
                                                                        fit "contain"
                                                                        yalign 0.5
                                                            
                                                            # Información del sprite
                                                            vbox:
                                                                spacing 5
                                                                xfill True
                                                                
                                                                text f"Expresión actual: {current_expression or 'happy'}" color "#ffffff" size 18
                                                                text f"Sprites disponibles: {len(character_sprites)}" color "#95a5a6" size 18
                                                    
                                                    # Botones de gestión de sprites
                                                    hbox:
                                                        spacing 10
                                                        xalign 0.5
                                                        
                                                        textbutton "📁 Importar Sprite":
                                                            action Function(import_sprite_to_character, current_speaker)
                                                            xminimum 120
                                                            ysize 50
                                                            padding (8, 5)
                                                            background "#e67e22"
                                                            text_style "text_with_outline"
                                                        
                                                        textbutton "🔄 Refrescar":
                                                            action Function(define_character_sprites)
                                                            xminimum 80
                                                            ysize 80
                                                            padding (8, 5)
                                                            background "#3498db"
                                                            text_style "text_with_outline"
                                                    
                                                    # Grid de sprites disponibles
                                                    viewport:
                                                        xminimum 350
                                                        ysize 200
                                                        scrollbars "vertical"
                                                        mousewheel True
                                                        xalign 0.5
                                                        
                                                        vbox:
                                                            spacing 8
                                                            xfill True
                                                            
                                                            for sprite_name in character_sprites:
                                                                textbutton sprite_name:
                                                                    action [
                                                                        SetScreenVariable("current_expression", sprite_name),
                                                                        Function(set_character_expression, sprite_name)
                                                                    ]
                                                                    selected (current_expression == sprite_name)
                                                                    xminimum 320
                                                                    ysize 50
                                                                    padding (8, 5)
                                                                    background "#34495e"
                                                                    xalign 0.5
                                                                    text_style "text_with_outline"
                                                else:
                                                    # Mensaje si no hay sprites
                                                    frame:
                                                        xfill True
                                                        ysize 120
                                                        background "#34495e"
                                                        padding (20, 20)
                                                        xalign 0.5
                                                        
                                                        vbox:
                                                            spacing 10
                                                            xalign 0.5
                                                            yalign 0.5
                                                            
                                                            text "🎭" size 30 xalign 0.5
                                                            text "No hay sprites disponibles" color "#95a5a6" size 18 xalign 0.5
                                                            text f"Agrega imágenes a: images/character/{current_speaker.lower()}/" color "#7f8c8d" size 18 xalign 0.5
                                                            
                                                            # Botón para importar el primer sprite
                                                            textbutton "📁 Importar Primer Sprite":
                                                                action Function(import_sprite_to_character, current_speaker)
                                                                xminimum 150
                                                                ysize 80
                                                                padding (8, 5)
                                                                background "#e67e22"
                                                                xalign 0.5
                                                                text_style "text_with_outline"
                                    
                                    # Panel de Definición de Personaje
                                    if current_speaker:
                                        python:
                                            try:
                                                # Calcular ancho dinámico según el contenido
                                                definition_panel_width = 700  # Ancho optimizado para este panel
                                                
                                                # Calcular altura dinámica según el contenido
                                                # Altura base: título + espaciado
                                                base_height = 100
                                                
                                                # Altura por sección
                                                name_field_height = 40       # Campo de nombre
                                                color_section_height = 200   # Sección de colores (3 filas)
                                                type_section_height = 40     # Sección de tipo
                                                action_button_height = 50    # Botón de acción
                                                
                                                # Calcular altura total
                                                definition_panel_height = (base_height + name_field_height + color_section_height + type_section_height + action_button_height)
                                                
                                                # Altura mínima y máxima
                                                min_height = 450
                                                max_height = 600
                                                definition_panel_height = max(min_height, min(definition_panel_height, max_height))
                                                
                                            except:
                                                definition_panel_width = 500
                                                definition_panel_height = 400
                                        frame:
                                            xsize definition_panel_width
                                            ysize definition_panel_height
                                            background "#34495e"
                                            padding (20, 15)
                                            xalign 0.5
                                            xoffset -20
                                            yoffset -540

                                            vbox:
                                                spacing 12
                                                xfill True
                                                
                                                # Título del panel de definición
                                                text f"⚙️ Definir Personaje: {current_speaker}" color "#ffffff" size text_sizes.title_medium xalign 0.5 style "title_with_outline"
                                                
                                                # Campos de definición
                                                vbox:
                                                    spacing 8
                                                    xfill True
                                                    
                                                    # Nombre del personaje
                                                    hbox:
                                                        spacing 10
                                                        xfill True
                                                        yalign 0.5
                                                        
                                                        text "Nombre:" color "#ffffff" size text_sizes.text_medium xminimum 80
                                                        input value ScreenVariableInputValue("character_display_name", current_speaker) xfill True
                                                    
                                                    # Color del personaje
                                                    vbox:
                                                        spacing 5
                                                        xfill True
                                                        
                                                        text "Color:" color "#ffffff" size text_sizes.text_medium xminimum 80
                                                        
                                                        # Botones de colores predefinidos
                                                        hbox:
                                                            spacing 5
                                                            xfill True
                                                            yalign 0.5
                                                            
                                                            textbutton "🟢 Verde" action Function(set_character_color, "#c8ffc8") selected (character_color == "#c8ffc8") xminimum 80 ysize 40 text_style "text_with_outline"
                                                            textbutton "🔴 Rojo" action Function(set_character_color, "#ffc8c8") selected (character_color == "#ffc8c8") xminimum 80 ysize 40 text_style "text_with_outline"
                                                            textbutton "🔵 Azul" action Function(set_character_color, "#c8c8ff") selected (character_color == "#c8c8ff") xminimum 80 ysize 40 text_style "text_with_outline"
                                                            
                                                        hbox:
                                                            spacing 5
                                                            xfill True
                                                            yalign 0.5
                                                            
                                                            textbutton "🟡 Amarillo" action Function(set_character_color, "#ffffc8") selected (character_color == "#ffffc8") xminimum 80 ysize 40 text_style "text_with_outline"
                                                            textbutton "🟣 Morado" action Function(set_character_color, "#ffc8ff") selected (character_color == "#ffc8ff") xminimum 80 ysize 40 text_style "text_with_outline"
                                                            textbutton "🟠 Naranja" action Function(set_character_color, "#ffd8a8") selected (character_color == "#ffd8a8") xminimum 80 ysize 40 text_style "text_with_outline"
                                                            
                                                        hbox:
                                                            spacing 5
                                                            xfill True
                                                            yalign 0.5
                                                            
                                                            textbutton "⚪ Blanco" action Function(set_character_color, "#ffffff") selected (character_color == "#ffffff") xminimum 80 ysize 40 text_style "text_with_outline"
                                                            textbutton "⚫ Negro" action Function(set_character_color, "#000000") selected (character_color == "#000000") xminimum 80 ysize 40 text_style "text_with_outline"
                                                            textbutton "🟤 Marrón" action Function(set_character_color, "#d2b48c") selected (character_color == "#d2b48c") xminimum 80 ysize 40 text_style "text_with_outline"
                                                            
                                                        # Vista previa del color seleccionado
                                                        frame:
                                                            xfill True
                                                            ysize 50
                                                            background character_color
                                                            padding (10, 5)
                                                            xalign 0.5
                                                            
                                                            $ color_name = get_color_name(character_color)
                                                            text f"Color actual: {color_name}" color "#000000" size 18 xalign 0.5 yalign 0.5
                                                    
                                                    # Tipo de personaje
                                                    hbox:
                                                        spacing 10
                                                        xfill True
                                                        yalign 0.5
                                                        
                                                        text "Tipo:" color "#ffffff" size text_sizes.text_medium xminimum 80
                                                        textbutton "Personaje Normal" action SetScreenVariable("character_type", "normal") selected (character_type == "normal") xminimum 120 ysize 40 text_style "text_with_outline"
                                                        # textbutton "Narrador" action SetScreenVariable("character_type", "narrator") selected (character_type == "narrator") xminimum 80 ysize 40 text_style "text_with_outline"
                                                
                                                # Botón para definir personaje
                                                textbutton "✅ Definir Personaje":
                                                    action Function(define_character_in_script, current_speaker)
                                                    xminimum 150
                                                    ysize 50
                                                    padding (10, 8)
                                                    background "#27ae60"
                                                    xalign 0.5
                                                    text_style "text_with_outline"
                                    
                                    # Panel de Personajes Definidos
                                    python:
                                        try:
                                            # Calcular ancho dinámico según el contenido
                                            defined_panel_width = 500  # Ancho optimizado para este panel
                                            
                                            # Calcular altura dinámica según el contenido
                                            # Altura base: título + espaciado
                                            base_height = 80
                                            
                                            # Altura por sección
                                            action_buttons_height = 60     # Botones de gestión
                                            characters_list_height = 80    # Lista de personajes definidos
                                            
                                            # Calcular altura total
                                            defined_panel_height = (base_height + action_buttons_height + characters_list_height)
                                            
                                            # Altura mínima y máxima
                                            min_height = 500
                                            max_height = 500
                                            defined_panel_height = max(min_height, min(defined_panel_height, max_height))
                                            
                                        except:
                                            defined_panel_width = 500
                                            defined_panel_height = 200
                                    frame:
                                        xsize defined_panel_width
                                        ysize defined_panel_height
                                        background "#2c3e50"
                                        padding (20, 15)
                                        xalign 0.5
                                        yalign 0.5
                                        xoffset 1150
                                        yoffset -480
                                        
                                        vbox:
                                            spacing 10
                                            xfill True
                                            
                                            # Título del panel
                                            text "📋 Personajes Definidos" color "#ffffff" size text_sizes.title_medium xalign 0.5 style "title_with_outline"
                                            
                                            # Botones de gestión de archivo
                                            hbox:
                                                spacing 10
                                                xalign 0.5
                                                
                                                textbutton "📁 Generar Archivo":
                                                    action Function(generate_characters_file)
                                                    xminimum 120
                                                    ysize 50
                                                    padding (8, 5)
                                                    background "#27ae60"
                                                    text_style "text_with_outline"
                                                
                                                textbutton "📂 Cargar Archivo":
                                                    action Function(load_characters_from_file)
                                                    xminimum 120
                                                    ysize 120
                                                    padding (8, 5)
                                                    background "#3498db"
                                                    text_style "text_with_outline"
                                            
                                            # Lista de personajes definidos
                                            $ defined_chars = defined_characters
                                            if defined_chars:
                                                viewport:
                                                    xminimum 350
                                                    ysize 80
                                                    scrollbars "vertical"
                                                    mousewheel True
                                                    xalign 0.5
                                                    
                                                    vbox:
                                                        spacing 5
                                                        xfill True
                                                        
                                                        for char_name, char_def in defined_chars.items():
                                                            hbox:
                                                                spacing 8
                                                                xfill True
                                                                yalign 0.5
                                                                
                                                                text "• " + char_name color "#3498db" size 18 xminimum 80
                                                                text "(" + char_name + ")" color "#95a5a6" size 18
                                                                text "Personaje" color "#e67e22" size 18
                                                                
                                                                # Botones de acción
                                                                hbox:
                                                                    spacing 5
                                                                    xalign 1.0
                                                                    
                                                                    textbutton "✏️":
                                                                        action Function(edit_character_definition, char_name)
                                                                        xminimum 30
                                                                        ysize 30
                                                                        padding (3, 2)
                                                                        background "#f39c12"
                                                                        text_size 18
                                                                        text_style "text_with_outline"
                                                                    
                                                                    textbutton "🗑️":
                                                                        action Function(delete_character_definition, char_name)
                                                                        xminimum 30
                                                                        ysize 30
                                                                        padding (3, 2)
                                                                        background "#e74c3c"
                                                                        text_size 18
                                                                        text_style "text_with_outline"
                                            else:
                                                text "No hay personajes definidos" color "#95a5a6" size 18 xalign 0.5 yalign 0.5
                        
                        # PÁGINA 3: ESTRUCTURA
                        elif current_panel_page == "structure":
                            viewport:
                                xsize visual_layout.editor_width - 60
                                ysize visual_layout.bottom_area_height - 70
                                scrollbars "vertical"
                                mousewheel True
                                xalign 0.5
                                
                                vbox:
                                    spacing 20
                                    xalign 0.5
                                    
                                    # Panel de Estructura
                                    python:
                                        try:
                                            # Calcular ancho dinámico según el contenido activo
                                            if active_input_area == "choice":
                                                # Panel de choice necesita más espacio
                                                structure_panel_width = 1000
                                            elif active_input_area == "label" or active_input_area == "jump":
                                                # Paneles simples
                                                structure_panel_width = 800
                                            else:
                                                # Panel vacío
                                                structure_panel_width = 850
                                            
                                            # Calcular altura dinámica según el contenido activo
                                            # Altura base: título + espaciado
                                            base_height = 80
                                            
                                            # Altura por sección
                                            tools_height = 60           # Herramientas de estructura
                                            
                                            # Altura según el área activa
                                            if active_input_area == "choice":
                                                # Panel de choice necesita más altura
                                                content_height = 500    # Contenido de choice
                                                structure_panel_height = (base_height + tools_height + content_height)
                                            elif active_input_area == "label" or active_input_area == "jump":
                                                # Paneles simples
                                                content_height = 200    # Contenido de label/jump
                                                structure_panel_height = (base_height + tools_height + content_height)
                                            else:
                                                # Panel vacío
                                                content_height = 50     # Solo herramientas
                                                structure_panel_height = (base_height + tools_height + content_height)
                                            
                                            # Altura mínima y máxima
                                            min_height = 200
                                            max_height = 800
                                            structure_panel_height = max(min_height, min(structure_panel_height, max_height))
                                            
                                        except:
                                            structure_panel_width = 850
                                            structure_panel_height = 300
                                    frame:
                                        xsize structure_panel_width
                                        ysize structure_panel_height
                                        background colors.structure_panel
                                        padding (20, 15)
                                        xalign 0.5
                                        yalign 0.5
                                        xoffset -150
                                        yoffset 0
                                        
                                        vbox:
                                            spacing 15
                                            xfill True
                                            
                                            # Título centrado
                                            text "🏗️ Estructura" color "#ffffff" size text_sizes.title_medium xalign 0.5 style "title_with_outline"
                                            
                                            # Contenido del panel
                                            vbox:
                                                spacing 12
                                                xfill True
                                                
                                                # Herramientas de estructura
                                                hbox:
                                                    spacing 15
                                                    xalign 0.5
                                                    
                                                    textbutton "🏷️ Agregar Label":
                                                        action SetScreenVariable("active_input_area", "label")
                                                        xminimum 120
                                                        ysize 40
                                                        padding (12, 8)
                                                        background "#8e44ad"
                                                        xalign 0.5
                                                        text_style "text_with_outline"
                                                    
                                                    textbutton "🔄 Agregar Jump":
                                                        action SetScreenVariable("active_input_area", "jump")
                                                        xminimum 120
                                                        ysize 40
                                                        padding (12, 8)
                                                        background "#8e44ad"
                                                        xalign 0.5
                                                        text_style "text_with_outline"
                                                    
                                                    # Botón de Choice removido - ahora es un panel separado
                                                
                                                # Área de entrada de texto dinámica
                                                if active_input_area == "label":
                                                    frame:
                                                        xfill True
                                                        background "#2c3e50"
                                                        padding (15, 12)
                                                        margin (0, 10, 0, 0)
                                                        
                                                        vbox:
                                                            spacing 10
                                                            xfill True
                                                            
                                                            text "🏷️ Crear Label:" color "#ffffff" size text_sizes.text_medium xalign 0.5 style "text_with_outline"
            
                                                            text "Nombre del label (ej: start, menu_principal):" color "#bdc3c7" size text_sizes.text_small xalign 0.5 style "text_with_outline"
            
                                                            input value ScreenVariableInputValue("label_name") length 50 xminimum 350
                                                            
                                                            hbox:
                                                                spacing 15
                                                                xalign 0.5
                                                                
                                                                textbutton "✅ Crear Label":
                                                                    action Function(add_label_to_scene)
                                                                    xminimum 120
                                                                    ysize 35
                                                                    padding (12, 8)
                                                                    background "#27ae60"
                                                                    xalign 0.5
                                                                    text_style "text_with_outline"
                                                                
                                                                textbutton "❌ Cancelar":
                                                                    action SetScreenVariable("active_input_area", None)
                                                                    xminimum 100
                                                                    ysize 35
                                                                    padding (12, 8)
                                                                    background "#e74c3c"
                                                                    xalign 0.5
                                                                    text_style "text_with_outline"
                                                
                                                elif active_input_area == "jump":
                                                    frame:
                                                        xfill True
                                                        background "#2c3e50"
                                                        padding (15, 12)
                                                        margin (0, 10, 0, 0)
                                                        
                                                        vbox:
                                                            spacing 10
                                                            xfill True
                                                            
                                                            text "🔄 Crear Jump:" color "#ffffff" size text_sizes.text_medium xalign 0.5 style "text_with_outline"
            
                                                            text "Label de destino (ej: start, menu_principal):" color "#bdc3c7" size text_sizes.text_small xalign 0.5 style "text_with_outline"
            
                                                            input value ScreenVariableInputValue("jump_target") length 50 xminimum 350
                                                            
                                                            hbox:
                                                                spacing 15
                                                                xalign 0.5
                                                                
                                                                textbutton "✅ Crear Jump":
                                                                    action Function(add_jump_to_scene)
                                                                    xminimum 120
                                                                    ysize 35
                                                                    padding (12, 8)
                                                                    background "#27ae60"
                                                                    xalign 0.5
                                                                    text_style "text_with_outline"
                                                                
                                                                textbutton "❌ Cancelar":
                                                                    action SetScreenVariable("active_input_area", None)
                                                                    xminimum 100
                                                                    ysize 35
                                                                    padding (12, 8)
                                                                    background "#e74c3c"
                                                                    xalign 0.5
                                                                    text_style "text_with_outline"
                                                
                                                # Panel de Choice removido - ahora es un panel separado
                                                
                                                # Panel de Choice completamente removido - ahora es un panel separado
                                    
                                    # Panel de Choice
                                    python:
                                        try:
                                            # Calcular ancho dinámico según el contenido
                                            choice_panel_width = 1000  # Ancho optimizado para este panel
                                            
                                            # Calcular altura dinámica según el contenido real
                                            # Altura base: título + espaciado
                                            base_height = 80
                                            
                                            # Altura por sección según el estado actual
                                            question_height = 80       # Campo de pregunta (siempre visible)
                                            
                                            # Altura de confirmación de pregunta
                                            confirm_height = 0
                                            if choice_text and not choice_question_confirmed:
                                                confirm_height = 50     # Botones de confirmar/reiniciar
                                            elif choice_question_confirmed:
                                                confirm_height = 80     # Mensaje de confirmación
                                            
                                            # Altura de sección de opciones (solo si pregunta confirmada)
                                            options_section_height = 0
                                            if choice_question_confirmed:
                                                options_section_height = 300  # Título + botón agregar
                                                
                                                # Altura de opciones existentes
                                                if choice_options:
                                                    options_section_height += 250  # Lista de opciones
                                                else:
                                                    options_section_height += 80   # Mensaje "no hay opciones"
                                            
                                            # Altura del panel de agregar opciones
                                            add_panel_height = 0
                                            try:
                                                show_panel = renpy.get_screen_variable("show_choice_add_panel")
                                                if show_panel:
                                                    add_panel_height = 400  # Panel completo de agregar opciones
                                            except:
                                                show_panel = False
                                            
                                            # Altura de botones de acción (solo si pregunta confirmada)
                                            action_buttons_height = 0
                                            if choice_question_confirmed:
                                                action_buttons_height = 60
                                            
                                            # Altura de instrucciones (solo si no hay pregunta confirmada)
                                            instructions_height = 0
                                            if not choice_question_confirmed:
                                                instructions_height = 120
                                            
                                            # Calcular altura total dinámica
                                            choice_panel_height = (base_height + question_height + confirm_height + 
                                                                 options_section_height + add_panel_height + 
                                                                 action_buttons_height + instructions_height)
                                            
                                            # Altura mínima y máxima
                                            min_height = 500
                                            max_height = 1500
                                            choice_panel_height = max(min_height, min(choice_panel_height, max_height))
                                            
                                        except:
                                            choice_panel_width = 1200
                                            choice_panel_height = 600
                                    frame:
                                        xsize choice_panel_width
                                        ysize choice_panel_height
                                        background "#9b59b6"
                                        padding (20, 15)
                                        xalign 0.5  # Centrar horizontalmente
                                        yalign 0.5  # Centrar verticalmente
                                        xoffset 780   # Mover a la derecha
                                        yoffset -230   # Mover hacia arriba
                                        
                                        vbox:
                                            spacing 15
                                            xfill True
                                            
                                            # Título centrado
                                            text "❓ Panel de Choice" color "#ffffff" size text_sizes.title_medium xalign 0.5 style "title_with_outline"
                                            
                                            # Contenido del panel
                                            vbox:
                                                spacing 12
                                                xfill True
                                                
                                                # Campo de pregunta
                                                vbox:
                                                    spacing 10
                                                    xfill True
                                                    
                                                    text "❓ Crear Choice:" color "#ffffff" size 18 xalign 0.5 style "text_with_outline"
                                                    text "Texto de la pregunta (ej: ¿Quieres continuar?):" color "#bdc3c7" size 18 xalign 0.5 style "text_with_outline"
                                                    
                                                    hbox:
                                                        spacing 10
                                                        xalign 0.5
                                                        
                                                        # Campo de pregunta
                                                        frame:
                                                            xsize 400
                                                            ysize 50
                                                            background "#2c3e50"
                                                            padding (10, 5)
                                                            
                                                            if choice_text_active:
                                                                input:
                                                                    value ScreenVariableInputValue("choice_text")
                                                                    xfill True
                                                                    yfill True
                                                                    color "#ffffff"
                                                                    size text_sizes.text_medium
                                                                    default ""
                                                                    length 100
                                                                    id "choice_text_input"
                                                            else:
                                                                text choice_text or "Escribe la pregunta..." color "#ffffff" size 18 xalign 0.5 yalign 0.5
                                                        
                                                        # Botón para activar edición
                                                        if not choice_text_active:
                                                            textbutton "✏️ Editar":
                                                                action Function(activate_choice_text_edit)
                                                                xsize 80
                                                                ysize 50
                                                                background "#3498db"
                                                                text_size 15
                                                                text_style "text_with_outline"
                                                        else:
                                                            # Botón para aceptar
                                                            textbutton "✅ Aceptar":
                                                                action Function(accept_choice_text)
                                                                xsize 80
                                                                ysize 50
                                                                background "#27ae60"
                                                                text_size 15
                                                                text_style "text_with_outline"
                                                
                                                # Botón para confirmar la pregunta
                                                if choice_text and not choice_question_confirmed:
                                                    hbox:
                                                        spacing 10
                                                        xalign 0.5
                                                        
                                                        textbutton "✅ Confirmar Pregunta":
                                                            action Function(confirm_choice_question)
                                                            xminimum 150
                                                            ysize 35
                                                            background "#27ae60"
                                                            text_size 15
                                                            text_style "text_with_outline"
                                                        
                                                        textbutton "🔄 Reiniciar":
                                                            action Function(reset_choice_question)
                                                            xminimum 100
                                                            ysize 35
                                                            background "#f39c12"
                                                            text_size 15
                                                            text_style "text_with_outline"
                                                
                                                # Mostrar pregunta confirmada
                                                if choice_question_confirmed:
                                                    frame:
                                                        xfill True
                                                        background "#27ae60"
                                                        padding (10, 8)
                                                        margin (0, 5, 0, 0)
                                                        
                                                        vbox:
                                                            spacing 5
                                                            xfill True
                                                            
                                                            text "✅ Pregunta Confirmada:" color "#ffffff" size 18 xalign 0.5 style "text_with_outline"
                                                            text choice_text color "#ffffff" size 18 xalign 0.5 style "text_with_outline"
                                                            
                                                            textbutton "🔄 Cambiar Pregunta":
                                                                action Function(reset_choice_question)
                                                                xminimum 120
                                                                ysize 35
                                                                background "#f39c12"
                                                                text_size 15
                                                                xalign 0.5
                                                                text_style "text_with_outline"
                                                
                                                # Mostrar opciones existentes (solo si la pregunta está confirmada)
                                                if choice_question_confirmed:
                                                    vbox:
                                                        spacing 10
                                                        xfill True
                                                        
                                                        text "📋 Opciones del Choice:" color "#ffffff" size 18 xalign 0.5 style "text_with_outline"
                                                        
                                                        # Debug: Mostrar estado del panel (removido temporalmente)
                                                        
                                                        # Mostrar opciones existentes
                                                        if choice_options:
                                                            vbox:
                                                                spacing 8
                                                                xfill True
                                                                
                                                                text "Opciones actuales:" color "#ffffff" size text_sizes.text_medium xalign 0.5 style "text_with_outline"
                                                        else:
                                                            # Mensaje cuando no hay opciones
                                                            frame:
                                                                xfill True
                                                                background "#34495e"
                                                                padding (10, 15)
                                                                margin (0, 5, 0, 0)
                                                                
                                                                vbox:
                                                                    spacing 5
                                                                    xfill True
                                                                    xalign 0.5
                                                                    
                                                                    text "📝 No hay opciones aún" color "#ffffff" size 18 xalign 0.5 style "text_with_outline"
                                                                    text "Haz clic en '➕ Agregar Opción' para crear la primera opción" color "#bdc3c7" size 18 xalign 0.5 style "text_with_outline"
                                                        
                                                        viewport:
                                                            xminimum 400
                                                            ysize 150
                                                            scrollbars "vertical"
                                                            mousewheel True
                                                            xalign 0.5
                                                            
                                                            vbox:
                                                                spacing 5
                                                                xfill True
                                                                
                                                                for i, option in enumerate(choice_options):
                                                                    frame:
                                                                        xfill True
                                                                        background "#34495e"
                                                                        padding (8, 6)
                                                                        margin (0, 0, 0, 5)
                                                                        
                                                                        vbox:
                                                                            spacing 5
                                                                            xfill True
                                                                            
                                                                            # Línea principal con número y texto
                                                                            hbox:
                                                                                spacing 10
                                                                                xfill True
                                                                                
                                                                                text f"{i+1}." color "#f39c12" size 18
                                                                                
                                                                                # Manejar tanto strings como objetos
                                                                                if isinstance(option, dict):
                                                                                    text option.get('text', 'Opción') color "#ecf0f1" size 18
                                                                                else:
                                                                                    text option color "#ecf0f1" size 18
                                                                                
                                                                                textbutton "🗑️":
                                                                                    action Function(remove_choice_option, i)
                                                                                    xsize 35
                                                                                    ysize 35
                                                                                    background "#e74c3c"
                                                                                    text_size 18
                                                                                    text_style "text_with_outline"
                                                                            
                                                                            # Mostrar jump si existe
                                                                            if isinstance(option, dict) and option.get('jump'):
                                                                                hbox:
                                                                                    spacing 10
                                                                                    xfill True
                                                                                    
                                                                                    text "🔄" color "#3498db" size 18
                                                                                    text f"Jump a: {option.get('jump')}" color "#3498db" size 18 italic True
                                                            
                                                        # Botón para agregar opción
                                                        if len(choice_options) < 4:
                                                            textbutton "➕ Agregar Opción":
                                                                action Function(add_choice_option)
                                                                xminimum 150
                                                                ysize 50
                                                                padding (12, 8)
                                                                background "#3498db"
                                                                xalign 0.5
                                                                text_style "text_with_outline"
                                                        else:
                                                            text "Máximo 4 opciones alcanzado" color "#e74c3c" size text_sizes.text_small xalign 0.5 style "text_with_outline"
                                                    
                                                    # Panel integrado para agregar opciones (fuera del viewport)
                                                    python:
                                                        try:
                                                            show_panel = renpy.get_screen_variable("show_choice_add_panel")
                                                        except:
                                                            show_panel = False
                                                    if show_panel:
                                                        frame:
                                                            xfill True
                                                            ysize 450  # Panel de agregar opciones
                                                            background "#2c3e50"
                                                            padding (20, 20)
                                                            margin (0, 15, 0, 0)
                                                            
                                                            vbox:
                                                                        spacing 10
                                                                        xfill True
                                                                        
                                                                        text "📝 Agregar Nueva Opción" color "#ffffff" size 20 xalign 0.5 style "text_with_outline"
                                                                        
                                                                        # Campo de texto de la opción
                                                                        vbox:
                                                                            spacing 5
                                                                            xfill True
                                                                            
                                                                            text "Texto de la opción:" color "#bdc3c7" size 18 xalign 0.5
                                                                            
                                                                            hbox:
                                                                                spacing 10
                                                                                xalign 0.5
                                                                                
                                                                                # Campo de texto de opción
                                                                                frame:
                                                                                    xsize 250
                                                                                    ysize 40
                                                                                    background "#2c3e50"
                                                                                    padding (8, 5)
                                                                                    
                                                                                    if choice_option_active:
                                                                                        input:
                                                                                            value ScreenVariableInputValue("new_choice_option")
                                                                                            xfill True
                                                                                            yfill True
                                                                                            color "#ffffff"
                                                                                            size 18
                                                                                            default ""
                                                                                            length 40
                                                                                            id "choice_option_input"
                                                                                    else:
                                                                                        text new_choice_option or "Escribe el texto..." color "#ffffff" size 18 xalign 0.5 yalign 0.5
                                                                                
                                                                                # Botón para activar edición
                                                                                if not choice_option_active:
                                                                                    textbutton "✏️":
                                                                                        action Function(activate_choice_option_edit)
                                                                                        xsize 30
                                                                                        ysize 30
                                                                                        background "#3498db"
                                                                                        text_size 15
                                                                                        text_style "text_with_outline"
                                                                                else:
                                                                                    # Botón para aceptar
                                                                                    textbutton "✅":
                                                                                        action Function(accept_choice_option)
                                                                                        xsize 30
                                                                                        ysize 30
                                                                                        background "#27ae60"
                                                                                        text_size 15
                                                                                        text_style "text_with_outline"
                                                                        
                                                                        # Campo de nombre de jump
                                                                        vbox:
                                                                            spacing 5
                                                                            xfill True
                                                                            
                                                                            text "Jump (opcional):" color "#bdc3c7" size 18 xalign 0.5
                                                                            
                                                                            hbox:
                                                                                spacing 10
                                                                                xalign 0.5
                                                                                
                                                                                # Campo de jump
                                                                                frame:
                                                                                    xsize 250
                                                                                    ysize 40
                                                                                    background "#2c3e50"
                                                                                    padding (8, 5)
                                                                                    
                                                                                    if choice_jump_active:
                                                                                        input:
                                                                                            value ScreenVariableInputValue("new_choice_jump")
                                                                                            xfill True
                                                                                            yfill True
                                                                                            color "#ffffff"
                                                                                            size 18
                                                                                            default ""
                                                                                            length 40
                                                                                            id "choice_jump_input"
                                                                                    else:
                                                                                        text new_choice_jump or "Escribe el jump..." color "#ffffff" size 18 xalign 0.5 yalign 0.5
                                                                                
                                                                                # Botón para activar edición
                                                                                if not choice_jump_active:
                                                                                    textbutton "✏️":
                                                                                        action Function(activate_choice_jump_edit)
                                                                                        xsize 30
                                                                                        ysize 30
                                                                                        background "#3498db"
                                                                                        text_size 15
                                                                                        text_style "text_with_outline"
                                                                                else:
                                                                                    # Botón para aceptar
                                                                                    textbutton "✅":
                                                                                        action Function(accept_choice_jump)
                                                                                        xsize 30
                                                                                        ysize 30
                                                                                        background "#27ae60"
                                                                                        text_size 15
                                                                                        text_style "text_with_outline"
                                                                        
                                                                        # Botones de acción
                                                                        hbox:
                                                                            spacing 10
                                                                            xalign 0.5
                                                                            
                                                                            textbutton "➕ Agregar":
                                                                                action Function(confirm_add_choice_option)
                                                                                xsize 80
                                                                                ysize 50
                                                                                background "#27ae60"
                                                                                text_size 15
                                                                                text_style "text_with_outline"
                                                                            
                                                                            textbutton "🧹 Limpiar":
                                                                                action Function(clear_choice_inputs)
                                                                                xsize 80
                                                                                ysize 50
                                                                                background "#f39c12"
                                                                                text_size 15
                                                                                text_style "text_with_outline"
                                                                            
                                                                            textbutton "❌ Cancelar":
                                                                                action Function(cancel_choice_add_panel)
                                                                                xsize 80
                                                                                ysize 50
                                                                                background "#e74c3c"
                                                                                text_size 15
                                                                                text_style "text_with_outline"
                                                            
                                                            # Botones de acción
                                                            hbox:
                                                                spacing 15
                                                                xalign 0.5
                                                                yoffset 250  # ← Agrega esta línea en lugar de margin
                                                                
                                                                textbutton "✅ Crear Choice":
                                                                    action Function(add_choice_to_scene)
                                                                    xminimum 120
                                                                    ysize 50
                                                                    padding (12, 8)
                                                                    background "#27ae60"
                                                                    xalign 0.5
                                                                    text_style "text_with_outline"
                                                                
                                                                textbutton "❌ Cancelar":
                                                                    action Function(cancel_choice_creation)
                                                                    xminimum 100
                                                                    ysize 50
                                                                    padding (12, 8)
                                                                    background "#e74c3c"
                                                                    xalign 0.5
                                                                    text_style "text_with_outline"
                                                else:
                                                    # Mensaje cuando no hay pregunta confirmada
                                                    frame:
                                                        xfill True
                                                        background "#34495e"
                                                        padding (15, 20)
                                                        margin (0, 30, 0, 0)
                                                        
                                                        vbox:
                                                            spacing 10
                                                            xfill True
                                                            xalign 0.5
                                                            
                                                            text "📝 Instrucciones:" color "#ffffff" size 18 xalign 0.5 style "text_with_outline"
                                                            text "1. Escribe la pregunta del choice" color "#bdc3c7" size 18 xalign 0.5 style "text_with_outline"
                                                            text "2. Confirma la pregunta" color "#bdc3c7" size 18 xalign 0.5 style "text_with_outline"
                                                            text "3. Agrega las opciones con sus jumps" color "#bdc3c7" size 18 xalign 0.5 style "text_with_outline"
                                                            text "4. Crea el choice" color "#bdc3c7" size 18 xalign 0.5 style "text_with_outline"
                        
                        # PÁGINA 4: VISTA PREVIA
                        elif current_panel_page == "preview":
                            viewport:
                                xsize visual_layout.editor_width - 60
                                ysize visual_layout.bottom_area_height - 100
                                scrollbars "vertical"
                                mousewheel True
                                xalign 0.5
                                
                                hbox:
                                    spacing 20
                                    xalign 0.5
                                    
                                    # Panel de Controles de Vista Previa
                                    python:
                                        try:
                                            # Calcular ancho dinámico según el contenido
                                            preview_panel_width = 500  # Ancho fijo para este panel
                                            
                                            # Calcular altura dinámica según el contenido
                                            # Altura base: título + espaciado
                                            base_height = 80
                                            
                                            # Altura por sección
                                            expressions_height = 30  # Expresiones (desactivadas)
                                            position_height = 120   # Controles de posición
                                            actions_height = 130    # Botones de acciones
                                            info_height = 230       # Información de vista previa
                                            
                                            # Calcular altura total
                                            preview_panel_height = (base_height + expressions_height + 
                                                                  position_height + actions_height + info_height)
                                            
                                            # Altura mínima y máxima
                                            min_height = 800
                                            max_height = 800
                                            preview_panel_height = max(min_height, min(preview_panel_height, max_height))
                                            
                                        except:
                                            preview_panel_width = 450
                                            preview_panel_height = 600
                                    frame:
                                        xsize preview_panel_width
                                        ysize preview_panel_height
                                        background "#8e44ad"
                                        padding (20, 15)
                                        xalign 0.0
                                        yalign 0.0
                                        
                                        vbox:
                                            spacing 15
                                            xfill True
                                            xalign 0.5
                                            
                                            # Título centrado
                                            text "🎮 Controles de Vista Previa" color "#ffffff" size text_sizes.title_medium xalign 0.5 style "title_with_outline"
                                            
                                            # Contenido del panel
                                            vbox:
                                                spacing 12
                                                xfill True
                                                xalign 0.5
                                                
                                                # Controles de expresión (DESACTIVADOS TEMPORALMENTE)
                                                vbox:
                                                    spacing 8
                                                    xfill True
                                                    xalign 0.5
                                                    text "😊 Expresiones: (Desactivadas)" color "#95a5a6" size 20 xalign 0.5 italic True style "text_with_outline"
                                                
                                                # Controles de posición de sprite
                                                vbox:
                                                    spacing 8
                                                    xfill True
                                                    xalign 0.5
                                                    text "📍 Posición:" color "#ffffff" size 20 xalign 0.5 style "text_with_outline"
                                                    
                                                    # Primera fila de posiciones
                                                    hbox:
                                                        spacing 8
                                                        xalign 0.5
                                                        
                                                        textbutton "⬅️":
                                                            action Function(set_sprite_position, "left")
                                                            xsize 45
                                                            ysize 45
                                                            background "#e67e22"
                                                            xalign 0.5
                                                            yalign 0.5
                                                            text_size 20
                                                            text_style "text_with_outline"
                                                            selected (sprite_position == "left")
                                                        
                                                        textbutton "⬆️":
                                                            action Function(set_sprite_position, "center")
                                                            xsize 45
                                                            ysize 45
                                                            background "#27ae60"
                                                            xalign 0.5
                                                            yalign 0.5
                                                            text_size 20
                                                            text_style "text_with_outline"
                                                            selected (sprite_position == "center")
                                                        
                                                        textbutton "➡️":
                                                            action Function(set_sprite_position, "right")
                                                            xsize 45
                                                            ysize 45
                                                            background "#e67e22"
                                                            xalign 0.5
                                                            yalign 0.5
                                                            text_size 20
                                                            text_style "text_with_outline"
                                                            selected (sprite_position == "right")
                                                    
                                                    # Segunda fila de animaciones
                                                    hbox:
                                                        spacing 8
                                                        xalign 0.5
                                                        
                                                        textbutton "🚶‍♀️→":
                                                            action Function(set_sprite_animation, "enter_right")
                                                            xsize 60
                                                            ysize 35
                                                            background "#3498db"
                                                            xalign 0.5
                                                            yalign 0.5
                                                            text_size 16
                                                            text_style "text_with_outline"
                                                            selected (sprite_animation == "enter_right")
                                                        
                                                        textbutton "←🚶‍♀️":
                                                            action Function(set_sprite_animation, "enter_left")
                                                            xsize 60
                                                            ysize 35
                                                            background "#3498db"
                                                            xalign 0.5
                                                            yalign 0.5
                                                            text_size 16
                                                            text_style "text_with_outline"
                                                            selected (sprite_animation == "enter_left")
                                                        
                                                        textbutton "⬆️🚶‍♀️":
                                                            action Function(set_sprite_animation, "enter_center")
                                                            xsize 60
                                                            ysize 35
                                                            background "#3498db"
                                                            xalign 0.5
                                                            yalign 0.5
                                                            text_size 16
                                                            text_style "text_with_outline"
                                                            selected (sprite_animation == "enter_center")
                                                    
                                                    # Botón para limpiar animación
                                                    textbutton "❌ Sin Animación":
                                                        action Function(set_sprite_animation, "none")
                                                        xminimum 120
                                                        ysize 50
                                                        padding (8, 5)
                                                        background "#95a5a6"
                                                        xalign 0.5
                                                        text_style "text_with_outline"
                                                        selected (sprite_animation == "none")
                                                
                                                # Controles de vista previa
                                                vbox:
                                                    spacing 8
                                                    xfill True
                                                    xalign 0.5
                                                    text "🎬 Acciones:" color "#ffffff" size 20 xalign 0.5 style "text_with_outline"
                                                    
                                                    textbutton "🔄 Reiniciar Vista":
                                                        action Function(reset_preview)
                                                        xminimum 140
                                                        ysize 50
                                                        padding (12, 8)
                                                        background "#27ae60"
                                                        xalign 0.5
                                                        text_style "text_with_outline"
                                                    
                                                    textbutton "📋 Ver Secuencia":
                                                        action Function(preview_scene_sequence)
                                                        xminimum 140
                                                        ysize 50
                                                        padding (12, 8)
                                                        background "#f39c12"
                                                        xalign 0.5
                                                        text_style "text_with_outline"
                                                    
                                                    textbutton "🎮 Cambiar Modo":
                                                        action Function(toggle_preview_mode)
                                                        xminimum 140
                                                        ysize 50
                                                        padding (12, 8)
                                                        background "#8e44ad"
                                                        xalign 0.5
                                                        text_style "text_with_outline"
                                                    
                                                    textbutton "💾 Guardar Escena":
                                                        action Function(save_scene_from_preview)
                                                        xminimum 140
                                                        ysize 50
                                                        padding (12, 8)
                                                        background "#27ae60"
                                                        xalign 0.5
                                                        text_style "text_with_outline"
                                                
                                                # Información de vista previa
                                                vbox:
                                                    spacing 6
                                                    xfill True
                                                    xalign 0.5
                                                    text "📊 Información:" color "#ffffff" size 20 xalign 0.5 style "text_with_outline"
                                                    
                                                    # Información en una sola columna para mejor visibilidad
                                                    vbox:
                                                        spacing 3
                                                        xalign 0.5
                                                        
                                                        text f"🎭 Personaje: {current_speaker or 'Ninguno'}" color "#3498db" size 18 xalign 0.5 style "text_with_outline"
                                                        text f"😊 Expresión: {current_expression or 'happy'}" color "#f39c12" size 18 xalign 0.5 style "text_with_outline"
                                                        text f"📍 Posición: {sprite_position or 'center'}" color "#e67e22" size 18 xalign 0.5 style "text_with_outline"
                                                        text f"🎬 Animación: {sprite_animation or 'none'}" color "#9b59b6" size 18 xalign 0.5 style "text_with_outline"
                                                        text f"🖼️ Fondo: {selected_background_global or 'Ninguno'}" color "#27ae60" size 18 xalign 0.5 style "text_with_outline"
                                                        text f"📋 Escenas: {len(current_scenes) if current_scenes else 0}" color "#e74c3c" size 18 xalign 0.5 style "text_with_outline"
                                                        text f"💬 Diálogo: {'Sí' if dialogue_text else 'No'}" color "#9b59b6" size 18 xalign 0.5 style "text_with_outline"
                                                        text f"🎮 Modo: {preview_mode or 'game'}" color "#1abc9c" size 18 xalign 0.5 style "text_with_outline" 
                                    
                                    # Panel de Transiciones
                                    python:
                                        try:
                                            # Calcular ancho dinámico según el contenido
                                            transitions_panel_width = 500  # Ancho optimizado para este panel
                                            
                                            # Calcular altura dinámica según el contenido
                                            # Altura base: título + espaciado
                                            base_height = 80
                                            
                                            # Altura por sección
                                            background_transitions_height = 80   # Transiciones de fondo
                                            character_transitions_height = 120   # Transiciones de personajes (2 filas)
                                            info_height = 80                     # Información de transiciones
                                            
                                            # Calcular altura total
                                            transitions_panel_height = (base_height + background_transitions_height + 
                                                                      character_transitions_height + info_height)
                                            
                                            # Altura mínima y máxima
                                            min_height = 250
                                            max_height = 400
                                            transitions_panel_height = max(min_height, min(transitions_panel_height, max_height))
                                            
                                        except:
                                            transitions_panel_width = 500
                                            transitions_panel_height = 300
                                    frame:
                                        xsize transitions_panel_width
                                        ysize transitions_panel_height
                                        background "#2c3e50"
                                        padding (20, 15)
                                        xalign 1.0
                                        yalign 0.0
                                        
                                        vbox:
                                            spacing 15
                                            xfill True
                                            xalign 0.5
                                            
                                            # Título centrado
                                            text "🎬 Panel de Transiciones" color "#ffffff" size text_sizes.title_medium xalign 0.5 style "title_with_outline"
                                            
                                            # Contenido del panel
                                            vbox:
                                                spacing 12
                                                xfill True
                                                xalign 0.5
                                                
                                                # Transiciones para fondos
                                                vbox:
                                                    spacing 8
                                                    xfill True
                                                    xalign 0.5
                                                    text "🖼️ Transiciones de Fondo:" color "#ffffff" size 18 xalign 0.5 style "text_with_outline"
                                                    
                                                    hbox:
                                                        spacing 10
                                                        xalign 0.5
                                                        
                                                        textbutton "🌅 Dissolve":
                                                            action Function(set_background_transition, "dissolve")
                                                            xsize 80
                                                            ysize 50
                                                            background "#3498db"
                                                            xalign 0.5
                                                            yalign 0.5
                                                            text_size 15
                                                            text_style "text_with_outline"
                                                            selected (background_transition == "dissolve")
                                                        
                                                        textbutton "⚡ Fade":
                                                            action Function(set_background_transition, "fade")
                                                            xsize 80
                                                            ysize 50
                                                            background "#3498db"
                                                            xalign 0.5
                                                            yalign 0.5
                                                            text_size 15
                                                            text_style "text_with_outline"
                                                            selected (background_transition == "fade")
                                                        
                                                        textbutton "🔄 Move":
                                                            action Function(set_background_transition, "move")
                                                            xsize 80
                                                            ysize 50
                                                            background "#3498db"
                                                            xalign 0.5
                                                            yalign 0.5
                                                            text_size 15
                                                            text_style "text_with_outline"
                                                            selected (background_transition == "move")
                                                
                                                # Transiciones para personajes
                                                vbox:
                                                    spacing 8
                                                    xfill True
                                                    xalign 0.5
                                                    text "👤 Transiciones de Personajes:" color "#ffffff" size 18 xalign 0.5 style "text_with_outline"
                                                    
                                                    hbox:
                                                        spacing 10
                                                        xalign 0.5
                                                        
                                                        textbutton "🌅 Dissolve":
                                                            action Function(set_character_transition, "dissolve")
                                                            xsize 80
                                                            ysize 50
                                                            background "#e67e22"
                                                            xalign 0.5
                                                            yalign 0.5
                                                            text_size 15
                                                            text_style "text_with_outline"
                                                            selected (character_transition == "dissolve")
                                                        
                                                        textbutton "⚡ Fade":
                                                            action Function(set_character_transition, "fade")
                                                            xsize 80
                                                            ysize 50
                                                            background "#e67e22"
                                                            xalign 0.5
                                                            yalign 0.5
                                                            text_size 15
                                                            text_style "text_with_outline"
                                                            selected (character_transition == "fade")
                                                        
                                                        textbutton "🔄 Move":
                                                            action Function(set_character_transition, "move")
                                                            xsize 80
                                                            ysize 50
                                                            background "#e67e22"
                                                            xalign 0.5
                                                            yalign 0.5
                                                            text_size 15
                                                            text_style "text_with_outline"
                                                            selected (character_transition == "move")
                                                    
                                                    hbox:
                                                        spacing 10
                                                        xalign 0.5
                                                        
                                                        textbutton "⬅️ MoveInLeft":
                                                            action Function(set_character_transition, "moveinleft")
                                                            xsize 100
                                                            ysize 50
                                                            background "#e67e22"
                                                            xalign 0.5
                                                            yalign 0.5
                                                            text_size 15
                                                            text_style "text_with_outline"
                                                            selected (character_transition == "moveinleft")
                                                        
                                                        textbutton "➡️ MoveInRight":
                                                            action Function(set_character_transition, "moveinright")
                                                            xsize 105
                                                            ysize 50
                                                            background "#e67e22"
                                                            xalign 0.5
                                                            yalign 0.5
                                                            text_size 15
                                                            text_style "text_with_outline"
                                                            selected (character_transition == "moveinright")
                                                        
                                                        textbutton "⬆️ MoveInBottom":
                                                            action Function(set_character_transition, "moveinbottom")
                                                            xsize 120
                                                            ysize 50
                                                            background "#e67e22"
                                                            xalign 0.5
                                                            yalign 0.5
                                                            text_size 15
                                                            text_style "text_with_outline"
                                                            selected (character_transition == "moveinbottom")
                                                
                                                # Información de transiciones
                                                vbox:
                                                    spacing 6
                                                    xfill True
                                                    xalign 0.5
                                                    text "📊 Transiciones Actuales:" color "#ffffff" size 20 xalign 0.5 style "text_with_outline"
                                                    
                                                    vbox:
                                                        spacing 3
                                                        xalign 0.5
                                                        
                                                        text f"🖼️ Fondo: {background_transition or 'dissolve'}" color "#27ae60" size 18 xalign 0.5 style "text_with_outline"
                                                        text f"👤 Personaje: {character_transition or 'dissolve'}" color "#e67e22" size 18 xalign 0.5 style "text_with_outline"
                                    
                                    # Panel de Configuración del Narrador
                                    python:
                                        try:
                                            # Calcular ancho dinámico según el contenido
                                            narrator_panel_width = 850  # Ancho optimizado para este panel
                                            
                                            # Calcular altura dinámica según el contenido
                                            # Altura base: título + espaciado
                                            base_height = 80
                                            
                                            # Altura por sección
                                            style_height = 60           # Estilo de narrador
                                            name_height = 80            # Nombre del narrador
                                            transition_height = 60      # Transición del narrador
                                            
                                            # Altura de posición (condicional)
                                            position_height = 0
                                            if narrator_style != "textbox":
                                                position_height = 300   # Controles de posición X/Y
                                            
                                            color_height = 60           # Color del texto
                                            size_height = 60            # Tamaño del texto
                                            text_field_height = 120     # Campo de texto del narrador
                                            action_buttons_height = 60  # Botones de acción
                                            
                                            # Calcular altura total
                                            narrator_panel_height = (base_height + style_height + name_height + 
                                                                   transition_height + position_height + color_height + 
                                                                   size_height + text_field_height + action_buttons_height)
                                            
                                            # Altura mínima y máxima
                                            min_height = 1000
                                            max_height = 1000
                                            narrator_panel_height = max(min_height, min(narrator_panel_height, max_height))
                                            
                                        except:
                                            narrator_panel_width = 850
                                            narrator_panel_height = 700
                                    frame:
                                        xsize narrator_panel_width
                                        ysize narrator_panel_height
                                        background "#34495e"
                                        padding (20, 15)
                                        xalign 0.5
                                        
                                        vbox:
                                            spacing 15
                                            xfill True
                                            xalign 0.5
                                            
                                            # Título centrado
                                            text "📖 Configuración del Narrador" color "#ffffff" size text_sizes.title_medium xalign 0.5 style "title_with_outline"
                                            
                                            # Contenido del panel
                                            vbox:
                                                spacing 12
                                                xfill True
                                                xalign 0.5
                                                
                                                # Estilo de narrador
                                                vbox:
                                                    spacing 8
                                                    xfill True
                                                    xalign 0.5
                                                    text "📝 Estilo de Narrador:" color "#ffffff" size 20 xalign 0.5
                                                    
                                                    hbox:
                                                        spacing 10
                                                        xalign 0.5
                                                        
                                                        textbutton "📋 Textbox":
                                                            action Function(set_narrator_style, "textbox")
                                                            xsize 100
                                                            ysize 35
                                                            background "#3498db"
                                                            xalign 0.5
                                                            yalign 0.5
                                                            text_size 15
                                                            text_style "text_with_outline"
                                                            selected (narrator_style == "textbox")
                                                        
                                                        textbutton "💬 Flotante":
                                                            action Function(set_narrator_style, "floating")
                                                            xsize 100
                                                            ysize 35
                                                            background "#3498db"
                                                            xalign 0.5
                                                            yalign 0.5
                                                            text_size 15
                                                            text_style "text_with_outline"
                                                            selected (narrator_style == "floating")
                                                        
                                                        textbutton "📜 Pantalla":
                                                            action Function(set_narrator_style, "screen")
                                                            xsize 100
                                                            ysize 35
                                                            background "#3498db"
                                                            xalign 0.5
                                                            yalign 0.5
                                                            text_size 14
                                                            text_style "text_with_outline"
                                                            selected (narrator_style == "screen")
                                                
                                                # Nombre personalizable del narrador
                                                vbox:
                                                    spacing 8
                                                    xfill True
                                                    xalign 0.5
                                                    text "🏷️ Nombre del Narrador:" color "#ffffff" size 20 xalign 0.5
                                                    
                                                    hbox:
                                                        spacing 10
                                                        xalign 0.5
                                                        
                                                        # Campo de nombre
                                                        frame:
                                                            xsize 300
                                                            ysize 35
                                                            background "#2c3e50"
                                                            padding (10, 5)
                                                            
                                                            if narrator_name_active:
                                                                input:
                                                                    value ScreenVariableInputValue("narrator_name")
                                                                    xfill True
                                                                    yfill True
                                                                    color "#ffffff"
                                                                    size text_sizes.text_medium
                                                                    default "Narrador"
                                                                    length 50
                                                            else:
                                                                text narrator_name color "#ffffff" size 20 xalign 0.5 yalign 0.5
                                                        
                                                        # Botón para activar edición
                                                        if not narrator_name_active:
                                                            textbutton "✏️ Editar":
                                                                action Function(activate_narrator_name_edit)
                                                                xsize 80
                                                                ysize 35
                                                                background "#3498db"
                                                                text_size 14
                                                                text_style "text_with_outline"
                                                        else:
                                                            # Botón para aceptar
                                                            textbutton "✅ Aceptar":
                                                                action Function(accept_narrator_name)
                                                                xsize 80
                                                                ysize 35
                                                                background "#27ae60"
                                                                text_size 12
                                                                text_style "text_with_outline"
                                                
                                                # Campo de fecha y hora (DESACTIVADO)
                                                # vbox:
                                                #     spacing 8
                                                #     xfill True
                                                #     xalign 0.5
                                                #     text "🕐 Fecha y Hora:" color "#ffffff" size text_sizes.text_medium xalign 0.5
                                                #     
                                                #     hbox:
                                                #         spacing 10
                                                #         xalign 0.5
                                                #         
                                                #         frame:
                                                #             xsize 200
                                                #             ysize 35
                                                #             background "#2c3e50"
                                                #             padding (10, 5)
                                                #             
                                                #             input:
                                                #                 value ScreenVariableInputValue("narrator_date_time")
                                                #                 xfill True
                                                #                 yfill True
                                                #                 color "#ffffff"
                                                #                 size text_sizes.text_medium
                                                #                 default ""
                                                #                 length 50
                                                #         
                                                #         textbutton "🕐 Ahora":
                                                #             action Function(lambda: renpy.set_screen_variable("narrator_date_time", get_current_datetime()))
                                                #             xsize 80
                                                #             ysize 35
                                                #             background "#f39c12"
                                                #             text_size 10
                                                
                                                # Campo de ubicación (DESACTIVADO)
                                                # vbox:
                                                #     spacing 8
                                                #     xfill True
                                                #     xalign 0.5
                                                #     text "📍 Ubicación:" color "#ffffff" size text_sizes.text_medium xalign 0.5
                                                #     
                                                #     hbox:
                                                #         spacing 10
                                                #         xalign 0.5
                                                #         
                                                #         frame:
                                                #             xsize 200
                                                #             ysize 35
                                                #             background "#2c3e50"
                                                #             padding (10, 5)
                                                #             
                                                #             input:
                                                #                 value ScreenVariableInputValue("narrator_location")
                                                #                 xfill True
                                                #                 yfill True
                                                #                 color "#ffffff"
                                                #                 size text_sizes.text_medium
                                                #                 default ""
                                                #                 length 50
                                                #         
                                                #         textbutton "📍 Ejemplo":
                                                #             action Function(lambda: renpy.set_screen_variable("narrator_location", "Sala de estar"))
                                                #             xsize 80
                                                #             ysize 35
                                                #             background "#27ae60"
                                                #             text_size 10
                                                
                                                # Transición del narrador
                                                vbox:
                                                    spacing 8
                                                    xfill True
                                                    xalign 0.5
                                                    text "🎬 Transición del Narrador:" color "#ffffff" size 20 xalign 0.5
                                                    
                                                    hbox:
                                                        spacing 10
                                                        xalign 0.5
                                                        
                                                        textbutton "🔄 Dissolve":
                                                            action Function(set_narrator_transition, "dissolve")
                                                            xsize 80
                                                            ysize 50
                                                            background "#e67e22"
                                                            text_size 15
                                                            text_style "text_with_outline"
                                                            selected (narrator_transition == "dissolve")
                                                        
                                                        textbutton "🌫️ Fade":
                                                            action Function(set_narrator_transition, "fade")
                                                            xsize 80
                                                            ysize 50
                                                            background "#e67e22"
                                                            text_size 15
                                                            text_style "text_with_outline"
                                                            selected (narrator_transition == "fade")
                                                        
                                                        textbutton "➡️ Move":
                                                            action Function(set_narrator_transition, "move")
                                                            xsize 80
                                                            ysize 50
                                                            background "#e67e22"
                                                            text_size 15
                                                            text_style "text_with_outline"
                                                            selected (narrator_transition == "move")
                                                
                                                # Posición del narrador (solo para estilos flotante y pantalla)
                                                if narrator_style != "textbox":
                                                    vbox:
                                                        spacing 8
                                                        xfill True
                                                        xalign 0.5
                                                        text "📍 Posición del Texto:" color "#ffffff" size 20 xalign 0.5
                                                        
                                                        # Control de posición X con botones
                                                        vbox:
                                                            spacing 5
                                                            xfill True
                                                            
                                                            hbox:
                                                                xfill True
                                                                spacing 10
                                                                
                                                                text "⬅️ X:" color "#ffffff" size 18
                                                                text f"{narrator_pos_x:.2f}" color "#f39c12" size 18
                                                                text "➡️" color "#ffffff" size 18
                                                            
                                                            # Barra visual de posición X
                                                            frame:
                                                                xfill True
                                                                ysize 25
                                                                background "#2c3e50"
                                                                padding (5, 5)
                                                                
                                                                # Barra de progreso X
                                                                frame:
                                                                    xsize (narrator_pos_x * (visual_layout.panel_width - 50))
                                                                    yfill True
                                                                    background "#3498db"
                                                                
                                                                # Indicador de posición X
                                                                frame:
                                                                    xsize 20
                                                                    ysize 20
                                                                    xpos (narrator_pos_x * (visual_layout.panel_width - 50) - 10)
                                                                    yalign 0.5
                                                                    background "#e74c3c"
                                                            
                                                            # Botones de control X
                                                            hbox:
                                                                spacing 5
                                                                xalign 0.5
                                                                
                                                                textbutton "◀◀":
                                                                    action Function(set_narrator_pos_x, max(0.0, narrator_pos_x - 0.2))
                                                                    xsize 30
                                                                    ysize 20
                                                                    background "#34495e"
                                                                    text_size 10
                                                                    text_style "text_with_outline"
                                                                
                                                                textbutton "◀":
                                                                    action Function(set_narrator_pos_x, max(0.0, narrator_pos_x - 0.1))
                                                                    xsize 30
                                                                    ysize 20
                                                                    background "#34495e"
                                                                    text_size 10
                                                                    text_style "text_with_outline"
                                                                
                                                                textbutton "▶":
                                                                    action Function(set_narrator_pos_x, min(1.0, narrator_pos_x + 0.1))
                                                                    xsize 30
                                                                    ysize 20
                                                                    background "#34495e"
                                                                    text_size 10
                                                                    text_style "text_with_outline"
                                                                
                                                                textbutton "▶▶":
                                                                    action Function(set_narrator_pos_x, min(1.0, narrator_pos_x + 0.2))
                                                                    xsize 30
                                                                    ysize 20
                                                                    background "#34495e"
                                                                    text_size 10
                                                                    text_style "text_with_outline"
                                                        
                                                        # Control de posición Y con botones
                                                        vbox:
                                                            spacing 5
                                                            xfill True
                                                            
                                                            hbox:
                                                                xfill True
                                                                spacing 10
                                                                
                                                                text "⬆️ Y:" color "#ffffff" size 18
                                                                text f"{narrator_pos_y:.2f}" color "#f39c12" size 18
                                                                text "⬇️" color "#ffffff" size 18
                                                            
                                                            # Barra visual de posición Y
                                                            frame:
                                                                xfill True
                                                                ysize 25
                                                                background "#2c3e50"
                                                                padding (5, 5)
                                                                
                                                                # Barra de progreso Y
                                                                frame:
                                                                    xsize (narrator_pos_y * (visual_layout.panel_width - 50))
                                                                    yfill True
                                                                    background "#27ae60"
                                                                
                                                                # Indicador de posición Y
                                                                frame:
                                                                    xsize 20
                                                                    ysize 20
                                                                    xpos (narrator_pos_y * (visual_layout.panel_width - 50) - 10)
                                                                    yalign 0.5
                                                                    background "#e74c3c"
                                                            
                                                            # Botones de control Y
                                                            hbox:
                                                                spacing 5
                                                                xalign 0.5
                                                                
                                                                textbutton "◀◀":
                                                                    action Function(set_narrator_pos_y, max(0.0, narrator_pos_y - 0.2))
                                                                    xsize 40
                                                                    ysize 20
                                                                    background "#34495e"
                                                                    text_size 18
                                                                    text_style "text_with_outline"
                                                                
                                                                textbutton "◀":
                                                                    action Function(set_narrator_pos_y, max(0.0, narrator_pos_y - 0.1))
                                                                    xsize 30
                                                                    ysize 20
                                                                    background "#34495e"
                                                                    text_size 18
                                                                    text_style "text_with_outline"
                                                                
                                                                textbutton "▶":
                                                                    action Function(set_narrator_pos_y, min(1.0, narrator_pos_y + 0.1))
                                                                    xsize 30
                                                                    ysize 20
                                                                    background "#34495e"
                                                                    text_size 18
                                                                    text_style "text_with_outline"
                                                                
                                                                textbutton "▶▶":
                                                                    action Function(set_narrator_pos_y, min(1.0, narrator_pos_y + 0.2))
                                                                    xsize 30
                                                                    ysize 20
                                                                    background "#34495e"
                                                                    text_size 18
                                                                    text_style "text_with_outline"
                                                        
                                                        # Botones de posiciones rápidas
                                                        vbox:
                                                            spacing 5
                                                            xfill True
                                                            
                                                            text "🎯 Posiciones Rápidas:" color "#ffffff" size 20 xalign 0.5
                                                            
                                                            hbox:
                                                                spacing 10
                                                                xalign 0.5
                                                                
                                                                textbutton "🎯 Centro":
                                                                    action [Function(set_narrator_pos_x, 0.5), Function(set_narrator_pos_y, 0.5)]
                                                                    xsize 80
                                                                    ysize 50
                                                                    background "#3498db"
                                                                    text_size 15
                                                                    text_style "text_with_outline"
                                                                
                                                                textbutton "🔄 Reset":
                                                                    action [Function(set_narrator_pos_x, 0.5), Function(set_narrator_pos_y, 0.5)]
                                                                    xsize 80
                                                                    ysize 50
                                                                    background "#e74c3c"
                                                                    text_size 15
                                                                    text_style "text_with_outline"
                                                
                                                # Color del texto
                                                vbox:
                                                    spacing 8
                                                    xfill True
                                                    xalign 0.5
                                                    text "🎨 Color del Texto:" color "#ffffff" size 20 xalign 0.5
                                                    
                                                    hbox:
                                                        spacing 10
                                                        xalign 0.5
                                                        
                                                        textbutton "⚪ Blanco":
                                                            action Function(set_narrator_color, "#ffffff")
                                                            xsize 80
                                                            ysize 50
                                                            background "#ffffff"
                                                            text_color "#000000"
                                                            xalign 0.5
                                                            yalign 0.5
                                                            text_size 15
                                                            text_style "text_with_outline"
                                                            selected (narrator_color == "#ffffff")
                                                        
                                                        textbutton "🟡 Amarillo":
                                                            action Function(set_narrator_color, "#f1c40f")
                                                            xsize 80
                                                            ysize 50
                                                            background "#f1c40f"
                                                            text_color "#000000"
                                                            xalign 0.5
                                                            yalign 0.5
                                                            text_size 15
                                                            text_style "text_with_outline"
                                                            selected (narrator_color == "#f1c40f")
                                                        
                                                        textbutton "🔵 Azul":
                                                            action Function(set_narrator_color, "#3498db")
                                                            xsize 80
                                                            ysize 50
                                                            background "#3498db"
                                                            text_color "#ffffff"
                                                            xalign 0.5
                                                            yalign 0.5
                                                            text_size 15
                                                            text_style "text_with_outline"
                                                            selected (narrator_color == "#3498db")
                                                        
                                                        textbutton "🟢 Verde":
                                                            action Function(set_narrator_color, "#27ae60")
                                                            xsize 80
                                                            ysize 50
                                                            background "#27ae60"
                                                            text_color "#ffffff"
                                                            xalign 0.5
                                                            yalign 0.5
                                                            text_size 15
                                                            text_style "text_with_outline"
                                                            selected (narrator_color == "#27ae60")
                                                
                                                # Tamaño del texto
                                                vbox:
                                                    spacing 8
                                                    xfill True
                                                    xalign 0.5
                                                    text "📏 Tamaño del Texto:" color "#ffffff" size 20 xalign 0.5
                                                    
                                                    hbox:
                                                        spacing 10
                                                        xalign 0.5
                                                        
                                                        textbutton "📝 Pequeño":
                                                            action Function(set_narrator_size, "small")
                                                            xsize 80
                                                            ysize 50
                                                            background "#95a5a6"
                                                            xalign 0.5
                                                            yalign 0.5
                                                            text_size 14
                                                            text_style "text_with_outline"
                                                            selected (narrator_size == "small")
                                                        
                                                        textbutton "📄 Mediano":
                                                            action Function(set_narrator_size, "medium")
                                                            xsize 80
                                                            ysize 50
                                                            background "#95a5a6"
                                                            xalign 0.5
                                                            yalign 0.5
                                                            text_size 14
                                                            text_style "text_with_outline"
                                                            selected (narrator_size == "medium")
                                                        
                                                        textbutton "📰 Grande":
                                                            action Function(set_narrator_size, "large")
                                                            xsize 80
                                                            ysize 50
                                                            background "#95a5a6"
                                                            xalign 0.5
                                                            yalign 0.5
                                                            text_size 14
                                                            text_style "text_with_outline"
                                                            selected (narrator_size == "large")
                                                
                                                # Campo de texto para narrador
                                                vbox:
                                                    spacing 8
                                                    xfill True
                                                    xalign 0.5
                                                    text "📝 Texto del Narrador:" color "#ffffff" size 20 xalign 0.5
                                                    
                                                    # Botón para activar el campo de texto
                                                    textbutton "✏️ Activar Campo de Texto":
                                                        action SetScreenVariable("narrator_text_active", True)
                                                        xminimum 200
                                                        ysize 50
                                                        padding (12, 8)
                                                        background "#3498db"
                                                        xalign 0.5
                                                        text_style "text_with_outline"
                                                    
                                                    # Campo de texto (solo visible cuando está activo)
                                                    if narrator_text_active:
                                                        frame:
                                                            xfill True
                                                            ysize 80
                                                            background "#2c3e50"
                                                            padding (10, 10)
                                                            
                                                            viewport:
                                                                xfill True
                                                                yfill True
                                                                scrollbars "vertical"
                                                                mousewheel True
                                                                
                                                                input:
                                                                    value ScreenVariableInputValue("narrator_text")
                                                                    xfill True
                                                                    yfill True
                                                                    color "#ffffff"
                                                                    size text_sizes.text_medium
                                                                    default ""
                                                                    length 500
                                                    else:
                                                        # Mensaje cuando no está activo
                                                        frame:
                                                            xfill True
                                                            ysize 80
                                                            background "#34495e"
                                                            padding (10, 10)
                                                            
                                                            text "Haz clic en '✏️ Activar Campo de Texto' para escribir" color "#95a5a6" size 20 xalign 0.5 yalign 0.5
                                                
                                                # Botones de acción para narrador
                                                hbox:
                                                    spacing 15
                                                    xalign 0.5
                                                    
                                                    textbutton "📝 Agregar Narrador":
                                                        action Function(add_narrator_to_scene)
                                                        xminimum 150
                                                        ysize 50
                                                        padding (12, 8)
                                                        background "#8e44ad"
                                                        text_style "text_with_outline"
                                                    
                                                    textbutton "🗑️ Limpiar":
                                                        action Function(clear_narrator_text)
                                                        xminimum 100
                                                        text_style "text_with_outline"
                                                        ysize 50
                                                        padding (12, 8)
                                                        background "#e74c3c"
                                                
                                                # Información de configuración
                                                vbox:
                                                    spacing 6
                                                    xfill True
                                                    xalign 0.5
                                                    text "📊 Configuración Actual:" color "#ffffff" size 20 xalign 0.5
                                                    
                                                    vbox:
                                                        spacing 3
                                                        xalign 0.5
                                                        
                                                        text f"📝 Estilo: {narrator_style or 'textbox'}" color "#3498db" size 18 xalign 0.5
                                                        if narrator_style != "textbox":
                                                            text f"📍 Posición: {narrator_position or 'center'}" color "#e67e22" size 18 xalign 0.5
                                                        text f"🎨 Color: {narrator_color or '#ffffff'}" color "#f1c40f" size 18 xalign 0.5
                                                        text f"📏 Tamaño: {narrator_size or 'medium'}" color "#95a5a6" size 18 xalign 0.5
                                    
                                    # PÁGINA 5: HERRAMIENTAS
                        elif current_panel_page == "tools":
                            viewport:
                                xsize visual_layout.editor_width - 60
                                ysize visual_layout.bottom_area_height - 70
                                scrollbars "vertical"
                                mousewheel True
                                xalign 0.5
                                
                                vbox:
                                    spacing 20
                                    xalign 0.5
                                    
                                    # Panel de Gestión de Proyectos
                                    frame:
                                        xminimum 400
                                        ysize 350
                                        background "#8e44ad"
                                        padding (20, 15)
                                        xalign 0.5
                                        
                                        vbox:
                                            spacing 15
                                            xfill True
                                            xalign 0.5
                                            
                                            # Título centrado
                                            text "💾 Gestión de Proyectos" color "#ffffff" size text_sizes.title_medium xalign 0.5 style "title_with_outline"
                                            
                                            # Contenido del panel
                                            vbox:
                                                spacing 12
                                                xfill True
                                                xalign 0.5
                                                
                                                # Botones de acción
                                                hbox:
                                                    spacing 15
                                                    xalign 0.5
                                                    
                                                    textbutton "💾 Guardar":
                                                        action Function(save_project_modal)
                                                        xminimum 100
                                                        ysize 50
                                                        padding (12, 8)
                                                        background "#27ae60"
                                                        xalign 0.5
                                                        text_style "text_with_outline"
                                                    
                                                    textbutton "💾 Sobrescribir":
                                                        action Function(overwrite_project_modal)
                                                        xminimum 100
                                                        ysize 50
                                                        padding (12, 8)
                                                        background "#f39c12"
                                                        xalign 0.5
                                                        text_style "text_with_outline"
                                                    
                                                    textbutton "📂 Cargar":
                                                        action Function(load_project_modal)
                                                        xminimum 100
                                                        ysize 50
                                                        padding (12, 8)
                                                        background "#3498db"
                                                        xalign 0.5
                                                        text_style "text_with_outline"
                                                    
                                                    textbutton "🗑️ Eliminar":
                                                        action Function(clear_project)
                                                        xminimum 100
                                                        ysize 50
                                                        padding (12, 8)
                                                        background "#e74c3c"
                                                        xalign 0.5
                                                        text_style "text_with_outline"
                                                    
                                                    textbutton "🔧 Arreglar":
                                                        action Function(fix_duplicate_labels)
                                                        xminimum 100
                                                        ysize 50
                                                        padding (12, 8)
                                                        background "#9b59b6"
                                                        xalign 0.5
                                                        text_style "text_with_outline"
                                                    
                                                    textbutton "🧹 Limpiar":
                                                        action Function(clear_current_editor)
                                                        xminimum 100
                                                        ysize 50
                                                        padding (12, 8)
                                                        background "#95a5a6"
                                                        xalign 0.5
                                                        text_style "text_with_outline"
                                                    
                                                    textbutton "🗑️ Limpiar No Guardadas":
                                                        action Function(cleanup_unsaved_scenes)
                                                        xminimum 120
                                                        ysize 50
                                                        padding (12, 8)
                                                        background "#e67e22"
                                                        xalign 0.5
                                                        text_style "text_with_outline"
                                    
                                    # Panel de Gestión de Recursos
                                    frame:
                                        xminimum 400
                                        ysize 180
                                        background "#8e44ad"
                                        padding (20, 15)
                                        xalign 0.5
                                        
                                        vbox:
                                            spacing 15
                                            xfill True
                                            xalign 0.5
                                            
                                            # Título centrado
                                            text "🖼️ Gestión de Recursos" color "#ffffff" size text_sizes.title_medium xalign 0.5 style "title_with_outline"
                                            
                                            # Contenido del panel
                                            vbox:
                                                spacing 12
                                                xfill True
                                                xalign 0.5
                                                
                                                # Botones de acción
                                                hbox:
                                                    spacing 15
                                                    xalign 0.5
                                                    
                                                    textbutton "📁 Importar Fondo":
                                                        action Function(import_background)
                                                        xminimum 120
                                                        ysize 50
                                                        padding (12, 8)
                                                        background "#9b59b6"
                                                        xalign 0.5
                                                        text_style "text_with_outline"
                                                    
                                                    textbutton "👤 Importar Sprite":
                                                        action Function(import_sprite)
                                                        xminimum 120
                                                        ysize 50
                                                        padding (12, 8)
                                                        background "#f39c12"
                                                        xalign 0.5
                                                        text_style "text_with_outline"
                                                    
                                                    textbutton "🔄 Recargar":
                                                        action Function(reload_resources)
                                                        xminimum 100
                                                        ysize 50
                                                        padding (12, 8)
                                                        background "#16a085"
                                                        xalign 0.5
                                                        text_style "text_with_outline"
                                    
                                    # Panel de Herramientas de Desarrollo
                                    frame:
                                        xminimum 400
                                        ysize 180
                                        background "#8e44ad"
                                        padding (20, 15)
                                        xalign 0.5
                                        
                                        vbox:
                                            spacing 15
                                            xfill True
                                            xalign 0.5
                                            
                                            # Título centrado
                                            text "🔧 Herramientas de Desarrollo" color "#ffffff" size text_sizes.title_medium xalign 0.5 style "title_with_outline"
                                            
                                            # Contenido del panel
                                            vbox:
                                                spacing 12
                                                xfill True
                                                xalign 0.5
                                                
                                                # Botones de acción
                                                hbox:
                                                    spacing 15
                                                    xalign 0.5
                                                    
                                                    textbutton "📊 Estadísticas":
                                                        action Function(show_statistics)
                                                        xminimum 100
                                                        ysize 50
                                                        padding (12, 8)
                                                        background "#8e44ad"
                                                        xalign 0.5
                                                        text_style "text_with_outline"
                                                    
                                                    textbutton "🔍 Debug":
                                                        action Function(debug_project)
                                                        xminimum 100
                                                        ysize 50
                                                        padding (12, 8)
                                                        background "#e67e22"
                                                        xalign 0.5
                                                        text_style "text_with_outline"
                                                    
                                                    textbutton "📝 Exportar":
                                                        action Function(export_script)
                                                        xminimum 100
                                                        ysize 50
                                                        padding (12, 8)
                                                        background "#2c3e50"
                                                        xalign 0.5
                                                        text_style "text_with_outline"
                                    
                                    # Panel de Configuración
                                    frame:
                                        xminimum 400
                                        ysize 150
                                        background "#8e44ad"
                                        padding (20, 15)
                                        xalign 0.5
                                        
                                        vbox:
                                            spacing 15
                                            xfill True
                                            xalign 0.5
                                            
                                            # Título centrado
                                            text "⚙️ Configuración" color "#ffffff" size text_sizes.title_medium xalign 0.5 style "title_with_outline"
                                            
                                            # Contenido del panel
                                            vbox:
                                                spacing 12
                                                xfill True
                                                xalign 0.5
                                                
                                                # Botones de acción
                                                hbox:
                                                    spacing 15
                                                    xalign 0.5
                                                    
                                                    textbutton "🎨 Layout":
                                                        action Function(open_layout_config)
                                                        xminimum 100
                                                        ysize 50
                                                        padding (12, 8)
                                                        background "#34495e"
                                                        xalign 0.5
                                                        text_style "text_with_outline"
                                                    
                                                    textbutton "💾 Config":
                                                        action Function(open_persistent_config)
                                                        xminimum 100
                                                        ysize 50
                                                        padding (12, 8)
                                                        background "#7f8c8d"
                                                        xalign 0.5
                                                        text_style "text_with_outline"
                                                    
                                                    textbutton "❌ Cerrar":
                                                        action Return()
                                                        xminimum 100
                                                        ysize 50
                                                        padding (12, 8)
                                                        background "#e74c3c"
                                                        xalign 0.5
                                                        text_style "text_with_outline"
                                    
                                    # Panel de Herramientas Avanzadas
                                    frame:
                                        xminimum 400
                                        ysize 180
                                        background "#8e44ad"
                                        padding (20, 15)
                                        xalign 0.5
                                        
                                        vbox:
                                            spacing 15
                                            xfill True
                                            xalign 0.5
                                            
                                            # Título centrado
                                            text "🔧 Herramientas Avanzadas" color "#ffffff" size text_sizes.title_medium xalign 0.5 style "title_with_outline"
                                            
                                            # Contenido del panel
                                            vbox:
                                                spacing 12
                                                xfill True
                                                xalign 0.5
                                                
                                                # Botones de acción
                                                hbox:
                                                    spacing 15
                                                    xalign 0.5
                                                    
                                                    textbutton "🔍 Diagnóstico":
                                                        action Function(show_diagnostic_tools)
                                                        xminimum 120
                                                        ysize 50
                                                        padding (12, 8)
                                                        background "#e67e22"
                                                        xalign 0.5
                                                        text_style "text_with_outline"
                                                    
                                                    textbutton "📁 Gestión Archivos":
                                                        action Function(show_file_management)
                                                        xminimum 140
                                                        ysize 50
                                                        padding (12, 8)
                                                        background "#8e44ad"
                                                        xalign 0.5
                                                        text_style "text_with_outline"
                                                    
                                                    textbutton "📤 Exportar Script":
                                                        action Function(export_script_advanced)
                                                        xminimum 120
                                                        ysize 50
                                                        padding (12, 8)
                                                        background "#2c3e50"
                                                        xalign 0.5
                                                        text_style "text_with_outline"
                                    
                                    # Panel de Proyectos
                                    frame:
                                        xminimum 400
                                        ysize 150
                                        background "#8e44ad"
                                        padding (20, 15)
                                        xalign 0.5
                                        
                                        vbox:
                                            spacing 15
                                            xfill True
                                            xalign 0.5
                                            
                                            # Título centrado
                                            text "📂 Gestión de Proyectos" color "#ffffff" size text_sizes.title_medium xalign 0.5 style "title_with_outline"
                                            
                                            # Contenido del panel
                                            vbox:
                                                spacing 12
                                                xfill True
                                                xalign 0.5
                                                
                                                # Botones de acción
                                                hbox:
                                                    spacing 15
                                                    xalign 0.5
                                                    
                                                    textbutton "🆕 Nuevo Proyecto":
                                                        action Function(save_project_modal)
                                                        xminimum 120
                                                        ysize 50
                                                        padding (12, 8)
                                                        background "#16a085"
                                                        xalign 0.5
                                                        text_style "text_with_outline"
                                                    
                                                    textbutton "📥 Cargar Script":
                                                        action Function(load_project_modal)
                                                        xminimum 120
                                                        ysize 50
                                                        padding (12, 8)
                                                        background "#9b59b6"
                                                        xalign 0.5
                                                        text_style "text_with_outline"
                                                    
                                                    textbutton "🗑️ Limpiar Todos":
                                                        action Function(clear_project)
                                                        xminimum 120
                                                        ysize 50
                                                        padding (12, 8)
                                                        background "#e74c3c"
                                                        xalign 0.5
                                                        text_style "text_with_outline"
            
            # Overlay de diseño (solo cuando está activado) - DESACTIVADO TEMPORALMENTE
            # if design_mode_active:
            #     use design_overlay
            
            # Botón de cerrar con verificación de cambios no guardados
            textbutton "❌":
                action Function(smart_exit_editor)
                xsize 150
                ysize 40
                background "#e74c3c"
                xalign 1.02
                yalign 0.0
                margin (20, 20)

# Pantalla para agregar opciones de choice (ELIMINADA - reemplazada por panel integrado)

# Funciones auxiliares para la pantalla
init python:
    from datetime import datetime
    
    def scroll_to_bottom():
        """Hace scroll automático hacia abajo en la lista de escenas"""
        try:
            # Forzar actualización de la pantalla para que el viewport se actualice
            # Esto asegura que la lista se muestre correctamente y el scroll funcione
            renpy.restart_interaction()
            
            # Nota: En Ren'Py, el scroll automático se maneja mejor con restart_interaction
            # que fuerza una actualización completa de la pantalla y permite que el viewport
            # se ajuste automáticamente al nuevo contenido
            
            # Opcional: También podemos intentar hacer scroll programático al viewport
            # pero restart_interaction es generalmente suficiente
        except Exception as e:
            print(f"⚠️ Error en scroll automático: {e}")
    
    def force_viewport_update():
        """Fuerza la actualización del viewport de manera más agresiva"""
        try:
            # Primera actualización
            renpy.restart_interaction()
            
            # Pequeña pausa para permitir que la pantalla se actualice
            import time
            time.sleep(0.1)
            
            # Segunda actualización para asegurar que el viewport se ajuste
            renpy.restart_interaction()
            
        except Exception as e:
            print(f"⚠️ Error en actualización forzada del viewport: {e}")
    
    def auto_scroll_to_bottom():
        """Función mejorada para scroll automático hacia abajo"""
        try:
            # Forzar actualización inmediata
            renpy.restart_interaction()
            
            # Usar un enfoque más directo para el scroll
            # En Ren'Py, a veces necesitamos múltiples actualizaciones
            renpy.restart_interaction()
            
            # Notificar al usuario que se ha hecho scroll
            renpy.notify("📜 Scroll automático aplicado")
            
        except Exception as e:
            print(f"⚠️ Error en scroll automático mejorado: {e}")
    
    def smart_scroll_update():
        """Función inteligente para actualización de scroll"""
        try:
            # Obtener la lista actual de escenas
            scenes = renpy.get_screen_variable("current_scenes")
            
            if scenes and len(scenes) > 1:
                # Si hay más de una escena, forzar scroll hacia abajo
                renpy.restart_interaction()
                
                # Pequeña pausa para permitir que la pantalla se actualice
                import time
                time.sleep(0.05)
                
                # Segunda actualización
                renpy.restart_interaction()
                
                # Notificar al usuario
                renpy.notify(f"📜 Scroll automático - {len(scenes)} escenas")
            else:
                # Si es la primera escena, solo actualizar
                renpy.restart_interaction()
                
        except Exception as e:
            print(f"⚠️ Error en scroll inteligente: {e}")
    
    def force_scroll_to_bottom():
        """Fuerza el scroll hacia abajo de manera más agresiva"""
        try:
            # Obtener la lista actual de escenas
            scenes = renpy.get_screen_variable("current_scenes")
            
            if scenes and len(scenes) > 1:
                # Forzar múltiples actualizaciones para asegurar el scroll
                for i in range(3):
                    renpy.restart_interaction()
                    import time
                    time.sleep(0.02)  # Pausa más corta pero múltiple
                
                # Notificar al usuario
                renpy.notify(f"📜 Scroll forzado - {len(scenes)} escenas")
            else:
                # Si es la primera escena, solo actualizar
                renpy.restart_interaction()
                
        except Exception as e:
            print(f"⚠️ Error en scroll forzado: {e}")
    
    def auto_scroll_with_delay():
        """Scroll automático con delay para permitir renderizado"""
        try:
            # Obtener la lista actual de escenas
            scenes = renpy.get_screen_variable("current_scenes")
            
            if scenes and len(scenes) > 1:
                # Primera actualización inmediata
                renpy.restart_interaction()
                
                # Delay más largo para permitir que se renderice
                import time
                time.sleep(0.1)
                
                # Segunda actualización
                renpy.restart_interaction()
                
                # Delay adicional
                time.sleep(0.05)
                
                # Tercera actualización final
                renpy.restart_interaction()
                
                # Notificar al usuario
                renpy.notify(f"📜 Scroll automático aplicado - {len(scenes)} escenas")
            else:
                # Si es la primera escena, solo actualizar
                renpy.restart_interaction()
                
        except Exception as e:
            print(f"⚠️ Error en scroll con delay: {e}")
    
    def simple_scroll_update():
        """Scroll simple sin delays que pueden causar problemas"""
        try:
            # Obtener la lista actual de escenas
            scenes = renpy.get_screen_variable("current_scenes")
            
            if scenes and len(scenes) > 1:
                # Múltiples actualizaciones rápidas sin delays
                renpy.restart_interaction()
                renpy.restart_interaction()
                renpy.restart_interaction()
                
                # Notificar al usuario
                renpy.notify(f"📜 Scroll aplicado - {len(scenes)} escenas")
            else:
                # Si es la primera escena, solo actualizar
                renpy.restart_interaction()
                
        except Exception as e:
            print(f"⚠️ Error en scroll simple: {e}")
    
    def immediate_scroll():
        """Scroll inmediato sin delays ni pausas"""
        try:
            # Obtener la lista actual de escenas
            scenes = renpy.get_screen_variable("current_scenes")
            
            if scenes and len(scenes) > 1:
                # Solo una actualización inmediata
                renpy.restart_interaction()
                
                # Notificar al usuario
                renpy.notify(f"📜 Scroll inmediato - {len(scenes)} escenas")
            else:
                # Si es la primera escena, solo actualizar
                renpy.restart_interaction()
                
        except Exception as e:
            print(f"⚠️ Error en scroll inmediato: {e}")
    
    def notify_new_scene():
        """Notifica al usuario sobre nueva escena agregada"""
        try:
            # Obtener la lista actual de escenas
            scenes = renpy.get_screen_variable("current_scenes")
            
            if scenes and len(scenes) > 1:
                # Notificar al usuario que hay nuevas escenas
                renpy.notify(f"📋 Nueva escena agregada - Total: {len(scenes)} escenas")
                renpy.notify("💡 Usa la rueda del mouse o arrastra para ver todas las escenas")
            else:
                # Si es la primera escena, solo notificar
                renpy.notify("📋 Primera escena agregada")
                
        except Exception as e:
            print(f"⚠️ Error en notificación: {e}")
    
    def force_viewport_update():
        """Fuerza la actualización del viewport de manera más agresiva"""
        try:
            # Obtener la lista actual de escenas
            scenes = renpy.get_screen_variable("current_scenes")
            
            if scenes and len(scenes) > 1:
                # Forzar múltiples actualizaciones
                for i in range(5):
                    renpy.restart_interaction()
                
                # Notificar al usuario
                renpy.notify(f"🔄 Viewport actualizado - {len(scenes)} escenas")
            else:
                # Si es la primera escena, solo actualizar
                renpy.restart_interaction()
                
        except Exception as e:
            print(f"⚠️ Error en actualización forzada: {e}")
    
    def simple_viewport_refresh():
        """Actualización simple del viewport sin forzar scroll"""
        try:
            # Obtener la lista actual de escenas
            scenes = renpy.get_screen_variable("current_scenes")
            
            if scenes and len(scenes) > 1:
                # Actualización simple
                renpy.restart_interaction()
                
                # Notificar al usuario
                renpy.notify(f"📋 Nueva escena agregada - Total: {len(scenes)} escenas")
                renpy.notify("💡 Usa la rueda del mouse para ver todas las escenas")
            else:
                # Si es la primera escena, solo actualizar
                renpy.restart_interaction()
                renpy.notify("📋 Primera escena agregada")
                
        except Exception as e:
            print(f"⚠️ Error en actualización simple: {e}")
    
    def add_background_to_scene():
        """Agrega un fondo a la escena actual"""
        try:
            # Obtener variables de la pantalla de forma segura
            bg_selected = renpy.get_screen_variable("selected_background_global")
            scenes = renpy.get_screen_variable("current_scenes")
            bg_transition = renpy.get_screen_variable("background_transition")
            current_scene_name = renpy.get_screen_variable("current_scene_name")
            
            # Verificar que haya una escena actual seleccionada
            if not current_scene_name:
                renpy.notify("⚠️ Primero crea o selecciona una escena")
                return
            
            # Si scenes es None, inicializar como lista vacía
            if scenes is None:
                scenes = []
            
            if bg_selected:
                scene_data = {
                    'type': 'background',
                    'background': bg_selected,
                    'transition': bg_transition or 'dissolve',
                    'timestamp': datetime.now().isoformat(),
                    'scene_name': current_scene_name  # Agregar referencia a la escena
                }
                scenes.append(scene_data)
                renpy.set_screen_variable("current_scenes", scenes)
                
                # Actualizar la escena en el diccionario de todas las escenas
                all_scenes = get_all_scenes_safe()
                all_scenes[current_scene_name] = scenes.copy()
                renpy.set_screen_variable("all_scenes", all_scenes)
                
                # Actualización simple del viewport
                simple_viewport_refresh()
                renpy.notify(f"✅ Fondo '{bg_selected}' agregado a escena '{current_scene_name}' con transición '{bg_transition or 'dissolve'}'")
            else:
                renpy.notify("⚠️ Selecciona un fondo primero")
        except Exception as e:
            renpy.notify(f"❌ Error agregando fondo: {e}")
    
    def add_character_to_scene():
        """Agrega un personaje a la escena actual"""
        try:
            # Obtener variables de la pantalla de forma segura
            character = renpy.get_screen_variable("current_speaker")
            expression = renpy.get_screen_variable("current_expression")
            position = renpy.get_screen_variable("sprite_position")
            scenes = renpy.get_screen_variable("current_scenes")
            char_transition = renpy.get_screen_variable("character_transition")
            current_scene_name = renpy.get_screen_variable("current_scene_name")
            
            # Verificar que haya una escena actual seleccionada
            if not current_scene_name:
                renpy.notify("⚠️ Primero crea o selecciona una escena")
                return
            
            # Si scenes is None, inicializar como lista vacía
            if scenes is None:
                scenes = []
            
            if character:
                scene_data = {
                    'type': 'character',
                    'character': character,
                    'expression': expression or 'happy',
                    'position': position or 'center',
                    'transition': char_transition or 'dissolve',
                    'timestamp': datetime.now().isoformat(),
                    'scene_name': current_scene_name  # Agregar referencia a la escena
                }
                scenes.append(scene_data)
                renpy.set_screen_variable("current_scenes", scenes)
                
                # Actualizar la escena en el diccionario de todas las escenas
                all_scenes = get_all_scenes_safe()
                all_scenes[current_scene_name] = scenes.copy()
                renpy.set_screen_variable("all_scenes", all_scenes)
                
                # Actualización simple del viewport
                simple_viewport_refresh()
                renpy.notify(f"✅ Personaje '{character}' agregado a escena '{current_scene_name}' con transición '{char_transition or 'dissolve'}'")
            else:
                renpy.notify("⚠️ Selecciona un personaje primero")
        except Exception as e:
            renpy.notify(f"❌ Error agregando personaje: {e}")
    
    def add_dialogue_to_scene():
        """Agrega un diálogo a la escena actual"""
        try:
            # Obtener variables de la pantalla de forma segura
            dialogue = renpy.get_screen_variable("dialogue_text")
            dialogue_char = renpy.get_screen_variable("dialogue_character")
            speaker = renpy.get_screen_variable("current_speaker")
            scenes = renpy.get_screen_variable("current_scenes")
            char_transition = renpy.get_screen_variable("character_transition")
            
            # Si scenes is None, inicializar como lista vacía
            if scenes is None:
                scenes = []
            
            # Si dialogue is None, inicializar como string vacío
            if dialogue is None:
                dialogue = ""
            
            # Determinar el personaje a usar
            character_to_use = dialogue_char or speaker or 'Narrator'
            
            # Si se seleccionó un personaje definido, obtener su nombre de visualización
            if dialogue_char:
                defined_chars = renpy.get_screen_variable("defined_characters")
                if defined_chars and dialogue_char in defined_chars:
                    char_def = defined_chars[dialogue_char]
                    display_name = char_def.get('display_name', dialogue_char)
                    character_to_use = display_name
            
            if dialogue.strip():
                # Determinar si es narrador y aplicar configuración especial
                is_narrator = character_to_use == 'Narrator' or character_to_use == 'narrator'
                
                # Obtener el nombre de la escena actual
                current_scene_name = renpy.get_screen_variable("current_scene_name")
                if not current_scene_name:
                    renpy.notify("⚠️ Primero crea o selecciona una escena")
                    return
                
                scene_data = {
                    'type': 'dialogue',
                    'character': character_to_use,
                    'dialogue': dialogue.strip(),
                    'scene_name': current_scene_name,  # Agregar referencia a la escena
                    'transition': char_transition or 'dissolve',
                    'timestamp': datetime.now().isoformat()
                }
                
                # Agregar configuración del narrador si es narrador
                if is_narrator:
                    scene_data.update({
                        'narrator_style': renpy.get_screen_variable("narrator_style") or 'textbox',
                        'narrator_position': renpy.get_screen_variable("narrator_position") or 'center',
                        'narrator_color': renpy.get_screen_variable("narrator_color") or '#ffffff',
                        'narrator_size': renpy.get_screen_variable("narrator_size") or 'medium'
                    })
                scenes.append(scene_data)
                renpy.set_screen_variable("current_scenes", scenes)
                
                # Actualizar la escena en el diccionario de todas las escenas
                all_scenes = get_all_scenes_safe()
                all_scenes[current_scene_name] = scenes.copy()
                renpy.set_screen_variable("all_scenes", all_scenes)
                
                renpy.set_screen_variable("dialogue_text", "")  # Limpiar el campo
                # Actualización simple del viewport
                simple_viewport_refresh()
                renpy.notify(f"✅ Diálogo agregado a escena '{current_scene_name}': {character_to_use} con transición '{char_transition or 'dissolve'}'")
            else:
                renpy.notify("⚠️ Escribe un diálogo primero")
        except Exception as e:
            renpy.notify(f"❌ Error agregando diálogo: {e}")
    
    def clear_background_selection():
        """Limpia la selección de fondo"""
        renpy.set_screen_variable("selected_background_global", None)
        renpy.notify("✅ Selección de fondo limpiada")
    
    def edit_scene(index):
        """Edita una escena específica"""
        try:
            scenes = renpy.get_screen_variable("current_scenes")
            if scenes is None:
                scenes = []
            
            if 0 <= index < len(scenes):
                renpy.notify(f"✏️ Editando escena {index + 1}")
            else:
                renpy.notify("❌ Índice de escena inválido")
        except Exception as e:
            renpy.notify(f"❌ Error editando escena: {e}")
    
    def delete_scene(index):
        """Elimina una escena específica"""
        try:
            scenes = renpy.get_screen_variable("current_scenes")
            if scenes is None:
                scenes = []
            
            if 0 <= index < len(scenes):
                deleted_scene = scenes.pop(index)
                renpy.set_screen_variable("current_scenes", scenes)
                renpy.notify(f"🗑️ Escena {index + 1} eliminada")
            else:
                renpy.notify("❌ Índice de escena inválido")
        except Exception as e:
            renpy.notify(f"❌ Error eliminando escena: {e}")
    
    # Funciones eliminadas - reemplazadas por el nuevo sistema de gestión de proyectos
    
    # ===== NUEVAS FUNCIONES DE HERRAMIENTAS =====
    
    def import_background():
        """Importa un fondo desde un archivo"""
        try:
            from resource_manager import import_image_to_backgrounds
            success = import_image_to_backgrounds()
            if success:
                renpy.notify("✅ Fondo importado exitosamente")
            else:
                renpy.notify("⚠️ No se pudo importar el fondo")
        except Exception as e:
            renpy.notify(f"❌ Error importando fondo: {e}")
    
    def import_sprite():
        """Importa un sprite desde un archivo"""
        try:
            from resource_manager import import_sprite_to_character
            success = import_sprite_to_character()
            if success:
                renpy.notify("✅ Sprite importado exitosamente")
            else:
                renpy.notify("⚠️ No se pudo importar el sprite")
        except Exception as e:
            renpy.notify(f"❌ Error importando sprite: {e}")
    
    def reload_resources():
        """Recarga los recursos del editor"""
        try:
            from resource_manager import define_background_images, define_character_sprites
            define_background_images()
            define_character_sprites()
            renpy.notify("🔄 Recursos recargados exitosamente")
        except Exception as e:
            renpy.notify(f"❌ Error recargando recursos: {e}")
    
    def show_statistics():
        """Muestra estadísticas del proyecto"""
        try:
            scenes = renpy.get_screen_variable("current_scenes")
            if scenes is None:
                scenes = []
            
            dialogue_count = len([s for s in scenes if s.get('type') == 'dialogue'])
            background_count = len([s for s in scenes if s.get('type') == 'background'])
            
            stats_text = f"📊 Estadísticas del Proyecto:\n"
            stats_text += f"• Total de escenas: {len(scenes)}\n"
            stats_text += f"• Diálogos: {dialogue_count}\n"
            stats_text += f"• Fondos: {background_count}\n"
            
            renpy.notify(stats_text)
        except Exception as e:
            renpy.notify(f"❌ Error mostrando estadísticas: {e}")
    
    def debug_project():
        """Ejecuta debug del proyecto"""
        try:
            # Debug del sistema de proyectos actual
            projects = getattr(renpy.store, 'available_projects', [])
            current_scenes = getattr(renpy.store, 'current_scenes', [])
            
            debug_info = f"🔍 Debug del Sistema de Proyectos:\n"
            debug_info += f"• Proyectos disponibles: {len(projects)}\n"
            debug_info += f"• Escenas actuales: {len(current_scenes)}\n"
            debug_info += f"• Escena actual: {getattr(renpy.store, 'current_scene_name', 'Ninguna')}"
            
            print(debug_info)
            renpy.notify("🔍 Debug ejecutado, revisa la consola")
        except Exception as e:
            renpy.notify(f"❌ Error en debug: {e}")
        except Exception as e:
            renpy.notify(f"❌ Error en debug: {e}")
    
    # ===== FUNCIONES DE GESTIÓN DE ESCENAS MÚLTIPLES =====
    
    def create_new_scene():
        """Crea una nueva escena con nombre"""
        try:
            scene_name = renpy.get_screen_variable("new_scene_name")
            if scene_name and scene_name.strip():
                scene_name = scene_name.strip()
                
                # Verificar que el nombre no exista
                all_scenes = get_all_scenes_safe()
                
                if scene_name in all_scenes:
                    renpy.notify("⚠️ Ya existe una escena con ese nombre")
                    return
                
                # Crear nueva escena
                all_scenes[scene_name] = []
                renpy.set_screen_variable("all_scenes", all_scenes)
                renpy.set_screen_variable("current_scene_name", scene_name)
                renpy.set_screen_variable("current_scenes", [])
                renpy.set_screen_variable("new_scene_name", "")
                renpy.set_screen_variable("scene_creation_mode", False)
                renpy.set_screen_variable("new_scene_name_active", False)
                
                # Debug: verificar que se guardó correctamente
                saved_scenes = get_all_scenes_safe()
                print(f"🔍 Debug: Escenas después de crear '{scene_name}': {list(saved_scenes.keys())}")
                
                # Organizar automáticamente las escenas para la nueva escena
                organize_scenes_by_current()
                
                renpy.notify(f"✅ Nueva escena '{scene_name}' creada y organizada")
            else:
                renpy.notify("⚠️ Ingresa un nombre para la escena")
        except Exception as e:
            renpy.notify(f"❌ Error creando escena: {e}")
            print(f"🔍 Debug: Error completo: {e}")
    
    def select_scene_to_edit():
        """Selecciona una escena para editar"""
        try:
            scene_name = renpy.get_screen_variable("selected_scene_to_edit")
            if scene_name:
                all_scenes = get_all_scenes_safe()
                
                if scene_name in all_scenes:
                    # Cargar la escena seleccionada
                    renpy.set_screen_variable("current_scene_name", scene_name)
                    renpy.set_screen_variable("current_scenes", all_scenes[scene_name])
                    renpy.set_screen_variable("selected_scene_to_edit", "")
                    
                    # Debug: verificar que se cargó correctamente
                    print(f"🔍 Debug: Cargando escena '{scene_name}' con {len(all_scenes[scene_name])} elementos")
                    
                    # Organizar automáticamente las escenas para la escena seleccionada
                    organize_scenes_by_current()
                    
                    renpy.notify(f"📝 Editando escena: '{scene_name}' - Organizada")
                else:
                    renpy.notify("⚠️ Escena no encontrada")
                    print(f"🔍 Debug: Escena '{scene_name}' no encontrada en {list(all_scenes.keys())}")
            else:
                renpy.notify("⚠️ Selecciona una escena para editar")
        except Exception as e:
            renpy.notify(f"❌ Error seleccionando escena: {e}")
            print(f"🔍 Debug: Error completo: {e}")
    
    def save_current_scene():
        """Guarda la escena actual en el diccionario de escenas"""
        try:
            current_name = renpy.get_screen_variable("current_scene_name")
            current_scenes = renpy.get_screen_variable("current_scenes")
            
            if current_name and current_scenes is not None:
                all_scenes = get_all_scenes_safe()
                
                all_scenes[current_name] = current_scenes.copy()
                renpy.set_screen_variable("all_scenes", all_scenes)
                
                # Debug: verificar que se guardó correctamente
                saved_scenes = get_all_scenes_safe()
                print(f"🔍 Debug: Escenas después de guardar '{current_name}': {list(saved_scenes.keys())}")
                
                renpy.notify(f"💾 Escena '{current_name}' guardada")
            else:
                renpy.notify("⚠️ No hay escena activa para guardar")
        except Exception as e:
            renpy.notify(f"❌ Error guardando escena: {e}")
            print(f"🔍 Debug: Error completo: {e}")
    
    def delete_scene_by_name():
        """Elimina una escena del diccionario por nombre"""
        try:
            scene_name = renpy.get_screen_variable("selected_scene_to_edit")
            if scene_name:
                all_scenes = renpy.get_screen_variable("all_scenes")
                if all_scenes is None:
                    all_scenes = {}
                
                if scene_name in all_scenes:
                    del all_scenes[scene_name]
                    renpy.set_screen_variable("all_scenes", all_scenes)
                    renpy.set_screen_variable("selected_scene_to_edit", "")
                    
                    # Si la escena eliminada era la actual, limpiar
                    current_name = renpy.get_screen_variable("current_scene_name")
                    if current_name == scene_name:
                        renpy.set_screen_variable("current_scene_name", "")
                        renpy.set_screen_variable("current_scenes", [])
                    
                    renpy.notify(f"🗑️ Escena '{scene_name}' eliminada")
                else:
                    renpy.notify("⚠️ Escena no encontrada")
            else:
                renpy.notify("⚠️ Selecciona una escena para eliminar")
        except Exception as e:
            renpy.notify(f"❌ Error eliminando escena: {e}")
    
    def export_all_scenes():
        """Exporta todas las escenas a un script Ren'Py"""
        try:
            all_scenes = renpy.get_screen_variable("all_scenes")
            if all_scenes is None or not all_scenes:
                renpy.notify("⚠️ No hay escenas para exportar")
                return
            
            # Generar código Ren'Py
            script_content = "# Script generado por el Editor Visual\n\n"
            script_content += "label start:\n"
            
            for scene_name, scenes in all_scenes.items():
                script_content += f"\n    # === ESCENA: {scene_name} ===\n"
                
                for scene in scenes:
                    if scene.get('type') == 'background':
                        script_content += f"    scene {scene.get('background', 'bg room')}\n"
                    elif scene.get('type') == 'dialogue':
                        character = scene.get('character', 'narrator')
                        dialogue = scene.get('dialogue', '')
                        script_content += f"    {character} \"{dialogue}\"\n"
                    elif scene.get('type') == 'label':
                        label_name = scene.get('label_name', '')
                        script_content += f"\nlabel {label_name}:\n"
                    elif scene.get('type') == 'jump':
                        jump_target = scene.get('jump_target', '')
                        script_content += f"    jump {jump_target}\n"
                    elif scene.get('type') == 'choice':
                        question = scene.get('question', '')
                        options = scene.get('options', [])
                        
                        script_content += f"    menu:\n"
                        script_content += f"        \"{question}\"\n"
                        
                        for option in options:
                            option_text = option.get('text', '')
                            option_jump = option.get('jump', '')
                            script_content += f"        \"{option_text}\":\n"
                            script_content += f"            jump {option_jump}\n"
            
            # Guardar archivo (simulado)
            renpy.notify(f"📄 Script exportado con {len(all_scenes)} escenas")
            print("=== SCRIPT EXPORTADO ===")
            print(script_content)
            print("========================")
            
        except Exception as e:
            renpy.notify(f"❌ Error exportando escenas: {e}")
    
    def export_script():
        """Exporta el script a un archivo .rpy"""
        try:
            scenes = renpy.get_screen_variable("current_scenes")
            if scenes is None:
                scenes = []
            
            if not scenes:
                renpy.notify("⚠️ No hay escenas para exportar")
                return
            
            # Generar código Ren'Py básico
            script_content = "# Script generado por el Editor Visual\n\n"
            script_content += "label start:\n"
            
            for i, scene in enumerate(scenes):
                if scene.get('type') == 'background':
                    script_content += f"    scene {scene.get('background', 'bg room')}\n"
                elif scene.get('type') == 'dialogue':
                    character = scene.get('character', 'narrator')
                    dialogue = scene.get('dialogue', '')
                    script_content += f"    {character} \"{dialogue}\"\n"
                elif scene.get('type') == 'label':
                    label_name = scene.get('label_name', '')
                    script_content += f"\nlabel {label_name}:\n"
                elif scene.get('type') == 'jump':
                    jump_target = scene.get('jump_target', '')
                    script_content += f"    jump {jump_target}\n"
                elif scene.get('type') == 'choice':
                    question = scene.get('question', '')
                    options = scene.get('options', [])
                    
                    script_content += f"    menu:\n"
                    script_content += f"        \"{question}\"\n"
                    
                    for option in options:
                        if isinstance(option, dict):
                            option_text = option.get('text', 'Opción')
                            option_jump = option.get('jump')
                            if option_jump:
                                script_content += f"        \"{option_text}\":\n"
                                script_content += f"            jump {option_jump}\n"
                            else:
                                script_content += f"        \"{option_text}\":\n"
                                script_content += f"            pass\n"
                        else:
                            # Fallback para opciones antiguas (strings)
                            script_content += f"        \"{option}\":\n"
                            script_content += f"            pass\n"
                    
                    script_content += "\n"
            
            # Guardar archivo
            import os
            script_path = os.path.join(renpy.config.gamedir, "generated_script.rpy")
            with open(script_path, 'w', encoding='utf-8') as f:
                f.write(script_content)
            
            renpy.notify(f"✅ Script exportado a: {script_path}")
        except Exception as e:
            renpy.notify(f"❌ Error exportando script: {e}")
    
    def open_layout_config():
        """Abre el configurador de layout"""
        try:
            renpy.show_screen("layout_configurator")
            renpy.notify("🎨 Configurador de layout abierto")
        except Exception as e:
            renpy.notify(f"❌ Error abriendo configurador: {e}")
    
    def open_persistent_config():
        """Abre el configurador persistente"""
        try:
            renpy.show_screen("persistent_config_screen")
            renpy.notify("💾 Configurador persistente abierto")
        except Exception as e:
            renpy.notify(f"❌ Error abriendo configurador: {e}")
    
    # ===== FUNCIONES AVANZADAS DEL EDITOR ORIGINAL =====
    
    def show_diagnostic_tools():
        """Muestra herramientas de diagnóstico"""
        try:
            scenes = renpy.get_screen_variable("current_scenes")
            if scenes is None:
                scenes = []
            
            diagnostic_info = "🔍 Diagnóstico del Sistema:\n"
            diagnostic_info += f"• Directorio del juego: {renpy.config.gamedir}\n"
            diagnostic_info += f"• Escenas actuales: {len(scenes)}\n"
            diagnostic_info += f"• Fondos disponibles: {len(get_available_backgrounds())}\n"
            diagnostic_info += f"• Personajes disponibles: {len(editor_character_list)}\n"
            
            renpy.notify(diagnostic_info)
        except Exception as e:
            renpy.notify(f"❌ Error en diagnóstico: {e}")
    
    def show_file_management():
        """Muestra herramientas de gestión de archivos"""
        try:
            import os
            file_info = "📁 Gestión de Archivos:\n"
            file_info += f"• Directorio actual: {os.getcwd()}\n"
            file_info += f"• Archivos en game/: {len(os.listdir(renpy.config.gamedir))}\n"
            file_info += f"• Archivos en images/: {len(os.listdir(os.path.join(renpy.config.gamedir, 'images')))}"
            
            renpy.notify(file_info)
        except Exception as e:
            renpy.notify(f"❌ Error en gestión de archivos: {e}")
    
    def export_script_advanced():
        """Exporta el script con formato avanzado"""
        try:
            scenes = renpy.get_screen_variable("current_scenes")
            if scenes is None:
                scenes = []
            
            if not scenes:
                renpy.notify("⚠️ No hay escenas para exportar")
                return
            
            # Generar código Ren'Py avanzado
            script_content = "# Script generado por el Editor Visual Avanzado\n"
            script_content += "# Fecha: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n\n"
            
            # Referencia a archivo de personajes
            script_content += "# Importar definiciones de personajes\n"
            script_content += "# Asegúrate de que el archivo 'characters.rpy' esté en la carpeta del proyecto\n"
            script_content += "# Si no existe, genera el archivo desde el panel de personajes\n\n"
            
            # Definir personajes (fallback si no existe el archivo)
            characters_used = set()
            for scene in scenes:
                if scene.get('type') == 'dialogue':
                    characters_used.add(scene.get('character', 'narrator'))
            
            script_content += "# Definiciones de personajes (fallback)\n"
            defined_chars = renpy.get_screen_variable("defined_characters")
            if defined_chars is None:
                defined_chars = {}
            
            for char in characters_used:
                if char in defined_chars:
                    # Usar definición personalizada
                    char_def = defined_chars[char]
                    display_name = char_def.get('display_name', char)
                    color = char_def.get('color', '#c8ffc8')
                    char_type = char_def.get('type', 'normal')
                    
                    if char_type == 'narrator':
                        script_content += f"define {char} = Character(None, kind=nvl)\n"
                    else:
                        script_content += f"define {char} = Character('{display_name}', color='{color}')\n"
                else:
                    # Definición por defecto
                    script_content += f"define {char} = Character('{char}')\n"
            script_content += "\n"
            
            # Definir imágenes
            backgrounds_used = set()
            for scene in scenes:
                if scene.get('type') == 'background':
                    backgrounds_used.add(scene.get('background', 'bg room'))
            
            script_content += "# Definición de imágenes\n"
            for bg in backgrounds_used:
                script_content += f"image {bg} = \"images/backgrounds/{bg}.png\"\n"
            script_content += "\n"
            
            # Script principal
            script_content += "label start:\n"
            for i, scene in enumerate(scenes):
                if scene.get('type') == 'background':
                    script_content += f"    scene {scene.get('background', 'bg room')}\n"
                elif scene.get('type') == 'dialogue':
                    character = scene.get('character', 'narrator')
                    dialogue = scene.get('dialogue', '')
                    script_content += f"    {character} \"{dialogue}\"\n"
                elif scene.get('type') == 'label':
                    label_name = scene.get('label_name', '')
                    script_content += f"\nlabel {label_name}:\n"
                elif scene.get('type') == 'jump':
                    jump_target = scene.get('jump_target', '')
                    script_content += f"    jump {jump_target}\n"
                elif scene.get('type') == 'choice':
                    question = scene.get('question', '')
                    options = scene.get('options', [])
                    
                    script_content += f"    menu:\n"
                    script_content += f"        \"{question}\"\n"
                    
                    for option in options:
                        if isinstance(option, dict):
                            option_text = option.get('text', 'Opción')
                            option_jump = option.get('jump')
                            if option_jump:
                                script_content += f"        \"{option_text}\":\n"
                                script_content += f"            jump {option_jump}\n"
                            else:
                                script_content += f"        \"{option_text}\":\n"
                                script_content += f"            pass\n"
                        else:
                            # Fallback para opciones antiguas (strings)
                            script_content += f"        \"{option}\":\n"
                            script_content += f"            pass\n"
                    
                    script_content += "\n"
            
            # Guardar archivo
            import os
            script_path = os.path.join(renpy.config.gamedir, "generated_script_advanced.rpy")
            with open(script_path, 'w', encoding='utf-8') as f:
                f.write(script_content)
            
            renpy.notify(f"✅ Script avanzado exportado a: {script_path}")
        except Exception as e:
            renpy.notify(f"❌ Error exportando script avanzado: {e}")
    
    def create_new_project():
        """Crea un nuevo proyecto"""
        try:
            renpy.set_screen_variable("current_scenes", [])
            renpy.set_screen_variable("selected_background_global", None)
            renpy.set_screen_variable("current_speaker", None)
            renpy.set_screen_variable("dialogue_text", "")
            renpy.notify("🆕 Nuevo proyecto creado")
        except Exception as e:
            renpy.notify(f"❌ Error creando proyecto: {e}")
    
    def load_script_advanced():
        """Carga un script avanzado"""
        try:
            import os
            script_path = os.path.join(renpy.config.gamedir, "generated_script_advanced.rpy")
            if os.path.exists(script_path):
                with open(script_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                renpy.notify(f"✅ Script cargado: {len(content)} caracteres")
            else:
                renpy.notify("⚠️ No se encontró script avanzado")
        except Exception as e:
            renpy.notify(f"❌ Error cargando script: {e}")
    
    def clear_all_projects():
        """Limpia todos los proyectos"""
        try:
            renpy.set_screen_variable("current_scenes", [])
            renpy.set_screen_variable("selected_background_global", None)
            renpy.set_screen_variable("current_speaker", None)
            renpy.set_screen_variable("dialogue_text", "")
            renpy.notify("🗑️ Todos los proyectos limpiados")
        except Exception as e:
            renpy.notify(f"❌ Error limpiando proyectos: {e}")
    
    def get_available_backgrounds():
        """Obtiene la lista de fondos disponibles"""
        try:
            import os
            backgrounds_path = os.path.join(renpy.config.gamedir, "images", "backgrounds")
            if os.path.isdir(backgrounds_path):
                backgrounds = []
                for item in os.listdir(backgrounds_path):
                    if any(item.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.webp']):
                        backgrounds.append(item)
                return backgrounds
            return []
        except Exception as e:
            print(f"Error obteniendo fondos: {e}")
            return []
    
    # ===== FUNCIONES PARA VISTA PREVIA EN TIEMPO REAL =====
    
    def get_character_expressions(character_name):
        """Obtiene las expresiones disponibles para un personaje"""
        try:
            import os
            character_path = os.path.join(renpy.config.gamedir, "images", "character", character_name.lower())
            if os.path.isdir(character_path):
                expressions = []
                for item in os.listdir(character_path):
                    if item.lower().endswith('.png'):
                        expressions.append(item.replace('.png', ''))
                return expressions
            return ['happy']  # Expresión por defecto
        except Exception as e:
            print(f"Error obteniendo expresiones: {e}")
            return ['happy']
    
    def get_current_character_sprite():
        """Obtiene el sprite actual del personaje para la vista previa"""
        try:
            speaker = renpy.get_screen_variable("current_speaker")
            if not speaker:
                return None
            
            # Obtener expresión actual (por defecto 'happy')
            current_expression = renpy.get_screen_variable("current_expression")
            if not current_expression:
                current_expression = "happy"
            
            # Construir ruta del sprite
            sprite_path = f"images/character/{speaker.lower()}/{current_expression}.png"
            
            # Verificar si existe
            if renpy.loadable(sprite_path):
                return sprite_path
            else:
                # Intentar con expresión por defecto
                default_path = f"images/character/{speaker.lower()}/happy.png"
                if renpy.loadable(default_path):
                    return default_path
            
            return None
        except Exception as e:
            print(f"Error obteniendo sprite: {e}")
            return None
    
    def set_character_expression(expression):
        """Establece la expresión del personaje actual"""
        try:
            renpy.set_screen_variable("current_expression", expression)
            renpy.notify(f"😊 Expresión cambiada a: {expression}")
        except Exception as e:
            renpy.notify(f"❌ Error cambiando expresión: {e}")
    
    def preview_scene_sequence():
        """Muestra una vista previa de la secuencia de escenas"""
        try:
            scenes = renpy.get_screen_variable("current_scenes")
            if not scenes:
                renpy.notify("⚠️ No hay escenas para previsualizar")
                return
            
            # Mostrar información de la secuencia
            sequence_info = "🎬 Secuencia de Escenas:\n"
            for i, scene in enumerate(scenes):
                if scene.get('type') == 'background':
                    sequence_info += f"{i+1}. 🖼️ Fondo: {scene.get('background')}\n"
                elif scene.get('type') == 'dialogue':
                    sequence_info += f"{i+1}. 💬 {scene.get('character')}: \"{scene.get('dialogue')[:50]}...\"\n"
            
            renpy.notify(sequence_info)
        except Exception as e:
            renpy.notify(f"❌ Error previsualizando secuencia: {e}")
    
    def toggle_preview_mode():
        """Alterna entre modos de vista previa"""
        try:
            current_mode = renpy.get_screen_variable("preview_mode")
            if current_mode == "game":
                renpy.set_screen_variable("preview_mode", "editor")
                renpy.notify("📝 Modo editor activado")
            else:
                renpy.set_screen_variable("preview_mode", "game")
                renpy.notify("🎮 Modo juego activado")
        except Exception as e:
            renpy.notify(f"❌ Error cambiando modo: {e}")
    
    def reset_preview():
        """Reinicia la vista previa"""
        try:
            renpy.set_screen_variable("current_expression", "happy")
            renpy.notify("🔄 Vista previa reiniciada")
        except Exception as e:
            renpy.notify(f"❌ Error reiniciando vista previa: {e}")
    
    def define_character_in_script(character_name):
        """Define un personaje en el script con sus propiedades"""
        try:
            # Obtener valores del panel
            display_name = renpy.get_screen_variable("character_display_name")
            color = renpy.get_screen_variable("character_color")
            char_type = renpy.get_screen_variable("character_type")
            
            # Validar valores
            if not display_name or not display_name.strip():
                display_name = character_name
            
            if not color or not color.strip():
                color = "#c8ffc8"
            
            # Crear definición del personaje
            character_definition = {
                'name': character_name,
                'display_name': display_name,
                'color': color,
                'type': char_type
            }
            
            # Guardar en el diccionario de personajes definidos
            defined_chars = renpy.get_screen_variable("defined_characters")
            if defined_chars is None:
                defined_chars = {}
            
            defined_chars[character_name] = character_definition
            renpy.set_screen_variable("defined_characters", defined_chars)
            
            # Notificar éxito
            renpy.notify(f"✅ Personaje '{character_name}' definido correctamente")
            
            # Forzar actualización de la pantalla para redimensionar el panel
            renpy.restart_interaction()
            
            # Limpiar campos
            renpy.set_screen_variable("character_display_name", "")
            renpy.set_screen_variable("character_color", "#c8ffc8")
            renpy.set_screen_variable("character_type", "normal")
            
        except Exception as e:
            renpy.notify(f"❌ Error definiendo personaje: {e}")
    
    def get_character_definition(character_name):
        """Obtiene la definición de un personaje"""
        try:
            defined_chars = renpy.get_screen_variable("defined_characters")
            if defined_chars and character_name in defined_chars:
                return defined_chars[character_name]
            return None
        except Exception as e:
            print(f"Error obteniendo definición: {e}")
            return None
    
    def generate_characters_file():
        """Genera un archivo .rpy con las definiciones de personajes"""
        try:
            defined_chars = renpy.get_screen_variable("defined_characters")
            if not defined_chars:
                renpy.notify("⚠️ No hay personajes definidos para exportar")
                return
            
            # Generar contenido del archivo
            content = "# Definiciones de personajes generadas por el Editor Visual\n"
            content += "# Fecha: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n\n"
            
            for char_name, char_def in defined_chars.items():
                display_name = char_def.get('display_name', char_name)
                color = char_def.get('color', '#c8ffc8')
                char_type = char_def.get('type', 'normal')
                
                if char_type == 'narrator':
                    content += f"define {char_name} = Character(None, kind=nvl)\n"
                else:
                    content += f"define {char_name} = Character('{display_name}', color='{color}')\n"
            
            content += "\n# Fin de definiciones de personajes\n"
            
            # Guardar archivo
            import os
            characters_path = os.path.join(renpy.config.gamedir, "characters.rpy")
            with open(characters_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            renpy.notify(f"✅ Archivo de personajes generado: characters.rpy")
            
        except Exception as e:
            renpy.notify(f"❌ Error generando archivo de personajes: {e}")
    
    def load_characters_from_file():
        """Carga definiciones de personajes desde el archivo"""
        try:
            import os
            characters_path = os.path.join(renpy.config.gamedir, "characters.rpy")
            if not os.path.exists(characters_path):
                renpy.notify("⚠️ No se encontró archivo characters.rpy")
                return
            
            # Por ahora solo notificamos que existe
            renpy.notify(f"📋 Archivo de personajes encontrado: characters.rpy")
            
        except Exception as e:
            renpy.notify(f"❌ Error cargando archivo de personajes: {e}")
    
    def set_character_color(color_hex):
        """Establece el color del personaje"""
        try:
            renpy.set_screen_variable("character_color", color_hex)
            
            # Actualizar la definición del personaje actual si existe
            current_speaker = renpy.get_screen_variable("current_speaker")
            if current_speaker:
                defined_chars = renpy.get_screen_variable("defined_characters")
                if defined_chars is None:
                    defined_chars = {}
                
                if current_speaker in defined_chars:
                    defined_chars[current_speaker]['color'] = color_hex
                    renpy.set_screen_variable("defined_characters", defined_chars)
            
            color_name = get_color_name(color_hex)
            renpy.notify(f"🎨 Color cambiado a: {color_name}")
            
        except Exception as e:
            renpy.notify(f"❌ Error cambiando color: {e}")
    
    def get_color_name(color_hex):
        """Obtiene el nombre del color basado en el código hexadecimal"""
        color_names = {
            "#c8ffc8": "Verde",
            "#ffc8c8": "Rojo", 
            "#c8c8ff": "Azul",
            "#ffffc8": "Amarillo",
            "#ffc8ff": "Morado",
            "#ffd8a8": "Naranja",
            "#ffffff": "Blanco",
            "#000000": "Negro",
            "#d2b48c": "Marrón"
        }
        return color_names.get(color_hex, "Personalizado")
    
    def get_current_character_color():
        """Obtiene el color del personaje actual para la vista previa"""
        try:
            current_speaker = renpy.get_screen_variable("current_speaker")
            if not current_speaker:
                return "#3498db"  # Color por defecto
            
            # Primero verificar si hay una definición guardada
            defined_chars = renpy.get_screen_variable("defined_characters")
            if defined_chars and current_speaker in defined_chars:
                return defined_chars[current_speaker].get('color', '#3498db')
            
            # Si no hay definición, usar el color actual del panel
            current_color = renpy.get_screen_variable("character_color")
            if current_color:
                return current_color
            
            return "#3498db"  # Color por defecto
            
        except Exception as e:
            print(f"Error obteniendo color: {e}")
            return "#3498db"
    
    def get_narrator_color():
        """Obtiene el color configurado para el narrador"""
        try:
            return renpy.get_screen_variable("narrator_color") or "#ffffff"
        except Exception as e:
            return "#ffffff"
    
    def get_narrator_size():
        """Obtiene el tamaño configurado para el narrador"""
        try:
            size = renpy.get_screen_variable("narrator_size") or "medium"
            # Mapear tamaños a valores de Ren'Py
            size_map = {
                "small": text_sizes.text_small,
                "medium": text_sizes.text_medium,
                "large": text_sizes.text_large
            }
            return size_map.get(size, text_sizes.text_medium)
        except Exception as e:
            return text_sizes.text_medium
    
    def get_narrator_position():
        """Obtiene la posición configurada para el narrador"""
        try:
            return renpy.get_screen_variable("narrator_position") or "center"
        except Exception as e:
            return "center"
    
    def get_narrator_style():
        """Obtiene el estilo configurado para el narrador"""
        try:
            return renpy.get_screen_variable("narrator_style") or "textbox"
        except Exception as e:
            return "textbox"
    
    def get_narrator_size_name():
        """Obtiene el nombre del tamaño configurado para el narrador"""
        try:
            size = renpy.get_screen_variable("narrator_size") or "medium"
            size_names = {
                "small": "Pequeño",
                "medium": "Mediano", 
                "large": "Grande"
            }
            return size_names.get(size, "Mediano")
        except Exception as e:
            return "Mediano"
    
    def edit_character_definition(character_name):
        """Carga un personaje definido para edición"""
        try:
            # Obtener la definición del personaje
            defined_chars = renpy.get_screen_variable("defined_characters")
            if defined_chars and character_name in defined_chars:
                char_def = defined_chars[character_name]
                
                # Cargar los datos en el panel de edición
                renpy.set_screen_variable("current_speaker", character_name)
                renpy.set_screen_variable("character_display_name", char_def.get('display_name', character_name))
                renpy.set_screen_variable("character_color", char_def.get('color', '#c8ffc8'))
                renpy.set_screen_variable("character_type", char_def.get('type', 'normal'))
                
                renpy.notify(f"✏️ Editando personaje: {character_name}")
            else:
                renpy.notify(f"❌ Personaje no encontrado: {character_name}")
                
        except Exception as e:
            renpy.notify(f"❌ Error editando personaje: {e}")
    
    def delete_character_definition(character_name):
        """Elimina un personaje definido"""
        try:
            # Obtener la lista actual de personajes definidos
            defined_chars = renpy.get_screen_variable("defined_characters")
            if defined_chars and character_name in defined_chars:
                # Eliminar el personaje
                del defined_chars[character_name]
                renpy.set_screen_variable("defined_characters", defined_chars)
                
                # Si el personaje eliminado era el actual, limpiar el panel
                current_speaker = renpy.get_screen_variable("current_speaker")
                if current_speaker == character_name:
                    renpy.set_screen_variable("current_speaker", "")
                    renpy.set_screen_variable("character_display_name", "")
                    renpy.set_screen_variable("character_color", "#c8ffc8")
                    renpy.set_screen_variable("character_type", "normal")
                
                renpy.notify(f"🗑️ Personaje eliminado: {character_name}")
            else:
                renpy.notify(f"❌ Personaje no encontrado: {character_name}")
                
        except Exception as e:
            renpy.notify(f"❌ Error eliminando personaje: {e}")
    
    def set_sprite_position(position):
        """Establece la posición del sprite"""
        try:
            renpy.set_screen_variable("sprite_position", position)
            
            # Mapear posiciones a nombres descriptivos
            position_names = {
                "left": "Izquierda",
                "center": "Centro",
                "right": "Derecha"
            }
            
            position_name = position_names.get(position, position)
            renpy.notify(f"📍 Posición cambiada a: {position_name}")
            
        except Exception as e:
            renpy.notify(f"❌ Error cambiando posición: {e}")
    
    def set_sprite_animation(animation):
        """Establece la animación del sprite"""
        try:
            renpy.set_screen_variable("sprite_animation", animation)
            
            # Forzar actualización de la vista previa
            renpy.set_screen_variable("force_animation_update", True)
            
            # Mapear animaciones a nombres descriptivos
            animation_names = {
                "none": "Sin animación",
                "enter_right": "Entrar por la derecha",
                "enter_left": "Entrar por la izquierda",
                "enter_center": "Entrar por el centro"
            }
            
            animation_name = animation_names.get(animation, animation)
            renpy.notify(f"🎬 Animación cambiada a: {animation_name}")
            
        except Exception as e:
            renpy.notify(f"❌ Error cambiando animación: {e}")
    
    def load_character_definition(character_name):
        """Carga la definición de un personaje en el panel"""
        try:
            char_def = get_character_definition(character_name)
            if char_def:
                # Cargar valores en el panel
                renpy.set_screen_variable("character_display_name", char_def.get('display_name', character_name))
                renpy.set_screen_variable("character_color", char_def.get('color', '#c8ffc8'))
                renpy.set_screen_variable("character_type", char_def.get('type', 'normal'))
                renpy.notify(f"📋 Definición de '{character_name}' cargada")
            else:
                # Valores por defecto
                renpy.set_screen_variable("character_display_name", character_name)
                renpy.set_screen_variable("character_color", "#c8ffc8")
                renpy.set_screen_variable("character_type", "normal")
        except Exception as e:
            print(f"Error cargando definición: {e}")
    
    # ===== FUNCIONES PARA ESTRUCTURA (LABELS, JUMPS, CHOICES) =====
    
    def add_label_to_scene():
        """Agrega un label a la escena actual"""
        try:
            label_name = renpy.get_screen_variable("label_name")
            scenes = renpy.get_screen_variable("current_scenes")
            
            if scenes is None:
                scenes = []
            
            if label_name and label_name.strip():
                scene_data = {
                    'type': 'label',
                    'label_name': label_name.strip(),
                    'timestamp': datetime.now().isoformat()
                }
                scenes.append(scene_data)
                renpy.set_screen_variable("current_scenes", scenes)
                renpy.set_screen_variable("label_name", "")  # Limpiar campo
                renpy.set_screen_variable("active_input_area", None)  # Cerrar área de entrada
                # Actualización simple del viewport
                simple_viewport_refresh()
                renpy.notify(f"✅ Label '{label_name.strip()}' agregado a la escena")
            else:
                renpy.notify("⚠️ Escribe un nombre para el label")
        except Exception as e:
            renpy.notify(f"❌ Error agregando label: {e}")
    
    def add_jump_to_scene():
        """Agrega un jump a la escena actual"""
        try:
            jump_target = renpy.get_screen_variable("jump_target")
            scenes = renpy.get_screen_variable("current_scenes")
            
            if scenes is None:
                scenes = []
            
            if jump_target and jump_target.strip():
                scene_data = {
                    'type': 'jump',
                    'jump_target': jump_target.strip(),
                    'timestamp': datetime.now().isoformat()
                }
                scenes.append(scene_data)
                renpy.set_screen_variable("current_scenes", scenes)
                renpy.set_screen_variable("jump_target", "")  # Limpiar campo
                renpy.set_screen_variable("active_input_area", None)  # Cerrar área de entrada
                # Actualización simple del viewport
                simple_viewport_refresh()
                renpy.notify(f"✅ Jump a '{jump_target.strip()}' agregado a la escena")
            else:
                renpy.notify("⚠️ Escribe un destino para el jump")
        except Exception as e:
            renpy.notify(f"❌ Error agregando jump: {e}")
    
    def add_choice_to_scene():
        """Agrega un choice a la escena actual"""
        try:
            choice_text = renpy.get_screen_variable("choice_text")
            
            # Obtener choice_options con fallback a variable global
            try:
                choice_options = renpy.get_screen_variable("choice_options")
            except:
                if hasattr(renpy.store, 'choice_options_global'):
                    choice_options = renpy.store.choice_options_global
                else:
                    choice_options = []
            
            scenes = renpy.get_screen_variable("current_scenes")
            
            if scenes is None:
                scenes = []
            
            if choice_text and choice_text.strip() and choice_options and len(choice_options) >= 2:
                scene_data = {
                    'type': 'choice',
                    'question': choice_text.strip(),
                    'options': choice_options.copy(),
                    'timestamp': datetime.now().isoformat()
                }
                scenes.append(scene_data)
                renpy.set_screen_variable("current_scenes", scenes)
                renpy.set_screen_variable("choice_text", "")  # Limpiar campos
                renpy.set_screen_variable("choice_text_active", False)
                renpy.set_screen_variable("choice_options", [])
                
                # Limpiar variable global también
                if hasattr(renpy.store, 'choice_options_global'):
                    renpy.store.choice_options_global = []
                
                renpy.set_screen_variable("active_input_area", None)  # Cerrar área de entrada
                # Actualización simple del viewport
                simple_viewport_refresh()
                renpy.notify(f"✅ Choice '{choice_text.strip()}' agregado a la escena")
            else:
                renpy.notify("⚠️ Completa la pregunta y agrega al menos 2 opciones")
        except Exception as e:
            renpy.notify(f"❌ Error agregando choice: {e}")
    
    def add_choice_option():
        """Activa el panel integrado para agregar una opción"""
        try:
            renpy.set_screen_variable("show_choice_add_panel", True)
            renpy.notify("📝 Panel de agregar opción activado")
        except Exception as e:
            renpy.notify(f"❌ Error activando panel: {e}")
    
    def confirm_add_choice_option():
        """Confirma la adición de una opción con jump opcional"""
        try:
            new_option = renpy.get_screen_variable("new_choice_option")
            new_jump = renpy.get_screen_variable("new_choice_jump")
            
            # Obtener choice_options de la pantalla principal
            try:
                choice_options = renpy.get_screen_variable("choice_options", screen="visual_editor")
            except:
                choice_options = []
            
            if choice_options is None:
                choice_options = []
            
            if new_option and new_option.strip():
                # Crear objeto de opción con texto y jump opcional
                option_data = {
                    'text': new_option.strip(),
                    'jump': new_jump.strip() if new_jump and new_jump.strip() else None
                }
                
                choice_options.append(option_data)
                
                # Actualizar en la pantalla principal
                try:
                    renpy.set_screen_variable("choice_options", choice_options, screen="visual_editor")
                except:
                    # Fallback: usar variable global
                    global choice_options_global
                    if not hasattr(renpy.store, 'choice_options_global'):
                        renpy.store.choice_options_global = []
                    renpy.store.choice_options_global = choice_options
                
                # Limpiar campos
                renpy.set_screen_variable("new_choice_option", "")
                renpy.set_screen_variable("new_choice_jump", "")
                renpy.set_screen_variable("choice_option_active", False)
                renpy.set_screen_variable("choice_jump_active", False)
                renpy.set_screen_variable("show_choice_add_panel", False)
                
                # Mensaje de confirmación
                if new_jump and new_jump.strip():
                    renpy.notify(f"✅ Opción '{new_option.strip()}' agregada con jump a '{new_jump.strip()}'")
                else:
                    renpy.notify(f"✅ Opción '{new_option.strip()}' agregada")
            else:
                renpy.notify("⚠️ Escribe el texto de la opción")
        except Exception as e:
            renpy.notify(f"❌ Error agregando opción: {e}")
    
    def clear_choice_inputs():
        """Limpia los campos de entrada de opciones de choice"""
        try:
            renpy.set_screen_variable("new_choice_option", "")
            renpy.set_screen_variable("new_choice_jump", "")
            renpy.set_screen_variable("choice_option_active", False)
            renpy.set_screen_variable("choice_jump_active", False)
            renpy.notify("🧹 Campos de opción limpiados")
        except Exception as e:
            renpy.notify(f"❌ Error limpiando campos: {e}")
    
    def activate_choice_option_edit():
        """Activa el campo de edición del texto de la opción"""
        try:
            renpy.set_screen_variable("choice_option_active", True)
            renpy.restart_interaction()
            renpy.notify("✏️ Campo de texto de opción activado - puedes editar")
        except Exception as e:
            renpy.notify(f"❌ Error activando edición: {e}")
    
    def accept_choice_option():
        """Acepta y guarda el texto de la opción"""
        try:
            renpy.set_screen_variable("choice_option_active", False)
            renpy.notify("✅ Texto de opción guardado")
        except Exception as e:
            renpy.notify(f"❌ Error guardando texto: {e}")
    
    def activate_choice_jump_edit():
        """Activa el campo de edición del jump"""
        try:
            renpy.set_screen_variable("choice_jump_active", True)
            renpy.restart_interaction()
            renpy.notify("✏️ Campo de jump activado - puedes editar")
        except Exception as e:
            renpy.notify(f"❌ Error activando edición: {e}")
    
    def accept_choice_jump():
        """Acepta y guarda el jump"""
        try:
            renpy.set_screen_variable("choice_jump_active", False)
            renpy.notify("✅ Jump guardado")
        except Exception as e:
            renpy.notify(f"❌ Error guardando jump: {e}")
    
    def cancel_choice_add_panel():
        """Cancela el panel de agregar opciones"""
        try:
            renpy.set_screen_variable("show_choice_add_panel", False)
            renpy.set_screen_variable("new_choice_option", "")
            renpy.set_screen_variable("new_choice_jump", "")
            renpy.set_screen_variable("choice_option_active", False)
            renpy.set_screen_variable("choice_jump_active", False)
            renpy.notify("❌ Panel de agregar opción cancelado")
        except Exception as e:
            renpy.notify(f"❌ Error cancelando panel: {e}")
    
    def activate_choice_text_edit():
        """Activa el campo de edición de la pregunta del choice"""
        try:
            renpy.set_screen_variable("choice_text_active", True)
            renpy.notify("✏️ Campo de pregunta activado - puedes editar")
        except Exception as e:
            renpy.notify(f"❌ Error activando edición: {e}")
    
    def accept_choice_text():
        """Acepta y guarda la pregunta del choice"""
        try:
            renpy.set_screen_variable("choice_text_active", False)
            renpy.notify("✅ Pregunta guardada")
        except Exception as e:
            renpy.notify(f"❌ Error guardando pregunta: {e}")
    
    def confirm_choice_question():
        """Confirma la pregunta del choice para poder agregar opciones"""
        try:
            choice_text = renpy.get_screen_variable("choice_text")
            if choice_text and choice_text.strip():
                renpy.set_screen_variable("choice_question_confirmed", True)
                renpy.notify("✅ Pregunta confirmada. Ahora puedes agregar opciones.")
            else:
                renpy.notify("❌ Primero debes escribir una pregunta")
        except Exception as e:
            renpy.notify(f"❌ Error confirmando pregunta: {e}")
    
    def reset_choice_question():
        """Reinicia la pregunta del choice"""
        try:
            renpy.set_screen_variable("choice_text", "")
            renpy.set_screen_variable("choice_text_active", False)
            renpy.set_screen_variable("choice_question_confirmed", False)
            renpy.set_screen_variable("choice_options", [])
            renpy.notify("🔄 Pregunta reiniciada")
        except Exception as e:
            renpy.notify(f"❌ Error reiniciando pregunta: {e}")
    
    def remove_choice_option(index):
        """Elimina una opción del choice"""
        try:
            choice_options = renpy.get_screen_variable("choice_options")
            if choice_options and 0 <= index < len(choice_options):
                removed_option = choice_options.pop(index)
                renpy.set_screen_variable("choice_options", choice_options)
                
                # Obtener texto de la opción eliminada
                if isinstance(removed_option, dict):
                    option_text = removed_option.get('text', 'Opción')
                else:
                    option_text = removed_option
                
                renpy.notify(f"🗑️ Opción '{option_text}' eliminada")
            else:
                renpy.notify("❌ Opción no encontrada")
        except Exception as e:
            renpy.notify(f"❌ Error eliminando opción: {e}")
    
    def cancel_choice_creation():
        """Cancela la creación del choice"""
        try:
            renpy.set_screen_variable("choice_text", "")
            renpy.set_screen_variable("choice_text_active", False)
            renpy.set_screen_variable("choice_question_confirmed", False)
            renpy.set_screen_variable("choice_options", [])
            renpy.set_screen_variable("active_input_area", None)
            renpy.notify("❌ Creación de choice cancelada")
        except Exception as e:
            renpy.notify(f"❌ Error cancelando choice: {e}")
    
    # ===== FUNCIONES PARA TRANSICIONES =====
    
    def set_background_transition(transition):
        """Establece la transición para fondos"""
        try:
            renpy.set_screen_variable("background_transition", transition)
            
            # Mapear transiciones a nombres descriptivos
            transition_names = {
                "dissolve": "Dissolve (Desvanecimiento)",
                "fade": "Fade (Desvanecimiento)",
                "move": "Move (Movimiento)"
            }
            
            transition_name = transition_names.get(transition, transition)
            renpy.notify(f"🖼️ Transición de fondo cambiada a: {transition_name}")
            
        except Exception as e:
            renpy.notify(f"❌ Error cambiando transición de fondo: {e}")
    
    def set_character_transition(transition):
        """Establece la transición para personajes"""
        try:
            renpy.set_screen_variable("character_transition", transition)
            
            # Mapear transiciones a nombres descriptivos
            transition_names = {
                "dissolve": "Dissolve (Desvanecimiento)",
                "fade": "Fade (Desvanecimiento)",
                "move": "Move (Movimiento)",
                "moveinleft": "MoveInLeft (Entrar desde la izquierda)",
                "moveinright": "MoveInRight (Entrar desde la derecha)",
                "moveinbottom": "MoveInBottom (Entrar desde abajo)"
            }
            
            transition_name = transition_names.get(transition, transition)
            renpy.notify(f"👤 Transición de personaje cambiada a: {transition_name}")
            
        except Exception as e:
            renpy.notify(f"❌ Error cambiando transición de personaje: {e}")
    
    # ===== FUNCIONES PARA CONFIGURACIÓN DEL NARRADOR =====
    
    def set_narrator_style(style):
        """Establece el estilo del narrador"""
        try:
            renpy.set_screen_variable("narrator_style", style)
            
            # Mapear estilos a nombres descriptivos
            style_names = {
                "textbox": "Textbox (Caja de texto)",
                "floating": "Flotante (Texto libre)",
                "screen": "Pantalla (Texto en pantalla)"
            }
            
            style_name = style_names.get(style, style)
            renpy.notify(f"📝 Estilo de narrador cambiado a: {style_name}")
            
        except Exception as e:
            renpy.notify(f"❌ Error cambiando estilo de narrador: {e}")
    
    def set_narrator_position(position):
        """Establece la posición del texto del narrador"""
        try:
            renpy.set_screen_variable("narrator_position", position)
            
            # Mapear posiciones a nombres descriptivos
            position_names = {
                "left": "Izquierda",
                "center": "Centro",
                "right": "Derecha",
                "top": "Arriba",
                "bottom": "Abajo"
            }
            
            position_name = position_names.get(position, position)
            renpy.notify(f"📍 Posición del narrador cambiada a: {position_name}")
            
        except Exception as e:
            renpy.notify(f"❌ Error cambiando posición del narrador: {e}")
    
    def set_narrator_color(color):
        """Establece el color del texto del narrador"""
        try:
            renpy.set_screen_variable("narrator_color", color)
            
            # Mapear colores a nombres descriptivos
            color_names = {
                "#ffffff": "Blanco",
                "#f1c40f": "Amarillo",
                "#3498db": "Azul",
                "#27ae60": "Verde"
            }
            
            color_name = color_names.get(color, color)
            renpy.notify(f"🎨 Color del narrador cambiado a: {color_name}")
            
        except Exception as e:
            renpy.notify(f"❌ Error cambiando color del narrador: {e}")
    
    def set_narrator_size(size):
        """Establece el tamaño del texto del narrador"""
        try:
            renpy.set_screen_variable("narrator_size", size)
            
            # Mapear tamaños a nombres descriptivos
            size_names = {
                "small": "Pequeño",
                "medium": "Mediano",
                "large": "Grande"
            }
            
            size_name = size_names.get(size, size)
            renpy.notify(f"📏 Tamaño del narrador cambiado a: {size_name}")
            
        except Exception as e:
            renpy.notify(f"❌ Error cambiando tamaño del narrador: {e}")
    
    def set_narrator_pos_x(value):
        """Establece la posición X del narrador"""
        try:
            renpy.set_screen_variable("narrator_pos_x", value)
            # Forzar actualización de la vista previa
            renpy.restart_interaction()
            renpy.notify(f"📍 Posición X: {value:.2f}")
        except Exception as e:
            renpy.notify(f"❌ Error cambiando posición X: {e}")
    
    def set_narrator_pos_y(value):
        """Establece la posición Y del narrador"""
        try:
            renpy.set_screen_variable("narrator_pos_y", value)
            # Forzar actualización de la vista previa
            renpy.restart_interaction()
            renpy.notify(f"📍 Posición Y: {value:.2f}")
        except Exception as e:
            renpy.notify(f"❌ Error cambiando posición Y: {e}")
    
    def set_narrator_transition(transition):
        """Establece la transición del narrador"""
        try:
            renpy.set_screen_variable("narrator_transition", transition)
            renpy.notify(f"🎬 Transición del narrador: {transition}")
        except Exception as e:
            renpy.notify(f"❌ Error cambiando transición: {e}")
    
    def get_current_datetime():
        """Obtiene la fecha y hora actual"""
        try:
            from datetime import datetime
            return datetime.now().strftime("%d/%m/%Y %H:%M")
        except Exception as e:
            return "Fecha/Hora"
    
    def get_default_location():
        """Obtiene ubicación por defecto"""
        return "Ubicación"
    
    def activate_narrator_name_edit():
        """Activa el campo de edición del nombre del narrador"""
        try:
            renpy.set_screen_variable("narrator_name_active", True)
            renpy.notify("✏️ Campo de nombre activado - puedes editar")
        except Exception as e:
            renpy.notify(f"❌ Error activando edición: {e}")
    
    def accept_narrator_name():
        """Acepta y guarda el nombre del narrador"""
        try:
            renpy.set_screen_variable("narrator_name_active", False)
            renpy.notify("✅ Nombre del narrador guardado")
        except Exception as e:
            renpy.notify(f"❌ Error guardando nombre: {e}")
    
    def add_narrator_to_scene():
        """Agrega un diálogo del narrador a la escena actual"""
        try:
            narrator_text_content = renpy.get_screen_variable("narrator_text")
            scenes = renpy.get_screen_variable("current_scenes")
            
            # Si scenes es None, inicializar como lista vacía
            if scenes is None:
                scenes = []
            
            if narrator_text_content and narrator_text_content.strip():
                scene_data = {
                    'type': 'dialogue',
                    'character': 'Narrator',
                    'dialogue': narrator_text_content.strip(),
                    'transition': renpy.get_screen_variable("narrator_transition") or 'dissolve',
                    'timestamp': datetime.now().isoformat(),
                    'narrator_style': renpy.get_screen_variable("narrator_style") or 'textbox',
                    'narrator_position': renpy.get_screen_variable("narrator_position") or 'center',
                    'narrator_pos_x': renpy.get_screen_variable("narrator_pos_x") or 0.5,
                    'narrator_pos_y': renpy.get_screen_variable("narrator_pos_y") or 0.5,
                    'narrator_color': renpy.get_screen_variable("narrator_color") or '#ffffff',
                    'narrator_size': renpy.get_screen_variable("narrator_size") or 'medium',
                    'narrator_name': renpy.get_screen_variable("narrator_name") or 'Narrador',
                    'narrator_date_time': renpy.get_screen_variable("narrator_date_time") or '',
                    'narrator_location': renpy.get_screen_variable("narrator_location") or ''
                }
                
                scenes.append(scene_data)
                renpy.set_screen_variable("current_scenes", scenes)
                renpy.set_screen_variable("narrator_text", "")  # Limpiar el campo
                renpy.set_screen_variable("narrator_text_active", False)  # Desactivar el campo
                # Actualización simple del viewport
                simple_viewport_refresh()
                renpy.notify(f"✅ Narrador agregado a la escena con estilo '{renpy.get_screen_variable('narrator_style') or 'textbox'}'")
            else:
                renpy.notify("⚠️ Escribe un texto para el narrador primero")
        except Exception as e:
            renpy.notify(f"❌ Error agregando narrador: {e}")
    
    def clear_narrator_text():
        """Limpia el campo de texto del narrador"""
        try:
            renpy.set_screen_variable("narrator_text", "")
            renpy.set_screen_variable("narrator_text_active", False)
            renpy.notify("🗑️ Texto del narrador limpiado y campo desactivado")
        except Exception as e:
            renpy.notify(f"❌ Error limpiando texto: {e}")
    
    def get_all_scenes_safe():
        """Obtiene todas las escenas de manera segura"""
        try:
            return renpy.get_screen_variable("all_scenes", {})
        except:
            return {}
    
    def get_scene_count_safe(scene_name):
        """Obtiene el número de elementos de una escena de manera segura"""
        try:
            all_scenes = get_all_scenes_safe()
            if scene_name in all_scenes:
                return len(all_scenes[scene_name])
            return 0
        except:
            return 0
    
    def debug_scenes_state():
        """Función de debug para verificar el estado de las escenas"""
        try:
            all_scenes = get_all_scenes_safe()
            current_name = renpy.get_screen_variable("current_scene_name", "")
            current_scenes = renpy.get_screen_variable("current_scenes", [])
            
            print("🔍 === DEBUG ESTADO DE ESCENAS ===")
            print(f"📋 Total de escenas: {len(all_scenes)}")
            print(f"📝 Escenas disponibles: {list(all_scenes.keys())}")
            print(f"🎭 Escena actual: '{current_name}'")
            print(f"📊 Elementos en escena actual: {len(current_scenes)}")
            print("==================================")
            
            return True
        except Exception as e:
            print(f"🔍 Error en debug: {e}")
            return False
    
    def init_create_scene_modal():
        """Inicializa la ventana modal para crear escenas"""
        try:
            # Asegurar que las variables estén inicializadas
            renpy.set_screen_variable("new_scene_name", "")
            renpy.set_screen_variable("modal_mode", "create")
            return True
        except Exception as e:
            print(f"🔍 Error inicializando modal: {e}")
            return False
    
    def simple_init_scene():
        """Inicializa la ventana modal simple para crear escenas"""
        try:
            # Limpiar la variable simple
            renpy.set_screen_variable("simple_scene_name", "")
            return True
        except Exception as e:
            print(f"🔍 Error inicializando modal simple: {e}")
            return False
    
    def simple_create_scene():
        """Crea una nueva escena desde la pantalla modal simple"""
        try:
            # Obtener el valor de la variable global directamente
            scene_name = simple_scene_name
            print(f"🔍 Debug: Valor obtenido del input: '{scene_name}'")
            
            if scene_name and scene_name.strip():
                scene_name = scene_name.strip()
                print(f"🔍 Debug: Nombre procesado: '{scene_name}'")
                
                # Obtener las escenas actuales
                all_scenes = renpy.get_screen_variable("all_scenes", {})
                
                if scene_name in all_scenes:
                    renpy.notify("⚠️ Ya existe una escena con ese nombre")
                    return
                
                # Crear la nueva escena
                all_scenes[scene_name] = []
                renpy.set_screen_variable("all_scenes", all_scenes)
                renpy.set_screen_variable("current_scene_name", scene_name)
                renpy.set_screen_variable("current_scenes", [])
                
                # Limpiar la variable global
                simple_scene_name = ""
                
                # Notificar éxito
                renpy.notify(f"✅ Nueva escena '{scene_name}' creada")
                
                # Debug
                print(f"🔍 Debug: Escena '{scene_name}' creada desde modal simple")
                
            else:
                renpy.notify("⚠️ Ingresa un nombre para la escena")
                print(f"🔍 Debug: Nombre vacío o inválido: '{scene_name}'")
                
        except Exception as e:
            renpy.notify(f"❌ Error creando escena: {e}")
            print(f"🔍 Debug: Error completo: {e}")
    
    def simple_create_scene_alt():
        """Crea una nueva escena desde la pantalla modal alternativa"""
        try:
            # Obtener el valor de la variable global directamente
            scene_name = simple_scene_name
            print(f"🔍 Debug Alt: Valor obtenido del input: '{scene_name}'")
            
            if scene_name and scene_name.strip():
                scene_name = scene_name.strip()
                print(f"🔍 Debug Alt: Nombre procesado: '{scene_name}'")
                
                # Obtener las escenas actuales
                all_scenes = renpy.get_screen_variable("all_scenes", {})
                
                if scene_name in all_scenes:
                    renpy.notify("⚠️ Ya existe una escena con ese nombre")
                    return
                
                # Crear la nueva escena
                all_scenes[scene_name] = []
                renpy.set_screen_variable("all_scenes", all_scenes)
                renpy.set_screen_variable("current_scene_name", scene_name)
                renpy.set_screen_variable("current_scenes", [])
                
                # Limpiar la variable global
                simple_scene_name = ""
                
                # Notificar éxito
                renpy.notify(f"✅ Nueva escena '{scene_name}' creada")
                
                # Debug
                print(f"🔍 Debug Alt: Escena '{scene_name}' creada desde modal alternativo")
                
            else:
                renpy.notify("⚠️ Ingresa un nombre para la escena")
                print(f"🔍 Debug Alt: Nombre vacío o inválido: '{scene_name}'")
                
        except Exception as e:
            renpy.notify(f"❌ Error creando escena: {e}")
            print(f"🔍 Debug Alt: Error completo: {e}")
    
    def create_new_scene_direct():
        """Crea una nueva escena directamente desde el panel principal"""
        try:
            scene_name = renpy.get_screen_variable("new_scene_name")
            if scene_name and scene_name.strip():
                scene_name = scene_name.strip()
                
                # Obtener las escenas actuales
                all_scenes = renpy.get_screen_variable("all_scenes", {})
                
                if scene_name in all_scenes:
                    renpy.notify("⚠️ Ya existe una escena con ese nombre")
                    return
                
                # Crear la nueva escena
                all_scenes[scene_name] = []
                renpy.set_screen_variable("all_scenes", all_scenes)
                renpy.set_screen_variable("current_scene_name", scene_name)
                renpy.set_screen_variable("current_scenes", [])
                
                # Limpiar la variable
                renpy.set_screen_variable("new_scene_name", "")
                
                # Notificar éxito
                renpy.notify(f"✅ Nueva escena '{scene_name}' creada")
                
                # Debug
                print(f"🔍 Debug: Escena '{scene_name}' creada directamente")
                
            else:
                renpy.notify("⚠️ Ingresa un nombre para la escena")
                
        except Exception as e:
            renpy.notify(f"❌ Error creando escena: {e}")
            print(f"🔍 Debug: Error completo: {e}")
    
    def focus_scene_input():
        """Establece el foco en el campo de entrada de escena"""
        try:
            # Forzar el foco en el campo de entrada
            renpy.restart_interaction()
            return True
        except Exception as e:
            print(f"🔍 Error estableciendo foco: {e}")
            return False
    
    print("✅ Pantalla visual_editor cargada")

# ===== FUNCIONES PARA CREAR ESCENAS =====

init python:
    def focus_simple_input():
        """Enfoca el campo de entrada de la ventana modal simple sin reiniciar"""
        try:
            # Simplemente notificar que el campo está listo para escribir
            renpy.notify("✏️ Campo de entrada listo - haz clic en el área de texto")
            return True
        except Exception as e:
            print(f"🔍 Error enfocando input: {e}")
            return False

    def create_new_scene_with_input():
        """Crea una nueva escena usando renpy.input() para entrada de texto confiable"""
        try:
            # Usar renpy.input() directamente - más confiable que el input en pantalla
            scene_name = renpy.input("🎬 Nombre de la nueva escena:", length=30, default="")
            
            if scene_name and scene_name.strip():
                scene_name = scene_name.strip()
                
                # Obtener las escenas actuales
                all_scenes = renpy.get_screen_variable("all_scenes", {})
                
                if scene_name in all_scenes:
                    renpy.notify("⚠️ Ya existe una escena con ese nombre")
                    return
                
                # Crear la nueva escena
                all_scenes[scene_name] = []
                renpy.set_screen_variable("all_scenes", all_scenes)
                renpy.set_screen_variable("current_scene_name", scene_name)
                renpy.set_screen_variable("current_scenes", [])
                
                # Notificar éxito
                renpy.notify(f"✅ Nueva escena '{scene_name}' creada")
                
                # Debug
                print(f"🔍 Debug: Escena '{scene_name}' creada con input directo")
                
            else:
                renpy.notify("⚠️ No se ingresó un nombre válido")
                
        except Exception as e:
            renpy.notify(f"❌ Error creando escena: {e}")
            print(f"🔍 Debug: Error completo: {e}")
    
    def create_new_scene_direct_alt():
        """Crea una nueva escena directamente desde el panel principal"""
        try:
            scene_name = renpy.get_screen_variable("new_scene_name")
            if scene_name and scene_name.strip():
                scene_name = scene_name.strip()
                
                # Obtener las escenas actuales
                all_scenes = renpy.get_screen_variable("all_scenes", {})
                
                if scene_name in all_scenes:
                    renpy.notify("⚠️ Ya existe una escena con ese nombre")
                    return
                
                # Crear la nueva escena
                all_scenes[scene_name] = []
                renpy.set_screen_variable("all_scenes", all_scenes)
                renpy.set_screen_variable("current_scene_name", scene_name)
                renpy.set_screen_variable("current_scenes", [])
                
                # Limpiar la variable
                renpy.set_screen_variable("new_scene_name", "")
                
                # Notificar éxito
                renpy.notify(f"✅ Nueva escena '{scene_name}' creada")
                
                # Debug
                print(f"🔍 Debug: Escena '{scene_name}' creada directamente")
                
            else:
                renpy.notify("⚠️ Ingresa un nombre para la escena")
                
        except Exception as e:
            renpy.notify(f"❌ Error creando escena: {e}")
            print(f"🔍 Debug: Error completo: {e}")

# ===== MENÚ DE SELECCIÓN DE ESCENAS =====

screen scene_selector():
    modal True
    
    frame:
        xfill True
        yfill True
        background "#000000cc"
        
        frame:
            xsize 600
            ysize 400
            background "#2c3e50"
            xalign 0.5
            yalign 0.5
            padding (20, 20)
            
            vbox:
                spacing 15
                xfill True
                yfill True
                
                # Título
                text "🎬 Seleccionar Escena" color "#ffffff" size text_sizes.title_medium xalign 0.5
                
                # Lista de escenas
                frame:
                    xfill True
                    yfill True
                    background "#1a252f"
                    padding (15, 15)
                    
                    viewport:
                        xfill True
                        yfill True
                        scrollbars "vertical"
                        mousewheel True
                        
                        vbox:
                            spacing 8
                            xfill True
                            
                            $ all_scenes = get_all_scenes_safe()
                            if all_scenes:
                                for scene_name in all_scenes.keys():
                                    frame:
                                        xfill True
                                        background "#34495e"
                                        padding (12, 8)
                                        
                                        hbox:
                                            xfill True
                                            spacing 10
                                            
                                            # Nombre de la escena
                                            text f"🎭 {scene_name}" color "#ffffff" size text_sizes.text_medium
                                            
                                            # Contador de elementos
                                            $ scene_count = get_scene_count_safe(scene_name)
                                            text f"({scene_count} elementos)" color "#f39c12" size text_sizes.text_small
                                            
                                            # Botón seleccionar
                                            textbutton "📝 Seleccionar" action [SetScreenVariable("selected_scene_to_edit", scene_name), Function(select_scene_to_edit), Hide("scene_selector")] background "#27ae60" hover_background "#2ecc71" text_color "#ffffff" text_hover_color "#ffffff" text_size text_sizes.text_small
                            else:
                                text "No hay escenas creadas" color "#95a5a6" size text_sizes.text_medium xalign 0.5
                
                # Botón cerrar
                textbutton "❌ Cerrar" action Hide("scene_selector") background "#e74c3c" hover_background "#c0392b" text_color "#ffffff" text_hover_color "#ffffff" text_size text_sizes.text_medium xalign 0.5

# ===== VENTANA MODAL SIMPLE PARA CREAR ESCENAS =====

screen simple_create_scene():
    modal True
    
    # Usar la variable global que ya está definida en la pantalla principal
    # No necesitamos default aquí porque simple_scene_name ya está definida arriba
    
    frame:
        xfill True
        yfill True
        background "#000000cc"
        
        frame:
            xsize 300
            ysize 220  # Aumentado ligeramente para el botón extra
            background "#2c3e50"
            xalign 0.5
            yalign 0.5
            padding (15, 15)
            
            vbox:
                spacing 10
                xfill True
                yfill True
                
                # Título
                text "🎬 Nueva Escena" color "#ffffff" size 20 xalign 0.5
                
                # Campo de entrada - MEJORADO para funcionar correctamente
                frame:
                    xfill True
                    background "#1a252f"
                    padding (8, 6)
                    
                    # Input usando VariableInputValue para acceder a la variable global
                    input value VariableInputValue("simple_scene_name") length 25 color "#ffffff" size 16
                
                # Texto de ayuda
                text "📝 Escribe el nombre de la escena" color "#95a5a6" size 14 xalign 0.5
                
                # Botón para enfocar el input (ayuda visual)
                textbutton "✏️ Haz clic aquí para escribir" action NullAction() background "#34495e" hover_background "#4a5f6a" text_color "#ecf0f1" text_hover_color "#ffffff" text_size 12 xalign 0.5
                
                # Botones de acción
                hbox:
                    spacing 8
                    xfill True
                    
                    textbutton "✅ Crear" action [Function(simple_create_scene), Hide("simple_create_scene")] background "#27ae60" hover_background "#2ecc71" text_color "#ffffff" text_hover_color "#ffffff" text_size 16
                    textbutton "❌ Cancelar" action [SetVariable("simple_scene_name", ""), Hide("simple_create_scene")] background "#e74c3c" hover_background "#c0392b" text_color "#ffffff" text_hover_color "#ffffff" text_size 16

# ===== VENTANA MODAL ALTERNATIVA PARA CREAR ESCENAS =====

screen simple_create_scene_alt():
    modal True
    
    # Variable para el nombre de la escena
    default simple_scene_name = ""
    
    frame:
        xfill True
        yfill True
        background "#000000cc"
        
        frame:
            xsize 300
            ysize 200
            background "#2c3e50"
            xalign 0.5
            yalign 0.5
            padding (15, 15)
            
            vbox:
                spacing 10
                xfill True
                yfill True
                
                # Título
                text "🎬 Nueva Escena" color "#ffffff" size 20 xalign 0.5
                
                # Campo de entrada usando un enfoque más directo
                frame:
                    xfill True
                    background "#1a252f"
                    padding (8, 6)
                    
                    # Input usando VariableInputValue para acceder a la variable global
                    input value VariableInputValue("simple_scene_name") length 25 color "#ffffff" size 16
                
                # Texto de ayuda
                text "📝 Escribe el nombre de la escena" color "#95a5a6" size 14 xalign 0.5
                
                # Botones de acción
                hbox:
                    spacing 8
                    xfill True
                    
                    textbutton "✅ Crear" action [Function(simple_create_scene_alt), Hide("simple_create_scene_alt")] background "#27ae60" hover_background "#2ecc71" text_color "#ffffff" text_hover_color "#ffffff" text_size 16
                    textbutton "❌ Cancelar" action [SetVariable("simple_scene_name", ""), Hide("simple_create_scene_alt")] background "#e74c3c" hover_background "#c0392b" text_color "#ffffff" text_hover_color "#ffffff" text_size 16

# ===== VENTANA MODAL HERMOSA PARA CREAR ESCENAS =====

screen new_scene_modal():
    modal True
    
    # Variables para el nombre de la escena (siguiendo el patrón de choice)
    default new_scene_name = ""
    default scene_name_active = False  # Control para activar edición del nombre
    default created_scenes_in_modal = []  # Lista de escenas creadas en esta sesión
    
    # Fondo oscuro con efecto de desenfoque
    frame:
        xfill True
        yfill True
        background "#000000cc"
        
        # Ventana modal principal
        frame:
            xsize 500
            ysize 400
            background "#2c3e50"
            xalign 0.5
            yalign 0.5
            padding (25, 25)
            
            vbox:
                spacing 20
                xfill True
                yfill True
                
                # Título con icono
                frame:
                    xfill True
                    background "#34495e"
                    padding (15, 10)
                    
                    
                    hbox:
                        spacing 10
                        xfill True
                        
                        text "🎬" size 24
                        text "Crear Nueva Escena" color "#ffffff" size 22 bold True
                
                # Campo de entrada con diseño mejorado
                frame:
                    xfill True
                    background "#1a252f"
                    padding (15, 12)
                    
                    vbox:
                        spacing 8
                        xfill True
                        
                        # Etiqueta del campo
                        text "📝 Nombre de la escena:" color "#ecf0f1" size 16
                        
                        # Campo de entrada siguiendo el patrón de choice
                        frame:
                            xfill True
                            background "#34495e"
                            padding (10, 8)
                            
                            vbox:
                                spacing 10
                                xfill True
                                
                                # Área del input (condicional como en choice)
                                frame:
                                    xfill True
                                    ysize 50
                                    background "#2c3e50"
                                    padding (10, 5)
                                    
                                    if scene_name_active and scene_name_active is not None:
                                        input:
                                            value FieldInputValue(renpy.store, "new_scene_name")
                                            xfill True
                                            yfill True
                                            color "#ffffff"
                                            size 18
                                            default "Nueva Escena"
                                            length 30
                                            id "scene_name_input"
                                    else:
                                        text new_scene_name or "Escribe el nombre de la escena..." color "#ffffff" size 18 xalign 0.5 yalign 0.5
                                
                                # Botones de control (como en choice)
                                hbox:
                                    spacing 10
                                    xalign 0.5
                                    
                                    if not scene_name_active or scene_name_active is None:
                                        textbutton "✏️ Editar Nombre":
                                            action Function(activate_scene_name_edit)
                                            xsize 120
                                            ysize 35
                                            background "#3498db"
                                            text_size 15
                                            text_color "#ffffff"
                                    else:
                                        textbutton "✅ Aceptar":
                                            action Function(accept_scene_name)
                                            xsize 100
                                            ysize 35
                                            background "#27ae60"
                                            text_size 15
                                            text_color "#ffffff"
                
                # Sección de escenas creadas en esta sesión
                if created_scenes_in_modal:
                    frame:
                        xfill True
                        background "#27ae60"
                        padding (10, 8)
                        margin (0, 5, 0, 5)
                        
                        vbox:
                            spacing 5
                            xfill True
                            
                            text f"✅ Escenas creadas ({len(created_scenes_in_modal)}):" color "#ffffff" size 16 bold True xalign 0.5
                            
                            for scene_name in created_scenes_in_modal:
                                text f"• {scene_name}" color "#ffffff" size 14 xalign 0.5
                
                # Texto de ayuda mejorado
                frame:
                    xfill True
                    background "#34495e"
                    padding (10, 8)
                    
                    vbox:
                        spacing 5
                        xfill True
                        
                        text "💡 Sugerencia: Usa nombres descriptivos como 'Introducción', 'Capítulo 1', etc." color "#bdc3c7" size 14 xalign 0.5
                        text "📝 PASOS: 1) Editar Nombre → 2) Escribir → 3) Aceptar → 4) Crear Escena" color "#f39c12" size 12 xalign 0.5
                
                # Botones de acción
                hbox:
                    spacing 15
                    xfill True
                    
                    # Botón crear escena (sin cerrar modal)
                    textbutton "➕ Crear Escena" action Function(add_scene_to_modal) background "#27ae60" hover_background "#2ecc71" text_color "#ffffff" text_hover_color "#ffffff" text_size 15 xsize 150
                    
                    # Botón aceptar (para salir)
                    textbutton "✅ Aceptar" action Function(accept_modal_scenes) background "#3498db" hover_background "#2980b9" text_color "#ffffff" text_hover_color "#ffffff" text_size 15 xsize 120 ysize 25
                    
                    # Botón cancelar
                    textbutton "❌ Cancelar" action Function(cancel_modal_scenes) background "#e74c3c" hover_background "#c0392b" text_color "#ffffff" text_hover_color "#ffffff" text_size 15 xsize 120 ysize 25

# ===== VENTANA MODAL PARA ORGANIZAR ESCENAS =====

screen organize_scenes_modal():
    modal True
    
    # Variables para el organizador
    default organizer_scenes_list = getattr(renpy.store, 'organizer_scenes_list', [])
    default selected_scene_index = 0
    default search_text = ""
    
    # Fondo oscuro con efecto de desenfoque
    frame:
        xfill True
        yfill True
        background "#000000cc"
        
        # Ventana modal principal
        frame:
            xsize 800
            ysize 600
            background "#2c3e50"
            xalign 0.5
            yalign 0.5
            padding (25, 25)
            
            vbox:
                spacing 20
                xfill True
                yfill True
                
                # Título con icono
                frame:
                    xfill True
                    background "#34495e"
                    padding (15, 10)
                    
                    hbox:
                        spacing 10
                        xfill True
                        
                        text "📋" size 24
                        text "Organizador de Escenas" color "#ffffff" size 22 bold True
                
                # Barra de búsqueda
                frame:
                    xfill True
                    background "#1a252f"
                    padding (15, 12)
                    
                    vbox:
                        spacing 8
                        xfill True
                        
                        text "🔍 Buscar escenas:" color "#ecf0f1" size 16
                        
                        frame:
                            xfill True
                            background "#34495e"
                            padding (10, 8)
                            
                            input:
                                value FieldInputValue(renpy.store, "search_text")
                                xfill True
                                ysize 40
                                color "#ffffff"
                                size 16
                                default "Escribe para buscar escenas..."
                                length 50
                
                # Lista de escenas con scroll
                frame:
                    xfill True
                    yfill True
                    background "#1a252f"
                    padding (15, 12)
                    
                    vbox:
                        spacing 10
                        xfill True
                        yfill True
                        
                        # Encabezado de la lista
                        frame:
                            xfill True
                            background "#34495e"
                            padding (10, 8)
                            
                            hbox:
                                spacing 10
                                xfill True
                                
                                text "📝 Nombre de Escena" color "#ffffff" size 16 bold True xsize 300
                                text "🎬 Tipo" color "#ffffff" size 16 bold True xsize 100
                                text "📊 Elementos" color "#ffffff" size 16 bold True xsize 100
                                text "⚙️ Acciones" color "#ffffff" size 16 bold True xsize 150
                        
                        # Lista de escenas con scroll
                        viewport:
                            xfill True
                            yfill True
                            scrollbars "vertical"
                            
                            vbox:
                                spacing 5
                                xfill True
                                
                                if organizer_scenes_list:
                                    for i, scene in enumerate(organizer_scenes_list):
                                        frame:
                                            xfill True
                                            background "#2c3e50"
                                            padding (10, 8)
                                            margin (0, 2, 0, 2)
                                            
                                            hbox:
                                                spacing 10
                                                xfill True
                                                
                                                # Nombre de la escena
                                                frame:
                                                    xsize 300
                                                    background "#1a252f"
                                                    padding (8, 5)
                                                    
                                                    text scene.get('name', 'Sin nombre') color "#ffffff" size 14 xalign 0.5
                                                
                                                # Tipo de escena
                                                frame:
                                                    xsize 100
                                                    background "#1a252f"
                                                    padding (8, 5)
                                                    
                                                    text scene.get('type', 'scene') color "#bdc3c7" size 12 xalign 0.5
                                                
                                                # Número de elementos
                                                frame:
                                                    xsize 100
                                                    background "#1a252f"
                                                    padding (8, 5)
                                                    
                                                    text str(len(scene.get('content', []))) color "#f39c12" size 12 xalign 0.5
                                                
                                                # Botones de acción
                                                frame:
                                                    xsize 150
                                                    background "#1a252f"
                                                    padding (5, 5)
                                                    
                                                    hbox:
                                                        spacing 5
                                                        xalign 0.5
                                                        
                                                        textbutton "✏️ Editar":
                                                            action Function(edit_scene_from_organizer, scene.get('name', ''))
                                                            xsize 60
                                                            ysize 25
                                                            background "#3498db"
                                                            text_size 12
                                                            text_color "#ffffff"
                                                        
                                                        textbutton "👁️ Ver":
                                                            action Function(view_scene_from_organizer, scene.get('name', ''))
                                                            xsize 50
                                                            ysize 25
                                                            background "#27ae60"
                                                            text_size 12
                                                            text_color "#ffffff"
                                                        
                                                        textbutton "🗑️ Eliminar":
                                                            action Function(confirm_delete_scene, scene.get('name', ''))
                                                            xsize 70
                                                            ysize 25
                                                            background "#e74c3c"
                                                            text_size 12
                                                            text_color "#ffffff"
                                else:
                                    # Mensaje cuando no hay escenas
                                    frame:
                                        xfill True
                                        background "#34495e"
                                        padding (20, 15)
                                        
                                        vbox:
                                            spacing 10
                                            xalign 0.5
                                            yalign 0.5
                                            
                                            text "📭 No hay escenas creadas" color "#bdc3c7" size 18 xalign 0.5
                                            text "Crea algunas escenas primero usando el botón 'Crear Escena'" color "#95a5a6" size 14 xalign 0.5
                                            text "Las escenas aparecerán aquí automáticamente" color "#7f8c8d" size 12 xalign 0.5
                
                # Información y estadísticas
                frame:
                    xfill True
                    background "#34495e"
                    padding (10, 8)
                    
                    hbox:
                        spacing 20
                        xfill True
                        
                        text f"📊 Total de escenas: {len(organizer_scenes_list)}" color "#ffffff" size 14
                        text f"🎬 Escenas de diálogo: {sum(1 for s in organizer_scenes_list if 'dialogue' in s.get('name', ''))}" color "#27ae60" size 14
                        text f"🖼️ Escenas de fondo: {sum(1 for s in organizer_scenes_list if 'background' in s.get('name', ''))}" color "#3498db" size 14
                
                # Botones de acción
                hbox:
                    spacing 15
                    xfill True
                    
                    # Botón actualizar lista
                    textbutton "🔄 Actualizar" action Function(load_all_scenes_for_organizer) background "#f39c12" hover_background "#e67e22" text_color "#ffffff" text_hover_color "#ffffff" text_size 15 xsize 120
                    
                    # Botón crear nueva escena
                    textbutton "➕ Nueva Escena" action [Function(renpy.hide_screen, "organize_scenes_modal"), Function(renpy.show_screen, "new_scene_modal")] background "#27ae60" hover_background "#2ecc71" text_color "#ffffff" text_hover_color "#ffffff" text_size 15 xsize 120
                    
                    # Botón cerrar
                    textbutton "❌ Cerrar" action Function(renpy.hide_screen, "organize_scenes_modal") background "#e74c3c" hover_background "#c0392b" text_color "#ffffff" text_hover_color "#ffffff" text_size 15 xsize 100

# ===== PANTALLA DEL EDITOR INTEGRADO =====

screen scene_editor_modal():
    modal True
    
    # Variables para el editor
    default current_scene = getattr(renpy.store, 'current_editing_scene', None)
    default scene_name = current_scene.get('name', 'Escena') if current_scene else 'Escena'
    default filename = current_scene.get('filename', '') if current_scene else ''
    
    # Fondo principal
    frame:
        style_prefix "modal"
        xfill True
        yfill True
        background "#1a1a1a"
        
        vbox:
            spacing 20
            xfill True
            yfill True
            
            # Header del editor
            frame:
                background "#2c3e50"
                xfill True
                padding (20, 15)
                
                hbox:
                    spacing 20
                    xfill True
                    
                    # Información de la escena
                    vbox:
                        spacing 5
                        xfill True
                        
                        text "✏️ Editor de Escena" color "#ecf0f1" size 24 xalign 0.0
                        text f"Archivo: {filename}" color "#bdc3c7" size 14 xalign 0.0
                        text f"Escena: {scene_name}" color "#bdc3c7" size 14 xalign 0.0
                    
                    # Botones de acción
                    vbox:
                        spacing 10
                        xalign 1.0
                        
                        textbutton "💾 Guardar" action Function(save_scene_edits) background "#27ae60" hover_background "#2ecc71"
                        textbutton "❌ Cancelar" action [Function(cancel_scene_edits), Hide("scene_editor_modal")] background "#e74c3c" hover_background "#c0392b"
            
            # Área de edición principal
            frame:
                background "#2c3e50"
                xfill True
                yfill True
                padding (20, 20)
                
                vbox:
                    spacing 15
                    xfill True
                    yfill True
                    
                    # Barra de herramientas del editor
                    frame:
                        background "#34495e"
                        xfill True
                        padding (15, 10)
                        
                        hbox:
                            spacing 15
                            xfill True
                            
                            textbutton "📝 Nueva Línea" action NullAction() background "#3498db" hover_background "#2980b9"
                            textbutton "🗑️ Eliminar Línea" action NullAction() background "#e67e22" hover_background "#d35400"
                            textbutton "📋 Copiar" action NullAction() background "#9b59b6" hover_background "#8e44ad"
                            textbutton "📋 Pegar" action NullAction() background "#9b59b6" hover_background "#8e44ad"
                    
                    # Editor de texto principal
                    frame:
                        background "#34495e"
                        xfill True
                        yfill True
                        padding (15, 15)
                        
                        vbox:
                            spacing 10
                            xfill True
                            yfill True
                            
                            # Área de texto editable
                            viewport:
                                scrollbars "vertical"
                                mousewheel True
                                xfill True
                                yfill True
                                
                                vbox:
                                    spacing 5
                                    xfill True
                                    
                                    # Mostrar líneas del editor
                                    for i, line in enumerate(getattr(renpy.store, 'editor_lines', [])):
                                        frame:
                                            background "#2c3e50"
                                            xfill True
                                            padding (10, 5)
                                            
                                            hbox:
                                                spacing 10
                                                xfill True
                                                
                                                # Número de línea
                                                text f"{i+1:3d}" color "#7f8c8d" size 12 xalign 0.0
                                                
                                                # Contenido de la línea (editable)
                                                input:
                                                    value FieldInputValue(renpy.store, f"editor_line_{i}")
                                                    default line
                                                    xfill True
                                                    color "#ecf0f1"
                                                    size 14
                                                    style_prefix "editor_input"
                    
                    # Barra de estado
                    frame:
                        background "#34495e"
                        xfill True
                        padding (15, 10)
                        
                        hbox:
                            spacing 20
                            xfill True
                            
                            text f"Líneas: {len(getattr(renpy.store, 'editor_lines', []))}" color "#bdc3c7" size 12
                            text f"Línea actual: {getattr(renpy.store, 'current_line_index', 0) + 1}" color "#bdc3c7" size 12
                            text f"Archivo: {filename}" color "#bdc3c7" size 12
                            
                            # Indicador de cambios
                            text "💾 Guardado" color "#27ae60" size 12 xalign 1.0
            
            # Botones de navegación
            frame:
                background "#2c3e50"
                xfill True
                padding (20, 15)
                
                hbox:
                    spacing 20
                    xalign 0.5
                    
                    textbutton "⬅️ Volver al Organizador" action [Hide("scene_editor_modal"), Show("organize_scenes_modal")] background "#3498db" hover_background "#2980b9"
                    textbutton "🏠 Volver al Editor" action [Hide("scene_editor_modal"), Show("visual_editor_screen")] background "#9b59b6" hover_background "#8e44ad"

# ===== SISTEMA DE CONFIRMACIÓN DE ELIMINACIÓN (MODAL SEGURO) =====
# El sistema de eliminación ahora funciona con modal de confirmación:
# 1. Usuario presiona "Eliminar" → Se muestra modal de confirmación
# 2. Usuario confirma → Se ejecuta la eliminación
# 3. Se vuelve al organizador automáticamente

# ===== PANTALLA DE CONFIRMACIÓN DE ELIMINACIÓN =====

screen confirm_delete_scene_modal(scene_name):
    modal True
    
    # Fondo semi-transparente
    frame:
        xfill True
        yfill True
        background "#000000"
        at transform:
            alpha 0.7
    
    # Modal compacto centrado
    frame:
        xsize 500
        ysize 400
        xalign 0.5
        yalign 0.5
        background "#2c3e50"
        padding (20, 20)
        at transform:
            alpha 1.0
        
        vbox:
            spacing 15
            xfill True
            yfill True
            
            # Header de confirmación
            frame:
                background "#e74c3c"
                xfill True
                padding (15, 10)
                
                vbox:
                    spacing 5
                    xfill True
                    
                    text "🗑️ Confirmar Eliminación" color "#ffffff" size 20 xalign 0.5
                    text f"Escena: {scene_name}" color "#ecf0f1" size 14 xalign 0.5
            
            # Mensaje de confirmación
            frame:
                background "#34495e"
                xfill True
                yfill True
                padding (15, 15)
                
                vbox:
                    spacing 10
                    xfill True
                    yfill True
                    
                    # Mensaje principal
                    text "¿Estás seguro de que quieres eliminar esta escena?" color "#ecf0f1" size 16 xalign 0.5 text_align 0.5
                    
                    # Advertencia compacta
                    frame:
                        background "#c0392b"
                        xfill True
                        padding (10, 10)
                        
                        vbox:
                            spacing 5
                            xalign 0.5
                            
                            text "⚠️ ADVERTENCIA" color "#ffffff" size 16 xalign 0.5
                            text "Esta acción eliminará:" color "#ecf0f1" size 14 xalign 0.5
                            text "• El archivo .rpy de la escena" color "#ecf0f1" size 12 xalign 0.5
                            text "• El archivo .rpyc compilado" color "#ecf0f1" size 12 xalign 0.5
                            text "• La escena de la lista del organizador" color "#ecf0f1" size 12 xalign 0.5
                            text "Esta acción NO se puede deshacer." color "#ffffff" size 14 xalign 0.5
                    
                    # Información de la escena
                    frame:
                        background "#2c3e50"
                        xfill True
                        padding (10, 10)
                        
                        vbox:
                            spacing 5
                            xalign 0.5
                            
                            text "📋 Información de la escena:" color "#f39c12" size 14 xalign 0.5
                            
                            # Buscar información de la escena
                            python:
                                scenes = getattr(renpy.store, 'organizer_scenes_list', [])
                                target_scene = None
                                for scene in scenes:
                                    if scene.get('name') == scene_name:
                                        target_scene = scene
                                        break
                                
                                scene_info = ""
                                if target_scene:
                                    content = target_scene.get('content', [])
                                    filename = target_scene.get('filename', '')
                                    scene_info = f"📁 Archivo: {filename}\n"
                                    scene_info += f"📊 Elementos: {len(content)} líneas\n"
                                    scene_info += f"📅 Creada: {target_scene.get('created_date', 'Desconocida')}"
                                else:
                                    scene_info = "❌ Información no disponible"
                            
                            text scene_info color "#bdc3c7" size 12 xalign 0.5 text_align 0.5
            
            # Botones de acción
            hbox:
                spacing 15
                xalign 0.5
                
                # Botón Cancelar
                textbutton "❌ Cancelar" action [Hide("confirm_delete_scene_modal"), Show("organize_scenes_modal")] background "#95a5a6" hover_background "#7f8c8d" text_color "#ffffff" text_hover_color "#ffffff" text_size 14 xsize 100 ysize 35
                
                                                 # Botón Confirmar Eliminación
                textbutton "🗑️ Eliminar":
                    action [Function(execute_scene_deletion, scene_name)]
                    background "#e74c3c"
                    hover_background "#c0392b"
                    text_color "#ffffff"
                    text_hover_color "#ffffff"
                    text_size 14
                    xsize 100
                    ysize 35

# ===== PANTALLA DE GUARDAR PROYECTO =====

screen save_project_modal():
    modal True
    
    # Fondo semi-transparente
    frame:
        xfill True
        yfill True
        background "#000000"
        at transform:
            alpha 0.7
    
    # Modal compacto centrado
    frame:
        xsize 500
        ysize 300
        xalign 0.5
        yalign 0.5
        background "#2c3e50"
        padding (20, 20)
        at transform:
            alpha 1.0
        
        vbox:
            spacing 15
            xfill True
            yfill True
            
            # Header
            frame:
                background "#27ae60"
                xfill True
                padding (15, 10)
                
                vbox:
                    spacing 5
                    xfill True
                    
                    text "💾 Guardar Proyecto" color "#ffffff" size 20 xalign 0.5
                    text "Guarda todas las escenas actuales en un proyecto" color "#ecf0f1" size 14 xalign 0.5
            
            # Contenido
            frame:
                background "#34495e"
                xfill True
                yfill True
                padding (15, 15)
                
                vbox:
                    spacing 15
                    xfill True
                    yfill True
                    
                    # Información del proyecto actual
                    frame:
                        background "#2c3e50"
                        xfill True
                        padding (10, 10)
                        
                        vbox:
                            spacing 5
                            xalign 0.5
                            
                            text "📋 Información del Proyecto:" color "#f39c12" size 16 xalign 0.5
                            
                            python:
                                current_scenes = getattr(renpy.store, 'current_scenes', [])
                                current_scene_name = getattr(renpy.store, 'current_scene_name', '')
                                scenes_dir = os.path.join(config.gamedir, "scenes")
                                scene_count = 0
                                if os.path.exists(scenes_dir):
                                    scene_count = len([f for f in os.listdir(scenes_dir) if f.endswith('.rpy')])
                                
                                project_info = f"📊 Escenas en editor: {len(current_scenes)}\n"
                                project_info += f"📁 Archivos de escenas: {scene_count}\n"
                                project_info += f"🎭 Escena actual: {current_scene_name if current_scene_name else 'Ninguna'}"
                            
                            text project_info color "#bdc3c7" size 14 xalign 0.5 text_align 0.5
                    
                    # Campo de nombre del proyecto
                    frame:
                        background "#2c3e50"
                        xfill True
                        padding (10, 10)
                        
                        vbox:
                            spacing 10
                            xalign 0.5
                            
                            text "📝 Nombre del Proyecto:" color "#f39c12" size 16 xalign 0.5
                            
                            input:
                                value FieldInputValue(renpy.store, "new_project_name")
                                xfill True
                                color "#ffffff"
                                size 16
                                default "Mi Proyecto"
            
            # Botones
            hbox:
                spacing 15
                xalign 0.5
                
                # Botón Cancelar
                textbutton "❌ Cancelar" action [Hide("save_project_modal"), Show("visual_editor")] background "#95a5a6" hover_background "#7f8c8d" text_color "#ffffff" text_hover_color "#ffffff" text_size 14 xsize 100 ysize 35
                
                # Botón Guardar
                textbutton "💾 Guardar" action [Function(execute_save_project, getattr(renpy.store, 'new_project_name', 'Mi Proyecto'))] background "#27ae60" hover_background "#2ecc71" text_color "#ffffff" text_hover_color "#ffffff" text_size 14 xsize 100 ysize 35

# ===== PANTALLA DE CARGAR PROYECTO =====

screen load_project_modal():
    modal True
    
    # Fondo semi-transparente
    frame:
        xfill True
        yfill True
        background "#000000"
        at transform:
            alpha 0.7
    
    # Modal compacto centrado
    frame:
        xsize 600
        ysize 500
        xalign 0.5
        yalign 0.5
        background "#2c3e50"
        padding (20, 20)
        at transform:
            alpha 1.0
        
        vbox:
            spacing 15
            xfill True
            yfill True
            
            # Header
            frame:
                background "#3498db"
                xfill True
                padding (15, 10)
                
                vbox:
                    spacing 5
                    xfill True
                    
                    text "📁 Cargar Proyecto" color "#ffffff" size 20 xalign 0.5
                    text "Selecciona un proyecto para cargar" color "#ecf0f1" size 14 xalign 0.5
            
            # Lista de proyectos
            frame:
                background "#34495e"
                xfill True
                yfill True
                padding (15, 15)
                
                vbox:
                    spacing 10
                    xfill True
                    yfill True
                    
                    # Barra de búsqueda
                    frame:
                        background "#2c3e50"
                        xfill True
                        padding (10, 10)
                        
                        vbox:
                            spacing 5
                            xalign 0.5
                            
                            text "🔍 Buscar Proyecto:" color "#f39c12" size 14 xalign 0.5
                            
                            input:
                                value FieldInputValue(renpy.store, "project_search_text")
                                xfill True
                                color "#ffffff"
                                size 14
                                default "Buscar proyectos..."
                    
                    # Lista de proyectos
                    frame:
                        background "#2c3e50"
                        xfill True
                        yfill True
                        padding (10, 10)
                        
                        viewport:
                            scrollbars "vertical"
                            mousewheel True
                            
                            vbox:
                                spacing 10
                                xfill True
                                
                                python:
                                    projects = getattr(renpy.store, 'available_projects', [])
                                    search_text = getattr(renpy.store, 'project_search_text', '').lower()
                                    
                                    if search_text:
                                        filtered_projects = [p for p in projects if search_text in p['name'].lower()]
                                    else:
                                        filtered_projects = projects
                                
                                if filtered_projects:
                                    for project in filtered_projects:
                                        frame:
                                            background "#34495e"
                                            xfill True
                                            padding (15, 15)
                                            
                                            vbox:
                                                spacing 10
                                                xfill True
                                                
                                                # Información del proyecto
                                                vbox:
                                                    spacing 5
                                                    xfill True
                                                    
                                                    text f"📁 {project['name']}" color "#ffffff" size 16 xalign 0.0
                                                    text f"📅 Creado: {project['created_date']}" color "#bdc3c7" size 12 xalign 0.0
                                                    text f"📊 Escenas: {project['total_scenes']}" color "#27ae60" size 12 xalign 0.0
                                                    if project['current_scene']:
                                                        text f"🎭 Escena actual: {project['current_scene']}" color "#3498db" size 12 xalign 0.0
                                                
                                                # Botón cargar
                                                textbutton "📁 Cargar Proyecto" action [Function(execute_load_project, project['folder'])] background "#3498db" hover_background "#2980b9" text_color "#ffffff" text_hover_color "#ffffff" text_size 12 xsize 120 ysize 25
                                else:
                                    frame:
                                        background "#34495e"
                                        xfill True
                                        padding (20, 15)
                                        
                                        vbox:
                                            spacing 10
                                            xalign 0.5
                                            yalign 0.5
                                            
                                            text "📭 No hay proyectos disponibles" color "#bdc3c7" size 16 xalign 0.5
                                            text "Crea algunos proyectos primero usando 'Guardar Proyecto'" color "#95a5a6" size 12 xalign 0.5
            
            # Botones
            hbox:
                spacing 15
                xalign 0.5
                
                # Botón Actualizar
                textbutton "🔄 Actualizar" action Function(load_projects_list) background "#f39c12" hover_background "#e67e22" text_color "#ffffff" text_hover_color "#ffffff" text_size 14 xsize 100 ysize 35
                
                # Botón Cancelar
                textbutton "❌ Cancelar" action [Hide("load_project_modal"), Show("visual_editor")] background "#95a5a6" hover_background "#7f8c8d" text_color "#ffffff" text_hover_color "#ffffff" text_size 14 xsize 100 ysize 35

# ===== PANTALLA DE SOBRESCRIBIR PROYECTO =====

screen overwrite_project_modal():
    modal True
    
    # Fondo semi-transparente
    frame:
        xfill True
        yfill True
        background "#000000"
        at transform:
            alpha 0.7
    
    # Modal compacto centrado
    frame:
        xsize 600
        ysize 500
        xalign 0.5
        yalign 0.5
        background "#2c3e50"
        padding (20, 20)
        at transform:
            alpha 1.0
        
        vbox:
            spacing 15
            xfill True
            yfill True
            
            # Header
            frame:
                background "#f39c12"
                xfill True
                padding (15, 10)
                
                vbox:
                    spacing 5
                    xfill True
                    
                    text "💾 Sobrescribir Proyecto" color "#ffffff" size 20 xalign 0.5
                    text "Selecciona un proyecto para sobrescribir con los cambios actuales" color "#ecf0f1" size 14 xalign 0.5
            
            # Información del proyecto actual
            frame:
                background "#34495e"
                xfill True
                padding (15, 15)
                
                vbox:
                    spacing 10
                    xfill True
                    
                    text "📋 Cambios Actuales:" color "#f39c12" size 16 xalign 0.5
                    
                    python:
                        current_scenes = getattr(renpy.store, 'current_scenes', [])
                        current_scene_name = getattr(renpy.store, 'current_scene_name', '')
                        scenes_dir = os.path.join(config.gamedir, "scenes")
                        scene_count = 0
                        if os.path.exists(scenes_dir):
                            scene_count = len([f for f in os.listdir(scenes_dir) if f.endswith('.rpy')])
                        
                        current_info = f"📊 Escenas en editor: {len(current_scenes)}\n"
                        current_info += f"📁 Archivos de escenas: {scene_count}\n"
                        current_info += f"🎭 Escena actual: {current_scene_name if current_scene_name else 'Ninguna'}"
                    
                    text current_info color "#bdc3c7" size 14 xalign 0.5 text_align 0.5
            
            # Lista de proyectos
            frame:
                background "#34495e"
                xfill True
                yfill True
                padding (15, 15)
                
                vbox:
                    spacing 10
                    xfill True
                    yfill True
                    
                    # Barra de búsqueda
                    frame:
                        background "#2c3e50"
                        xfill True
                        padding (10, 10)
                        
                        vbox:
                            spacing 5
                            xalign 0.5
                            
                            text "🔍 Buscar Proyecto:" color "#f39c12" size 14 xalign 0.5
                            
                            input:
                                value FieldInputValue(renpy.store, "overwrite_search_text")
                                xfill True
                                color "#ffffff"
                                size 14
                                default "Buscar proyectos..."
                    
                    # Lista de proyectos
                    frame:
                        background "#2c3e50"
                        xfill True
                        yfill True
                        padding (10, 10)
                        
                        viewport:
                            scrollbars "vertical"
                            mousewheel True
                            
                            vbox:
                                spacing 10
                                xfill True
                                
                                python:
                                    projects = getattr(renpy.store, 'available_projects', [])
                                    search_text = getattr(renpy.store, 'overwrite_search_text', '').lower()
                                    
                                    if search_text:
                                        filtered_projects = [p for p in projects if search_text in p['name'].lower()]
                                    else:
                                        filtered_projects = projects
                                
                                if filtered_projects:
                                    for project in filtered_projects:
                                        frame:
                                            background "#34495e"
                                            xfill True
                                            padding (15, 15)
                                            
                                            vbox:
                                                spacing 10
                                                xfill True
                                                
                                                # Información del proyecto
                                                vbox:
                                                    spacing 5
                                                    xfill True
                                                    
                                                    text f"📁 {project['name']}" color "#ffffff" size 16 xalign 0.0
                                                    text f"📅 Creado: {project['created_date']}" color "#bdc3c7" size 12 xalign 0.0
                                                    text f"📊 Escenas actuales: {project['total_scenes']}" color "#27ae60" size 12 xalign 0.0
                                                    if project['current_scene']:
                                                        text f"🎭 Escena actual: {project['current_scene']}" color "#3498db" size 12 xalign 0.0
                                                
                                                # Botón sobrescribir
                                                textbutton "💾 Sobrescribir Proyecto" action [Function(execute_overwrite_project, project['folder'])] background "#f39c12" hover_background "#e67e22" text_color "#ffffff" text_hover_color "#ffffff" text_size 12 xsize 140 ysize 25
                                else:
                                    frame:
                                        background "#34495e"
                                        xfill True
                                        padding (20, 15)
                                        
                                        vbox:
                                            spacing 10
                                            xalign 0.5
                                            yalign 0.5
                                            
                                            text "📭 No hay proyectos disponibles" color "#bdc3c7" size 16 xalign 0.5
                                            text "Crea algunos proyectos primero usando 'Guardar Proyecto'" color "#95a5a6" size 12 xalign 0.5
            
            # Botones
            hbox:
                spacing 15
                xalign 0.5
                
                # Botón Actualizar
                textbutton "🔄 Actualizar" action Function(load_projects_list) background "#f39c12" hover_background "#e67e22" text_color "#ffffff" text_hover_color "#ffffff" text_size 14 xsize 100 ysize 35
                
                # Botón Cancelar
                textbutton "❌ Cancelar" action [Hide("overwrite_project_modal"), Show("visual_editor")] background "#95a5a6" hover_background "#7f8c8d" text_color "#ffffff" text_hover_color "#ffffff" text_size 14 xsize 100 ysize 35

# ===== PANTALLA DE ELIMINAR PROYECTO COMPLETO =====

screen delete_project_modal():
    modal True
    
    # Fondo semi-transparente
    frame:
        xfill True
        yfill True
        background "#000000"
        at transform:
            alpha 0.7
    
    # Modal compacto centrado
    frame:
        xsize 600
        ysize 500
        xalign 0.5
        yalign 0.5
        background "#2c3e50"
        padding (20, 20)
        at transform:
            alpha 1.0
        
        vbox:
            spacing 15
            xfill True
            yfill True
            
            # Header
            frame:
                background "#e74c3c"
                xfill True
                padding (15, 10)
                
                vbox:
                    spacing 5
                    xfill True
                    
                    text "🗑️ Eliminar Proyecto Completo" color "#ffffff" size 20 xalign 0.5
                    text "Selecciona un proyecto para eliminar TODA su carpeta" color "#ecf0f1" size 14 xalign 0.5
            
            # Advertencia
            frame:
                background "#8b0000"
                xfill True
                padding (15, 15)
                
                vbox:
                    spacing 10
                    xfill True
                    
                    text "⚠️ ADVERTENCIA: Esta acción es IRREVERSIBLE" color "#ffffff" size 16 xalign 0.5
                    text "• Se eliminará TODA la carpeta del proyecto" color "#ffcccc" size 14 xalign 0.5
                    text "• Se perderán TODOS los archivos y escenas" color "#ffcccc" size 14 xalign 0.5
                    text "• No se puede recuperar después de eliminar" color "#ffcccc" size 14 xalign 0.5
            
            # Lista de proyectos
            frame:
                background "#34495e"
                xfill True
                yfill True
                padding (15, 15)
                
                vbox:
                    spacing 10
                    xfill True
                    yfill True
                    
                    # Barra de búsqueda
                    frame:
                        background "#2c3e50"
                        xfill True
                        padding (10, 10)
                        
                        vbox:
                            spacing 5
                            xalign 0.5
                            
                            text "🔍 Buscar Proyecto a Eliminar:" color "#e74c3c" size 14 xalign 0.5
                            
                            input:
                                value FieldInputValue(renpy.store, "delete_project_search_text")
                                xfill True
                                color "#ffffff"
                                size 14
                                default "Buscar proyectos..."
                    
                    # Lista de proyectos
                    frame:
                        background "#2c3e50"
                        xfill True
                        yfill True
                        padding (10, 10)
                        
                        viewport:
                            scrollbars "vertical"
                            mousewheel True
                            
                            vbox:
                                spacing 10
                                xfill True
                                
                                python:
                                    projects = getattr(renpy.store, 'available_projects', [])
                                    search_text = getattr(renpy.store, 'delete_project_search_text', '').lower()
                                    
                                    if search_text:
                                        filtered_projects = [p for p in projects if search_text in p['name'].lower()]
                                    else:
                                        filtered_projects = projects
                                
                                if filtered_projects:
                                    for project in filtered_projects:
                                        frame:
                                            background "#34495e"
                                            xfill True
                                            padding (15, 15)
                                            
                                            vbox:
                                                spacing 10
                                                xfill True
                                                
                                                # Información del proyecto
                                                vbox:
                                                    spacing 5
                                                    xfill True
                                                    
                                                    text f"📁 {project['name']}" color "#ffffff" size 16 xalign 0.0
                                                    text f"📅 Creado: {project['created_date']}" color "#bdc3c7" size 12 xalign 0.0
                                                    text f"📊 Escenas: {project['total_scenes']}" color "#27ae60" size 12 xalign 0.0
                                                    if project['current_scene']:
                                                        text f"🎭 Escena actual: {project['current_scene']}" color "#3498db" size 12 xalign 0.0
                                                
                                                # Botón eliminar
                                                textbutton "🗑️ ELIMINAR PROYECTO" action [Function(execute_delete_project, project['folder'])] background "#e74c3c" hover_background "#c0392b" text_color "#ffffff" text_hover_color "#ffffff" text_size 12 xsize 140 ysize 25
                                else:
                                    frame:
                                        background "#34495e"
                                        xfill True
                                        padding (20, 15)
                                        
                                        vbox:
                                            spacing 10
                                            xalign 0.5
                                            yalign 0.5
                                            
                                            text "📭 No hay proyectos disponibles" color "#bdc3c7" size 16 xalign 0.5
                                            text "Crea algunos proyectos primero usando 'Guardar Proyecto'" color "#95a5a6" size 12 xalign 0.5
            
            # Botones
            hbox:
                spacing 15
                xalign 0.5
                
                # Botón Actualizar
                textbutton "🔄 Actualizar" action Function(load_projects_list) background "#e74c3c" hover_background "#c0392b" text_color "#ffffff" text_hover_color "#ffffff" text_size 14 xsize 100 ysize 35
                
                # Botón Cancelar
                textbutton "❌ Cancelar" action [Hide("delete_project_modal"), Show("visual_editor")] background "#95a5a6" hover_background "#7f8c8d" text_color "#ffffff" text_hover_color "#ffffff" text_size 14 xsize 100 ysize 35

init python:
    # ===== SISTEMA HÍBRIDO MCKEE-ROTHAMEL PARA CREACIÓN DE ESCENAS =====
    
    class SceneCreationState:
        """Estado simple pero robusto para la creación de escenas (Enfoque Rothamel)"""
        
        def __init__(self):
            self.ready = False
            self.error_count = 0
            self.last_error_time = 0
        
        def can_create_scene(self):
            """Verificación simple pero efectiva"""
            return (
                self.ready and 
                self.error_count < 3 and
                self._is_modal_accessible()
            )
        
        def mark_ready(self):
            """Transición de estado clara"""
            self.ready = True
            self.error_count = 0
        
        def mark_error(self):
            """Registra un error y ajusta el estado"""
            self.error_count += 1
            self.last_error_time = renpy.get_game_runtime()
        
        def _is_modal_accessible(self):
            """Verifica si la modal está accesible de forma segura"""
            try:
                # Verificar si la pantalla está activa
                return renpy.get_screen_variable("new_scene_name", None) is not None
            except:
                return False
    
    # Instancia global del estado de creación
    scene_creation_state = SceneCreationState()
    
    def create_clear_notification(message_type, details=""):
        """Notificaciones que informan sin abrumar (Enfoque McKee)"""
        messages = {
            "ready": "✅ Listo para crear escenas",
            "waiting": "⏳ Preparando el editor...",
            "success": f"🎬 {details}",
            "error": f"⚠️ {details} - intenta de nuevo",
            "validation": f"📝 {details}",
            "conflict": f"⚡ {details}"
        }
        return messages.get(message_type, details)
    
    def get_scene_name_safely():
        """Obtiene el nombre de forma segura, con fallbacks claros (Enfoque Rothamel)"""
        try:
            # Intento principal: variable global (más confiable)
            scene_name = getattr(renpy.store, 'new_scene_name', "")
            if scene_name and scene_name.strip():
                print(f"🔍 Debug: Usando variable global: '{scene_name.strip()}'")
                return scene_name.strip()
        except Exception as e:
            print(f"🔍 Debug: Error obteniendo variable global: {e}")

        try:
            # Fallback 1: variable de pantalla
            scene_name = renpy.get_screen_variable("new_scene_name", "")
            if scene_name and scene_name.strip():
                print(f"🔍 Debug: Usando variable de pantalla: '{scene_name.strip()}'")
                return scene_name.strip()
        except Exception as e:
            print(f"🔍 Debug: Error obteniendo variable de pantalla: {e}")
            
        try:
            # Fallback 2: Variable global alternativa
            scene_name = getattr(renpy.store, 'new_scene_name_global', "")
            if scene_name and scene_name.strip():
                print(f"🔍 Debug: Usando fallback global: '{scene_name.strip()}'")
                return scene_name.strip()
        except Exception as e:
            print(f"🔍 Debug: Error en fallback global: {e}")
            pass
        
        # Fallback 2: Verificar si el campo está activo pero vacío
        try:
            scene_name_active = renpy.get_screen_variable("scene_name_active", False)
            print(f"🔍 Debug: Fallback 2 - scene_name_active: {scene_name_active} (tipo: {type(scene_name_active)})")
            
            # Verificar que scene_name_active sea un booleano válido
            if isinstance(scene_name_active, bool) and scene_name_active:
                # Si está activo, dar una segunda oportunidad
                scene_name = renpy.get_screen_variable("new_scene_name", "")
                print(f"🔍 Debug: Fallback 2 - segunda oportunidad: '{scene_name}' (tipo: {type(scene_name)})")
                if scene_name and scene_name.strip():
                    return scene_name.strip()
            else:
                print(f"🔍 Debug: Fallback 2 - scene_name_active no es True: {scene_name_active}")
        except Exception as e:
            print(f"🔍 Debug: Error en fallback 2: {e}")
            pass
        
        # Fallback 3: Valor por defecto con mensaje de debug
        print(f"🔍 Debug: No se pudo obtener nombre de escena, devolviendo vacío")
        return ""
    
    def validate_scene_name(name):
        """Validación que cuenta una historia (Enfoque McKee)"""
        print(f"🔍 Debug: Validando nombre: '{name}' (tipo: {type(name)})")
        
        if not name:
            print(f"🔍 Debug: Nombre es None o vacío")
            return False, "El nombre está vacío"
        
        if not name.strip():
            print(f"🔍 Debug: Nombre solo contiene espacios")
            return False, "El nombre está vacío"
        
        if len(name.strip()) > 50:
            print(f"🔍 Debug: Nombre demasiado largo: {len(name.strip())} caracteres")
            return False, "El nombre es demasiado largo (máximo 50 caracteres)"
        
        # Verificar si ya existe en la sesión actual
        try:
            created_scenes = renpy.get_screen_variable("created_scenes_in_modal", [])
            if created_scenes and name.strip() in created_scenes:
                print(f"🔍 Debug: Nombre ya existe en la sesión")
                return False, "Ya existe una escena con ese nombre en esta sesión"
        except:
            pass
        
        print(f"🔍 Debug: Nombre válido: '{name.strip()}'")
        return True, "Nombre válido"
    
    def is_modal_ready():
        """Verificación de estado simple pero efectiva"""
        try:
            # Verificar si la pantalla modal está activa
            test_var = renpy.get_screen_variable("new_scene_name", None)
            return test_var is not None
        except:
            return False
    
    def get_created_scenes_safely():
        """Obtiene la lista de escenas creadas de forma segura"""
        try:
            created_scenes = renpy.get_screen_variable("created_scenes_in_modal")
            if created_scenes is None:
                created_scenes = []
            return created_scenes
        except:
            # Fallback: variable global
            if hasattr(renpy.store, 'created_scenes_modal_global'):
                return renpy.store.created_scenes_modal_global
            return []
    
    def update_created_scenes_safely(created_scenes):
        """Actualiza la lista de escenas de forma segura"""
        try:
            renpy.set_screen_variable("created_scenes_in_modal", created_scenes)
        except:
            # Fallback: variable global
            renpy.store.created_scenes_modal_global = created_scenes
                
    def clear_scene_input_safely():
        """Limpia el campo de entrada de forma segura"""
        try:
            renpy.set_screen_variable("new_scene_name", "")
            renpy.set_screen_variable("scene_name_active", False)
            print(f"🔍 Debug: Campo limpiado exitosamente")
        except Exception as e:
            print(f"🔍 Debug: Error limpiando campo: {e}")
            # Fallback: limpiar variables globales
            try:
                renpy.store.new_scene_name_global = ""
                renpy.store.scene_name_active_global = False
                print(f"🔍 Debug: Variables globales limpiadas como fallback")
            except:
                print(f"🔍 Debug: Fallback de limpieza también falló")
    
    def sync_scene_variables():
        """Sincroniza las variables de pantalla con las globales"""
        try:
            # Sincronizar new_scene_name desde pantalla a global
            try:
                screen_name = renpy.get_screen_variable("new_scene_name", "")
                renpy.store.new_scene_name = screen_name
                renpy.store.new_scene_name_global = screen_name
                print(f"🔍 Debug: new_scene_name sincronizado desde pantalla: '{screen_name}'")
            except Exception as e:
                print(f"🔍 Debug: Error sincronizando new_scene_name desde pantalla: {e}")
            
            # Sincronizar scene_name_active
            try:
                screen_active = renpy.get_screen_variable("scene_name_active", False)
                renpy.store.scene_name_active = screen_active
                renpy.store.scene_name_active_global = screen_active
                print(f"🔍 Debug: scene_name_active sincronizado desde pantalla: {screen_active}")
            except Exception as e:
                print(f"🔍 Debug: Error sincronizando scene_name_active desde pantalla: {e}")
            
            # Sincronizar desde global a pantalla (si es necesario)
            try:
                global_name = getattr(renpy.store, 'new_scene_name', "")
                if global_name and global_name.strip():
                    renpy.set_screen_variable("new_scene_name", global_name)
                    print(f"🔍 Debug: new_scene_name sincronizado desde global: '{global_name}'")
            except Exception as e:
                print(f"🔍 Debug: Error sincronizando new_scene_name desde global: {e}")
                
        except Exception as e:
            print(f"🔍 Debug: Error en sincronización: {e}")
    
    def activate_scene_name_edit():
        """Activa el campo de edición del nombre de la escena"""
        try:
            print(f"🔍 Debug: Activando edición del nombre...")
            
            # Activar el campo de forma segura
            try:
                renpy.set_screen_variable("scene_name_active", True)
                renpy.store.scene_name_active = True
                renpy.store.scene_name_active_global = True
                print(f"🔍 Debug: Campo activado, scene_name_active = True (pantalla y global)")
            except Exception as e:
                print(f"🔍 Debug: Error activando campo: {e}")
                # Fallback: usar variable global
                try:
                    renpy.store.scene_name_active = True
                    renpy.store.scene_name_active_global = True
                    print(f"🔍 Debug: Usando fallback global para activar campo")
                except:
                    print(f"🔍 Debug: Fallback global también falló")
                    renpy.notify(create_clear_notification("error", "Error activando edición"))
                    return
            
            renpy.notify("✏️ Campo de nombre activado - escribe el nombre y haz clic en 'Aceptar'")
            print(f"🔍 Debug: Activación completada exitosamente")
            
            # Sincronizar variables
            sync_scene_variables()
            
        except Exception as e:
            print(f"🔍 Debug: Error en activate_scene_name_edit: {e}")
            renpy.notify(create_clear_notification("error", "Error activando edición"))
    
    def accept_scene_name():
        """Acepta y guarda el nombre de la escena"""
        try:
            print(f"🔍 Debug: Aceptando nombre de escena...")
            
            # Obtener el nombre actual usando el patrón seguro
            current_name = get_scene_name_safely()
            print(f"🔍 Debug: Nombre actual obtenido de forma segura: '{current_name}'")
            
            # Desactivar el campo de forma segura
            try:
                renpy.set_screen_variable("scene_name_active", False)
                print(f"🔍 Debug: Campo desactivado, scene_name_active = False")
            except Exception as e:
                print(f"🔍 Debug: Error desactivando campo: {e}")
                # Continuar aunque falle la desactivación
            
            if current_name and current_name.strip():
                renpy.notify(f"✅ Nombre guardado: '{current_name.strip()}'")
                print(f"🔍 Debug: Nombre guardado exitosamente")
                
                # Sincronizar variables después de guardar
                sync_scene_variables()
            else:
                renpy.notify("⚠️ Nombre vacío - escribe algo antes de aceptar")
                print(f"🔍 Debug: Nombre vacío detectado")
                
        except Exception as e:
            print(f"🔍 Debug: Error en accept_scene_name: {e}")
            renpy.notify(create_clear_notification("error", "Error guardando nombre"))

    def add_scene_to_modal():
        """Agrega una escena a la lista con enfoque híbrido McKee-Rothamel"""
        
        print(f"🔍 Debug: Iniciando add_scene_to_modal()")
        
        # PLANTEAMIENTO: Verificar el estado del mundo
        if not is_modal_ready():
            print(f"🔍 Debug: Modal no está lista")
            renpy.notify(create_clear_notification("waiting", "El editor se está preparando..."))
            scene_creation_state.mark_error()
            return
        
        print(f"🔍 Debug: Modal está lista, obteniendo nombre...")
        
        # Obtener el nombre de la escena de forma segura
        scene_name = get_scene_name_safely()
        print(f"🔍 Debug: Nombre obtenido: '{scene_name}' (tipo: {type(scene_name)})")
        
        # CONFLICTO: Validación narrativa
        print(f"🔍 Debug: Iniciando validación...")
        is_valid, message = validate_scene_name(scene_name)
        print(f"🔍 Debug: Resultado validación: {is_valid} - {message}")
        
        if not is_valid:
            print(f"🔍 Debug: Validación falló: {message}")
            renpy.notify(create_clear_notification("validation", message))
            return
        
        # RESOLUCIÓN: Creación con manejo de errores
        try:
            print(f"🔍 Debug: Creando nueva escena en carpeta scenes/...")
            
            # Crear nombre de archivo seguro
            safe_name = scene_name.lower().replace(" ", "_").replace("-", "_")
            safe_name = ''.join(c for c in safe_name if c.isalnum() or c == '_')
            
            # Crear archivo individual en carpeta scenes/
            import os
            scenes_dir = os.path.join(config.gamedir, "scenes")
            
            if not os.path.exists(scenes_dir):
                print(f"🔍 Debug: Creando carpeta scenes/...")
                os.makedirs(scenes_dir)
            
            # Generar nombre único para el archivo
            scene_filename = f"{safe_name}.rpy"
            scene_filepath = os.path.join(scenes_dir, scene_filename)
            
            # Verificar si el archivo ya existe
            counter = 1
            while os.path.exists(scene_filepath):
                scene_filename = f"{safe_name}_{counter}.rpy"
                scene_filepath = os.path.join(scenes_dir, scene_filename)
                counter += 1
            
            # Crear contenido de la escena
            scene_content = [
                f"# {scene_name}.rpy",
                f"# Escena creada automáticamente por el Editor Visual",
                f"# Generado el: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                "",
                f"# Escena: {scene_name}",
                f"label {safe_name}:",
                f"    # Aquí puedes agregar el contenido de la escena",
                f"    # Por ejemplo:",
                f"    # scene bg room",
                f"    # show eileen happy at center",
                f"    # eileen \"¡Hola! Esta es la escena {scene_name}\"",
                f"    ",
                f"    # Contenido de la escena se agregará aquí",
                f"    ",
                f"    return"
            ]
            
            # Escribir el archivo de la escena
            try:
                with open(scene_filepath, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(scene_content))
                
                print(f"🔍 Debug: Escena creada exitosamente: {scene_filename}")
                print(f"🔍 Debug: Ruta del archivo: {scene_filepath}")
                
                # Notificar éxito
                renpy.notify(create_clear_notification("success", f"Escena '{scene_name}' creada en scenes/{scene_filename}"))
                
            except Exception as file_error:
                print(f"🔍 Debug: Error creando archivo de escena: {file_error}")
                renpy.notify(create_clear_notification("error", f"Error creando archivo de escena: {file_error}"))
                return
            
            # Obtener la lista actual de escenas para la modal
            created_scenes = get_created_scenes_safely()
            
            # Agregar la nueva escena a la lista de la modal
            created_scenes.append(scene_name)
            
            # Actualizar la lista de forma segura
            update_created_scenes_safely(created_scenes)
            
            # Marcar la escena como creada para seguimiento de limpieza
            mark_scene_as_created(scene_name)
            
            # Limpiar el campo de entrada
            clear_scene_input_safely()
            
            # Marcar como exitoso
            scene_creation_state.mark_ready()
            
            # Notificar éxito
            renpy.notify(create_clear_notification("success", f"Escena '{scene_name}' creada y guardada"))
            
        except Exception as e:
            # Manejo específico del error "Screen is not showing"
            if "Screen is not showing" in str(e):
                renpy.notify(create_clear_notification("conflict", "Error de sincronización - intenta de nuevo"))
                scene_creation_state.mark_error()
            else:
                renpy.notify(create_clear_notification("error", "Error inesperado al crear la escena"))
                print(f"🔍 Debug: Error completo en add_scene_to_modal: {e}")
                scene_creation_state.mark_error()
    
    def accept_modal_scenes():
        """Acepta todas las escenas creadas en la modal con enfoque híbrido McKee-Rothamel"""
        
        # PLANTEAMIENTO: Verificar qué escenas tenemos
        created_scenes = get_created_scenes_safely()

        if not created_scenes:
            renpy.notify(create_clear_notification("validation", "No hay escenas para guardar"))
            return
            
        # CONFLICTO: Procesar y guardar las escenas
        try:
            # Obtener las escenas existentes de forma segura
            try:
                all_scenes = renpy.get_screen_variable("all_scenes")
            except:
                all_scenes = {}
            
            # Si all_scenes es None, inicializar como diccionario vacío
            if all_scenes is None:
                all_scenes = {}
            
            # Agregar todas las escenas creadas en la modal
            scenes_added = 0
            for scene_name in created_scenes:
                if scene_name not in all_scenes:
                    all_scenes[scene_name] = []
                    scenes_added += 1
            
            # RESOLUCIÓN: Guardar y configurar
            try:
                # Guardar las escenas de forma segura
                renpy.set_screen_variable("all_scenes", all_scenes)
            except:
                # Fallback: usar variable global
                renpy.store.all_scenes_global = all_scenes
            
            # Si hay escenas creadas, establecer la primera como actual
            if created_scenes:
                try:
                    renpy.set_screen_variable("current_scene_name", created_scenes[0])
                    renpy.set_screen_variable("current_scenes", [])
                except:
                    # Fallback: usar variables globales
                    renpy.store.current_scene_name_global = created_scenes[0]
                    renpy.store.current_scenes_global = []
            
            # Ocultar la modal de forma segura
            try:
                renpy.hide_screen("new_scene_modal")
            except:
                pass  # Si no se puede ocultar, continuar
            
            # Notificar éxito
            renpy.notify(create_clear_notification("success", f"{scenes_added} escena(s) guardada(s) exitosamente"))
            
        except Exception as e:
            # Manejo específico del error "Screen is not showing"
            if "Screen is not showing" in str(e):
                renpy.notify(create_clear_notification("conflict", "Error de sincronización al guardar - intenta de nuevo"))
                scene_creation_state.mark_error()
            else:
                renpy.notify(create_clear_notification("error", "Error inesperado al guardar las escenas"))
            print(f"🔍 Debug: Error completo en accept_modal_scenes: {e}")
            scene_creation_state.mark_error()
    
    def cancel_modal_scenes():
        """Cancela la creación de escenas con enfoque híbrido McKee-Rothamel"""
        
        # PLANTEAMIENTO: Limpiar el estado
        try:
            # Limpiar todas las variables de la modal de forma segura
            clear_scene_input_safely()
            
            # Limpiar la lista de escenas creadas
            try:
                renpy.set_screen_variable("created_scenes_in_modal", [])
            except:
                # Fallback: limpiar variables globales
                if hasattr(renpy.store, 'created_scenes_modal_global'):
                    renpy.store.created_scenes_modal_global = []
            
            # CONFLICTO: Ocultar la modal
            try:
                renpy.hide_screen("new_scene_modal")
            except:
                pass  # Si no se puede ocultar, continuar
            
            # RESOLUCIÓN: Notificar cancelación
            renpy.notify(create_clear_notification("validation", "Creación de escenas cancelada"))
            
        except Exception as e:
            # Manejo específico del error "Screen is not showing"
            if "Screen is not showing" in str(e):
                renpy.notify(create_clear_notification("conflict", "Error de sincronización al cancelar - intenta de nuevo"))
                scene_creation_state.mark_error()
            else:
                renpy.notify(create_clear_notification("error", "Error inesperado al cancelar"))
            print(f"🔍 Debug: Error completo en cancel_modal_scenes: {e}")
            scene_creation_state.mark_error()

    def focus_simple_input():
        """Enfoca el campo de entrada de la ventana modal simple sin reiniciar"""
        try:
            # Simplemente notificar que el campo está listo para escribir
            renpy.notify("✏️ Campo de entrada listo - haz clic en el área de texto")
            return True
        except Exception as e:
            print(f"🔍 Error enfocando input: {e}")
            return False


