# Sistema de Guardado y Carga para el Editor Visual
# Archivo dedicado para operaciones de archivo

init python:
    import os
    import json
    from datetime import datetime
    
    # Obtener la ruta del directorio del proyecto actual
    def get_project_directory():
        """Obtiene el directorio del proyecto actual de forma segura"""
        try:
            # Obtener el directorio actual de trabajo
            current_dir = os.getcwd()
            
            # Verificar si estamos en un proyecto Ren'Py válido
            # Buscar hacia arriba en la jerarquía de directorios
            search_dir = current_dir
            max_levels = 10  # Máximo 10 niveles hacia arriba
            
            for level in range(max_levels):
                # Verificar si hay una carpeta 'game' con script.rpy
                game_dir = os.path.join(search_dir, 'game')
                script_path = os.path.join(game_dir, 'script.rpy')
                
                if os.path.exists(script_path):
                    return search_dir
                
                # Verificar si estamos en la carpeta 'game' y subir un nivel
                if os.path.basename(search_dir) == 'game':
                    parent_dir = os.path.dirname(search_dir)
                    script_path = os.path.join(search_dir, 'script.rpy')
                    if os.path.exists(script_path):
                        return parent_dir
                
                # Subir un nivel
                parent_dir = os.path.dirname(search_dir)
                if parent_dir == search_dir:  # Llegamos a la raíz del sistema
                    break
                search_dir = parent_dir
            
            # Si no encontramos un proyecto válido, usar el directorio actual
            return current_dir
                
        except Exception as e:
            # En caso de error, usar el directorio actual
            return os.getcwd()
    
    # Directorio para proyectos (en la raíz del proyecto)
    # FORZAR DIRECTORIO ESPECÍFICO - NO USAR DETECCIÓN AUTOMÁTICA
    PROJECT_DIR = "E:\\backups\\Ejemplo"  # RUTA FIJA PARA TU PROYECTO
    PROJECTS_DIR = os.path.join(PROJECT_DIR, "editor_projects")
    
    # Crear directorio de proyectos si no existe
    if not os.path.exists(PROJECTS_DIR):
        try:
            os.makedirs(PROJECTS_DIR)
        except:
            # Si falla, usar directorio actual como fallback
            PROJECT_DIR = os.getcwd()
            PROJECTS_DIR = os.path.join(PROJECT_DIR, "editor_projects")
    if not os.path.exists(PROJECTS_DIR):
        os.makedirs(PROJECTS_DIR)

    def save_project_quick():
        """Guarda las escenas de forma rápida"""
        try:
            renpy.notify("💾 Guardando...")
            
            # Cargar escenas del archivo temporal
            temp_file = "temp_scenes.json"
            try:
                if os.path.exists(temp_file):
                    with open(temp_file, 'r', encoding='utf-8') as f:
                        scenes = json.load(f)
                    renpy.notify(f"📂 Cargadas {len(scenes)} escenas del archivo temporal")
                else:
                    scenes = []
                    renpy.notify("📂 No hay archivo temporal")
            except Exception as e:
                scenes = []
                renpy.notify(f"❌ Error al cargar archivo temporal: {str(e)}")
            
            renpy.notify(f"📊 Escenas encontradas: {len(scenes)}")
            
            if not scenes:
                renpy.notify("⚠️ No hay escenas para guardar")
                return
            
            # SISTEMA DE SELECCIÓN MANUAL DE DIRECTORIO
            renpy.notify("📁 SELECCIÓN DE DIRECTORIO DE GUARDADO")
            
            # Opciones de directorio predefinidas
            desktop_dir = os.path.expanduser("~/Desktop")
            documents_dir = os.path.expanduser("~/Documents")
            current_dir = os.getcwd()
            
            # Mostrar opciones disponibles
            renpy.notify(f"1. Escritorio: {desktop_dir}")
            renpy.notify(f"2. Documentos: {documents_dir}")
            renpy.notify(f"3. Directorio actual: {current_dir}")
            renpy.notify("4. Directorio personalizado (E:\\backups\\Ejemplo)")
            
            # Por defecto, usar el directorio personalizado
            selected_dir = "E:\\backups\\Ejemplo"
            projects_subdir = "editor_projects"
            
            # Crear el directorio de proyectos
            save_dir = os.path.join(selected_dir, projects_subdir)
            
            renpy.notify(f"🔧 DIRECTORIO SELECCIONADO: {save_dir}")
            
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
                renpy.notify(f"📁 Directorio {save_dir} creado")
            else:
                renpy.notify(f"📁 Directorio {save_dir} ya existe")
            
            # Generar nombre
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(save_dir, f"proyecto_{timestamp}.rpy")
            renpy.notify(f"📄 Archivo a crear: {filename}")
            
            # Crear contenido básico
            content = f"""# Proyecto guardado
# Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# Escenas: {len(scenes)}

define e = Character("Eileen", color="#c8ffc8")
define narrator = Character(None, kind=nvl)

label start:
    $ renpy.block_rollback()
    
"""
            
            # Agregar escenas
            for i, scene in enumerate(scenes):
                scene_type = scene.get('type', 'dialogue')
                
                if scene_type == 'dialogue':
                    character = scene.get('character', 'narrator')
                    dialogue = scene.get('dialogue', '').replace('"', '\\"')
                    
                    if character == "Narrator":
                        content += f'    "{dialogue}"\n'
                    else:
                        content += f'    {character.lower()} "{dialogue}"\n'
                
                elif scene_type == 'stage':
                    background = scene.get('background', 'bg room')
                    content += f"    scene {background}\n"
            
            content += """    return
"""
            
            renpy.notify(f"📝 Contenido generado: {len(content)} caracteres")
            renpy.notify(f"📝 Escenas a guardar: {len(scenes)}")
            
            # Guardar
            renpy.notify(f"💾 Intentando guardar archivo...")
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                renpy.notify(f"✅ Archivo guardado exitosamente: {filename}")
                
                # Verificar que el archivo existe
                if os.path.exists(filename):
                    file_size = os.path.getsize(filename)
                    renpy.notify(f"✅ Archivo existe y tiene {file_size} bytes")
                else:
                    renpy.notify(f"❌ Archivo no existe después de guardar")
            except Exception as e:
                renpy.notify(f"❌ Error al escribir archivo: {str(e)}")
                return
            
        except Exception as e:
            renpy.notify(f"❌ Error: {str(e)}")

    def save_project_with_name(project_name):
        """Guarda con nombre específico"""
        try:
            renpy.notify("💾 Guardando...")
            
            # Cargar escenas del archivo temporal
            temp_file = "temp_scenes.json"
            try:
                if os.path.exists(temp_file):
                    with open(temp_file, 'r', encoding='utf-8') as f:
                        scenes = json.load(f)
                    renpy.notify(f"📂 Cargadas {len(scenes)} escenas del archivo temporal")
                else:
                    scenes = []
                    renpy.notify("📂 No hay archivo temporal")
            except Exception as e:
                scenes = []
                renpy.notify(f"❌ Error al cargar archivo temporal: {str(e)}")
            
            if not scenes:
                renpy.notify("⚠️ No hay escenas para guardar")
                return
            
            # Usar el directorio de proyectos configurado
            if not os.path.exists(PROJECTS_DIR):
                os.makedirs(PROJECTS_DIR)
            
            # Generar nombre seguro
            safe_name = "".join(c for c in project_name.strip() if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_name = safe_name.replace(' ', '_')
            filename = os.path.join(PROJECTS_DIR, f"{safe_name}.rpy")
            
            # Crear contenido básico
            content = f"""# Proyecto: {project_name}
# Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# Escenas: {len(scenes)}

define e = Character("Eileen", color="#c8ffc8")
define narrator = Character(None, kind=nvl)

label start:
    $ renpy.block_rollback()
    
"""
            
            # Agregar escenas
            for i, scene in enumerate(scenes):
                scene_type = scene.get('type', 'dialogue')
                
                if scene_type == 'dialogue':
                    character = scene.get('character', 'narrator')
                    dialogue = scene.get('dialogue', '').replace('"', '\\"')
                    
                    if character == "Narrator":
                        content += f'    "{dialogue}"\n'
                    else:
                        content += f'    {character.lower()} "{dialogue}"\n'
                
                elif scene_type == 'stage':
                    background = scene.get('background', 'bg room')
                    content += f"    scene {background}\n"
            
            content += """    return
"""
            
            # Guardar
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            
            renpy.notify(f"💾 Guardado como {safe_name}.rpy")
            
        except Exception as e:
            renpy.notify(f"❌ Error: {str(e)}")

    def load_project_from_file(filename):
        """Carga un proyecto desde archivo"""
        try:
            filepath = os.path.join(PROJECTS_DIR, f"{filename}.rpy")
            if not os.path.exists(filepath):
                renpy.notify(f"❌ Archivo {filename}.rpy no encontrado en {PROJECTS_DIR}")
                return False
            
            # Leer el archivo
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parsear el contenido y convertir a escenas
            scenes = []
            lines = content.split('\n')
            
            i = 0
            while i < len(lines):
                line = lines[i].strip()
                
                # Ignorar comentarios y líneas vacías
                if line.startswith('#') or not line:
                    i += 1
                    continue
                
                # Buscar diálogos
                if '"' in line and ('"' in line[line.find('"')+1:]):
                    # Es un diálogo
                    if line.startswith('    '):
                        line = line[4:]  # Remover indentación
                    
                    # Extraer personaje y diálogo
                    if ' "' in line:
                        # Formato: personaje "diálogo"
                        parts = line.split(' "', 1)
                        if len(parts) == 2:
                            character = parts[0].strip()
                            dialogue = parts[1].rstrip('"')
                            
                            # Convertir personajes especiales
                            if character.lower() in ['e', 'eileen']:
                                character = 'Eileen'
                            elif character.lower() in ['narrator', 'n']:
                                character = 'Narrator'
                            
                            scenes.append({
                                'type': 'dialogue',
                                'character': character,
                                'dialogue': dialogue,
                                'xalign': 0.5,
                                'yalign': 0.9
                            })
                    else:
                        # Formato: "diálogo" (narrator)
                        if line.startswith('"') and line.endswith('"'):
                            dialogue = line[1:-1]
                            scenes.append({
                                'type': 'dialogue',
                                'character': 'Narrator',
                                'dialogue': dialogue,
                                'xalign': 0.5,
                                'yalign': 0.9
                            })
                
                # Buscar escenas
                elif line.startswith('scene '):
                    if line.startswith('    '):
                        line = line[4:]  # Remover indentación
                    
                    background = line.replace('scene ', '').strip()
                    # Remover transiciones
                    if ' with ' in background:
                        background = background.split(' with ')[0]
                    
                    scenes.append({
                        'type': 'stage',
                        'background': background,
                        'transition': 'None',
                        'characters': []
                    })
                
                i += 1
            
            # Guardar al archivo temporal
            temp_file = "temp_scenes.json"
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(scenes, f, ensure_ascii=False, indent=2)
            
            # Actualizar pantalla
            renpy.set_screen_variable("current_scene", scenes)
            
            renpy.notify(f"📂 Cargado {filename}.rpy con {len(scenes)} escenas")
            return True
            
        except Exception as e:
            renpy.notify(f"❌ Error al cargar proyecto: {str(e)}")
            return False

    def get_projects_list():
        """Obtiene la lista de proyectos disponibles"""
        try:
            projects = []
            if os.path.exists(PROJECTS_DIR):
                rpy_files = [f for f in os.listdir(PROJECTS_DIR) if f.endswith('.rpy')]
                for file in rpy_files:
                    projects.append({
                        'name': file[:-4],
                        'filename': file[:-4],
                        'type': 'rpy',
                        'created_date': '',
                        'scene_count': 'Archivo .rpy'
                    })
            return projects
        except Exception as e:
            renpy.notify(f"❌ Error al obtener lista: {str(e)}")
            return []

    def test_file_system():
        """Prueba el sistema de archivos"""
        try:
            # Mostrar información del directorio del proyecto
            renpy.notify(f"🎮 Directorio del proyecto: {PROJECT_DIR}")
            renpy.notify(f"📁 Directorio de proyectos: {PROJECTS_DIR}")
            
            # Verificar directorio actual
            current_dir = os.getcwd()
            renpy.notify(f"📁 Directorio actual: {current_dir}")
            
            # Verificar si podemos crear archivos
            test_file = "test_write.txt"
            try:
                with open(test_file, 'w', encoding='utf-8') as f:
                    f.write("Prueba de escritura")
                renpy.notify(f"✅ Archivo de prueba creado: {test_file}")
                
                # Verificar que existe
                if os.path.exists(test_file):
                    renpy.notify(f"✅ Archivo existe: {test_file}")
                    # Eliminar archivo de prueba
                    os.remove(test_file)
                    renpy.notify(f"🗑️ Archivo de prueba eliminado")
                else:
                    renpy.notify(f"❌ Archivo no existe después de crear")
                    
            except Exception as e:
                renpy.notify(f"❌ Error al crear archivo de prueba: {str(e)}")
            
            # Verificar directorio editor_projects
            if os.path.exists(PROJECTS_DIR):
                renpy.notify(f"📁 Directorio {PROJECTS_DIR} existe")
                try:
                    files = os.listdir(PROJECTS_DIR)
                    renpy.notify(f"📂 Archivos en {PROJECTS_DIR}: {len(files)}")
                    for file in files:
                        renpy.notify(f"📄 {file}")
                except Exception as e:
                    renpy.notify(f"❌ Error al listar archivos: {str(e)}")
            else:
                renpy.notify(f"❌ Directorio {PROJECTS_DIR} no existe")
                
        except Exception as e:
            renpy.notify(f"❌ Error en prueba: {str(e)}")

    def show_project_info():
        """Muestra información sobre el directorio de proyectos"""
        try:
            # Información detallada de diagnóstico
            renpy.notify("🔍 DIAGNÓSTICO DEL SISTEMA DE ARCHIVOS")
            renpy.notify(f"📁 Directorio actual: {os.getcwd()}")
            
            if hasattr(config, 'gamedir'):
                renpy.notify(f"🎮 config.gamedir: {config.gamedir}")
            else:
                renpy.notify("❌ config.gamedir no disponible")
            
            renpy.notify(f"🎮 Directorio del proyecto detectado: {PROJECT_DIR}")
            renpy.notify(f"📁 Directorio de proyectos: {PROJECTS_DIR}")
            
            # Verificar estructura del proyecto
            game_script_path = os.path.join(PROJECT_DIR, 'game', 'script.rpy')
            if os.path.exists(game_script_path):
                renpy.notify("✅ Estructura de proyecto válida detectada")
            else:
                renpy.notify("⚠️ No se encontró game/script.rpy")
            
            if os.path.exists(PROJECTS_DIR):
                files = os.listdir(PROJECTS_DIR)
                renpy.notify(f"📂 Proyectos guardados: {len(files)}")
                if files:
                    for file in files[:5]:  # Mostrar solo los primeros 5
                        renpy.notify(f"📄 {file}")
                    if len(files) > 5:
                        renpy.notify(f"... y {len(files) - 5} más")
                else:
                    renpy.notify("📂 No hay proyectos guardados aún")
            else:
                renpy.notify("📁 El directorio de proyectos será creado automáticamente")
                
        except Exception as e:
            renpy.notify(f"❌ Error al mostrar información: {str(e)}")

    def diagnose_project_location():
        """Diagnóstico detallado de la ubicación del proyecto"""
        try:
            renpy.notify("🔍 DIAGNÓSTICO DETALLADO DE UBICACIÓN")
            
            # Información del directorio actual
            current_dir = os.getcwd()
            renpy.notify(f"📁 Directorio actual: {current_dir}")
            
            # Buscar proyectos Ren'Py en el directorio actual y padres
            search_dir = current_dir
            level = 0
            
            while level < 10:
                renpy.notify(f"🔍 Nivel {level}: {search_dir}")
                
                # Verificar si hay game/script.rpy
                game_dir = os.path.join(search_dir, 'game')
                script_path = os.path.join(game_dir, 'script.rpy')
                
                if os.path.exists(script_path):
                    renpy.notify(f"✅ ¡PROYECTO ENCONTRADO! en: {search_dir}")
                    return search_dir
                
                # Verificar si estamos en la carpeta 'game'
                if os.path.basename(search_dir) == 'game':
                    parent_dir = os.path.dirname(search_dir)
                    script_path = os.path.join(search_dir, 'script.rpy')
                    if os.path.exists(script_path):
                        renpy.notify(f"✅ ¡PROYECTO ENCONTRADO! (subiendo desde 'game'): {parent_dir}")
                        return parent_dir
                
                # Subir un nivel
                parent_dir = os.path.dirname(search_dir)
                if parent_dir == search_dir:
                    break
                search_dir = parent_dir
                level += 1
            
            renpy.notify("❌ No se encontró proyecto Ren'Py válido")
            return None
                
        except Exception as e:
            renpy.notify(f"❌ Error en diagnóstico: {str(e)}")
            return None

    def force_project_directory():
        """Fuerza el uso del directorio actual como proyecto"""
        global PROJECT_DIR, PROJECTS_DIR
        try:
            current_dir = os.getcwd()
            renpy.notify(f"🔧 Forzando directorio del proyecto a: {current_dir}")
            
            PROJECT_DIR = current_dir
            PROJECTS_DIR = os.path.join(PROJECT_DIR, "editor_projects")
            
            # Crear directorio si no existe
            if not os.path.exists(PROJECTS_DIR):
                os.makedirs(PROJECTS_DIR)
                renpy.notify(f"📁 Directorio creado: {PROJECTS_DIR}")
            
            renpy.notify("✅ Directorio del proyecto actualizado")
            
        except Exception as e:
            renpy.notify(f"❌ Error al forzar directorio: {str(e)}")

    def set_custom_project_directory(custom_path):
        """Establece un directorio personalizado para el proyecto"""
        global PROJECT_DIR, PROJECTS_DIR
        try:
            # Convertir a ruta absoluta
            if os.path.isabs(custom_path):
                project_dir = custom_path
            else:
                project_dir = os.path.abspath(custom_path)
            
            renpy.notify(f"🔧 Estableciendo directorio personalizado: {project_dir}")
            
            # Verificar que el directorio existe
            if not os.path.exists(project_dir):
                os.makedirs(project_dir)
                renpy.notify(f"📁 Directorio creado: {project_dir}")
            
            PROJECT_DIR = project_dir
            PROJECTS_DIR = os.path.join(PROJECT_DIR, "editor_projects")
            
            # Crear directorio de proyectos si no existe
            if not os.path.exists(PROJECTS_DIR):
                os.makedirs(PROJECTS_DIR)
                renpy.notify(f"📁 Directorio de proyectos creado: {PROJECTS_DIR}")
            
            renpy.notify("✅ Directorio personalizado establecido")
            
        except Exception as e:
            renpy.notify(f"❌ Error al establecer directorio: {str(e)}")

    def set_project_to_current_game():
        """Establece el directorio del proyecto al directorio actual del juego"""
        global PROJECT_DIR, PROJECTS_DIR
        try:
            # Obtener el directorio donde está el archivo script.rpy actual
            current_script = renpy.get_filename_line()[0]  # Obtiene el archivo actual
            if current_script:
                # Obtener el directorio del archivo actual
                script_dir = os.path.dirname(os.path.abspath(current_script))
                renpy.notify(f"📁 Archivo actual: {current_script}")
                renpy.notify(f"📁 Directorio del archivo: {script_dir}")
                
                # Si estamos en la carpeta 'game', subir un nivel
                if os.path.basename(script_dir) == 'game':
                    project_dir = os.path.dirname(script_dir)
                    renpy.notify(f"📁 Subiendo desde 'game' a: {project_dir}")
                else:
                    project_dir = script_dir
                    renpy.notify(f"📁 Usando directorio actual: {project_dir}")
                
                PROJECT_DIR = project_dir
                PROJECTS_DIR = os.path.join(PROJECT_DIR, "editor_projects")
                
                # Crear directorio si no existe
                if not os.path.exists(PROJECTS_DIR):
                    os.makedirs(PROJECTS_DIR)
                    renpy.notify(f"📁 Directorio creado: {PROJECTS_DIR}")
                
                renpy.notify("✅ Directorio del proyecto establecido correctamente")
            else:
                renpy.notify("❌ No se pudo obtener la ubicación del archivo actual")
                
        except Exception as e:
            renpy.notify(f"❌ Error al establecer directorio: {str(e)}")

    def set_project_to_specific_path():
        """Establece el directorio del proyecto a una ruta específica común"""
        global PROJECT_DIR, PROJECTS_DIR
        try:
            # Rutas comunes donde podrían estar los proyectos
            possible_paths = [
                "C:\\Users\\" + os.getenv('USERNAME', '') + "\\Desktop\\Ejemplo",
                "C:\\Users\\" + os.getenv('USERNAME', '') + "\\Documents\\Ejemplo",
                "E:\\backups\\Ejemplo\\game",
                "E:\\backups\\Ejemplo",
                os.path.dirname(os.getcwd()),  # Directorio padre del actual
            ]
            
            renpy.notify("🔍 Buscando proyecto en rutas comunes...")
            
            for path in possible_paths:
                if os.path.exists(path):
                    # Verificar si es un proyecto Ren'Py válido
                    if os.path.basename(path) == 'game':
                        # Estamos en la carpeta game, subir un nivel
                        project_dir = os.path.dirname(path)
                        script_path = os.path.join(path, 'script.rpy')
                    else:
                        # Verificar si hay una carpeta game
                        game_path = os.path.join(path, 'game')
                        script_path = os.path.join(game_path, 'script.rpy')
                        project_dir = path
                    
                    if os.path.exists(script_path):
                        renpy.notify(f"✅ Proyecto encontrado en: {project_dir}")
                        PROJECT_DIR = project_dir
                        PROJECTS_DIR = os.path.join(PROJECT_DIR, "editor_projects")
                        
                        if not os.path.exists(PROJECTS_DIR):
                            os.makedirs(PROJECTS_DIR)
                            renpy.notify(f"📁 Directorio creado: {PROJECTS_DIR}")
                        
                        renpy.notify("✅ Directorio del proyecto establecido")
                        return
            
            renpy.notify("❌ No se encontró proyecto en rutas comunes")
            
        except Exception as e:
            renpy.notify(f"❌ Error al buscar rutas: {str(e)}")

    def fix_renpy_sdk_issue():
        """Solución específica para el problema del SDK de Ren'Py"""
        global PROJECT_DIR, PROJECTS_DIR
        try:
            current_dir = os.getcwd()
            renpy.notify(f"🔧 SOLUCIÓN PARA SDK REN'PY")
            renpy.notify(f"📁 Directorio actual: {current_dir}")
            
            # Buscar el proyecto específico del usuario
            # Asumimos que el proyecto está en una carpeta específica del usuario
            user_desktop = os.path.expanduser("~/Desktop")
            user_documents = os.path.expanduser("~/Documents")
            
            # Buscar en ubicaciones comunes
            search_locations = [
                current_dir,  # Directorio actual
                user_desktop,  # Escritorio
                user_documents,  # Documentos
                os.path.dirname(current_dir),  # Directorio padre
            ]
            
            for location in search_locations:
                if os.path.exists(location):
                    # Buscar carpetas que contengan 'game' con script.rpy
                    try:
                        for item in os.listdir(location):
                            item_path = os.path.join(location, item)
                            if os.path.isdir(item_path):
                                game_path = os.path.join(item_path, 'game')
                                script_path = os.path.join(game_path, 'script.rpy')
                                if os.path.exists(script_path):
                                    renpy.notify(f"✅ Proyecto encontrado: {item_path}")
                                    PROJECT_DIR = item_path
                                    PROJECTS_DIR = os.path.join(PROJECT_DIR, "editor_projects")
                                    
                                    # Crear directorio si no existe
                                    if not os.path.exists(PROJECTS_DIR):
                                        os.makedirs(PROJECTS_DIR)
                                        renpy.notify(f"📁 Directorio creado: {PROJECTS_DIR}")
                                    
                                    renpy.notify("✅ Problema del SDK solucionado")
                                    return
                    except:
                        continue
            
            # Si no encontramos nada, usar el directorio actual
            renpy.notify("⚠️ No se encontró proyecto específico, usando directorio actual")
            PROJECT_DIR = current_dir
            PROJECTS_DIR = os.path.join(PROJECT_DIR, "editor_projects")
            
            if not os.path.exists(PROJECTS_DIR):
                os.makedirs(PROJECTS_DIR)
            
        except Exception as e:
            renpy.notify(f"❌ Error en solución SDK: {str(e)}")

    def set_to_ejemplo_project():
        """Establece específicamente el directorio del proyecto 'Ejemplo'"""
        global PROJECT_DIR, PROJECTS_DIR
        try:
            # Ruta específica del proyecto Ejemplo
            ejemplo_path = "E:\\backups\\Ejemplo"
            
            if os.path.exists(ejemplo_path):
                renpy.notify(f"✅ Proyecto 'Ejemplo' encontrado en: {ejemplo_path}")
                PROJECT_DIR = ejemplo_path
                PROJECTS_DIR = os.path.join(PROJECT_DIR, "editor_projects")
                
                # Crear directorio si no existe
                if not os.path.exists(PROJECTS_DIR):
                    os.makedirs(PROJECTS_DIR)
                    renpy.notify(f"📁 Directorio creado: {PROJECTS_DIR}")
                
                renpy.notify("✅ Directorio del proyecto 'Ejemplo' establecido")
            else:
                renpy.notify(f"❌ No se encontró el proyecto en: {ejemplo_path}")
                renpy.notify("🔍 Intentando buscar en otras ubicaciones...")
                set_project_to_specific_path()
            
        except Exception as e:
            renpy.notify(f"❌ Error al establecer proyecto 'Ejemplo': {str(e)}")

    def force_ejemplo_directory():
        """Fuerza el uso del directorio Ejemplo sin importar la detección"""
        global PROJECT_DIR, PROJECTS_DIR
        try:
            # FORZAR RUTA ESPECÍFICA
            PROJECT_DIR = "E:\\backups\\Ejemplo"
            PROJECTS_DIR = os.path.join(PROJECT_DIR, "editor_projects")
            
            renpy.notify(f"🔧 FORZANDO DIRECTORIO: {PROJECT_DIR}")
            renpy.notify(f"📁 DIRECTORIO DE PROYECTOS: {PROJECTS_DIR}")
            
            # Crear directorio si no existe
            if not os.path.exists(PROJECTS_DIR):
                os.makedirs(PROJECTS_DIR)
                renpy.notify(f"📁 Directorio creado: {PROJECTS_DIR}")
            else:
                renpy.notify(f"📁 Directorio ya existe: {PROJECTS_DIR}")
            
            # Verificar que podemos escribir en el directorio
            test_file = os.path.join(PROJECTS_DIR, "test_write.txt")
            try:
                with open(test_file, 'w', encoding='utf-8') as f:
                    f.write("Prueba de escritura")
                os.remove(test_file)
                renpy.notify("✅ Permisos de escritura verificados")
            except Exception as e:
                renpy.notify(f"❌ Error de permisos: {str(e)}")
            
            renpy.notify("✅ Directorio forzado exitosamente")
            
        except Exception as e:
            renpy.notify(f"❌ Error al forzar directorio: {str(e)}")

    def verify_current_directory():
        """Verifica el directorio actual del sistema"""
        try:
            renpy.notify("🔍 VERIFICACIÓN DE DIRECTORIO ACTUAL")
            renpy.notify(f"📁 PROJECT_DIR: {PROJECT_DIR}")
            renpy.notify(f"📁 PROJECTS_DIR: {PROJECTS_DIR}")
            renpy.notify(f"📁 Directorio actual de trabajo: {os.getcwd()}")
            
            if os.path.exists(PROJECTS_DIR):
                renpy.notify(f"✅ Directorio de proyectos existe: {PROJECTS_DIR}")
                files = os.listdir(PROJECTS_DIR)
                renpy.notify(f"📂 Archivos en el directorio: {len(files)}")
                for file in files:
                    renpy.notify(f"📄 {file}")
            else:
                renpy.notify(f"❌ Directorio de proyectos NO existe: {PROJECTS_DIR}")
            
            # Verificar si la ruta contiene "renpy" (motor)
            if "renpy" in PROJECT_DIR.lower():
                renpy.notify("⚠️ ¡ADVERTENCIA! El directorio contiene 'renpy' (motor)")
            else:
                renpy.notify("✅ Directorio no contiene 'renpy' (bueno)")
                
        except Exception as e:
            renpy.notify(f"❌ Error en verificación: {str(e)}")

    def set_save_to_desktop():
        """Establece el guardado en el escritorio"""
        global PROJECT_DIR, PROJECTS_DIR
        try:
            desktop_dir = os.path.expanduser("~/Desktop")
            PROJECT_DIR = desktop_dir
            PROJECTS_DIR = os.path.join(PROJECT_DIR, "editor_projects")
            
            if not os.path.exists(PROJECTS_DIR):
                os.makedirs(PROJECTS_DIR)
            
            renpy.notify(f"✅ Guardado configurado en: {PROJECTS_DIR}")
            
        except Exception as e:
            renpy.notify(f"❌ Error: {str(e)}")

    def set_save_to_documents():
        """Establece el guardado en documentos"""
        global PROJECT_DIR, PROJECTS_DIR
        try:
            documents_dir = os.path.expanduser("~/Documents")
            PROJECT_DIR = documents_dir
            PROJECTS_DIR = os.path.join(PROJECT_DIR, "editor_projects")
            
            if not os.path.exists(PROJECTS_DIR):
                os.makedirs(PROJECTS_DIR)
            
            renpy.notify(f"✅ Guardado configurado en: {PROJECTS_DIR}")
            
        except Exception as e:
            renpy.notify(f"❌ Error: {str(e)}")

    def set_save_to_current():
        """Establece el guardado en el directorio actual"""
        global PROJECT_DIR, PROJECTS_DIR
        try:
            current_dir = os.getcwd()
            PROJECT_DIR = current_dir
            PROJECTS_DIR = os.path.join(PROJECT_DIR, "editor_projects")
            
            if not os.path.exists(PROJECTS_DIR):
                os.makedirs(PROJECTS_DIR)
            
            renpy.notify(f"✅ Guardado configurado en: {PROJECTS_DIR}")
            
        except Exception as e:
            renpy.notify(f"❌ Error: {str(e)}")

    def show_save_options():
        """Muestra las opciones de guardado disponibles"""
        try:
            renpy.notify("📁 OPCIONES DE GUARDADO DISPONIBLES")
            renpy.notify("")
            renpy.notify("1. set_save_to_desktop() - Guardar en Escritorio")
            renpy.notify("2. set_save_to_documents() - Guardar en Documentos")
            renpy.notify("3. set_save_to_current() - Guardar en directorio actual")
            renpy.notify("4. set_custom_project_directory('ruta') - Ruta personalizada")
            renpy.notify("5. force_ejemplo_directory() - Forzar directorio Ejemplo")
            renpy.notify("")
            renpy.notify("📁 DIRECTORIO ACTUAL:")
            renpy.notify(f"   {PROJECTS_DIR}")
            
        except Exception as e:
            renpy.notify(f"❌ Error: {str(e)}")

    def reset_to_default_directory():
        """Resetea al directorio por defecto"""
        global PROJECT_DIR, PROJECTS_DIR
        try:
            # Recalcular el directorio del proyecto
            PROJECT_DIR = get_project_directory()
            PROJECTS_DIR = os.path.join(PROJECT_DIR, "editor_projects")
            
            # Crear directorio si no existe
            if not os.path.exists(PROJECTS_DIR):
                os.makedirs(PROJECTS_DIR)
            
            renpy.notify(f"🔄 Reseteado a directorio por defecto: {PROJECT_DIR}")
            
        except Exception as e:
            renpy.notify(f"❌ Error al resetear: {str(e)}")

# Panel de Opciones de Guardado y Carga
# Interfaz dedicada para gestionar proyectos

screen save_load_panel():
    modal True
    
    frame:
        style_prefix "save_load"
        xfill True
        yfill True
        background "#00000080"
        
        frame:
            xalign 0.5
            yalign 0.5
            xsize 800
            ysize 600
            background "#2a2a2a"
            padding (20, 20)
            
            vbox:
                spacing 20
                
                # Título
                label "💾 Panel de Guardado y Carga" xalign 0.5
                
                # Sección de Guardado
                frame:
                    background "#3a3a3a"
                    padding (15, 15)
                    
                    vbox:
                        spacing 10
                        
                        label "📁 OPCIONES DE GUARDADO" xalign 0.5
                        
                        # Opciones de directorio
                        hbox:
                            spacing 10
                            xfill True
                            
                            textbutton "🖥️ Escritorio" action Function(set_save_to_desktop):
                                style "save_load_button"
                                xsize 150
                            
                            textbutton "📄 Documentos" action Function(set_save_to_documents):
                                style "save_load_button"
                                xsize 150
                            
                            textbutton "📂 Actual" action Function(set_save_to_current):
                                style "save_load_button"
                                xsize 150
                        
                        hbox:
                            spacing 10
                            xfill True
                            
                            textbutton "🎯 Proyecto Ejemplo" action Function(force_ejemplo_directory):
                                style "save_load_button"
                                xsize 150
                            
                            textbutton "🔧 Personalizado" action Function(show_custom_path_input):
                                style "save_load_button"
                                xsize 150
                        
                        # Información del directorio actual
                        frame:
                            background "#1a1a1a"
                            padding (10, 10)
                            
                            vbox:
                                spacing 5
                                
                                text "📁 Directorio Actual:" size 16
                                text "[PROJECTS_DIR]" size 14 color "#888888"
                
                # Sección de Acciones
                frame:
                    background "#3a3a3a"
                    padding (15, 15)
                    
                    vbox:
                        spacing 10
                        
                        label "⚡ ACCIONES RÁPIDAS" xalign 0.5
                        
                        hbox:
                            spacing 10
                            xfill True
                            
                            textbutton "💾 Guardar Rápido" action Function(save_project_quick):
                                style "save_load_button"
                                xsize 150
                            
                            textbutton "📂 Cargar Proyecto" action Function(show_load_projects):
                                style "save_load_button"
                                xsize 150
                            
                            textbutton "🔍 Ver Proyectos" action Function(show_projects_list):
                                style "save_load_button"
                                xsize 150
                        
                        hbox:
                            spacing 10
                            xfill True
                            
                            textbutton "🔧 Diagnóstico" action Function(verify_current_directory):
                                style "save_load_button"
                                xsize 150
                            
                            textbutton "📋 Información" action Function(show_project_info):
                                style "save_load_button"
                                xsize 150
                
                # Botón de cerrar
                textbutton "❌ Cerrar Panel" action Hide("save_load_panel"):
                    style "save_load_button"
                    xalign 0.5
                    xsize 200

# Panel para cargar proyectos
screen load_projects_panel():
    modal True
    
    frame:
        style_prefix "save_load"
        xfill True
        yfill True
        background "#00000080"
        
        frame:
            xalign 0.5
            yalign 0.5
            xsize 700
            ysize 500
            background "#2a2a2a"
            padding (20, 20)
            
            vbox:
                spacing 15
                
                label "📂 Cargar Proyecto" xalign 0.5
                
                # Lista de proyectos
                frame:
                    background "#3a3a3a"
                    padding (15, 15)
                    
                    vbox:
                        spacing 10
                        
                        text "📁 Proyectos Disponibles:" size 16
                        
                        # Aquí se mostrarían los proyectos
                        viewport:
                            scrollbars "vertical"
                            mousewheel True
                            xsize 600
                            ysize 300
                            
                            vbox:
                                spacing 5
                                
                                # Lista de proyectos (se generará dinámicamente)
                                for project in get_projects_list():
                                    textbutton "[project['name']]" action Function(load_project_from_file, project['filename']):
                                        style "save_load_button"
                                        xfill True
                
                # Botones de acción
                hbox:
                    spacing 10
                    xalign 0.5
                    
                    textbutton "🔄 Actualizar Lista" action Function(refresh_projects_list):
                        style "save_load_button"
                        xsize 150
                    
                    textbutton "❌ Cerrar" action Hide("load_projects_panel"):
                        style "save_load_button"
                        xsize 150

# Panel para mostrar proyectos
screen projects_list_panel():
    modal True
    
    frame:
        style_prefix "save_load"
        xfill True
        yfill True
        background "#00000080"
        
        frame:
            xalign 0.5
            yalign 0.5
            xsize 800
            ysize 600
            background "#2a2a2a"
            padding (20, 20)
            
            vbox:
                spacing 15
                
                label "📋 Lista de Proyectos" xalign 0.5
                
                # Información del directorio
                frame:
                    background "#3a3a3a"
                    padding (15, 15)
                    
                    vbox:
                        spacing 5
                        
                        text "📁 Directorio: [PROJECTS_DIR]" size 16
                        
                        if os.path.exists(PROJECTS_DIR):
                            $ files = os.listdir(PROJECTS_DIR)
                            text "📂 Proyectos encontrados: [len(files)]" size 14
                        else:
                            text "❌ Directorio no existe" size 14 color "#ff6666"
                
                # Lista de archivos
                frame:
                    background "#3a3a3a"
                    padding (15, 15)
                    
                    viewport:
                        scrollbars "vertical"
                        mousewheel True
                        xsize 700
                        ysize 400
                        
                        vbox:
                            spacing 5
                            
                            if os.path.exists(PROJECTS_DIR):
                                for file in os.listdir(PROJECTS_DIR):
                                    if file.endswith('.rpy'):
                                        text "📄 [file]" size 14 color "#cccccc"
                            else:
                                text "❌ No hay proyectos guardados" size 14 color "#ff6666"
                
                # Botón de cerrar
                textbutton "❌ Cerrar" action Hide("projects_list_panel"):
                    style "save_load_button"
                    xalign 0.5
                    xsize 150

# Estilos para el panel
style save_load_button:
    background "#4a4a4a"
    hover_background "#5a5a5a"
    padding (10, 5)
    size 14

style save_load_button_text:
    color "#ffffff"
    hover_color "#ffff00"
    size 14

# Funciones auxiliares para el panel
init python:
    def show_save_load_panel():
        """Muestra el panel principal de guardado y carga"""
        renpy.show_screen("save_load_panel")
    
    def show_load_projects():
        """Muestra el panel de carga de proyectos"""
        renpy.show_screen("load_projects_panel")
    
    def show_projects_list():
        """Muestra la lista de proyectos"""
        renpy.show_screen("projects_list_panel")
    
    def show_custom_path_input():
        """Muestra input para ruta personalizada"""
        renpy.notify("🔧 Para ruta personalizada usa: set_custom_project_directory('tu_ruta')")
    
    def refresh_projects_list():
        """Actualiza la lista de proyectos"""
        renpy.notify("🔄 Lista actualizada")
        renpy.restart_interaction()
