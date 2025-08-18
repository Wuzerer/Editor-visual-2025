# persistent_config.rpy
# Sistema de configuración persistente que funciona dentro de Ren'Py

init -1 python:
    import json
    import os
    from datetime import datetime
    
    # ===== SISTEMA DE CONFIGURACIÓN PERSISTENTE =====
    
    class PersistentConfig:
        def __init__(self):
            self.config_file = "persistent_layout.json"
            self.default_config = {
                'layout': {
                    'editor_width': 1880,
                    'editor_height': 1040,
                    'left_panel_width': 650,
                    'right_panel_width': 1170,
                    'preview_area_ratio': 0.55,
                    'scenes_area_ratio': 0.45,
                    'preview_textbox_ratio': 0.12,
                    'preview_text_size': 24,
                    'line_height': 40,
                    'content_width': 400,
                    'action_button_size': 35
                },
                'colors': {
                    'background_panel': '#e74c3c',
                    'character_panel': '#3498db',
                    'expressions_panel': '#9b59b6',
                    'stage_panel': '#f39c12',
                    'dialogue_panel': '#27ae60',
                    'structure_panel': '#8e44ad',
                    'projects_panel': '#16a085',
                    'developer_panel': '#e74c3c'
                },
                'text_sizes': {
                    'title_large': 32,
                    'title_medium': 28,
                    'title_small': 24,
                    'text_large': 18,
                    'text_medium': 14,
                    'text_small': 12
                }
            }
            self.current_config = self.load_config()
        
        def load_config(self):
            """Carga configuración desde archivo"""
            try:
                if os.path.exists(self.config_file):
                    with open(self.config_file, 'r', encoding='utf-8') as f:
                        return json.load(f)
                else:
                    return self.default_config.copy()
            except:
                return self.default_config.copy()
        
        def save_config(self):
            """Guarda configuración actual"""
            try:
                with open(self.config_file, 'w', encoding='utf-8') as f:
                    json.dump(self.current_config, f, ensure_ascii=False, indent=2)
                return True
            except:
                return False
        
        def update_config(self, section, key, value):
            """Actualiza un valor específico en la configuración"""
            if section not in self.current_config:
                self.current_config[section] = {}
            self.current_config[section][key] = value
        
        def get_value(self, section, key, default=None):
            """Obtiene un valor de la configuración"""
            return self.current_config.get(section, {}).get(key, default)
        
        def apply_to_editor(self):
            """Aplica la configuración al editor"""
            try:
                global visual_layout, colors, text_sizes
                
                # Aplicar layout
                layout_config = self.current_config.get('layout', {})
                for key, value in layout_config.items():
                    if hasattr(visual_layout, key):
                        setattr(visual_layout, key, value)
                
                # Aplicar colores
                colors_config = self.current_config.get('colors', {})
                for key, value in colors_config.items():
                    if hasattr(colors, key):
                        setattr(colors, key, value)
                
                # Aplicar tamaños de texto
                text_config = self.current_config.get('text_sizes', {})
                for key, value in text_config.items():
                    if hasattr(text_sizes, key):
                        setattr(text_sizes, key, value)
                
                return True
            except:
                return False
    
    # Instancia global
    persistent_config = PersistentConfig()

# ===== FUNCIONES DE INTEGRACIÓN =====

init python:
    def apply_persistent_config():
        """Aplica configuración persistente al editor"""
        persistent_config.apply_to_editor()
        renpy.notify("✅ Configuración aplicada")
    
    def save_current_configuration():
        """Guarda la configuración actual de forma robusta"""
        try:
            global visual_layout, colors, text_sizes
            
            # Guardar layout
            persistent_config.update_config('layout', 'editor_width', visual_layout.editor_width)
            persistent_config.update_config('layout', 'editor_height', visual_layout.editor_height)
            persistent_config.update_config('layout', 'left_panel_width', visual_layout.left_panel_width)
            persistent_config.update_config('layout', 'right_panel_width', visual_layout.right_panel_width)
            persistent_config.update_config('layout', 'preview_area_ratio', visual_layout.preview_area_ratio)
            persistent_config.update_config('layout', 'scenes_area_ratio', visual_layout.scenes_area_ratio)
            persistent_config.update_config('layout', 'preview_textbox_ratio', visual_layout.preview_textbox_ratio)
            persistent_config.update_config('layout', 'preview_text_size', visual_layout.preview_text_size)
            persistent_config.update_config('layout', 'line_height', visual_layout.line_height)
            persistent_config.update_config('layout', 'content_width', visual_layout.content_width)
            persistent_config.update_config('layout', 'action_button_size', visual_layout.action_button_size)
            
            # Guardar colores
            persistent_config.update_config('colors', 'background_panel', colors.background_panel)
            persistent_config.update_config('colors', 'character_panel', colors.character_panel)
            persistent_config.update_config('colors', 'expressions_panel', colors.expressions_panel)
            persistent_config.update_config('colors', 'stage_panel', colors.stage_panel)
            persistent_config.update_config('colors', 'dialogue_panel', colors.dialogue_panel)
            persistent_config.update_config('colors', 'structure_panel', colors.structure_panel)
            persistent_config.update_config('colors', 'projects_panel', colors.projects_panel)
            persistent_config.update_config('colors', 'developer_panel', colors.developer_panel)
            
            # Guardar tamaños de texto
            persistent_config.update_config('text_sizes', 'title_large', text_sizes.title_large)
            persistent_config.update_config('text_sizes', 'title_medium', text_sizes.title_medium)
            persistent_config.update_config('text_sizes', 'title_small', text_sizes.title_small)
            persistent_config.update_config('text_sizes', 'text_large', text_sizes.text_large)
            persistent_config.update_config('text_sizes', 'text_medium', text_sizes.text_medium)
            persistent_config.update_config('text_sizes', 'text_small', text_sizes.text_small)
            
            # Guardar archivo
            if persistent_config.save_config():
                renpy.notify("✅ Configuración guardada exitosamente")
            else:
                renpy.notify("❌ Error al guardar configuración")
        except Exception as e:
            renpy.notify(f"❌ Error: {str(e)}")
    
    def load_persistent_to_editor():
        """Carga configuración persistente al editor"""
        try:
            if persistent_config.apply_to_editor():
                # Actualizar variables de pantalla si el configurador está abierto
                force_screen_update()
                renpy.notify("✅ Configuración cargada desde archivo")
            else:
                renpy.notify("❌ Error al cargar configuración")
        except Exception as e:
            renpy.notify(f"❌ Error: {str(e)}")
    
    def reset_to_default_persistent():
        """Restaura configuración predeterminada"""
        try:
            persistent_config.current_config = persistent_config.default_config.copy()
            persistent_config.apply_to_editor()
            persistent_config.save_config()
            # Actualizar variables de pantalla si el configurador está abierto
            force_screen_update()
            renpy.notify("🔄 Configuración restaurada a predeterminado")
        except Exception as e:
            renpy.notify(f"❌ Error: {str(e)}")
    
    def save_from_screen_variables():
        """Guarda configuración desde variables de pantalla del configurador"""
        try:
            # Intentar guardar desde variables de pantalla si el configurador está abierto
            if renpy.get_screen("layout_configurator"):
                try:
                    # Aplicar cambios del configurador antes de guardar
                    apply_all_changes()
                    renpy.notify("✅ Cambios aplicados y guardados")
                except Exception as e:
                    # Si hay error, usar configuración actual
                    renpy.notify("⚠️ Guardando configuración actual")
                    save_current_configuration()
            else:
                # Si no está abierto el configurador, usar configuración actual
                save_current_configuration()
        except Exception as e:
            renpy.notify(f"❌ Error: {str(e)}")

# ===== PANTALLA DE GESTIÓN PERSISTENTE =====

screen persistent_config_screen():
    modal True
    
    add Solid("#1a1a1a")
    
    frame:
        background "#2c3e50"
        padding (30, 30)
        xalign 0.5
        yalign 0.5
        xsize 500
        ysize 400
        
        vbox:
            spacing 20
            
            text "💾 Gestión de Configuración Persistente" size 24 color "#ffffff" xalign 0.5
            
            # Información
            frame:
                background "#34495e"
                padding (15, 15)
                vbox:
                    text "📋 Estado Actual:" color "#ffffff" size 16
                    text "Archivo: persistent_layout.json" color "#ecf0f1" size 12
                    text "Configuración: [persistent_config.config_file]" color "#ecf0f1" size 12
            
            # Botones de acción
            vbox:
                spacing 10
                xalign 0.5
                
                textbutton "💾 Guardar Configuración Actual" action Function(save_current_configuration) style "confirm_button"
                textbutton "�� Cargar Configuración Guardada" action Function(load_persistent_to_editor) style "confirm_button"
                textbutton "🔄 Restaurar Predeterminado" action Function(reset_to_default_persistent) style "cancel_button"
                textbutton "❌ Cerrar" action Hide("persistent_config_screen") style "cancel_button"

# Aplicar configuración al iniciar
init 1 python:
    persistent_config.apply_to_editor()
