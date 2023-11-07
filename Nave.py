import pygame
import Proyectil


class naves(pygame.sprite.Sprite):
    "clase para las naves"

    def __init__ (self):
        pygame.sprite.Sprite.__init__(self)
        self.ImagenNave = pygame.image.load("imagenes/avion.xcf").convert_alpha()
        self.ImagenNave =pygame.transform.scale(self.ImagenNave,(70,70))
        self.rect = self.ImagenNave.get_rect()
        self.rect.centerx = ancho/2
        self.rect.centery = alto -30

        self.listaDisparo = []
        self.Vida = True

        self.velocidad = 30

        self.sonidodisparo = pygame.mixer.Sound("sonidos/disparo_personaje_1.wav")
    
    def movimientoderecha(self):
        self.rect.right += self.velocidad
        self.__movimiento()

    def movimientoIzquierda(self):
        self.rect.left -= self.velocidad
        self.__movimiento()

    def __movimiento(self):
        if self.Vida == True:
            if self.rect.left <=0:
                self.rect.left = 0
            elif self.rect.right> 480:
                self.rect.right = 480
    def disparar(self,x,y):
        x = self.rect.centerx-9
        y = self.rect.centery
        miProyectil = proyectil(x,y,"imagenes/bala1.xcf", True)
        self.listaDisparo.append(miProyectil)
        self.sonidodisparo.play()
        

    def dibujar(self,superficie):
        superficie.blit(self.ImagenNave,self.rect)
