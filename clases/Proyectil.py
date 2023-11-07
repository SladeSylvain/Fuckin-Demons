import pygame

class Proyectil(pygame.sprite.Sprite):
    def __init__(self, posx, posy, ruta, personaje):
        pygame.sprite.Sprite.__init__(self)
        self.imagen = pygame.image.load(ruta)
        self.imagenproyectil = pygame.image.load(ruta).convert_alpha()
        self.rect = self.imagenproyectil.get_rect()
        self.rect.top = posy
        self.rect.left = posx
        self.velocidadDisparo = 2
        self.disparopersonaje = personaje

        # Definir una máscara de colisión basada en la imagen del proyectil
        self.mask = pygame.mask.from_surface(self.imagenproyectil)

    def trayectoria(self):
        if not self.disparopersonaje:
            self.rect.top += self.velocidadDisparo

    def disparar(self):
        return True

    def dibujar(self, superficie):
        superficie.blit(self.imagenproyectil, self.rect)
