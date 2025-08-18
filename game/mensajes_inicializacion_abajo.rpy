# Pantalla para mostrar mensajes de inicialización en la parte inferior
# Se usa durante el agradecimiento para no sobreponerse

screen mensajes_inicializacion_abajo():
    # Zorder muy bajo para que aparezca por debajo del texto del agradecimiento
    zorder -100
    
    # Primer mensaje - en la parte inferior
    text "Inicializando Editor Visual...":
        size 16
        color "#ffffff"
        align (0.5, 0.8)  # 80% desde arriba (abajo)
    
    # Segundo mensaje - más abajo
    text "Por favor espera...":
        size 12
        color "#cccccc"
        align (0.5, 0.9)  # 90% desde arriba (más abajo)
