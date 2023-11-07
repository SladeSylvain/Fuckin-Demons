import pygame
from random import randint
import Proyectil
import random  # Importa el módulo random

# Lista de rutas de archivo para las imágenes de proyectiles
imagenes_proyectiles = [
    "imagenes/final/bala_enemigo1.xcf",
    "imagenes/final/bala_enemigo2.xcf",
    "imagenes/final/bala_enemigo3.xcf",
    "imagenes/final/bala_enemigo4.xcf"
]

class Invasor(pygame.sprite.Sprite):
    def __init__(self, posx, posy, distancia, imagen1, imagen2):
        pygame.sprite.Sprite.__init__(self)
        self.imagenA = pygame.image.load(imagen1).convert_alpha()
        self.imagenB = pygame.image.load(imagen2).convert_alpha()
        self.imagenA = pygame.transform.scale(self.imagenA, (50, 50))
        self.imagenB = pygame.transform.scale(self.imagenB, (50, 50))

        self.listaimagenes = [self.imagenA, self.imagenB]
        self.posimagen = 0
        self.imageninvasor = self.listaimagenes[self.posimagen]
        self.rect = self.imageninvasor.get_rect()

        self.listaDisparo = []
        self.velocidad = 1
        self.rect.top = posy
        self.rect.left = posx

        self.rangodisparo = 2
        self.tiempocambio = 1

        self.conquista = False
        self.explosion = False

        self.derecha = True
        self.contador = 0
        self.maxdescenso = self.rect.top + 40

        self.sonidodisparoenemigo = pygame.mixer.Sound("sonidos/disparo_enemigo_1.wav")
        self.sonidodestruccion = pygame.mixer.Sound("sonidos/explosion_nave_enemiga.wav")

        self.limitederecha = posx + distancia
        self.limiteizquierda = posx - distancia

    def dibujar(self, superficie):
        if not self.explosion:
            self.imageninvasor = self.listaimagenes[self.posimagen]
            superficie.blit(self.imageninvasor, self.rect)

    def comportamiento(self, tiempo):
        if self.conquista == False:
            self.__movimiento()
            self.__ataque()
            self.posimagen = int(tiempo % 2)
            self.tiempocambio += 1

            if self.posimagen > len(self.listaimagenes) - 1:
                self.posimagen = 0

    def __movimiento(self):
        if self.contador < 2:
            self.__movimientolateral()
        else:
            self.__descenso()

    def __descenso(self):
        if self.maxdescenso == self.rect.top:
            self.contador = 0
            self.maxdescenso = self.rect.top + 50
        else:
            self.rect.top += 5

    def __movimientolateral(self):
        if self.derecha == True:
            self.rect.left = self.rect.left + self.velocidad
            if self.rect.left > self.limitederecha:
                self.derecha = False

                self.contador += 0.5

        else:
            self.rect.left = self.rect.left - self.velocidad
            if self.rect.left < self.limiteizquierda:
                self.derecha = True

                self.contador += 1

    def __ataque(self):
        if (randint(0, 3000) < self.rangodisparo):
            self.__disparo()

    def __disparo(self):
        x, y = self.rect.center

        # Selecciona una ruta aleatoria para la imagen del proyectil
        ruta_imagen_proyectil = random.choice(imagenes_proyectiles)

        miproyectil = Proyectil.Proyectil(self.rect.centerx - 25, y, ruta_imagen_proyectil, False)
        self.listaDisparo.append(miproyectil)
        self.sonidodisparoenemigo.play()

    def destruccion(self):
        if not self.explosion:
            self.sonidodestruccion.play()
            self.conquista = True
            self.explosion = True

# Resto de tu código...
