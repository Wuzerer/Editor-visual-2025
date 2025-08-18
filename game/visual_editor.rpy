# Visual Editor - Editor Visual Dedicado
# Este archivo maneja el editor visual de forma independiente

init python:
    import os
    import json
    from datetime import datetime
    
    # Configuración del editor
    EDITOR_FILE = "visual_editor_scenes.rpy"
    PROJECTS_DIR = "editor_projects"
    
    # Asegurar que el directorio existe
    if not os.path.exists(PROJECTS_DIR):
        os.makedirs(PROJECTS_DIR)
    
    # ===== FUNCIONES DEL EDITOR =====
    
    def save_editor_scenes(project_name=None):
        """Guarda las escenas del editor directamente en formato .rpy"""
        try:
            # Obtener escenas de la pantalla
            try:
                scenes = renpy.get_screen_variable("current_scene", [])
                if not isinstance(scenes, list):
                    scenes = []
            except:
                scenes = []
            
            if not scenes:
                renpy.notify("⚠️ No hay escenas para guardar")
                return False
            
            # Generar nombre del archivo
            if project_name and project_name.strip():
                safe_name = "".join(c for c in project_name.strip() if c.isalnum() or c in (' ', '-', '_')).rstrip()
                safe_name = safe_name.replace(' ', '_')
                filename = f"{PROJECTS_DIR}/{safe_name}.rpy"
            else:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{PROJECTS_DIR}/proyecto_{timestamp}.rpy"
            
            # Crear contenido del archivo .rpy
            content = f"""# Proyecto: {project_name.strip() if project_name else 'Sin nombre'}
# Generado automáticamente por el Editor Visual
# Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

# Definir personajes
define e = Character("Eileen", color="#c8ffc8")
define narrator = Character(None, kind=nvl)

# Inicio del juego
label start:
    # Configuración inicial
    $ renpy.block_rollback()
    
"""
            
            # Convertir escenas a código Ren'Py
            for i, scene in enumerate(scenes):
                scene_type = scene.get('type', 'dialogue')
                
                if scene_type == 'stage':
                    # Escena de configuración
                    background = scene.get('background', 'bg room')
                    transition = scene.get('transition', 'None')
                    characters = scene.get('characters', [])
                    
                    content += f"    # Escena {i+1}: Configuración de escenario\n"
                    content += f"    scene {background}"
                    if transition and transition != "None":
                        content += f" with {transition}"
                    content += "\n"
                    
                    # Mostrar personajes
                    for char_name, char_pos in characters:
                        content += f"    show {char_name} {char_pos}\n"
                    content += "\n"
                
                elif scene_type == 'dialogue':
                    # Diálogo
                    character = scene.get('character', 'narrator')
                    dialogue = scene.get('dialogue', '').replace('"', '\\"')
                    
                    content += f"    # Escena {i+1}: Diálogo\n"
                    if character == "Narrator":
                        content += f'    "{dialogue}"\n'
                    else:
                        content += f'    {character.lower()} "{dialogue}"\n'
                    content += "\n"
                
                elif scene_type == 'label':
                    # Label
                    name = scene.get('name', '')
                    content += f"    # Escena {i+1}: Label\n"
                    content += f"    label {name}:\n"
                    content += "\n"
                
                elif scene_type == 'jump':
                    # Jump
                    target = scene.get('target', '')
                    content += f"    # Escena {i+1}: Jump\n"
                    content += f"    jump {target}\n"
                    content += "\n"
                
                elif scene_type == 'choice':
                    # Decisión
                    prompt = scene.get('prompt', '')
                    options = scene.get('options', [])
                    
                    content += f"    # Escena {i+1}: Decisión\n"
                    content += f"    menu:\n"
                    content += f'        "{prompt}":\n\n'
                    
                    for option_text, option_target in options:
                        content += f'            "{option_text}":\n'
                        content += f"                jump {option_target}\n"
                    content += "\n"
            
            # Finalizar el script
            content += """    # Fin del juego
    return
"""
            
            # Guardar archivo
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            
            if project_name and project_name.strip():
                renpy.notify(f"💾 Guardado como {safe_name}.rpy")
            else:
                renpy.notify(f"💾 Guardado como proyecto_{timestamp}.rpy")
            
            return True
            
        except Exception as e:
            renpy.notify(f"❌ Error al guardar: {str(e)}")
            return False
    
    def load_editor_scenes(filename):
        """Carga escenas desde un archivo .rpy al editor"""
        try:
            filepath = f"{PROJECTS_DIR}/{filename}.rpy"
            if not os.path.exists(filepath):
                renpy.notify(f"❌ Archivo {filename}.rpy no encontrado")
                return False
            
            # Leer el archivo
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parsear de forma simple
            scenes = []
            lines = content.split('\n')
            
            for line in lines:
                line = line.strip()
                
                # Ignorar comentarios y líneas vacías
                if line.startswith('#') or not line or line.startswith('label start:') or line == 'return':
                    continue
                
                # Diálogos
                if '"' in line and line.count('"') >= 2:
                    if line.startswith('    '):
                        line = line[4:]
                    
                    if ' "' in line:
                        parts = line.split(' "', 1)
                        if len(parts) == 2:
                            character = parts[0].strip()
                            dialogue = parts[1].rstrip('"')
                            
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
                    elif line.startswith('"') and line.endswith('"'):
                        dialogue = line[1:-1]
                        scenes.append({
                            'type': 'dialogue',
                            'character': 'Narrator',
                            'dialogue': dialogue,
                            'xalign': 0.5,
                            'yalign': 0.9
                        })
                
                # Escenas
                elif line.startswith('scene '):
                    if line.startswith('    '):
                        line = line[4:]
                    background = line.replace('scene ', '').strip()
                    scenes.append({
                        'type': 'stage',
                        'background': background,
                        'transition': 'None',
                        'characters': []
                    })
                
                # Mostrar personajes
                elif line.startswith('show '):
                    if line.startswith('    '):
                        line = line[4:]
                    # Extraer nombre del personaje y posición
                    show_parts = line.replace('show ', '').split(' at ')
                    if len(show_parts) >= 2:
                        char_name = show_parts[0].strip()
                        char_pos = f"at {show_parts[1].strip()}"
                        
                        # Buscar la última escena de stage para añadir el personaje
                        for i in range(len(scenes) - 1, -1, -1):
                            if scenes[i]['type'] == 'stage':
                                if 'characters' not in scenes[i]:
                                    scenes[i]['characters'] = []
                                scenes[i]['characters'].append([char_name, char_pos])
                                break
            
            # Actualizar la pantalla del editor
            try:
                renpy.set_screen_variable("current_scene", scenes)
                renpy.notify(f"📂 Cargado {filename}.rpy con {len(scenes)} escenas")
                return True
            except Exception as screen_error:
                renpy.notify(f"⚠️ Error al actualizar pantalla: {str(screen_error)}")
                return False
            
        except Exception as e:
            renpy.notify(f"❌ Error al cargar {filename}: {str(e)}")
            return False
    
    def add_dialogue_to_editor(character, dialogue, xalign, yalign):
        """Agrega diálogo directamente al editor"""
        if dialogue.strip():
            try:
                # Obtener escenas actuales
                try:
                    scenes = renpy.get_screen_variable("current_scene", [])
                    if not isinstance(scenes, list):
                        scenes = []
                except:
                    scenes = []
                
                # Crear nueva escena
                scene_data = {
                    'type': 'dialogue',
                    'character': character,
                    'dialogue': dialogue.strip(),
                    'xalign': xalign,
                    'yalign': yalign
                }
                
                # Agregar escena
                scenes.append(scene_data)
                
                # Actualizar pantalla
                renpy.set_screen_variable("current_scene", scenes)
                
                # Limpiar campo de texto
                try:
                    renpy.set_screen_variable("dialogue_text", "")
                except:
                    pass
                
                renpy.notify(f"✅ Línea agregada: {len(scenes)} escenas")
                
            except Exception as e:
                renpy.notify(f"❌ Error: {str(e)}")
        else:
            renpy.notify("⚠️ Diálogo vacío, no se agregó")
    
    def add_stage_to_editor(background, characters, transition):
        """Agrega escena de stage directamente al editor"""
        try:
            # Obtener escenas actuales
            try:
                scenes = renpy.get_screen_variable("current_scene", [])
                if not isinstance(scenes, list):
                    scenes = []
            except:
                scenes = []
            
            # Crear nueva escena
            scene_data = {
                'type': 'stage',
                'background': background,
                'characters': characters,
                'transition': transition
            }
            
            # Agregar escena
            scenes.append(scene_data)
            
            # Actualizar pantalla
            renpy.set_screen_variable("current_scene", scenes)
            
            renpy.notify(f"✅ Escena agregada: {len(scenes)} escenas")
            
        except Exception as e:
            renpy.notify(f"❌ Error: {str(e)}")
    
    def clear_editor():
        """Limpia el editor"""
        try:
            renpy.set_screen_variable("current_scene", [])
            renpy.notify("🗑️ Editor limpiado")
        except Exception as e:
            renpy.notify(f"❌ Error: {str(e)}")
    
    def get_editor_scenes():
        """Obtiene las escenas actuales del editor"""
        try:
            scenes = renpy.get_screen_variable("current_scene", [])
            if not isinstance(scenes, list):
                scenes = []
            return scenes
        except:
            return []
    
    def test_editor_system():
        """Prueba el sistema del editor"""
        try:
            renpy.notify("🧪 PRUEBA DEL SISTEMA DEL EDITOR")
            
            # Obtener escenas actuales
            scenes = get_editor_scenes()
            renpy.notify(f"📊 Escenas en editor: {len(scenes)}")
            
            # Agregar escena de prueba
            add_dialogue_to_editor("Eileen", "Esta es una prueba del sistema del editor", 0.5, 0.9)
            
            # Verificar que se agregó
            scenes_after = get_editor_scenes()
            renpy.notify(f"📊 Escenas después de agregar: {len(scenes_after)}")
            
            if len(scenes_after) > len(scenes):
                renpy.notify("✅ Sistema funcionando correctamente")
            else:
                renpy.notify("❌ Sistema no funcionó")
                
        except Exception as e:
            renpy.notify(f"❌ Error en prueba: {str(e)}")
