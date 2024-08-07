import pygame
from random import randint
import Proyectil

class Invasor(pygame.sprite.Sprite):
    def __init__(self,posx,posy,distancia,imagen1,imagen2):
        pygame.sprite.Sprite.__init__(self)
        self.imagenA = pygame.image.load(imagen1).convert_alpha()
        self.imagenB = pygame.image.load(imagen2).convert_alpha()
        self.imagenA = pygame.transform.rotate(self.imagenA,180)
        self.imagenB = pygame.transform.rotate(self.imagenB,180)
        self.imagenA = pygame.transform.scale(self.imagenA,(50,50))
        self.imagenB = pygame.transform.scale(self.imagenB,(50,50))

        self.listaimagenes = [self.imagenA,self.imagenB]
        self.posimagen = 0

        self.imageninvasor = self.listaimagenes[self.posimagen]
        self.rect = self.imageninvasor.get_rect()

        self.listaDisparo = []
        self.velocidad = 1
        self.rect.top = posy
        self.rect.left = posx

        self.rangodisparo = 2
        self.tiempocambio = 1

        self.derecha = True
        self.contador = 0
        self.maxdescenso = self.rect.top+40

        self.sonidodisparoenemigo = pygame.mixer.Sound("sonidos/disparo_enemigo_1.wav")
        
        self.limitederecha = posx+distancia
        self.limiteizquierda = posx-distancia
            
    def dibujar(self,superficie):
        self.imageninvasor = self.listaimagenes[self.posimagen]
        superficie.blit(self.imageninvasor,self.rect)   

    def comportamiento(self,tiempo):
            self.__ataque()
            self.__movimiento()
            self.posimagen = int(tiempo %2)
            self.tiempocambio +=1
            
            if self.posimagen > len(self.listaimagenes)-1:
                self.posimagen = 0
    
    def __movimiento(self):
        if self.contador <2:
            self.__movimientolateral()
        else:
            self.__descenso()

    def __descenso(self):
        if self.maxdescenso == self.rect.top:
            self.contador=0
            self.maxdescenso = self.rect.top +50
        else:
            self.rect.top +=5

    def __movimientolateral(self):
        if self.derecha == True:
            self.rect.left = self.rect.left+ self.velocidad
            if self.rect.left > self.limitederecha:
                self.derecha = False

                self.contador +=0.5

        else:
            self.rect.left = self.rect.left - self.velocidad
            if self.rect.left <self.limiteizquierda:
                self.derecha = True

                self.contador +=1

    def __ataque(self):
        if (randint(0,3000 )<self.rangodisparo):
            self.__disparo()

    def __disparo(self):
        x,y = self.rect.center
        miproyectil = proyectil(self.rect.centerx-25, y,"imagenes/disparos.xcf",False)
        self.listaDisparo.append(miproyectil)
        self.sonidodisparoenemigo.play()