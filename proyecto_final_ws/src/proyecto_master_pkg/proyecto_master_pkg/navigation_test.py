import rclpy
import time
import heapq
import matplotlib.pyplot as plt
from PIL import Image
from rclpy.node import Node
from proyecto_interfaces.srv import StartNavigationTest

#Declaracion posicion inical del robot global
global posx
global posy
posx = 0.0
posy = 0.0

# Definir las direcciones de movimiento permitidas
movements = [(1, 0), (-1, 0), (0, 1), (0, -1)]
#Se define la lista de puntos visitados
puntos_visitados = []
        
#Abrir el mapa formato pgm que se encuentra en la carpeta data
mapa = Image.open("data/MapaRobotica.pgm")
pixels = mapa.load()

# Obtener el ancho y alto de la imagen
width, height = mapa.size


class Navigation_test(Node):

    #Inicializacion del nodo publicador hacia el topico
    def __init__(self):

        super().__init__('navigation_test')

        #Ingresar posicion inicial en x e y
        self.get_logger().info('Ingrese posicion inicial en x:')
        posx = float(input())
        self.get_logger().info('Ingrese posicion inicial en y:')
        posy = float(input())
        
        #Declaracion del servicio
        self.service = self.create_service(StartNavigationTest, '/group_'+str(4)+'/start_navigation_test_srv', self.handle_request)
         
    def handle_request(self, request, response):
        
        # Inicializa la respuesta del servicio
        desx = request.x
        desy = request.y

        #Se imprime la solicitud recibida
        respuesta = "Se recibio la solicitud de navegacion a las coordenadas: " + str(desx) + ", " + str(desy) + "."
        response.answer = respuesta
        
        #Se llama al metodo que planifica la ruta
        self.planificar_ruta(desx, desy)


    # Definir una función de heurística para calcular la distancia de Manhattan
    def heuristic(a, b):
        return abs(b[0] - a[0]) + abs(b[1] - a[1])
    
    # Definir una función que devuelva una lista de vecinos válidos
    def getNeighbors(self, point):
        neighbors = []
        for move in movements:
            neighbor = (point[0] + move[0], point[1] + move[1])
            if 0 <= neighbor[0] < width and 0 <= neighbor[1] < height:
                if pixels[neighbor[0], neighbor[1]] == 255:
                    neighbors.append(neighbor)
        return neighbors
    

    def planificar_ruta(self, desx, desy):

        #Se definen las variables globales
        global posx
        global posy

        #Se definen las variables locales
        #Se define el punto inicial
        punto_inicial = (posx, posy)
        #Se define el punto final
        punto_final = (desx, desy)

        
def main(args=None):

    rclpy.init(args=args)
            
    navigation_test = Navigation_test()

    rclpy.spin(navigation_test) 

    navigation_test.destroy_node()    

    rclpy.shutdown()   


if __name__ == '__main__':

    main()


        