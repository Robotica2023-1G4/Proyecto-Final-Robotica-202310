import rclpy
import math
import numpy as np
from rclpy.node import Node
from geometry_msgs.msg import Twist
import time
import serial

#Nombres entrada del puerto para los motores
pserialCar = serial.Serial('/dev/ttyACM0', 9600)
pserialGar = serial.Serial('/dev/ttyACM1', 9600)

#Se crea la clase que se encarga de recibir los mensajes de velocidad
class RobotController(Node):

    def __init__(self):
        super().__init__('robot_controller')
        self.subscription1 = self.create_subscription(
            Twist,
            '/car_vel',
            self.listener_callback_car,
            10)
        self.subscription2 = self.create_subscription(
            Twist,
            '/gar_vel',
            self.listener_callback_gar,
            10)
        self.subscription1  # prevent unused variable warning
        self.subscription2  # prevent unused variable warning


    def listener_callback_car(self, msg):
        # Convertir velocidad lineal y angular en velocidades de los motores
        vel_linear = int(msg.linear.x)
        vel_linearY = int(msg.linear.y)
        vel_angular = int(msg.angular.z)

        if vel_linear > 0:
            pserialCar.write([87])
        elif vel_linear < 0:
            pserialCar.write([83])
        elif vel_linearY < 0:
            pserialCar.write([81])
        elif vel_linearY  > 0:
            pserialCar.write([69])
        elif vel_angular > 0:
            pserialCar.write([68])
        elif vel_angular < 0:
            pserialCar.write([65])
        else:
            pserialCar.write([48])



    def listener_callback_gar(self, msg):
        velRot = int(msg.linear.x) 
        print(velRot)
        velj1 = int(msg.linear.y) 
        velj2 = int(msg.linear.z)
        velj3 = int(msg.angular.x)
        velg = int(msg.angular.y)
        velrotg = int(msg.angular.z) 
        message = f"{velRot},{velj1},{velj2},{velj3},{velg},{velrotg}\n" # creamos el mensaje con el formato requerido por Arduino
        print(message)
        pserialGar.write(message.encode()) # enviamos el mensaje a través del puerto serial
        

def main(args=None):
    rclpy.init(args=args)
    robot_controller = RobotController()
    rclpy.spin(robot_controller)
    robot_controller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()