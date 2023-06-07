import rclpy
import time
import heapq
import matplotlib.pyplot as plt
import numpy as np
import cv2
import math
from PIL import Image
from queue import PriorityQueue
from rclpy.node import Node
from proyecto_interfaces.srv import StartNavigationTest

#Declaracion posicion inical del robot global
#Ingresar posicion inicial en x e y
global posInicial
posInicial = (38, 140)

global posFinal
global llamado 
posFinal = (0,0)
llamado = False

global orientacion
orientacion = 0
        
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
        
        global posFinal, llamado
        # Inicializa la respuesta del servicio
        desx = request.x
        desy = request.y

        posFinal = (int(desx),int(desy))

        #Se imprime la solicitud recibida
        respuesta = "Se recibio la solicitud de navegacion a las coordenadas: " + str(desx) + ", " + str(desy) + "."
        response.answer = respuesta

        #Se llamo
        llamado = True

        return response
    

    def navegacion(self):

        global posInicial, posFinal, llamado, camino, mapa

        #Se revisa si se llamo
        if llamado == True:

            d=20 # Span de pepe en centimetros
            r=10 # parametro de salto entre vecinos (pixeles)
    
            d=round(round(d*4)/2)  #mitad del span de pepe en pixeles
    
            gscore=np.full((len(mapa), len(mapa[0])), np.inf)
            fscore=np.full((len(mapa), len(mapa[0])), np.inf) 

            posInicial = self.cm_to_pix(posInicial)
            posFinal = self.cm_to_pix(posFinal)
            gscore[posInicial[1]][posInicial[0]]=0
            fscore[posInicial[1]][posInicial[0]]=self.h(posInicial, posFinal)

    
            open=PriorityQueue()
            open.put((self.h(posInicial, posFinal),self.h(posInicial, posFinal),posInicial))
            aPath={}


            while not open.empty():
        
                currPix=open.get()[2]

                    
                if currPix[0] in range(posFinal[0]-r,posFinal[0]+r) and currPix[1] in range(posFinal[1]-r,posFinal[1]+r):
                    posFinal=currPix
                    break
                    
                    
                #nodos vecindad
                izq=(currPix[0]-r,currPix[1])
                der=(currPix[0]+r,currPix[1])
                sup=(currPix[0],currPix[1]+r)
                inf=(currPix[0],currPix[1]-r)
                    
                vecinos=[izq,der,sup,inf]
                print(vecinos)
                    
                for vecino in vecinos:
                        
                    #revision de celdas libres y tamano
                    available=True
                    for i in range(vecino[1]-d,vecino[1]+d):
                        for j in range(vecino[0]-d,vecino[0]+d):
                            if mapa[i][j][0]==94:
                                available=False

                                
                    # analisis fscore y gscore
                    if available==True:
                        temp_gscore=gscore[currPix[1]][currPix[0]]+1
                        print(temp_gscore)
                        temp_fscore=self.h(vecino,posFinal)+temp_gscore
                        if temp_fscore<fscore[vecino[1]][vecino[0]]:
                            fscore[vecino[1]][vecino[0]]=temp_fscore
                            gscore[vecino[1]][vecino[0]]=temp_gscore
                            open.put((temp_fscore,self.h(vecino,posFinal),vecino))
                            aPath[vecino]=currPix

            #Se crea el camino
            cell = posFinal
            print(cell)
            path=[cell]
            while cell!=posFinal:
                path.append(aPath[cell])
                cell=aPath[cell]
            path.reverse()

            #Se imprime el camino
            print("El camino es: ")
            print(path)

            for val in path:
                mapa=self.draw(val,mapa,d)

            #Se muestra el mapa
            cv2.imshow("Mapa",mapa)

            #Simplificar el camino
            distancias = []
            distancia_actual = 0
            orientacion_actual = 0
            for i in range(len(path)-1):
                delta_x = path[i][0] - path[i-1][0]
                delta_y = path[i][1] - path[i-1][1]

                if delta_x > 0:
                    orientacion = 0
                elif delta_x < 0:
                    orientacion = 180
                elif delta_y < 0:
                    orientacion = 90
                elif delta_y > 0:
                    orientacion = -90

                if orientacion == orientacion_actual:
                    distancia_actual += math.sqrt(delta_x**2 + delta_y**2)
                else:
                    distancias.append((distancia_actual, orientacion_actual))
                    distancia_actual = math.sqrt(delta_x**2 + delta_y**2)
                    orientacion_actual = orientacion

            # Agregar la última distancia
            distancias.append((distancia_actual, orientacion_actual))

            #Hacer recorrer el camino
            self.movimiento_camino(distancias)


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
    
    def h(self,pos0,posf): 
        x=abs(posf[0]-pos0[0])
        y=abs(posf[1]-pos0[1])
     
        return x+y

    def cm_to_pix(self,p0) -> tuple:
        pix = (round(p0[0]*4),round(p0[1]*4))
        return pix
    

    def movimiento_camino(self, distancias):

        global orientacion 
        for distancia, orientacionNueva in distancias:
            #Cambiar orientacion del robot
            if (orientacionNueva - orientacion) == 0:
                self.car_twist(0.0, 0.0, 0.0, 1.0)
            elif (orientacionNueva - orientacion) == 90:
                self.car_twist(0.0, 0.0, 1.0, 1.0)
            elif (orientacionNueva - orientacion) == -90:
                self.car_twist(0.0, 0.0, -1.0, 1.0)
            elif (orientacionNueva - orientacion) == 180 or (orientacionNueva - orientacion) == -180:
                self.car_twist(0.0, 0.0, 1.0, 2.0)

            #Convertir distancia pixeles a tiempo 
            tiempo = distancia * (3/20) # 3/20 es la velocidad del robot en p/s

            #Recorrer distancia robot
            self.car_twist(1.0, 0.0, 0.0, tiempo)



    #Mover el robot
    #Metodo que mueve el robot en una direccion con una velocidad y tiempo determinado
    def car_twist(self, x, y, z, tiempo):
        twist = Twist()
        twist.linear.x = x
        twist.linear.y = y
        twist.linear.z = z
        self.pub_carro_vel.publish(twist)
        time.sleep(tiempo)
            
    
def main(args=None):

    rclpy.init(args=args)
            
    navigation_test = Navigation_test()

    rclpy.spin(navigation_test) 

    navigation_test.destroy_node()    

    rclpy.shutdown()   


if __name__ == '__main__':

    main()


    

        


        
