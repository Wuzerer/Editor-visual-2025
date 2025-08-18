# Pantalla de Inicialización Simple y Confiable
# Versión sin modal para evitar que se quede colgada

screen inicializacion_simple():
    # Sin modal para evitar problemas
    zorder 100
    
    # Fondo negro
    frame:
        background "#000000"
        xfill True
        yfill True
    
    # Primer mensaje - más arriba del centro
    text "Inicializando Editor Visual...":
        size 32
        color "#ffffff"
        align (0.5, 0.4)  # 40% desde arriba
    
    # Segundo mensaje - más abajo
    text "Por favor espera...":
        size 24
        color "#cccccc"
        align (0.5, 0.6)  # 60% desde arriba
    
    # Barra de progreso simple
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
            ease 3.0 xsize 300
