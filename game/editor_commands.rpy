# Editor Commands - Comandos del Editor Visual
# Este archivo usa un enfoque completamente diferente para evitar reinicios

init python:
    import os
    import json
    import shutil
    from datetime import datetime
    
    # Configuración del sistema
    PROJECTS_DIR = os.path.join(config.gamedir, "projects")
    CURRENT_SCENES_FILE = os.path.join(config.gamedir, "current_scenes.rpy")
    SCENES_DIR = os.path.join(config.gamedir, "scenes")
    
    # Asegurar que los directorios existen
    if not os.path.exists(PROJECTS_DIR):
        os.makedirs(PROJECTS_DIR)
    if not os.path.exists(SCENES_DIR):
        os.makedirs(SCENES_DIR)
    
    # ===== FUNCIONES BÁSICAS DE ARCHIVO =====
    
    def clear_file_basic():
        """Limpia el archivo RPY de forma básica"""
        try:
            if os.path.exists(CURRENT_SCENES_FILE):
                empty_content = "# current_scenes.rpy\n# Archivo vacío\n"
                with open(CURRENT_SCENES_FILE, 'w', encoding='utf-8') as f:
                    f.write(empty_content)
                renpy.notify("🗑️ Archivo RPY limpiado")
            else:
                renpy.notify("📝 Archivo RPY no existe")
        except Exception as e:
            renpy.notify(f"❌ Error: {str(e)}")
    
    def initialize_basic():
        """Inicializa el sistema de forma básica"""
        try:
            if os.path.exists(CURRENT_SCENES_FILE):
                with open(CURRENT_SCENES_FILE, 'r', encoding='utf-8') as f:
                    scenes = json.load(f)
                renpy.notify(f"✅ Sistema: {len(scenes)} escenas")
            else:
                renpy.notify("✅ Sistema: archivo vacío")
        except Exception as e:
            renpy.notify(f"❌ Error: {str(e)}")
    
    def add_test_basic():
        """Agrega escena de prueba de forma básica al archivo RPY"""
        try:
            # Crear contenido RPY de ejemplo
            rpy_content = """# current_scenes.rpy
# Archivo generado automáticamente por el Editor Visual
# Generado el: {datetime}

# Escena 1: Diálogo
label scene_1_dialogue:
    eileen "¡Hola! Esta es una escena de prueba generada automáticamente."
    return

# Escena 2: Diálogo del narrador
label scene_2_dialogue:
    "El sistema está funcionando correctamente."
    return

# Escena 3: Fondo
label scene_3_background:
    scene bg room with dissolve
    return
""".format(datetime=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            
            # Guardar el archivo RPY
            with open(CURRENT_SCENES_FILE, 'w', encoding='utf-8') as f:
                f.write(rpy_content)
            
            renpy.notify("✅ Archivo RPY de prueba creado exitosamente")
        except Exception as e:
            renpy.notify(f"❌ Error: {str(e)}")
    
    def check_files_basic():
        """Verifica archivos RPY de forma básica"""
        try:
            if os.path.exists(CURRENT_SCENES_FILE):
                with open(CURRENT_SCENES_FILE, 'r', encoding='utf-8') as f:
                    content = f.read()
                # Contar las líneas de label para estimar el número de escenas
                label_count = content.count('label ')
                renpy.notify(f"📁 Archivo RPY: {label_count} escenas encontradas")
            else:
                renpy.notify("📁 Archivo RPY: no existe")
        except Exception as e:
            renpy.notify(f"❌ Error: {str(e)}")
    
    def diagnostic_basic():
        """Diagnóstico básico"""
        try:
            renpy.notify("🔍 DIAGNÓSTICO BÁSICO")
            
            # Verificar archivo
            if os.path.exists(CURRENT_SCENES_FILE):
                with open(CURRENT_SCENES_FILE, 'r', encoding='utf-8') as f:
                    scenes = json.load(f)
                renpy.notify(f"✅ Archivo: {len(scenes)} escenas")
            else:
                renpy.notify("❌ Archivo: no existe")
            
            # Verificar directorio
            if os.path.exists(PROJECTS_DIR):
                renpy.notify("✅ Directorio: existe")
            else:
                renpy.notify("❌ Directorio: no existe")
        except Exception as e:
            renpy.notify(f"❌ Error: {str(e)}")
    
    def test_flow_basic():
        """Prueba flujo básico"""
        try:
            renpy.notify("🧪 FLUJO BÁSICO")
            
            # Limpiar
            clear_file_basic()
            
            # Agregar
            add_test_basic()
            
            renpy.notify("✅ Flujo completado")
        except Exception as e:
            renpy.notify(f"❌ Error: {str(e)}")
    
    def sync_screen_basic():
        """Sincroniza la pantalla con el archivo de forma básica"""
        try:
            if os.path.exists(CURRENT_SCENES_FILE):
                with open(CURRENT_SCENES_FILE, 'r', encoding='utf-8') as f:
                    scenes = json.load(f)
                
                # Actualizar la pantalla
                renpy.set_screen_variable("current_scene", scenes)
                renpy.notify(f"🔄 Pantalla actualizada: {len(scenes)} escenas")
            else:
                renpy.notify("📝 No hay archivo para sincronizar")
        except Exception as e:
            renpy.notify(f"❌ Error al sincronizar: {str(e)}")
