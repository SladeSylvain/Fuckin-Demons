import pygame

class Proyectil(pygame.sprite.Sprite):
    def __init__(self,posx,posy,ruta,personaje):
        pygame.sprite.Sprite.__init__(self)
        self.imagenproyectil = pygame.image.load(ruta).convert_alpha()
        self.rect = self.imagenproyectil.get_rect()
        self.velocidadDisparo = 2
        self.rect.top = posy
        self.rect.left = posx
        self.disparopersonaje = personaje

    def trayectoria(self):
        if self.disparopersonaje ==True:
            self.rect.top = self.rect.top - self.velocidadDisparo
        else:
            self.rect.top = self.rect.top + self.velocidadDisparo
    def dibujar(self,superficie):
        superficie.blit(self.imagenproyectil,self.rect)        
