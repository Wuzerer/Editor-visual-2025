# Pantalla Completa de Agradecimiento con Mensajes de Inicialización
# Maneja todo en una sola pantalla para evitar conflictos de zorder

screen agradecimiento_completo():
    modal False
    
    # Fondo negro
    frame:
        background "#000000"
        xfill True
        yfill True
    
    # Mensajes de inicialización abajo (se renderizan primero)
    text "Inicializando Editor Visual...":
        size 16
        color "#ffffff"
        align (0.5, 0.8)  # 80% desde arriba (abajo)
    
    text "Por favor espera...":
        size 12
        color "#cccccc"
        align (0.5, 0.9)  # 90% desde arriba (más abajo)
    
    # Mensaje de agradecimiento principal (se renderiza después)
    text "¡GRACIAS POR USAR NUESTRO EDITOR VISUAL!":
        size 32
        color "#ffffff"
        align (0.5, 0.3)  # 30% desde arriba (centro)
    
    # Subtítulos del agradecimiento
    text "Esperamos que disfrutes experimentando con esta herramienta":
        size 18
        color "#cccccc"
        align (0.5, 0.45)  # 45% desde arriba
    
    text "para crear tus propias novelas visuales.":
        size 18
        color "#cccccc"
        align (0.5, 0.5)  # 50% desde arriba
    
    # Mensaje motivacional
    text "¡Que tu creatividad no tenga límites!":
        size 24
        color "#ffff00"
        align (0.5, 0.6)  # 60% desde arriba
