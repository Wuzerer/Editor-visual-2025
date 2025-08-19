# scene_manager.rpy
# Módulo para gestión de escenas del editor visual

init -2 python:
    import os
    import json
    from datetime import datetime
    
    # Sistema de escenas basado en archivos RPY
    CURRENT_SCENES_FILE = os.path.join(config.gamedir, "current_scenes.rpy")
    SCENES_DIR = os.path.join(config.gamedir, "scenes")
    
    # Sistema de eliminación mejorado
    deleted_scenes_history = []  # Historial de eliminaciones para deshacer
    selected_scenes_for_deletion = []  # Escenas seleccionadas para eliminación múltiple
    show_delete_confirmation = False  # Mostrar diálogo de confirmación
    deletion_mode = False  # Modo de selección múltiple
    
    def save_scenes_to_file(scenes_data, filename=None):
        """Guarda las escenas actuales a un archivo JSON"""
        try:
            if filename is None:
                filepath = CURRENT_SCENES_FILE
            else:
                filepath = os.path.join(config.gamedir, filename)
            
            # Asegurar que el directorio existe
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            # Crear datos de escenas con metadatos
            scenes_with_metadata = {
                'scenes': scenes_data,
                'total_scenes': len(scenes_data),
                'last_modified': datetime.now().isoformat(),
                'version': '1.0'
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(scenes_with_metadata, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Escenas guardadas en {filepath}")
            return True
            
        except Exception as e:
            print(f"❌ Error guardando escenas: {e}")
            return False
    
    def load_scenes_from_file(filename=None):
        """Carga las escenas desde un archivo JSON"""
        try:
            if filename is None:
                filepath = CURRENT_SCENES_FILE
            else:
                filepath = os.path.join(config.gamedir, filename)
            
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    scenes = data.get('scenes', [])
                    print(f"✅ {len(scenes)} escenas cargadas desde {filepath}")
                    return scenes
            else:
                print(f"⚠️ Archivo {filepath} no encontrado, creando nuevo")
                return []
                
        except Exception as e:
            print(f"❌ Error cargando escenas: {e}")
            return []
    
    def add_scene_to_list(scene_data, scenes_list):
        """Agrega una nueva escena a la lista"""
        try:
            # Agregar metadatos a la escena
            scene_data['id'] = len(scenes_list) + 1
            scene_data['created'] = datetime.now().isoformat()
            
            scenes_list.append(scene_data)
            print(f"✅ Escena agregada: {scene_data.get('type', 'unknown')}")
            return True
            
        except Exception as e:
            print(f"❌ Error agregando escena: {e}")
            return False
    
    def remove_scene_from_list(scene_index, scenes_list):
        """Elimina una escena de la lista por índice"""
        try:
            if 0 <= scene_index < len(scenes_list):
                removed_scene = scenes_list.pop(scene_index)
                
                # Agregar al historial de eliminaciones
                deleted_scenes_history.append({
                    'scene': removed_scene,
                    'index': scene_index,
                    'timestamp': datetime.now().isoformat()
                })
                
                # Limitar el historial a 10 elementos
                if len(deleted_scenes_history) > 10:
                    deleted_scenes_history.pop(0)
                
                print(f"✅ Escena eliminada: {removed_scene.get('type', 'unknown')}")
                return True
            else:
                print(f"❌ Índice de escena inválido: {scene_index}")
                return False
                
        except Exception as e:
            print(f"❌ Error eliminando escena: {e}")
            return False
    
    def undo_last_deletion(scenes_list):
        """Deshace la última eliminación de escena"""
        try:
            if deleted_scenes_history:
                last_deletion = deleted_scenes_history.pop()
                scene = last_deletion['scene']
                original_index = last_deletion['index']
                
                # Insertar en la posición original o al final
                if original_index <= len(scenes_list):
                    scenes_list.insert(original_index, scene)
                else:
                    scenes_list.append(scene)
                
                print(f"✅ Eliminación deshecha: {scene.get('type', 'unknown')}")
                return True
            else:
                print("⚠️ No hay eliminaciones para deshacer")
                return False
                
        except Exception as e:
            print(f"❌ Error deshaciendo eliminación: {e}")
            return False
    
    def clear_all_scenes(scenes_list):
        """Limpia todas las escenas de la lista"""
        try:
            if scenes_list:
                # Guardar en historial antes de limpiar
                deleted_scenes_history.append({
                    'scenes': scenes_list.copy(),
                    'timestamp': datetime.now().isoformat()
                })
                
                scenes_list.clear()
                print("✅ Todas las escenas eliminadas")
                return True
            else:
                print("⚠️ No hay escenas para eliminar")
                return False
                
        except Exception as e:
            print(f"❌ Error limpiando escenas: {e}")
            return False
    
    def duplicate_scene(scene_index, scenes_list):
        """Duplica una escena existente"""
        try:
            if 0 <= scene_index < len(scenes_list):
                original_scene = scenes_list[scene_index]
                
                # Crear copia profunda de la escena
                duplicated_scene = original_scene.copy()
                duplicated_scene['id'] = len(scenes_list) + 1
                duplicated_scene['created'] = datetime.now().isoformat()
                duplicated_scene['duplicated_from'] = scene_index
                
                scenes_list.append(duplicated_scene)
                print(f"✅ Escena duplicada: {original_scene.get('type', 'unknown')}")
                return True
            else:
                print(f"❌ Índice de escena inválido: {scene_index}")
                return False
                
        except Exception as e:
            print(f"❌ Error duplicando escena: {e}")
            return False
    
    def move_scene_up(scene_index, scenes_list):
        """Mueve una escena hacia arriba en la lista"""
        try:
            if scene_index > 0 and scene_index < len(scenes_list):
                scenes_list[scene_index], scenes_list[scene_index - 1] = \
                    scenes_list[scene_index - 1], scenes_list[scene_index]
                print(f"✅ Escena movida hacia arriba")
                return True
            else:
                print(f"❌ No se puede mover la escena")
                return False
                
        except Exception as e:
            print(f"❌ Error moviendo escena: {e}")
            return False
    
    def move_scene_down(scene_index, scenes_list):
        """Mueve una escena hacia abajo en la lista"""
        try:
            if scene_index >= 0 and scene_index < len(scenes_list) - 1:
                scenes_list[scene_index], scenes_list[scene_index + 1] = \
                    scenes_list[scene_index + 1], scenes_list[scene_index]
                print(f"✅ Escena movida hacia abajo")
                return True
            else:
                print(f"❌ No se puede mover la escena")
                return False
                
        except Exception as e:
            print(f"❌ Error moviendo escena: {e}")
            return False
    
    def get_scene_statistics(scenes_list):
        """Obtiene estadísticas de las escenas"""
        try:
            stats = {
                'total': len(scenes_list),
                'dialogue': 0,
                'background': 0,
                'character': 0,
                'other': 0
            }
            
            for scene in scenes_list:
                scene_type = scene.get('type', 'other')
                if scene_type in stats:
                    stats[scene_type] += 1
                else:
                    stats['other'] += 1
            
            return stats
            
        except Exception as e:
            print(f"❌ Error obteniendo estadísticas: {e}")
            return {'total': 0, 'dialogue': 0, 'background': 0, 'character': 0, 'other': 0}
    
    print("✅ Módulo de gestión de escenas cargado")
