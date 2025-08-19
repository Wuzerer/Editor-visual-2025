# exit_confirmation_modal.rpy
# Modal de confirmación de salida con cambios no guardados

screen confirm_exit_unsaved_modal():
    modal True
    
    # Fondo semi-transparente
    frame:
        background "#000000"
        at transform:
            alpha 0.7
        xfill True
        yfill True
    
    # Modal principal
    frame:
        xsize 600
        ysize 400
        xalign 0.5
        yalign 0.5
        background "#2c3e50"
        at transform:
            alpha 1.0
        padding (30, 25)
        
        vbox:
            spacing 20
            xfill True
            xalign 0.5
            
            # Título
            text "⚠️ Cambios No Guardados" color "#e74c3c" size 24 xalign 0.5 style "title_with_outline"
            
            # Mensaje principal
            text "Tienes escenas creadas que no han sido guardadas en un proyecto." color "#ffffff" size 16 xalign 0.5
            
            # Lista de escenas no guardadas
            $ has_unsaved_changes, scenes_created = check_unsaved_changes()
            if scenes_created:
                text "Escenas no guardadas:" color "#f39c12" size 14 xalign 0.5
                for scene_name in scenes_created:
                    text f"• {scene_name}" color "#ecf0f1" size 12 xalign 0.5
            
            # Advertencia
            text "Si sales sin guardar, estos archivos se eliminarán automáticamente." color "#e74c3c" size 14 xalign 0.5
            
            # Botones de acción
            hbox:
                spacing 20
                xalign 0.5
                
                textbutton "💾 Guardar Proyecto":
                    action [Hide("confirm_exit_unsaved_modal"), Show("visual_editor"), Function(save_project_modal)]
                    xminimum 150
                    ysize 50
                    padding (15, 10)
                    background "#27ae60"
                    hover_background "#2ecc71"
                    text_color "#ffffff"
                    text_hover_color "#ffffff"
                    text_size 14
                    xalign 0.5
                    text_style "text_with_outline"
                
                textbutton "🧹 Salir y Limpiar":
                    action Function(exit_editor_with_cleanup)
                    xminimum 150
                    ysize 50
                    padding (15, 10)
                    background "#e67e22"
                    hover_background "#f39c12"
                    text_color "#ffffff"
                    text_hover_color "#ffffff"
                    text_size 14
                    xalign 0.5
                    text_style "text_with_outline"
                
                textbutton "❌ Cancelar":
                    action [Hide("confirm_exit_unsaved_modal"), Show("visual_editor")]
                    xminimum 120
                    ysize 50
                    padding (15, 10)
                    background "#95a5a6"
                    hover_background "#7f8c8d"
                    text_color "#ffffff"
                    text_hover_color "#ffffff"
                    text_size 14
                    xalign 0.5
                    text_style "text_with_outline"
