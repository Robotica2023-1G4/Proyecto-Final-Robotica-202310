import rclpy
import time
from rclpy.node import Node
from geometry_msgs.msg import Twist

from proyecto_interfaces.srv import StartManipulationTest


global ficha
global plataformaSalida
global llamado

ficha = 0
plataformaSalida = ""
llamado = False



class Manipulation_test(Node):

    #Inicializacion del nodo publicador hacia el topico
    def __init__(self):

        super().__init__('manipulation_test')

        #Declaración de nodos publicadores
        self.pub_carro_vel = self.create_publisher(Twist, '/car_vel', 10)
        self.pub_garra_vel = self.create_publisher(Twist, '/gar_vel', 10)

        #Declaracion del servicio
        self.service = self.create_service(StartManipulationTest, '/group_'+str(4)+'/start_manipulation_test_srv', self.handle_request)

        #Creacion temporizador 
        periodo = 1
        self.timer = self.create_timer(periodo, self.movimiento_punto)

    def handle_request(self, request, response):

        global ficha, plataformaSalida, llamado
        # Inicializa la respuesta del servicio
        plataformaSalida = request.platform
        plataformaLlegada = ""
        ficha = request.x

        #Reviso cual numero de plataforma recibio y digo si la otra es entonces la 1 o 2
        if plataformaSalida == "platform_1":
            plataformaLlegada = "platform_2"
        elif plataformaSalida == "platform_2":
            plataformaLlegada = "platform_1"
        else:
            response.answer = "La plataforma ingresada no existe."
            return response
        
        llamado = True

        #Se imprime la solicitud recibida
        respuesta = "La ficha de tipo " + str(ficha) + " se encuentra en la plataforma " + plataformaSalida+ " y la llevare a la plataforma " + plataformaLlegada + "."
        response.answer = respuesta

        return response
    
    #Metodo que realiza el movimiento del robot hasta la mitad entre plataformas
    def movimiento_punto(self):

        global ficha, plataformaSalida, llamado

        #Metodo que mueve el robot hasta la mitad entre plataformas
        if llamado == True:
            self.apagarTimer()

            self.car_twist(1.0,0.0,0.0,1.0)
            self.car_twist(0.0,0.0,1.0,1.0)
            self.car_twist(1.0,0.0,0.0,1.0)
            self.car_twist(0.0,0.0,0.0,0.1)

            #Recoger las 3 fichas
            for i in range(1,3):
                self.movimiento_garra()


    #Metodo que realiza el movimiento de la garra
    def movimiento_garra(self):
        global ficha, plataformaSalida, llamado

        #Grados plataforma 1
        rotP1, j1P1, j2P1, j3P1, rotgP1, garP1 = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
        #Grados plataforma 2
        rotP2, j1P2, j2P2, j3P2, rotgP2, garP2 = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0

        #Metodo que mueve la garra
        if llamado == True:
            if plataformaSalida == "platform_1":
                #Movimiento hasta plataforma 1 
                self.garra_twist(rotP1,j1P1,j2P1,j3P1,rotgP1,garP1,2.0)
                #Agarre de ficha
                self.garra_twist(rotP1,j1P1,j2P1,j3P1,rotgP1,90.0,2.0)

            elif plataformaSalida == "platform_2":
                #Movimiento hasta plataforma 1 
                self.garra_twist(rotP2,j1P2,j2P2,j3P2,rotgP2,garP2,2.0)
                #Agarre de ficha
                self.garra_twist(rotP2,j2P2,j2P2,j3P2,rotgP2,90.0,2.0)

            self.garra_twist(60.0,0.0,0.0,0.0,0.0,90.0,2.0)

            #Movimiento hacia la plataforma de destino
            if plataformaSalida == "platform_1":
                #Movimiento hasta plataforma 1 
                self.garra_twist(rotP1,j1P1,j2P1,j3P1,rotgP1,90.0,2.0)
                #Agarre de ficha
                self.garra_twist(rotP1,j1P1,j2P1,j3P1,rotgP1,garP1,2.0)
            elif plataformaSalida == "platform_2":
                #Movimiento hasta plataforma 1 
                self.garra_twist(rotP2,j1P2,j2P2,j3P2,rotgP2,90.0,2.0)
                #Agarre de ficha
                self.garra_twist(rotP2,j1P2,j2P2,j3P2,rotgP2,garP2,2.0)
            
            self.garra_twist(60.0,0.0,0.0,0.0,0.0,0.0,10.0)

    
    #Metodo que mueve el robot en una direccion con una velocidad y tiempo determinado
    def car_twist(self, x, y, z, tiempo):
        twist = Twist()
        twist.linear.x = x
        twist.linear.y = y
        twist.linear.z = z
        self.pub_carro_vel.publish(twist)
        time.sleep(tiempo)

    #Metodo que mueve la garra
    def garra_twist(self, rot, j1, j2, j3, rotg, g, tiempo):    
        twist = Twist()
        twist.linear.x = rot
        twist.linear.y = j1
        twist.linear.z = j2
        twist.angular.x = j3
        twist.angular.y = rotg
        twist.angular.z = g

        self.pub_garra_vel.publish(twist)
        time.sleep(tiempo)

    #Metodo que apaga el temporizador
    def apagarTimer(self):
        if self.timer is not None:
            self.timer.cancel()
            self.timer = None


def main(args=None):

    rclpy.init(args=args)
            
    manipulation_test = Manipulation_test()

    rclpy.spin(manipulation_test) 

    manipulation_test.destroy_node()    

    rclpy.shutdown()   


if __name__ == '__main__':

    main()
