import pygame
import sys
from pygame.locals import *
from random import randint
from clases.Nave import Nave
from clases.Invasor import Invasor
from clases.Proyectil import Proyectil

# Definición del tamaño de la pantalla
ancho = 480
alto = 600

# Inicialización de variables globales
nivel = 1
puntaje = 0
sonido_reproducido = False
menu_music_playing = False
fondo_juego = None
lista_enemigo = []

# Velocidad de los enemigos por nivel
velocidad_enemigo_por_nivel = {1: 1, 2: 2, 3: 3}

# Función para detener a todos los enemigos
def detenertodo():
    for enemigo in lista_enemigo:
        enemigo.listaDisparo = []
        enemigo.conquista = True

# Función para cargar los enemigos en el nivel actual
def cargarEnemigos():
    global nivel
    enemigos_por_fila = 10
    enemigos_a_cada_lado = 5 + nivel
    espacio_superior = 3
    separacion_vertical = -10

    # Aumenta la velocidad de los enemigos en función del nivel actual
    velocidad_enemigo = velocidad_enemigo_por_nivel.get(nivel, 3)  # Por defecto, nivel 3
    for fila in range(4):
        enemigos_a_cada_lado = min(enemigos_a_cada_lado, enemigos_por_fila // 2)
        enemigos_a_la_izquierda = enemigos_a_cada_lado
        enemigos_a_la_derecha = enemigos_a_cada_lado
        separacion_horizontal = 36
        espacio_izquierdo = -10
        espacio_derecho = -10

        posx = espacio_izquierdo + (ancho // 2) + separacion_horizontal // 2
        for _ in range(enemigos_a_la_derecha):
            enemigo = Invasor(posx, fila * 50 + espacio_superior, 50, "imagenes/final/Enemigo_1.xcf", "imagenes/final/enemigo_1.2.xcf")
            enemigo.velocidad = velocidad_enemigo  # Aplica la velocidad del nivel
            lista_enemigo.append(enemigo)
            posx += separacion_horizontal

        posx = (ancho // 2) - separacion_horizontal // 2 - separacion_horizontal - espacio_derecho
        for _ in range(enemigos_a_la_izquierda):
            enemigo = Invasor(posx, fila * 50 + espacio_superior, 50, "imagenes/final/enemigo_2.xcf", "imagenes/final/enemigo_2.1.xcf")
            enemigo.velocidad = velocidad_enemigo  # Aplica la velocidad del nivel
            lista_enemigo.append(enemigo)
            posx -= separacion_horizontal

        espacio_superior += separacion_vertical

# Función para mostrar el menú principal
def menu_principal(screen):
    global menu_music_playing, fondo_juego
    if not menu_music_playing:
        pygame.mixer.music.load("sonidos/musica_rock.mp3")
        pygame.mixer.music.play(-1)
        menu_music_playing = True

    fondo_menu = pygame.image.load("portadas/title1.jpg")
    fondo_menu = pygame.transform.scale(fondo_menu, (ancho, alto))

    mifuentesistema = pygame.font.SysFont("Fredericka the Great", 15)
    texto_inicio = mifuentesistema.render("Press SPACE to Start", 0, (255, 255, 255))

    rect_texto_inicio = texto_inicio.get_rect()
    rect_texto_inicio.center = (240, 530)

    en_menu = True

    while en_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_SPACE:
                    en_menu = False
                    pygame.mixer.music.stop()
                    fondo_juego = pygame.image.load("portadas/imagen_ejemplo.jpg").convert_alpha()
                    fondo_juego = pygame.transform.scale(fondo_juego, (ancho, alto))

        if fondo_juego:
            screen.blit(fondo_juego, (0, 0))
        else:
            screen.blit(fondo_menu, (0, 0))

        screen.blit(texto_inicio, rect_texto_inicio)
        pygame.display.update()

# Función para crear un rectángulo en la mitad de la pantalla con textura
def crearRectangulo():
    rectangulo_rect = pygame.Rect(ancho // 2 - 35, alto // 2 - -200, 70, 20)
    textura_rect = pygame.image.load("imagenes/final/wall_1.xcf").convert_alpha()
    textura_rect = pygame.transform.scale(textura_rect, (70, 20))
    return rectangulo_rect, textura_rect

# Función principal del juego
def jugar():
    global sonido_reproducido, fondo_juego, nivel, puntaje

    pygame.init()
    screen = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("Fukin Demons")

    mifuentesistema = pygame.font.SysFont("Fredericka the Great", 40)
    mifuentesistema1 = pygame.font.SysFont("Fredericka the Great", 42)

    texto1 = mifuentesistema1.render("YOU SUCK!!", 0, (255, 255, 255))
    rect_texto = texto1.get_rect()
    rect_texto.center = (ancho // 2, alto // 2)

    menu_principal(screen)

    pygame.mixer.music.load("sonidos/musica final/musica_fondo2.mp3")
    pygame.mixer.music.play(-1)

    jugador = Nave(ancho, alto)
    enJuego = True
    reloj = pygame.time.Clock()
    cargarEnemigos()

    FPS = 60

    espacio_presionado = False

    # Crear el rectángulo en el alcance de jugar
    rectangulo_rect, textura_rect = crearRectangulo()
    rectangulo_velocidad = 4  # Velocidad de movimiento del rectángulo
    rectangulo_direccion = -1  # Dirección inicial (izquierda)
    cambio_direccion_intervalo = randint(0, 120)  # Intervalo aleatorio para cambiar la dirección

    while enJuego:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            jugador.movimientoIzquierda()
        if keys[pygame.K_RIGHT]:
            jugador.movimientoDerecha()

        # Limitar el movimiento del rectángulo dentro de los límites de la pantalla
        if rectangulo_rect.left <= 0:
            rectangulo_direccion = 1
        elif rectangulo_rect.right >= ancho:
            rectangulo_direccion = -1

        if keys[pygame.K_SPACE] and not espacio_presionado:
            x, y = jugador.rect.center
            jugador.disparar()
            espacio_presionado = True  # La tecla espacio está presionada

        if not keys[pygame.K_SPACE]:
            espacio_presionado = False  # La tecla espacio se ha soltado y se puede presionar nuevamente en el próximo clic

        if fondo_juego:
            screen.blit(fondo_juego, (0, 0))
        else:
            screen.fill((0, 0, 0))
        jugador.dibujar(screen)
        proyectiles_a_eliminar = []

        for x in jugador.listaDisparo:
            x.dibujar(screen)
            x.trayectoria()
            if x.rect.top < -10:
                proyectiles_a_eliminar.append(x)

            if x.rect.colliderect(rectangulo_rect):
                proyectiles_a_eliminar.append(x)

            for enemigo in lista_enemigo:
                if x.rect.colliderect(enemigo.rect):
                    proyectiles_a_eliminar.append(x)
                    if enemigo in lista_enemigo:
                        lista_enemigo.remove(enemigo)

        for proyectil in proyectiles_a_eliminar:
            if proyectil in jugador.listaDisparo:
                jugador.listaDisparo.remove(proyectil)

        for enemigo in lista_enemigo:
            enemigo.comportamiento(pygame.time.get_ticks() / 1000)
            enemigo.dibujar(screen)

            if enemigo.rect.colliderect(jugador.rect):
                jugador.destruccion()
                enJuego = False
                detenertodo()
                mensaje_game_over = mifuentesistema.render("YOU SUCK", 0, (255, 0, 0))
                rect_mensaje_game_over = mensaje_game_over.get_rect()
                rect_mensaje_game_over.center = (ancho // 2, alto // 2)
                screen.blit(mensaje_game_over, rect_mensaje_game_over)
                break

            disparos_a_eliminar = []
            for x in enemigo.listaDisparo:
                x.dibujar(screen)
                x.trayectoria()

                if x.rect.colliderect(jugador.rect):
                    jugador.destruccion()
                    enJuego = False
                    detenertodo()
                    break

                if x.rect.top > 900:
                    disparos_a_eliminar.append(x)
                else:
                    for disparo in jugador.listaDisparo:
                        if x.rect.colliderect(disparo.rect):
                            if x in enemigo.listaDisparo:
                                enemigo.listaDisparo.remove(x)
                            if disparo in jugador.listaDisparo:
                                jugador.listaDisparo.remove(disparo)

            if enemigo.explosion:
                screen.blit(enemigo.imagen_explosion, enemigo.rect)
                pygame.mixer.music("sonidos/explosion.wav")

        if not lista_enemigo:
            pygame.mixer.music.stop()
            mensaje_you_win = mifuentesistema.render("YOU WIN!", 0, (0, 255, 0))
            rect_mensaje_you_win = mensaje_you_win.get_rect()
            rect_mensaje_you_win.center = (ancho // 2, alto // 2)
            sonido_youwin = pygame.mixer.Sound("sonidos/musica final/Youwin.mp3")
            screen.blit(mensaje_you_win, rect_mensaje_you_win)
            sonido_youwin.play()
            pygame.display.update()
            pygame.time.delay(3000)
            enJuego = False

        if not jugador.Vida:
            jugador.destruccion()
            mensaje_you_suck = mifuentesistema.render("YOU SUCK!", 0, (255, 255, 255))
            rect_mensaje_you_suck = mensaje_you_suck.get_rect()
            rect_mensaje_you_suck.center = (ancho // 2, alto // 2)
            sonidoyousuck = pygame.mixer.Sound("sonidos/yousuck_1.mp3")
            screen.blit(mensaje_you_suck, rect_mensaje_you_suck)
            pygame.display.update()
            sonidoyousuck.play()
            pygame.time.delay(4000)
            pygame.quit()
            sys.exit()

        # Actualizar las coordenadas del rectángulo
        rectangulo_rect.move_ip(rectangulo_velocidad * rectangulo_direccion, 0)
        
        # Comprobar si es hora de cambiar la dirección del rectángulo (en intervalos aleatorios)
        cambio_direccion_intervalo -= 1
        if cambio_direccion_intervalo <= 0:
            rectangulo_direccion = -rectangulo_direccion
            cambio_direccion_intervalo = randint(0, 480)  # Establecer un nuevo intervalo aleatorio

        pygame.draw.rect(screen, (255, 255, 255), rectangulo_rect)
        screen.blit(textura_rect, rectangulo_rect)

        pygame.display.update()
        reloj.tick(FPS)
    pygame.display.update()
    pygame.time.wait(3)
    pygame.quit()

if __name__ == "__main__":
    jugar()
