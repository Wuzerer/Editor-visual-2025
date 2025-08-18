# Pantalla de Inicialización del Editor Visual
# Pantalla personalizada para mostrar mensajes de inicialización

screen inicializacion_screen():
    modal True
    
    # Fondo negro
    frame:
        background "#000000"
        xfill True
        yfill True
    
    # Primer mensaje - más arriba del centro
    text "Inicializando Editor Visual...":
        size 32
        color "#ffffff"
        align (0.5, 0.4)  # 40% desde arriba (más arriba del centro)
    
    # Segundo mensaje - más abajo
    text "Por favor espera...":
        size 24
        color "#cccccc"
        align (0.5, 0.6)  # 60% desde arriba (más abajo del centro)
    
    # Indicador de progreso visual
    frame:
        background "#333333"
        xsize 300
        ysize 4
        align (0.5, 0.75)  # 75% desde arriba
    
    frame:
        background "#00ff00"
        xsize 300
        ysize 4
        align (0.5, 0.75)  # 75% desde arriba
        at transform:
            xsize 0
            ease 3.0 xsize 300  # Animación de progreso
