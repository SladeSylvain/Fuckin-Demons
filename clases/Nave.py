import pygame
from Proyectil import Proyectil

class Nave(pygame.sprite.Sprite):
    def __init__(self, ancho, alto):
        pygame.sprite.Sprite.__init__(self)
        self.ImagenNave = pygame.image.load("imagenes/final/nave principal_1.xcf").convert_alpha()
        self.ImagenNave = pygame.transform.scale(self.ImagenNave, (50, 50))
        self.imagenexplosion = pygame.image.load("imagenes/final/explosion_1.xcf").convert_alpha()
        

        self.rect = self.ImagenNave.get_rect()
        self.rect.width = 40    
        self.rect.height = 40
        self.rect.centerx = ancho / 2
        self.rect.centery = alto - 50

        self.listaDisparo = []
        self.Vida = True
        self.velocidad = 10
        self.sonidodisparo = pygame.mixer.Sound("sonidos/disparo_personaje_2.wav")
        self.sonidoexplosion = pygame.mixer.Sound("sonidos/explosion_nave_principal.wav")
        self.sonidoyousuck = pygame.mixer.Sound("sonidos/yousuck.mp3")

        # Agrega la variable para el tiempo del último disparo
        self.ultimo_disparo = 0

    def movimientoDerecha(self):
        self.rect.right += self.velocidad
        self.__movimiento()

    def movimientoIzquierda(self):
        self.rect.left -= self.velocidad
        self.__movimiento()

    def __movimiento(self):
        if self.Vida:
            if self.rect.left <= 0:
                self.rect.left = 0
            elif self.rect.right > 480:
                self.rect.right = 480

    def disparar(self):
        if self.Vida:
            now = pygame.time.get_ticks()

            # Agrega un retraso mínimo entre disparos (por ejemplo, 500 ms)
            if now - self.ultimo_disparo > 500:
                x, y = self.rect.center  # Obtiene las coordenadas del centro de la nave
                miProyectil = Proyectil(x, y, "imagenes/bala1.xcf", True)

                # Limita la cantidad de proyectiles en pantalla (por ejemplo, 5)
                if len(self.listaDisparo) < 3:
                    self.listaDisparo.append(miProyectil)
                    self.sonidodisparo.play()

                # Actualiza el tiempo del último disparo
                self.ultimo_disparo = now

    def destruccion(self):
        self.ImagenNave = self.imagenexplosion
        self.sonidoyousuck.play()
        self.sonidoexplosion.play()
        self.Vida = False
        self.velocidad = 0
        

    def dibujar(self, superficie):
        superficie.blit(self.ImagenNave, self.rect)

    def actualizar(self):
        for proyectil in self.listaDisparo:
            if proyectil.rect.top < -10:
                self.listaDisparo.remove(proyectil)
