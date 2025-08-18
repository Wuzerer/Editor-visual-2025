# project_manager.rpy
# Módulo para gestión de proyectos del editor visual

init -2 python:
    import os
    import json
    from datetime import datetime
    
    # Directorio de proyectos
    PROJECTS_DIR = os.path.join(config.gamedir, "projects")
    
    # Asegurar que el directorio existe
    if not os.path.exists(PROJECTS_DIR):
        os.makedirs(PROJECTS_DIR)
        print(f"✅ Directorio de proyectos creado: {PROJECTS_DIR}")
    
    def get_available_projects():
        """Obtiene la lista de proyectos disponibles"""
        try:
            projects = []
            if os.path.exists(PROJECTS_DIR):
                for filename in os.listdir(PROJECTS_DIR):
                    if filename.endswith('.rpy'):
                        project_name = filename[:-4]  # Remover .rpy
                        
                        # Intentar cargar información del proyecto
                        scene_count = 0
                        try:
                            json_file = os.path.join(PROJECTS_DIR, f"{project_name}.json")
                            if os.path.exists(json_file):
                                with open(json_file, 'r', encoding='utf-8') as f:
                                    project_data = json.load(f)
                                    scene_count = len(project_data.get('scenes', []))
                        except:
                            scene_count = 0
                        
                        projects.append({
                            'name': project_name,
                            'scene_count': scene_count,
                            'filename': filename
                        })
            
            return sorted(projects, key=lambda x: x['name'].lower())
        except Exception as e:
            print(f"❌ Error obteniendo proyectos: {e}")
            return []
    
    def save_project_rpy(project_name, scenes_data):
        """Guarda un proyecto como archivo .rpy"""
        try:
            if not os.path.exists(PROJECTS_DIR):
                os.makedirs(PROJECTS_DIR)
            
            # Generar contenido del script
            script_content = f"""# {project_name}.rpy
# Proyecto generado automáticamente por el Editor Visual
# Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

label start:
    "Iniciando {project_name}..."
    
"""
            
            # Agregar escenas
            for i, scene in enumerate(scenes_data, 1):
                if scene.get('type') == 'dialogue':
                    character = scene.get('character', 'Narrator')
                    dialogue = scene.get('dialogue', '')
                    script_content += f'    {character} "{dialogue}"\n\n'
                elif scene.get('type') == 'background':
                    background = scene.get('background', '')
                    script_content += f'    scene {background}\n\n'
                elif scene.get('type') == 'character':
                    character = scene.get('character', '')
                    sprite = scene.get('sprite', '')
                    position = scene.get('position', 'center')
                    script_content += f'    show {character} {sprite} at {position}\n\n'
            
            script_content += """    "Fin del proyecto."
    return
"""
            
            # Guardar archivo .rpy
            rpy_file = os.path.join(PROJECTS_DIR, f"{project_name}.rpy")
            with open(rpy_file, 'w', encoding='utf-8') as f:
                f.write(script_content)
            
            # Guardar metadatos en JSON
            json_file = os.path.join(PROJECTS_DIR, f"{project_name}.json")
            metadata = {
                'name': project_name,
                'created': datetime.now().isoformat(),
                'scenes': scenes_data,
                'scene_count': len(scenes_data)
            }
            
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Proyecto '{project_name}' guardado exitosamente")
            return True
            
        except Exception as e:
            print(f"❌ Error guardando proyecto: {e}")
            return False
    
    def load_project_rpy(project_name):
        """Carga un proyecto desde archivo .rpy"""
        try:
            json_file = os.path.join(PROJECTS_DIR, f"{project_name}.json")
            if os.path.exists(json_file):
                with open(json_file, 'r', encoding='utf-8') as f:
                    project_data = json.load(f)
                    return project_data.get('scenes', [])
            else:
                print(f"❌ Archivo de proyecto '{project_name}' no encontrado")
                return []
        except Exception as e:
            print(f"❌ Error cargando proyecto: {e}")
            return []
    
    def delete_project_simple(project_name):
        """Elimina un proyecto de forma simple"""
        try:
            rpy_filename = os.path.join(PROJECTS_DIR, f"{project_name}.rpy")
            json_filename = os.path.join(PROJECTS_DIR, f"{project_name}.json")
            
            deleted = False
            if os.path.exists(rpy_filename):
                os.remove(rpy_filename)
                deleted = True
            
            if os.path.exists(json_filename):
                os.remove(json_filename)
                deleted = True
            
            if deleted:
                print(f"🗑️ Proyecto '{project_name}' eliminado")
                return True
            else:
                print(f"❌ Proyecto '{project_name}' no encontrado")
                return False
                
        except Exception as e:
            print(f"❌ Error eliminando proyecto: {e}")
            return False
    
    def debug_projects():
        """Función de debug para verificar proyectos"""
        projects = get_available_projects()
        if projects:
            project_info = f"Proyectos encontrados: {len(projects)}\n"
            for i, project in enumerate(projects, 1):
                project_info += f"{i}. {project['name']} ({project['scene_count']} escenas)\n"
            print(project_info)
        else:
            print("No se encontraron proyectos")
        
        # Verificar directorio
        if os.path.exists(PROJECTS_DIR):
            files = os.listdir(PROJECTS_DIR)
            json_files = [f for f in files if f.endswith('.json')]
            print(f"Archivos JSON en directorio: {len(json_files)}")
        else:
            print("Directorio de proyectos no existe")
    
    def test_save_rpy():
        """Función de prueba para verificar el guardado"""
        try:
            # Crear una escena de prueba
            test_scenes = [
                {
                    'type': 'dialogue',
                    'character': 'Eileen',
                    'dialogue': '¡Hola! Esta es una prueba del sistema de archivos .rpy'
                },
                {
                    'type': 'dialogue',
                    'character': 'Narrator',
                    'dialogue': 'El sistema está funcionando correctamente.'
                }
            ]
            
            # Guardar proyecto de prueba
            success = save_project_rpy("test_project", test_scenes)
            if success:
                print("✅ Prueba de guardado exitosa")
            else:
                print("❌ Prueba de guardado fallida")
                
        except Exception as e:
            print(f"❌ Error en prueba: {e}")
    
    print("✅ Módulo de gestión de proyectos cargado")
