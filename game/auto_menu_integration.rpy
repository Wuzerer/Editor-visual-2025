# auto_menu_integration.rpy
# Integración automática del Editor Visual en el menú principal
# Este archivo se ejecuta automáticamente y agrega el botón del editor sin modificar archivos existentes

init python:
    import os
    
    # Verificar si el editor visual está presente
    def is_visual_editor_present():
        """Verifica si los archivos del editor visual están presentes"""
        required_files = [
            "visual_editor.rpy",
            "editor_modules/visual_editor_screen.rpy"
        ]
        
        for file_path in required_files:
            if not os.path.exists(file_path):
                print(f"❌ Archivo faltante: {file_path}")
                return False
        return True
    
    # Variable global para controlar si el editor está disponible
    visual_editor_available = is_visual_editor_present()
    
    if visual_editor_available:
        print("🎨 Editor Visual detectado - Integrando botón en menú principal")
        print("✅ El botón 'Editor Visual' aparecerá automáticamente en el menú")
    else:
        print("⚠️ Editor Visual no encontrado - Botón no se agregará al menú")
        print("💡 Para activar el editor, asegúrate de que todos los archivos estén presentes")

# Sobrescribir la pantalla de navegación para incluir el botón del editor
screen navigation():
    vbox:
        style_prefix "navigation"
        xpos gui.navigation_xpos
        yalign 0.5
        spacing gui.navigation_spacing

        if main_menu:
            textbutton _("Comenzar") action Start()
        else:
            textbutton _("Historial") action ShowMenu("history")
            textbutton _("Guardar") action ShowMenu("save")

        textbutton _("Cargar") action ShowMenu("load")
        textbutton _("Opciones") action ShowMenu("preferences")

        # Botón del Editor Visual (solo si está disponible)
        if visual_editor_available:
            textbutton _("Editor Visual") action ShowMenu("visual_editor")

        if _in_replay:
            textbutton _("Finaliza repetición") action EndReplay(confirm=True)
        elif not main_menu:
            textbutton _("Menú principal") action MainMenu()

        textbutton _("Acerca de") action ShowMenu("about")

        if renpy.variant("pc") or (renpy.variant("web") and not renpy.variant("mobile")):
            textbutton _("Ayuda") action ShowMenu("help")

        if renpy.variant("pc"):
            textbutton _("Salir") action Quit(confirm=not main_menu)
