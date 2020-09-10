# Imports
import pygame
import numpy as np
import time
import random
import copy

import sys
import os
import fnmatch

import argparse


# CLASES

# Clase del estado del juego
class GameState:

    def __init__(self, board, food, snakeCells, walls):

        # Celdas muro = -1
        # Celdas snake = 1
        # Celda cabeza snake = 2
        # Celdas comida = 3

        self.board = board

        for coord in walls:
            self.board[coord[0]][coord[1]] = -1


        # Comida
        self.food = food
        self.board[self.food[0]][self.food[1]] = 3



        # Cuerpo snake
        self.bodySnake = snakeCells[1]
        self.board[self.bodySnake[0]][self.bodySnake[1]] = 1

        #  Cabeza snake
        self.headSnake = snakeCells[0]
        self.board[self.headSnake[0]][self.headSnake[1]] = 2

        # Casillas que ocupa el snake
        self.snakeCells = snakeCells



        # Movimiento actual del snake
        self.currentMove = "right"

        # Partida terminada
        self.end = False


# Clase del juego
class Snake:

    def __init__(self):

        # Iniciar pygame
        pygame.init()

        # Crear pantalla del juego
        self.resolution_screen = (1000, 1000)
        self.screen = pygame.display.set_mode(self.resolution_screen)

        # Poner el fondo como gris oscuro
        self.bg = 25, 25, 25


        # Parser argumentos
        ap = argparse.ArgumentParser()
        # Añadimos argumentos al parser (FLAGS)
        ap.add_argument("-l", "--layout", required=False, help="mapa")
        ap.add_argument("-t", "--time", required=False, help="tiempo")

        args = vars(ap.parse_args())

        # Mapa y tiempo por defecto de la partida si no se especifican por consola
        self.defaultMap = 'square'
        self.defaultTime = 0.1

        # Flags
        l = args['layout']
        t = args['time']

        if l != None:
            self.defaultMap = l

        if t != None:
            self.defaultTime = float(t)

        # Leer mapa del input

        # Buscamos en la carpeta maps el mapa que nos han introducido por consola
        myMap = self.defaultMap
        aux = 0
        for file_name in os.listdir('maps/'):
            # Si existe lo abrimos para leerlo
            if fnmatch.fnmatch(file_name, myMap+'.txt'):

                currentDir = os.getcwd()

                with open(currentDir+'/maps/'+file_name, 'r') as file:
                    contents = file.readlines()

                    numX = len(contents)
                    numY = len(contents[0])-1 # porque hay que quitar el \n del final

                    walls = []
                    for count, row in enumerate(contents):
                        for count2, elem in enumerate(row):
                            if elem == '#':
                                walls.append([count, count2])
                            elif elem == 'F':
                                fX = count
                                fY = count2
                            elif elem == 'H':
                                hX = count
                                hY = count2
                            elif elem == 'S':
                                sX = count
                                sY = count2


                # Cambiamos el valor de la variable auxiliar porque se ha encontrado el mapa
                aux = 1

        # Si la variable auxiliar mantiene su valor inicial es porque no se ha encontrado el mapa
        if aux == 0:
            sys.exit("NO existe ningún mapa con ese nombre")



        # Número de celdas en el eje x e y
        self.numCells = (numX, numY)

        # Tamaño de las celdas según si el tablero es cuadrado o no
        if numX < numY:
            self.sizeCells = (int(self.resolution_screen[0]/self.numCells[1]), int(self.resolution_screen[1]/self.numCells[1]))
        elif numX > numY:
            self.sizeCells = (int(self.resolution_screen[0]/self.numCells[0]), int(self.resolution_screen[1]/self.numCells[0]))
        else:
            self.sizeCells = (int(self.resolution_screen[0]/self.numCells[0]), int(self.resolution_screen[1]/self.numCells[1]))


        # Tablero
        # Celdas vacías = 0
        board = np.zeros((self.numCells), dtype=np.int8)

        # Posición inicial del punto de comida
        food = [fX, fY]

        # Posición inicial del snake (ocupa dos casillas)
        snakeCells = [[hX, hY], [sX, sY]]

        self.gameState = GameState(board, food, snakeCells, walls)

    # Movimientos

    # Derecha
    def moveRight(self, gameState):
        if gameState.currentMove != "left":

            if gameState.board[gameState.headSnake[0]][gameState.headSnake[1]+1] != -1:

                for count, cell in enumerate(gameState.snakeCells[::-1]):
                    #cola
                    if count == 0:
                        gameState.snakeCells[len(gameState.snakeCells)-1] = gameState.snakeCells[len(gameState.snakeCells)-2]
                        gameState.board[cell[0]][cell[1]] = 0
                        gameState.board[gameState.snakeCells[len(gameState.snakeCells)-1][0]][gameState.snakeCells[len(gameState.snakeCells)-1][1]] = 1

                    #cabeza
                    elif count == len(gameState.snakeCells)-1:

                        # comida
                        if gameState.board[cell[0]][cell[1]+1] == 3 :
                            gameState.snakeCells.append(gameState.snakeCells[-1])
                            gameState.food = []


                        gameState.snakeCells[0] = [cell[0], cell[1]+1]

                        gameState.board[cell[0]][cell[1]] = 1

                        gameState.board[cell[0]][cell[1]+1] = 2
                        gameState.headSnake = [cell[0], cell[1]+1]

                    #cuerpo
                    else:
                        gameState.snakeCells[len(gameState.snakeCells)-1-count] = gameState.snakeCells[len(gameState.snakeCells)-2-count]
                        gameState.board[cell[0]][cell[1]] = 1

                # cabeza encuentra cuerpo
                if gameState.board[gameState.headSnake[0]][gameState.headSnake[1]+1] == 1:
                    gameState.end = True

                gameState.currentMove = "right"
                return gameState.currentMove

            else:
                gameState.end = True

        else:
            return self.moveLeft(gameState)


    # Arriba
    def moveUp(self, gameState):
        if gameState.currentMove != "down":

            if gameState.board[gameState.headSnake[0]-1][gameState.headSnake[1]] != -1:

                for count, cell in enumerate(gameState.snakeCells[::-1]):
                    #cola
                    if count == 0:
                        gameState.snakeCells[len(gameState.snakeCells)-1] = gameState.snakeCells[len(gameState.snakeCells)-2]
                        gameState.board[cell[0]][cell[1]] = 0
                        gameState.board[gameState.snakeCells[len(gameState.snakeCells)-1][0]][gameState.snakeCells[len(gameState.snakeCells)-1][1]] = 1

                    #cabeza
                    elif count == len(gameState.snakeCells)-1:

                        # comida
                        if gameState.board[cell[0]-1][cell[1]] == 3 :
                            gameState.snakeCells.append(gameState.snakeCells[-1])
                            gameState.food = []


                        gameState.snakeCells[0] = [cell[0]-1, cell[1]]

                        gameState.board[cell[0]][cell[1]] = 1

                        gameState.board[cell[0]-1][cell[1]] = 2
                        gameState.headSnake = [cell[0]-1, cell[1]]

                    #cuerpo
                    else:
                        gameState.snakeCells[len(gameState.snakeCells)-1-count] = gameState.snakeCells[len(gameState.snakeCells)-2-count]
                        gameState.board[cell[0]][cell[1]] = 1

                # cabeza encuentra cuerpo
                if gameState.board[gameState.headSnake[0]-1][gameState.headSnake[1]] == 1:
                    gameState.end = True

                gameState.currentMove = "up"
                return gameState.currentMove

            else:
                gameState.end = True

        else:
            return self.moveDown(gameState)


    # Izquierda
    def moveLeft(self, gameState):
        if  gameState.currentMove != "right":

            if gameState.board[gameState.headSnake[0]][gameState.headSnake[1]-1] != -1:

                for count, cell in enumerate(gameState.snakeCells[::-1]):
                    #cola
                    if count == 0:
                        gameState.snakeCells[len(gameState.snakeCells)-1] = gameState.snakeCells[len(gameState.snakeCells)-2]
                        gameState.board[cell[0]][cell[1]] = 0
                        gameState.board[gameState.snakeCells[len(gameState.snakeCells)-1][0]][gameState.snakeCells[len(gameState.snakeCells)-1][1]] = 1

                    #cabeza
                    elif count == len(gameState.snakeCells)-1:

                        # comida
                        if gameState.board[cell[0]][cell[1]-1] == 3 :
                            gameState.snakeCells.append(gameState.snakeCells[-1])
                            gameState.food = []


                        gameState.snakeCells[0] = [cell[0], cell[1]-1]

                        gameState.board[cell[0]][cell[1]] = 1

                        gameState.board[cell[0]][cell[1]-1] = 2
                        gameState.headSnake = [cell[0], cell[1]-1]

                    #cuerpo
                    else:
                        gameState.snakeCells[len(gameState.snakeCells)-1-count] = gameState.snakeCells[len(gameState.snakeCells)-2-count]
                        gameState.board[cell[0]][cell[1]] = 1

                # cabeza encuentra cuerpo
                if gameState.board[gameState.headSnake[0]][gameState.headSnake[1]-1] == 1:
                    gameState.end = True

                gameState.currentMove = "left"
                return gameState.currentMove

            else:
                gameState.end = True

        else:
            return self.moveRight(gameState)


    # Abajo
    def moveDown(self, gameState):
        if gameState.currentMove != "up":

            if gameState.board[gameState.headSnake[0]+1][gameState.headSnake[1]] != -1:

                for count, cell in enumerate(gameState.snakeCells[::-1]):
                    #cola
                    if count == 0:
                        gameState.snakeCells[len(gameState.snakeCells)-1] = gameState.snakeCells[len(gameState.snakeCells)-2]
                        gameState.board[cell[0]][cell[1]] = 0
                        gameState.board[gameState.snakeCells[len(gameState.snakeCells)-1][0]][gameState.snakeCells[len(gameState.snakeCells)-1][1]] = 1

                    #cabeza
                    elif count == len(gameState.snakeCells)-1:

                        # comida
                        if gameState.board[cell[0]+1][cell[1]] == 3:
                            gameState.snakeCells.append(gameState.snakeCells[-1])
                            gameState.food = []


                        gameState.snakeCells[0] = [cell[0]+1, cell[1]]

                        gameState.board[cell[0]][cell[1]] = 1

                        gameState.board[cell[0]+1][cell[1]] = 2
                        gameState.headSnake = [cell[0]+1, cell[1]]



                    #cuerpo
                    else:
                        gameState.snakeCells[len(gameState.snakeCells)-1-count] = gameState.snakeCells[len(gameState.snakeCells)-2-count]
                        gameState.board[cell[0]][cell[1]] = 1



                # cabeza encuentra cuerpo
                if gameState.board[gameState.headSnake[0]+1][gameState.headSnake[1]] == 1:
                    gameState.end = True

                gameState.currentMove = "down"
                return gameState.currentMove

            else:
                gameState.end = True

        else:
            return self.moveUp(gameState)




    # Bucle del juego
    def loop(self):
        while not self.gameState.end:

            # Copia del juego
            newGameState = copy.copy(self.gameState)

            # Limpiar pantalla
            self.screen.fill(self.bg)
            time.sleep(self.defaultTime)

            # Registrar interrupciones del teclado
            ev = pygame.event.get()

            moved = 0

            for event in ev:
                if event.type == pygame.QUIT:
                    newGameState.end = True

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        newGameState.currentMove = self.moveLeft(newGameState)
                        moved = 1

                    elif event.key == pygame.K_RIGHT:
                        newGameState.currentMove = self.moveRight(newGameState)
                        moved = 1

                    elif event.key == pygame.K_UP:
                        newGameState.currentMove = self.moveUp(newGameState)
                        moved = 1

                    elif event.key == pygame.K_DOWN:
                        newGameState.currentMove = self.moveDown(newGameState)
                        moved = 1


            if moved == 0:
                if newGameState.currentMove == "left":
                    newGameState.currentMove = self.moveLeft(newGameState)

                elif newGameState.currentMove == "right":
                    newGameState.currentMove = self.moveRight(newGameState)

                elif newGameState.currentMove == "up":
                    newGameState.currentMove = self.moveUp(newGameState)

                elif newGameState.currentMove == "down":
                    newGameState.currentMove = self.moveDown(newGameState)



            if newGameState.food == []:
                x = random.randint(1, np.shape(newGameState.board)[0] - 2)
                y = random.randint(1, np.shape(newGameState.board)[1] - 2)

                while newGameState.board[x][y] != 0:
                    x = random.randint(1, np.shape(newGameState.board)[0] - 2)
                    y = random.randint(1, np.shape(newGameState.board)[1] - 2)


                newGameState.food = [x, y]

                newGameState.board[newGameState.food[0]][newGameState.food[1]] = 3


            # print("NEW BOARD ", newGameState.board)
            # Pintar el tablero
            for y in range(0, self.numCells[1]):
                    for x in range(0, self.numCells[0]):
                        polygon = [((y)   * self.sizeCells[1], (x)   * self.sizeCells[0]),
                                               ((y+1) * self.sizeCells[1], (x)   * self.sizeCells[0]),
                                               ((y+1) * self.sizeCells[1], (x+1) * self.sizeCells[0]),
                                               ((y)   * self.sizeCells[1], (x+1) * self.sizeCells[0])]
                        color = (128, 128, 128)
                        border = 1

                        if newGameState.board[x][y] == -1:
                            color = (255, 255, 255)
                            border = 0
                        elif newGameState.board[x][y] == 1:#yx
                            color = (0, 255, 0)
                            border = 0
                        elif newGameState.board[x][y] == 2:#yx
                            color = (255, 0, 0)
                            border = 0
                        elif newGameState.board[x][y] == 3:
                            color = (0, 0, 255)
                            border = 0

                        pygame.draw.polygon(self.screen, color, polygon, border)

            self.gameState = newGameState
            pygame.display.flip()





# JUEGO
newGame = Snake()
newGame.loop()
