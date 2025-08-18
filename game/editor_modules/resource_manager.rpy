# resource_manager.rpy
# Módulo para gestión de recursos del editor visual

init -2 python:
    import os
    import shutil
    
    # El módulo tkinter es una herramienta del taller, no del escenario.
    # Su ausencia no debe demoler la estructura entera. Lo invocamos con cautela.
    _tkinter_available = False
    try:
        import tkinter as tk
        from tkinter import filedialog
        _tkinter_available = True
    except (ImportError, ModuleNotFoundError):
        # Si el espíritu de tkinter no responde, no insistimos.
        # La función de importación se convertirá en un eco silencioso.
        pass
    
    # Definir imágenes de fondo automáticamente
    def define_background_images():
        """Define todas las imágenes de fondo encontradas"""
        try:
            backgrounds_path = os.path.join(config.gamedir, "images", "backgrounds")
            if not os.path.isdir(backgrounds_path):
                return
            
            # Definir imágenes en la raíz
            for item in os.listdir(backgrounds_path):
                item_path = os.path.join(backgrounds_path, item)
                if os.path.isfile(item_path) and any(item.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.webp']):
                    image_name = f"bg_{item.split('.')[0]}"
                    renpy.image(image_name, item_path)
                    print(f"✅ Fondo definido: {image_name}")
            
            print(f"✅ Definición automática de fondos completada")
            
        except Exception as e:
            print(f"❌ Error definiendo fondos: {e}")
    
    # Definir sprites de personajes automáticamente
    def define_character_sprites():
        """Define todos los sprites de personajes encontrados"""
        try:
            characters_path = os.path.join(config.gamedir, "images", "character")
            if not os.path.isdir(characters_path):
                return
            
            character_sprites = {}
            
            # Recorrer directorios de personajes
            for char_dir in os.listdir(characters_path):
                char_path = os.path.join(characters_path, char_dir)
                if os.path.isdir(char_path):
                    char_name = char_dir.lower()
                    sprites = []
                    
                    # Buscar archivos de imagen en el directorio del personaje
                    for item in os.listdir(char_path):
                        item_path = os.path.join(char_path, item)
                        if os.path.isfile(item_path) and any(item.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.webp']):
                            sprite_name = item.split('.')[0]
                            sprites.append(sprite_name)
                            
                            # Definir la imagen en Ren'Py
                            image_name = f"{char_name}_{sprite_name}"
                            renpy.image(image_name, item_path)
                            print(f"✅ Sprite definido: {image_name}")
                    
                    character_sprites[char_name] = sprites
            
            # Hacer disponible globalmente
            renpy.store.character_sprites = character_sprites
            print(f"✅ Definición automática de sprites completada")
            
        except Exception as e:
            print(f"❌ Error definiendo sprites: {e}")
    
    # Función para seleccionar archivo con tkinter
    def select_file_with_tkinter(title="Seleccionar archivo", filetypes=None):
        """Selecciona un archivo usando tkinter"""
        if not _tkinter_available:
            print("❌ Tkinter no disponible para selección de archivos")
            return None
        
        try:
            root = tk.Tk()
            root.withdraw()  # Ocultar ventana principal
            
            if filetypes is None:
                filetypes = [
                    ("Imágenes", "*.png *.jpg *.jpeg *.webp"),
                    ("Todos los archivos", "*.*")
                ]
            
            filename = filedialog.askopenfilename(
                title=title,
                filetypes=filetypes
            )
            
            root.destroy()
            return filename if filename else None
            
        except Exception as e:
            print(f"❌ Error seleccionando archivo: {e}")
            return None
    
    # Función para copiar archivo a directorio de imágenes
    def copy_file_to_images(source_path, target_subdir="backgrounds"):
        """Copia un archivo al directorio de imágenes"""
        try:
            if not source_path or not os.path.exists(source_path):
                print("❌ Archivo fuente no válido")
                return None
            
            # Crear directorio de destino si no existe
            target_dir = os.path.join(config.gamedir, "images", target_subdir)
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)
            
            # Obtener nombre del archivo
            filename = os.path.basename(source_path)
            target_path = os.path.join(target_dir, filename)
            
            # Copiar archivo
            shutil.copy2(source_path, target_path)
            print(f"✅ Archivo copiado: {filename}")
            
            return filename
            
        except Exception as e:
            print(f"❌ Error copiando archivo: {e}")
            return None
    
    # Función para obtener lista de fondos disponibles
    def get_available_backgrounds():
        """Obtiene la lista de fondos disponibles"""
        try:
            backgrounds = []
            backgrounds_path = os.path.join(config.gamedir, "images", "backgrounds")
            
            if os.path.isdir(backgrounds_path):
                for item in os.listdir(backgrounds_path):
                    item_path = os.path.join(backgrounds_path, item)
                    if os.path.isfile(item_path) and any(item.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.webp']):
                        backgrounds.append(item)
            
            return sorted(backgrounds)
            
        except Exception as e:
            print(f"❌ Error obteniendo fondos: {e}")
            return []
    
    # Función para obtener lista de personajes disponibles
    def get_available_characters():
        """Obtiene la lista de personajes disponibles"""
        try:
            characters = []
            characters_path = os.path.join(config.gamedir, "images", "character")
            
            if os.path.isdir(characters_path):
                for item in os.listdir(characters_path):
                    item_path = os.path.join(characters_path, item)
                    if os.path.isdir(item_path):
                        characters.append(item)
            
            return sorted(characters)
            
        except Exception as e:
            print(f"❌ Error obteniendo personajes: {e}")
            return []
    
    # Función para obtener sprites de un personaje
    def get_character_sprites(character_name):
        """Obtiene los sprites disponibles para un personaje"""
        try:
            if not hasattr(renpy.store, 'character_sprites'):
                define_character_sprites()
            
            character_sprites = getattr(renpy.store, 'character_sprites', {})
            return character_sprites.get(character_name.lower(), [])
            
        except Exception as e:
            print(f"❌ Error obteniendo sprites: {e}")
            return []
    
    # Función para importar imagen desde archivo
    def import_image_to_backgrounds():
        """Importa una imagen al directorio de fondos"""
        try:
            if not _tkinter_available:
                print("❌ Tkinter no disponible para importación")
                return False
            
            filename = select_file_with_tkinter(
                title="Seleccionar imagen de fondo",
                filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.webp")]
            )
            
            if filename:
                copied_file = copy_file_to_images(filename, "backgrounds")
                if copied_file:
                    # Redefinir fondos
                    define_background_images()
                    print(f"✅ Fondo importado: {copied_file}")
                    return True
            
            return False
            
        except Exception as e:
            print(f"❌ Error importando imagen: {e}")
            return False
    
    # Función para importar sprite de personaje
    def import_sprite_to_character(character_name):
        """Importa un sprite al directorio de un personaje"""
        try:
            if not _tkinter_available:
                print("❌ Tkinter no disponible para importación")
                return False
            
            filename = select_file_with_tkinter(
                title=f"Seleccionar sprite para {character_name}",
                filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.webp")]
            )
            
            if filename:
                copied_file = copy_file_to_images(filename, f"character/{character_name}")
                if copied_file:
                    # Redefinir sprites
                    define_character_sprites()
                    print(f"✅ Sprite importado: {copied_file}")
                    return True
            
            return False
            
        except Exception as e:
            print(f"❌ Error importando sprite: {e}")
            return False
    
    # Inicializar recursos al cargar el módulo
    define_background_images()
    define_character_sprites()
    
    print("✅ Módulo de gestión de recursos cargado")
