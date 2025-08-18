# Editor Commands - Comandos del Editor Visual
# Este archivo usa un enfoque completamente diferente para evitar reinicios

init python:
    import os
    import json
    import shutil
    from datetime import datetime
    
    # Configuración del sistema
    PROJECTS_DIR = os.path.join(config.gamedir, "projects")
    CURRENT_SCENES_FILE = "current_scenes.json"
    
    # Asegurar que el directorio de proyectos existe
    if not os.path.exists(PROJECTS_DIR):
        os.makedirs(PROJECTS_DIR)
    
    # ===== FUNCIONES BÁSICAS DE ARCHIVO =====
    
    def clear_file_basic():
        """Limpia el archivo de forma básica"""
        try:
            if os.path.exists(CURRENT_SCENES_FILE):
                with open(CURRENT_SCENES_FILE, 'w', encoding='utf-8') as f:
                    json.dump([], f, ensure_ascii=False, indent=2)
                renpy.notify("🗑️ Archivo limpiado")
            else:
                renpy.notify("📝 Archivo no existe")
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
        """Agrega escena de prueba de forma básica"""
        try:
            test_scene = {
                'type': 'dialogue',
                'character': 'Eileen',
                'dialogue': 'Prueba básica al archivo',
                'xalign': 0.5,
                'yalign': 0.9
            }
            
            # Cargar escenas existentes
            scenes = []
            if os.path.exists(CURRENT_SCENES_FILE):
                with open(CURRENT_SCENES_FILE, 'r', encoding='utf-8') as f:
                    scenes = json.load(f)
            
            # Agregar nueva escena
            scenes.append(test_scene)
            
            # Guardar
            with open(CURRENT_SCENES_FILE, 'w', encoding='utf-8') as f:
                json.dump(scenes, f, ensure_ascii=False, indent=2)
            
            # Sincronizar pantalla automáticamente
            try:
                renpy.set_screen_variable("current_scene", scenes)
                renpy.notify(f"✅ Agregada y sincronizada: {len(scenes)} escenas")
            except:
                renpy.notify(f"✅ Agregada: {len(scenes)} escenas (sincronizar manualmente)")
        except Exception as e:
            renpy.notify(f"❌ Error: {str(e)}")
    
    def check_files_basic():
        """Verifica archivos de forma básica"""
        try:
            if os.path.exists(CURRENT_SCENES_FILE):
                with open(CURRENT_SCENES_FILE, 'r', encoding='utf-8') as f:
                    scenes = json.load(f)
                renpy.notify(f"📁 Archivo: {len(scenes)} escenas")
            else:
                renpy.notify("📁 Archivo: no existe")
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
