# Editor Operations - Operaciones del Editor Visual
# Este archivo contiene todas las operaciones críticas del editor
# para evitar reinicios del juego cuando ocurren errores

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
    
    # ===== FUNCIONES DE ARCHIVO BÁSICAS =====
    
    def save_scenes_to_file(scenes_list):
        """Guarda las escenas directamente a un archivo JSON"""
        try:
            with open(CURRENT_SCENES_FILE, 'w', encoding='utf-8') as f:
                json.dump(scenes_list, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            renpy.notify(f"❌ Error al guardar escenas: {str(e)}")
            return False
    
    def load_scenes_from_file():
        """Carga las escenas desde el archivo JSON"""
        try:
            if os.path.exists(CURRENT_SCENES_FILE):
                with open(CURRENT_SCENES_FILE, 'r', encoding='utf-8') as f:
                    scenes = json.load(f)
                return scenes
            else:
                return []
        except Exception as e:
            renpy.notify(f"❌ Error al cargar escenas: {str(e)}")
            return []
    
    def get_current_scenes():
        """Obtiene las escenas actuales desde el archivo"""
        return load_scenes_from_file()
    
    def add_scene_to_file(scene_data):
        """Agrega una escena al archivo"""
        try:
            scenes = load_scenes_from_file()
            scenes.append(scene_data)
            save_scenes_to_file(scenes)
            return True
        except Exception as e:
            renpy.notify(f"❌ Error al agregar escena: {str(e)}")
            return False
    
    # ===== FUNCIONES DE LIMPIEZA SIN PANTALLA =====
    
    def clear_scenes_file_safe():
        """Limpia SOLO el archivo, sin tocar la pantalla"""
        try:
            # Solo operaciones de archivo, nada de pantalla
            if os.path.exists(CURRENT_SCENES_FILE):
                # Crear un archivo vacío directamente
                empty_data = []
                with open(CURRENT_SCENES_FILE, 'w', encoding='utf-8') as f:
                    json.dump(empty_data, f, ensure_ascii=False, indent=2)
                
                renpy.notify("🗑️ Archivo limpiado exitosamente")
            else:
                renpy.notify("📝 Archivo no existe (ya está limpio)")
            
            return True
                
        except Exception as e:
            renpy.notify(f"❌ Error al limpiar archivo: {str(e)}")
            return False
    
    # ===== FUNCIONES DE INICIALIZACIÓN SIN PANTALLA =====
    
    def initialize_editor_safe():
        """Inicialización segura del editor - SOLO archivo"""
        try:
            # Solo cargar escenas del archivo, sin actualizar pantalla
            scenes = get_current_scenes()
            
            renpy.notify(f"✅ Editor inicializado con {len(scenes)} escenas en archivo")
            return True
            
        except Exception as e:
            renpy.notify(f"❌ Error en inicialización: {str(e)}")
            return False
    
    # ===== FUNCIONES DE AGREGADO SIN PANTALLA =====
    
    def add_dialogue_line_safe(scene_list, character, dialogue, xalign, yalign):
        """Agrega una línea de diálogo al archivo y sincroniza pantalla"""
        if dialogue.strip():
            # Crear la escena
            scene_data = {
                'type': 'dialogue',
                'character': character,
                'dialogue': dialogue.strip(),
                'xalign': xalign,
                'yalign': yalign
            }
            
            # Cargar escenas existentes
            scenes = []
            if os.path.exists(CURRENT_SCENES_FILE):
                with open(CURRENT_SCENES_FILE, 'r', encoding='utf-8') as f:
                    scenes = json.load(f)
            
            # Agregar nueva escena
            scenes.append(scene_data)
            
            # Guardar al archivo
            try:
                with open(CURRENT_SCENES_FILE, 'w', encoding='utf-8') as f:
                    json.dump(scenes, f, ensure_ascii=False, indent=2)
                
                # Sincronizar pantalla automáticamente
                try:
                    renpy.set_screen_variable("current_scene", scenes)
                    renpy.notify(f"✅ Línea agregada y sincronizada: {len(scenes)} escenas")
                except Exception as sync_error:
                    renpy.notify(f"✅ Línea agregada: {len(scenes)} escenas (sincronizar manualmente)")
                    renpy.notify(f"⚠️ Error de sincronización: {str(sync_error)}")
            except Exception as e:
                renpy.notify(f"❌ Error al guardar: {str(e)}")
        else:
            renpy.notify("⚠️ Diálogo vacío, no se agregó")
    
    def add_stage_scene_safe(scene_list, background, characters, transition):
        """Agrega una escena de stage al archivo y sincroniza pantalla"""
        # Crear la escena
        scene_data = {
            'type': 'stage',
            'background': background,
            'characters': characters,
            'transition': transition
        }
        
        # Cargar escenas existentes
        scenes = []
        if os.path.exists(CURRENT_SCENES_FILE):
            with open(CURRENT_SCENES_FILE, 'r', encoding='utf-8') as f:
                scenes = json.load(f)
        
        # Agregar nueva escena
        scenes.append(scene_data)
        
        # Guardar al archivo
        try:
            with open(CURRENT_SCENES_FILE, 'w', encoding='utf-8') as f:
                json.dump(scenes, f, ensure_ascii=False, indent=2)
            
            # Sincronizar pantalla automáticamente
            try:
                renpy.set_screen_variable("current_scene", scenes)
                renpy.notify(f"✅ Escena agregada y sincronizada: {len(scenes)} escenas")
            except Exception as sync_error:
                renpy.notify(f"✅ Escena agregada: {len(scenes)} escenas (sincronizar manualmente)")
                renpy.notify(f"⚠️ Error de sincronización: {str(sync_error)}")
        except Exception as e:
            renpy.notify(f"❌ Error al guardar: {str(e)}")
    
    # ===== FUNCIONES DE DIAGNÓSTICO SIN PANTALLA =====
    
    def full_diagnostic_safe():
        """Diagnóstico completo del sistema - SOLO archivo"""
        try:
            renpy.notify("🔍 DIAGNÓSTICO COMPLETO DEL SISTEMA")
            
            # 1. Verificar archivo de escenas
            if os.path.exists(CURRENT_SCENES_FILE):
                renpy.notify("✅ Archivo de escenas existe")
                scenes = load_scenes_from_file()
                renpy.notify(f"📊 Escenas en archivo: {len(scenes)}")
            else:
                renpy.notify("❌ Archivo de escenas no existe")
                scenes = []
            
            # 2. Verificar directorio de proyectos
            if os.path.exists(PROJECTS_DIR):
                renpy.notify("✅ Directorio de proyectos existe")
            else:
                renpy.notify("❌ Directorio de proyectos no existe")
            
            # 3. Probar escritura al archivo
            try:
                test_scene = {
                    'type': 'dialogue',
                    'character': 'Test',
                    'dialogue': 'Prueba de escritura',
                    'xalign': 0.5,
                    'yalign': 0.9
                }
                
                # Guardar escena de prueba
                save_scenes_to_file([test_scene])
                renpy.notify("✅ Escritura al archivo funciona")
                
                # Verificar que se guardó
                test_scenes = load_scenes_from_file()
                if len(test_scenes) > 0:
                    renpy.notify("✅ Lectura del archivo funciona")
                else:
                    renpy.notify("❌ Lectura del archivo falló")
                
                # Restaurar escenas originales
                save_scenes_to_file(scenes)
                
            except Exception as e:
                renpy.notify(f"❌ Error en prueba de archivo: {str(e)}")
            
            # 4. Verificar funciones disponibles
            renpy.notify("📋 Funciones del sistema:")
            try:
                # Probar get_current_scenes
                test_get = get_current_scenes()
                renpy.notify("   ✅ get_current_scenes() - funciona")
            except:
                renpy.notify("   ❌ get_current_scenes() - falló")
            
            try:
                # Probar add_scene_to_file
                test_scene = {
                    'type': 'dialogue',
                    'character': 'Test',
                    'dialogue': 'Prueba de función',
                    'xalign': 0.5,
                    'yalign': 0.9
                }
                test_result = add_scene_to_file(test_scene)
                if test_result:
                    renpy.notify("   ✅ add_scene_to_file() - funciona")
                else:
                    renpy.notify("   ❌ add_scene_to_file() - falló")
            except:
                renpy.notify("   ❌ add_scene_to_file() - error")
            
            # 5. Resumen
            renpy.notify(f"📊 RESUMEN: {len(scenes)} escenas en archivo")
            if len(scenes) > 0:
                renpy.notify("✅ Sistema funcionando - hay escenas guardadas")
            else:
                renpy.notify("⚠️ Sistema vacío - crea escenas para probar")
                
        except Exception as e:
            renpy.notify(f"❌ Error en diagnóstico: {str(e)}")
    
    def test_complete_flow_safe():
        """Prueba el flujo completo de agregado - SOLO archivo"""
        try:
            renpy.notify("🧪 PROBANDO FLUJO COMPLETO")
            
            # 1. Limpiar archivo
            clear_scenes_file_safe()
            renpy.notify("📝 Archivo limpiado")
            
            # 2. Verificar que está vacío
            scenes = get_current_scenes()
            renpy.notify(f"📊 Escenas iniciales: {len(scenes)}")
            
            # 3. Agregar escena usando add_dialogue_line_safe
            renpy.notify("➕ Agregando escena de prueba...")
            add_dialogue_line_safe([], "Eileen", "Esta es una prueba del flujo completo", 0.5, 0.9)
            
            # 4. Verificar que se agregó
            scenes_after = get_current_scenes()
            renpy.notify(f"📊 Escenas después de agregar: {len(scenes_after)}")
            
            # 5. Mostrar resultado
            if len(scenes_after) > len(scenes):
                renpy.notify("🎉 ¡FLUJO FUNCIONANDO!")
            else:
                renpy.notify("❌ FLUJO FALLÓ - no se agregó la escena")
                
        except Exception as e:
            renpy.notify(f"❌ Error en flujo: {str(e)}")
    
    def test_add_scene_directly_safe():
        """Prueba agregar una escena directamente al archivo"""
        try:
            renpy.notify("🧪 PRUEBA: Agregando escena al archivo")
            
            # Crear una escena de prueba
            test_scene = {
                'type': 'dialogue',
                'character': 'Eileen',
                'dialogue': 'Esta es una prueba directa al archivo',
                'xalign': 0.5,
                'yalign': 0.9
            }
            
            # Agregar al archivo
            success = add_scene_to_file(test_scene)
            
            if success:
                renpy.notify("✅ Escena agregada al archivo exitosamente")
                
                # Verificar que se guardó
                scenes = get_current_scenes()
                renpy.notify(f"📊 Verificación: {len(scenes)} escenas en archivo")
            else:
                renpy.notify("❌ Error al agregar escena al archivo")
                
        except Exception as e:
            renpy.notify(f"❌ Error en prueba: {str(e)}")
    
    def check_file_system_safe():
        """Verifica el sistema de archivos"""
        try:
            renpy.notify("📁 VERIFICANDO SISTEMA DE ARCHIVOS")
            
            # Verificar archivo de escenas
            if os.path.exists(CURRENT_SCENES_FILE):
                renpy.notify("✅ Archivo de escenas existe")
                scenes = load_scenes_from_file()
                renpy.notify(f"📊 Escenas en archivo: {len(scenes)}")
                
                # Mostrar contenido
                if len(scenes) > 0:
                    renpy.notify("📝 Contenido del archivo:")
                    for i, scene in enumerate(scenes[:3]):
                        if isinstance(scene, dict):
                            scene_type = scene.get('type', 'unknown')
                            if scene_type == 'dialogue':
                                char = scene.get('character', 'unknown')
                                text = scene.get('dialogue', '')[:30]
                                renpy.notify(f"   {i+1}. {char}: {text}...")
                            elif scene_type == 'stage':
                                bg = scene.get('background', 'unknown')
                                renpy.notify(f"   {i+1}. Escena: {bg}")
                else:
                    renpy.notify("📝 Archivo vacío")
            else:
                renpy.notify("❌ Archivo de escenas no existe")
            
            # Verificar directorio de proyectos
            if os.path.exists(PROJECTS_DIR):
                renpy.notify("✅ Directorio de proyectos existe")
                files = os.listdir(PROJECTS_DIR)
                renpy.notify(f"📊 Archivos en directorio: {len(files)}")
            else:
                renpy.notify("❌ Directorio de proyectos no existe")
                
        except Exception as e:
            renpy.notify(f"❌ Error al verificar archivos: {str(e)}")
    
    # ===== FUNCIÓN DE SINCRONIZACIÓN OPCIONAL =====
    
    def sync_screen_safe():
        """Sincroniza la pantalla con el archivo de forma segura"""
        try:
            # Cargar escenas del archivo
            scenes = get_current_scenes()
            
            # Intentar actualizar la pantalla de forma muy segura
            try:
                renpy.set_screen_variable("current_scene", scenes)
                renpy.notify(f"🔄 Pantalla sincronizada: {len(scenes)} escenas")
                return True
            except Exception as screen_error:
                renpy.notify("⚠️ No se pudo sincronizar la pantalla")
                return False
                
        except Exception as e:
            renpy.notify(f"❌ Error en sincronización: {str(e)}")
            return False
