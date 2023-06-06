import rclpy
import time
import heapq
import matplotlib.pyplot as plt
import numpy as np
import cv2
from PIL import Image
from queue import PriorityQueue
from rclpy.node import Node
from proyecto_interfaces.srv import StartNavigationTest

#Declaracion posicion inical del robot global
#Ingresar posicion inicial en x e y
global posx
global posy
print('Ingrese posicion inicial en x:')
posx = float(input())
print('Ingrese posicion inicial en y:')
posy = float(input())

global desx
global desy 
global llamado 
desx = 0
desy = 0
llamado = False


#Se define la lista de puntos visitados
global camino 
camino = []
        
#Abrir el mapa formato pgm que se encuentra en la carpeta data
global mapa 
mapa = cv2.imread("data/MapaRobotica.pgm")

class Navigation_test(Node):

    #Inicializacion del nodo publicador hacia el topico
    def __init__(self):

        super().__init__('navigation_test')
        
        #Declaracion del servicio
        self.service = self.create_service(StartNavigationTest, '/group_'+str(4)+'/start_navigation_test_srv', self.handle_request)

        #Creacion temporizador 
        periodo = 1
        self.timer = self.create_timer(periodo, self.navegacion)
         
    def handle_request(self, request, response):
        
        global desx, desy, llamado
        # Inicializa la respuesta del servicio
        desx = request.x
        desy = request.y

        #Se imprime la solicitud recibida
        respuesta = "Se recibio la solicitud de navegacion a las coordenadas: " + str(desx) + ", " + str(desy) + "."
        response.answer = respuesta

        #Se llamo
        llamado = True

        return response
    

    def navegacion(self):

        global posx, posy, desx, desy, llamado, camino, mapa

        #Se revisa si se llamo
        if llamado == True:

            d=23 # Span de pepe en centimetros
            r=10 # parametro de salto entre vecinos (pixeles)
    
            d=round(round(d*4)/2)  #mitad del span de pepe en pixeles
    
            gscore=np.full((len(mapa), len(mapa[0])), np.inf)
            fscore=np.full((len(mapa), len(mapa[0])), np.inf) 

            gscore[posy][posx]=0
            fscore[posy][posx]=self.h([posx,posy], [desx,desy])
    
            open=PriorityQueue()
            open.put((self.h([posx,posy], [desx,desy]),self.h([posx,posy], [desx,desy]),[posx,posy]))
            aPath={}

            while not open.empty():
        
                currPix=open.get()[2]
                    
                if currPix[0] in range(desx-r,desx+r) and currPix[1] in range(desy-r,desy+r):
                    posf=currPix
                    break
                    
                    
                #nodos vecindad
                izq=(currPix[0]-r,currPix[1])
                der=(currPix[0]+r,currPix[1])
                sup=(currPix[0],currPix[1]+r)
                inf=(currPix[0],currPix[1]-r)
                    
                vecinos=[izq,der,sup,inf]
                    
                for vecino in vecinos:
                        
                    #revision de celdas libres y tamano del Pepe
                    available=True
                    for i in range(vecino[1]-d,vecino[1]+d):
                        for j in range(vecino[0]-d,vecino[0]+d):
                            if mapa[i][j][0]==94:
                                available=False

                                
                    # analisis fscore y gscore
                    if available==True:
                        temp_gscore=gscore[currPix[1]][currPix[0]]+1
                        temp_fscore=self.h(vecino,posf)+temp_gscore
                        if temp_fscore<fscore[vecino[1]][vecino[0]]:
                            fscore[vecino[1]][vecino[0]]=temp_fscore
                            gscore[vecino[1]][vecino[0]]=temp_gscore
                            open.put((temp_fscore,self.h(vecino,posf),vecino))
                            aPath[vecino]=currPix

            #Se crea el camino
            path=[[desx,desy]]
            while path[-1]!=[posx,posy]:
                path.append(aPath[path[-1]])
            path.reverse()
            camino = path

            #Se imprime el camino
            print("El camino es: ")
            print(camino)

            for val in camino:
                mapa=self.draw(val,mapa,d)

            #Se muestra el mapa
            cv2.imshow("Mapa",mapa)

    def draw(self,pos,img,d):
        #conversion a pixeles
        d=round(round(d*4)/2)
        
        for i in range(pos[1]-d,pos[1]+d):
            for j in range(pos[0]-d,pos[0]+d):
                try:
                    img[i][j]=[0,0,0]
                except:
                    pass
        return img
    
    def h(self,pos0,posf):  #distancia manhattan (corresponde a la heuristica del problema)
        x=abs(posf[0]-pos0[0])
        y=abs(posf[1]-pos0[1])
     
        return x+y


    

        


        