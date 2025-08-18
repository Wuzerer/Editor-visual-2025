# Pantalla de Inicialización Dinámica
# Los mensajes aparecen abajo y luego se mueven al centro

screen inicializacion_dinamica():
    modal False
    
    # Fondo negro
    frame:
        background "#000000"
        xfill True
        yfill True
    
    # Primer mensaje - se mueve de abajo al centro
    text "Inicializando Editor Visual...":
        size 32
        color "#ffffff"
        align (0.5, 0.4)  # 40% desde arriba (centro)
        at transform:
            yalign 0.9  # Comienza abajo
            ease 2.0 yalign 0.4  # Se mueve al centro en 2 segundos
    
    # Segundo mensaje - se mueve de abajo al centro
    text "Por favor espera...":
        size 24
        color "#cccccc"
        align (0.5, 0.6)  # 60% desde arriba
        at transform:
            yalign 0.95  # Comienza más abajo
            ease 2.5 yalign 0.6  # Se mueve al centro en 2.5 segundos
    
    # Barra de progreso - aparece después
    frame:
        background "#333333"
        xsize 300
        ysize 4
        align (0.5, 0.75)  # 75% desde arriba
        at transform:
            alpha 0.0
            ease 1.0 alpha 1.0  # Aparece gradualmente
    
    frame:
        background "#00ff00"
        xsize 300
        ysize 4
        align (0.5, 0.75)  # 75% desde arriba
        at transform:
            xsize 0
            ease 3.0 xsize 300  # Animación de progreso
