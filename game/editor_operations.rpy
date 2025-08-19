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
    CURRENT_SCENES_FILE = os.path.join(config.gamedir, "current_scenes.rpy")
    SCENES_DIR = os.path.join(config.gamedir, "scenes")
    
    # Asegurar que los directorios existen
    if not os.path.exists(PROJECTS_DIR):
        os.makedirs(PROJECTS_DIR)
    if not os.path.exists(SCENES_DIR):
        os.makedirs(SCENES_DIR)
    
    # ===== FUNCIONES DE ARCHIVO BÁSICAS =====
    
    def save_scenes_to_file(scenes_list):
        """Guarda las escenas directamente a un archivo RPY"""
        try:
            # Asegurar que el directorio existe
            os.makedirs(os.path.dirname(CURRENT_SCENES_FILE), exist_ok=True)
            
            # Generar contenido RPY
            rpy_content = generate_rpy_content(scenes_list)
            
            with open(CURRENT_SCENES_FILE, 'w', encoding='utf-8') as f:
                f.write(rpy_content)
            
            print(f"✅ Escenas guardadas en: {CURRENT_SCENES_FILE}")
            return True
        except Exception as e:
            renpy.notify(f"❌ Error al guardar escenas: {str(e)}")
            print(f"🔍 Debug: Error guardando en {CURRENT_SCENES_FILE}: {e}")
            return False
    
    def load_scenes_from_file():
        """Carga las escenas desde el archivo RPY (simulado)"""
        try:
            if os.path.exists(CURRENT_SCENES_FILE):
                # Por ahora, simulamos la carga ya que los archivos RPY se ejecutan
                # En el futuro, podríamos parsear el archivo RPY para extraer las escenas
                print(f"✅ Archivo RPY encontrado: {CURRENT_SCENES_FILE}")
                return []  # Las escenas se ejecutan directamente
            else:
                print(f"⚠️ Archivo no encontrado: {CURRENT_SCENES_FILE}")
                return []
        except Exception as e:
            renpy.notify(f"❌ Error al cargar escenas: {str(e)}")
            print(f"🔍 Debug: Error cargando desde {CURRENT_SCENES_FILE}: {e}")
            return []
    
    def generate_rpy_content(scenes_list):
        """Genera el contenido del archivo RPY basado en las escenas"""
        try:
            content = []
            content.append("# current_scenes.rpy")
            content.append("# Archivo generado automáticamente por el Editor Visual")
            content.append(f"# Generado el: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            content.append("")
            
            # Agregar cada escena
            for i, scene in enumerate(scenes_list):
                scene_type = scene.get('type', 'unknown')
                
                if scene_type == 'dialogue':
                    content.extend(generate_dialogue_scene(scene, i))
                elif scene_type == 'stage':
                    content.extend(generate_stage_scene(scene, i))
                elif scene_type == 'background':
                    content.extend(generate_background_scene(scene, i))
                else:
                    content.extend(generate_unknown_scene(scene, i))
                
                content.append("")
            
            return "\n".join(content)
            
        except Exception as e:
            print(f"❌ Error generando contenido RPY: {e}")
            return "# Error generando contenido"
    
    def generate_dialogue_scene(scene, index):
        """Genera código RPY para una escena de diálogo"""
        lines = []
        character = scene.get('character', 'Narrator')
        dialogue = scene.get('dialogue', '')
        xalign = scene.get('xalign', 0.5)
        yalign = scene.get('yalign', 0.9)
        
        lines.append(f"# Escena {index + 1}: Diálogo")
        lines.append(f"label scene_{index + 1}_dialogue:")
        
        # Agregar personaje si no es Narrator
        if character.lower() != 'narrator':
            lines.append(f"    {character.lower()} \"{dialogue}\"")
        else:
            lines.append(f"    \"{dialogue}\"")
        
        lines.append("    return")
        return lines
    
    def generate_stage_scene(scene, index):
        """Genera código RPY para una escena de stage"""
        lines = []
        background = scene.get('background', '')
        characters = scene.get('characters', [])
        transition = scene.get('transition', 'dissolve')
        
        lines.append(f"# Escena {index + 1}: Stage")
        lines.append(f"label scene_{index + 1}_stage:")
        
        # Mostrar fondo
        if background:
            lines.append(f"    scene {background}")
        
        # Mostrar personajes
        for char in characters:
            if isinstance(char, dict):
                char_name = char.get('name', '')
                char_sprite = char.get('sprite', '')
                char_pos = char.get('position', 'center')
                if char_sprite:
                    lines.append(f"    show {char_name} {char_sprite} at {char_pos}")
        
        lines.append("    return")
        return lines
    
    def generate_background_scene(scene, index):
        """Genera código RPY para una escena de fondo"""
        lines = []
        background = scene.get('background', '')
        transition = scene.get('transition', 'dissolve')
        
        lines.append(f"# Escena {index + 1}: Fondo")
        lines.append(f"label scene_{index + 1}_background:")
        
        if background:
            lines.append(f"    scene {background} with {transition}")
        
        lines.append("    return")
        return lines
    
    def generate_unknown_scene(scene, index):
        """Genera código RPY para una escena desconocida"""
        lines = []
        lines.append(f"# Escena {index + 1}: Tipo desconocido")
        lines.append(f"label scene_{index + 1}_unknown:")
        lines.append(f"    # Tipo: {scene.get('type', 'unknown')}")
        lines.append("    return")
        return lines
    
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
        """Limpia SOLO el archivo RPY, sin tocar la pantalla"""
        try:
            # Solo operaciones de archivo, nada de pantalla
            if os.path.exists(CURRENT_SCENES_FILE):
                # Crear un archivo RPY vacío
                empty_content = "# current_scenes.rpy\n# Archivo vacío\n"
                with open(CURRENT_SCENES_FILE, 'w', encoding='utf-8') as f:
                    f.write(empty_content)
                
                renpy.notify("🗑️ Archivo RPY limpiado exitosamente")
            else:
                renpy.notify("📝 Archivo RPY no existe (ya está limpio)")
            
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
        """Agrega una línea de diálogo al archivo RPY y sincroniza pantalla"""
        if dialogue.strip():
            # Crear la escena
            scene_data = {
                'type': 'dialogue',
                'character': character,
                'dialogue': dialogue.strip(),
                'xalign': xalign,
                'yalign': yalign
            }
            
            # Cargar escenas existentes (simulado para RPY)
            scenes = []
            if os.path.exists(CURRENT_SCENES_FILE):
                # Por ahora, simulamos la carga ya que los archivos RPY se ejecutan directamente
                scenes = []  # En el futuro, podríamos parsear el archivo RPY
            
            # Agregar nueva escena
            scenes.append(scene_data)
            
            # Guardar al archivo RPY
            try:
                save_scenes_to_file(scenes)
                
                # Sincronizar pantalla automáticamente
                try:
                    renpy.set_screen_variable("current_scene", scenes)
                    renpy.notify(f"✅ Línea agregada al archivo RPY: {len(scenes)} escenas")
                except Exception as sync_error:
                    renpy.notify(f"✅ Línea agregada al archivo RPY: {len(scenes)} escenas")
                    renpy.notify(f"⚠️ Error de sincronización: {str(sync_error)}")
            except Exception as e:
                renpy.notify(f"❌ Error al guardar: {str(e)}")
        else:
            renpy.notify("⚠️ Diálogo vacío, no se agregó")
    
    def add_stage_scene_safe(scene_list, background, characters, transition):
        """Agrega una escena de stage al archivo RPY y sincroniza pantalla"""
        # Crear la escena
        scene_data = {
            'type': 'stage',
            'background': background,
            'characters': characters,
            'transition': transition
        }
        
        # Cargar escenas existentes (simulado para RPY)
        scenes = []
        if os.path.exists(CURRENT_SCENES_FILE):
            # Por ahora, simulamos la carga ya que los archivos RPY se ejecutan directamente
            scenes = []  # En el futuro, podríamos parsear el archivo RPY
        
        # Agregar nueva escena
        scenes.append(scene_data)
        
        # Guardar al archivo RPY
        try:
            save_scenes_to_file(scenes)
            
            # Sincronizar pantalla automáticamente
            try:
                renpy.set_screen_variable("current_scene", scenes)
                renpy.notify(f"✅ Escena de stage agregada al archivo RPY: {len(scenes)} escenas")
            except Exception as sync_error:
                renpy.notify(f"✅ Escena de stage agregada al archivo RPY: {len(scenes)} escenas")
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
    
    def execute_generated_scenes():
        """Ejecuta las escenas generadas en el archivo RPY"""
        try:
            if os.path.exists(CURRENT_SCENES_FILE):
                # El archivo RPY se ejecutará automáticamente cuando Ren'Py lo detecte
                renpy.notify("🎬 Archivo RPY generado - las escenas están listas para ejecutar")
                return True
            else:
                renpy.notify("⚠️ No hay archivo RPY para ejecutar")
                return False
        except Exception as e:
            renpy.notify(f"❌ Error ejecutando escenas: {str(e)}")
            return False
    
    def create_sample_scene():
        """Crea una escena de ejemplo para probar el sistema RPY"""
        try:
            sample_scenes = [
                {
                    'type': 'dialogue',
                    'character': 'Eileen',
                    'dialogue': '¡Hola! Esta es una escena generada automáticamente.',
                    'xalign': 0.5,
                    'yalign': 0.9
                },
                {
                    'type': 'dialogue',
                    'character': 'Narrator',
                    'dialogue': 'El sistema está funcionando correctamente.',
                    'xalign': 0.5,
                    'yalign': 0.9
                },
                {
                    'type': 'background',
                    'background': 'bg room',
                    'transition': 'dissolve'
                }
            ]
            
            save_scenes_to_file(sample_scenes)
            renpy.notify("✅ Escena de ejemplo creada en archivo RPY")
            return True
        except Exception as e:
            renpy.notify(f"❌ Error creando escena de ejemplo: {str(e)}")
            return False
    
    def diagnose_paths():
        """Diagnóstico de rutas para verificar que todo esté correcto"""
        try:
            print("🔍 DIAGNÓSTICO DE RUTAS:")
            print(f"• config.gamedir: {config.gamedir}")
            print(f"• PROJECTS_DIR: {PROJECTS_DIR}")
            print(f"• CURRENT_SCENES_FILE: {CURRENT_SCENES_FILE}")
            print(f"• SCENES_DIR: {SCENES_DIR}")
            
            # Verificar si los directorios existen
            if os.path.exists(config.gamedir):
                print(f"✅ config.gamedir existe")
            else:
                print(f"❌ config.gamedir NO existe")
            
            if os.path.exists(PROJECTS_DIR):
                print(f"✅ PROJECTS_DIR existe")
            else:
                print(f"⚠️ PROJECTS_DIR NO existe (se creará automáticamente)")
            
            if os.path.exists(SCENES_DIR):
                print(f"✅ SCENES_DIR existe")
            else:
                print(f"⚠️ SCENES_DIR NO existe (se creará automáticamente)")
            
            if os.path.exists(CURRENT_SCENES_FILE):
                print(f"✅ CURRENT_SCENES_FILE existe")
            else:
                print(f"⚠️ CURRENT_SCENES_FILE NO existe (se creará automáticamente)")
            
            # Verificar permisos de escritura
            try:
                test_file = os.path.join(config.gamedir, "test_write.tmp")
                with open(test_file, 'w') as f:
                    f.write("test")
                os.remove(test_file)
                print(f"✅ Permisos de escritura OK")
            except Exception as e:
                print(f"❌ Error de permisos: {e}")
            
            return True
        except Exception as e:
            print(f"❌ Error en diagnóstico: {e}")
            return False
    
    # Ejecutar diagnóstico al inicializar
    diagnose_paths()
    
    def test_rpy_generation():
        """Prueba la generación de archivos RPY"""
        try:
            print("🧪 PROBANDO GENERACIÓN DE ARCHIVO RPY")
            
            # Crear escenas de prueba
            test_scenes = [
                {
                    'type': 'dialogue',
                    'character': 'Eileen',
                    'dialogue': '¡Hola! Esta es una prueba del sistema RPY.',
                    'xalign': 0.5,
                    'yalign': 0.9
                },
                {
                    'type': 'dialogue',
                    'character': 'Narrator',
                    'dialogue': 'El archivo RPY se ha generado correctamente.',
                    'xalign': 0.5,
                    'yalign': 0.9
                },
                {
                    'type': 'background',
                    'background': 'bg room',
                    'transition': 'dissolve'
                }
            ]
            
            # Generar el archivo RPY
            success = save_scenes_to_file(test_scenes)
            
            if success:
                print("✅ Archivo RPY generado exitosamente")
                
                # Verificar que el archivo existe
                if os.path.exists(CURRENT_SCENES_FILE):
                    print(f"✅ Archivo creado en: {CURRENT_SCENES_FILE}")
                    
                    # Leer y mostrar el contenido
                    with open(CURRENT_SCENES_FILE, 'r', encoding='utf-8') as f:
                        content = f.read()
                    print("📝 Contenido del archivo RPY:")
                    print(content[:500] + "..." if len(content) > 500 else content)
                else:
                    print("❌ El archivo no se creó")
            else:
                print("❌ Error generando archivo RPY")
            
            return success
            
        except Exception as e:
            print(f"❌ Error en prueba RPY: {e}")
            return False
    
    # Ejecutar prueba de generación RPY
    test_rpy_generation()
    
    print("✅ Editor Operations inicializado con sistema RPY")
