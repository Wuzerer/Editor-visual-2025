# ===== VENTANAS MODALES DEL EDITOR VISUAL =====
# Archivo separado para evitar reinicios y mantener estabilidad

# Variables por defecto para las ventanas modales
default modal_scene_name = ""  # Nombre para nueva escena
default modal_current_mode = "create"  # Modo actual de la ventana modal

# ===== PANTALLA MODAL PARA CREAR ESCENAS =====

screen create_scene_modal():
    modal True
    
    frame:
        xfill True
        yfill True
        background "#000000cc"
        
        frame:
            xsize 350
            ysize 250
            background "#2c3e50"
            xalign 0.5
            yalign 0.5
            padding (15, 15)
            
            vbox:
                spacing 10
                xfill True
                yfill True
                
                # Título
                text "🎬 Crear Nueva Escena" color "#ffffff" size 24 xalign 0.5
                
                # Descripción
                text "Escribe un nombre para tu nueva escena:" color "#ecf0f1" size 16 xalign 0.5
                
                # Campo de entrada
                frame:
                    xfill True
                    background "#1a252f"
                    padding (8, 6)
                    
                    input value ScreenVariableInputValue("modal_scene_name", "") length 20 color "#ffffff" size 16
                
                # Texto de ayuda
                text "📝 Escribe el nombre de tu escena arriba" color "#95a5a6" size 14 xalign 0.5
                
                # Información adicional
                text "💡 Sugerencias: Introducción, Escena_Principal, Final_Feliz" color "#f39c12" size 14 xalign 0.5
                
                # Botones de acción
                hbox:
                    spacing 8
                    xfill True
                    
                    textbutton "✅ Crear Escena" action [Function(modal_create_new_scene), Hide("create_scene_modal")] background "#27ae60" hover_background "#2ecc71" text_color "#ffffff" text_hover_color "#ffffff" text_size 16
                    textbutton "❌ Cancelar" action [SetScreenVariable("modal_scene_name", ""), Hide("create_scene_modal")] background "#e74c3c" hover_background "#c0392b" text_color "#ffffff" text_hover_color "#ffffff" text_size 16

# ===== FUNCIONES PARA LAS VENTANAS MODALES =====

init python:
    def modal_create_new_scene():
        """Crea una nueva escena desde la ventana modal"""
        try:
            scene_name = renpy.get_screen_variable("modal_scene_name")
            if scene_name and scene_name.strip():
                scene_name = scene_name.strip()
                
                # Obtener las escenas actuales del editor principal
                all_scenes = renpy.get_screen_variable("all_scenes", {})
                
                if scene_name in all_scenes:
                    renpy.notify("⚠️ Ya existe una escena con ese nombre")
                    return
                
                # Crear la nueva escena
                all_scenes[scene_name] = []
                renpy.set_screen_variable("all_scenes", all_scenes)
                renpy.set_screen_variable("current_scene_name", scene_name)
                renpy.set_screen_variable("current_scenes", [])
                
                # Limpiar la variable modal
                renpy.set_screen_variable("modal_scene_name", "")
                
                # Notificar éxito
                renpy.notify(f"✅ Nueva escena '{scene_name}' creada")
                
                # Debug
                print(f"🔍 Debug: Escena '{scene_name}' creada desde modal")
                
            else:
                renpy.notify("⚠️ Ingresa un nombre para la escena")
                
        except Exception as e:
            renpy.notify(f"❌ Error creando escena: {e}")
            print(f"🔍 Debug: Error completo: {e}")
    
    def modal_init_scene_creation():
        """Inicializa la ventana modal para crear escenas"""
        try:
            # Limpiar la variable modal
            renpy.set_screen_variable("modal_scene_name", "")
            return True
        except Exception as e:
            print(f"🔍 Error inicializando modal: {e}")
            return False

# ===== PANTALLA MODAL PARA GESTIÓN DE ESCENAS (FUTURO) =====

screen scene_management_modal():
    modal True
    
    frame:
        xfill True
        yfill True
        background "#000000cc"
        
        frame:
            xsize 500
            ysize 400
            background "#2c3e50"
            xalign 0.5
            yalign 0.5
            padding (20, 20)
            
            vbox:
                spacing 15
                xfill True
                yfill True
                
                # Título
                text "🎬 Gestión de Escenas" color "#ffffff" size 24 xalign 0.5
                
                # Pestañas o secciones
                hbox:
                    spacing 10
                    xfill True
                    
                    # Botón para crear nueva escena
                    textbutton "➕ Crear Escena" action [SetScreenVariable("modal_current_mode", "create"), SetScreenVariable("modal_scene_name", "")] background "#27ae60" hover_background "#2ecc71" text_color "#ffffff" text_hover_color "#ffffff" text_size 16
                    
                    # Botón para ver lista de escenas
                    textbutton "📋 Lista de Escenas" action SetScreenVariable("modal_current_mode", "list") background "#3498db" hover_background "#2980b9" text_color "#ffffff" text_hover_color "#ffffff" text_size 16
                
                # Contenido dinámico
                if renpy.get_screen_variable("modal_current_mode", "create") == "create":
                    # Sección de creación de escena
                    vbox:
                        spacing 10
                        xfill True
                        yfill True
                        
                        # Descripción
                        text "Escribe un nombre para tu nueva escena:" color "#ecf0f1" size 16 xalign 0.5
                        
                        # Campo de entrada
                        frame:
                            xfill True
                            background "#1a252f"
                            padding (8, 6)
                            
                            input value ScreenVariableInputValue("modal_scene_name", "") length 25 color "#ffffff" size 16
                        
                        # Texto de ayuda
                        text "📝 Escribe el nombre de tu escena arriba" color "#95a5a6" size 14 xalign 0.5
                        
                        # Información adicional
                        text "💡 Sugerencias: Introducción, Escena_Principal, Final_Feliz" color "#f39c12" size 14 xalign 0.5
                        
                        # Botones de acción
                        hbox:
                            spacing 8
                            xfill True
                            
                            textbutton "✅ Crear Escena" action [Function(modal_create_new_scene), SetScreenVariable("modal_current_mode", "list")] background "#27ae60" hover_background "#2ecc71" text_color "#ffffff" text_hover_color "#ffffff" text_size 16
                            textbutton "❌ Cancelar" action [SetScreenVariable("modal_scene_name", ""), SetScreenVariable("modal_current_mode", "list")] background "#e74c3c" hover_background "#c0392b" text_color "#ffffff" text_hover_color "#ffffff" text_size 16
                
                else:
                    # Sección de lista de escenas
                    vbox:
                        spacing 10
                        xfill True
                        yfill True
                        
                        # Lista de escenas
                        frame:
                            xfill True
                            yfill True
                            background "#1a252f"
                            padding (10, 10)
                            
                            viewport:
                                xfill True
                                yfill True
                                scrollbars "vertical"
                                mousewheel True
                                
                                vbox:
                                    spacing 5
                                    xfill True
                                    
                                    $ all_scenes = renpy.get_screen_variable("all_scenes", {})
                                    if all_scenes:
                                        for scene_name in all_scenes.keys():
                                            frame:
                                                xfill True
                                                background "#34495e"
                                                padding (8, 6)
                                                
                                                hbox:
                                                    xfill True
                                                    spacing 8
                                                    
                                                    # Nombre de la escena
                                                    text f"🎭 {scene_name}" color "#ffffff" size 16
                                                    
                                                    # Contador de elementos
                                                    $ scene_count = len(all_scenes[scene_name])
                                                    text f"({scene_count} elementos)" color "#f39c12" size 14
                                                    
                                                    # Botón seleccionar
                                                    textbutton "📝 Seleccionar" action [SetScreenVariable("selected_scene_to_edit", scene_name), Function(modal_select_scene), Hide("scene_management_modal")] background "#27ae60" hover_background "#2ecc71" text_color "#ffffff" text_hover_color "#ffffff" text_size 14
                                                    
                                                    # Botón eliminar
                                                    textbutton "🗑️ Eliminar" action [SetScreenVariable("selected_scene_to_edit", scene_name), Function(modal_delete_scene), SetScreenVariable("modal_current_mode", "list")] background "#e74c3c" hover_background "#c0392b" text_color "#ffffff" text_hover_color "#ffffff" text_size 14
                                    else:
                                        text "No hay escenas creadas" color "#95a5a6" size 18 xalign 0.5
                
                # Botón cerrar
                textbutton "❌ Cerrar" action Hide("scene_management_modal") background "#95a5a6" hover_background "#7f8c8d" text_color "#ffffff" text_hover_color "#ffffff" text_size 16 xalign 0.5

# ===== FUNCIONES ADICIONALES PARA GESTIÓN =====

init python:
    def modal_select_scene():
        """Selecciona una escena para editar desde la modal"""
        try:
            scene_name = renpy.get_screen_variable("selected_scene_to_edit")
            if scene_name:
                all_scenes = renpy.get_screen_variable("all_scenes", {})
                if scene_name in all_scenes:
                    renpy.set_screen_variable("current_scene_name", scene_name)
                    renpy.set_screen_variable("current_scenes", all_scenes[scene_name])
                    renpy.set_screen_variable("selected_scene_to_edit", "")
                    print(f"🔍 Debug: Cargando escena '{scene_name}' desde modal")
                    renpy.notify(f"📝 Editando escena: '{scene_name}'")
                else:
                    renpy.notify("⚠️ Escena no encontrada")
            else:
                renpy.notify("⚠️ Selecciona una escena para editar")
        except Exception as e:
            renpy.notify(f"❌ Error seleccionando escena: {e}")
            print(f"🔍 Debug: Error completo: {e}")
    
    def modal_delete_scene():
        """Elimina una escena desde la modal"""
        try:
            scene_name = renpy.get_screen_variable("selected_scene_to_edit")
            if scene_name:
                all_scenes = renpy.get_screen_variable("all_scenes", {})
                if scene_name in all_scenes:
                    del all_scenes[scene_name]
                    renpy.set_screen_variable("all_scenes", all_scenes)
                    renpy.set_screen_variable("selected_scene_to_edit", "")
                    
                    # Si era la escena actual, limpiar
                    current_name = renpy.get_screen_variable("current_scene_name", "")
                    if current_name == scene_name:
                        renpy.set_screen_variable("current_scene_name", "")
                        renpy.set_screen_variable("current_scenes", [])
                    
                    print(f"🔍 Debug: Escena '{scene_name}' eliminada desde modal")
                    renpy.notify(f"🗑️ Escena '{scene_name}' eliminada")
                else:
                    renpy.notify("⚠️ Escena no encontrada")
            else:
                renpy.notify("⚠️ Selecciona una escena para eliminar")
        except Exception as e:
            renpy.notify(f"❌ Error eliminando escena: {e}")
            print(f"🔍 Debug: Error completo: {e}")

# ===== PANTALLA MODAL PARA CONFIGURACIÓN (FUTURO) =====

screen settings_modal():
    modal True
    
    frame:
        xfill True
        yfill True
        background "#000000cc"
        
        frame:
            xsize 400
            ysize 300
            background "#2c3e50"
            xalign 0.5
            yalign 0.5
            padding (20, 20)
            
            vbox:
                spacing 15
                xfill True
                yfill True
                
                # Título
                text "⚙️ Configuración del Editor" color "#ffffff" size 24 xalign 0.5
                
                # Contenido de configuración (futuro)
                text "Configuraciones futuras irán aquí" color "#ecf0f1" size 16 xalign 0.5
                
                # Botón cerrar
                textbutton "❌ Cerrar" action Hide("settings_modal") background "#95a5a6" hover_background "#7f8c8d" text_color "#ffffff" text_hover_color "#ffffff" text_size 16 xalign 0.5

# ===== PANTALLA MODAL PARA AYUDA (FUTURO) =====

screen help_modal():
    modal True
    
    frame:
        xfill True
        yfill True
        background "#000000cc"
        
        frame:
            xsize 500
            ysize 400
            background "#2c3e50"
            xalign 0.5
            yalign 0.5
            padding (20, 20)
            
            vbox:
                spacing 15
                xfill True
                yfill True
                
                # Título
                text "❓ Ayuda del Editor" color "#ffffff" size 24 xalign 0.5
                
                # Contenido de ayuda (futuro)
                text "Guía de uso del editor visual" color "#ecf0f1" size 16 xalign 0.5
                
                # Botón cerrar
                textbutton "❌ Cerrar" action Hide("help_modal") background "#95a5a6" hover_background "#7f8c8d" text_color "#ffffff" text_hover_color "#ffffff" text_size 16 xalign 0.5
