import rclpy
import time
from rclpy.node import Node
from proyecto_interfaces.srv import StartPerceptionTest
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
from proyecto_interfaces.msg import Banner
from cv_bridge import CvBridge
import pytesseract
import cv2
import numpy as np

global banner1
global banner2
global llamado 




banner1 = 0
banner2 = 0
llamado = False

#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Inicializar la cámara
#captura = cv2.VideoCapture(0)

# Diccionario para almacenar las figuras detectadas
figuras_detectadas = {}

# Especificar la región de interés (ROI)
roi_x = 0  # Posición x de la esquina superior izquierda de la ROI
roi_y = 0  # Posición y de la esquina superior izquierda de la ROI
roi_width = 640  # Ancho de la ROI
roi_height = 160  # Altura de la ROI



# Clase para representar una figura detectada
class Figura:
    def __init__(self, forma, tiempo_inicio):
        self.forma = forma
        self.tiempo_inicio = tiempo_inicio


class Perception_test(Node):

    #Inicializacion del nodo publicador hacia el topico
    def __init__(self):
            
            super().__init__('perception_test')
    
            #Declaración de nodos publicadores
            self.pub_carro_vel = self.create_publisher(Twist, '/car_vel', 10)
            self.pub_banner = self.create_publisher(Banner, 'vision/banner_group_'+str(4), 10)
            
    
            #Declaracion del servicio
            self.service = self.create_service(StartPerceptionTest, '/group_'+str(4)+'/start_perception_test_srv', self.handle_request)
    
            #Creacion temporizador 
            periodo = 1
            self.timer = self.create_timer(periodo, self.movimiento_a_banner)

            self.sub_video = self.create_subscription(Image, 'camara_topic',self.image_callback, 10)
            self.bridge = CvBridge()
            self.frame = 0
            self.n = 0

    def image_callback(self, msg):
        try:
            self.frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
            # Aquí puedes procesar el marco de imagen de OpenCV según tus necesidades
            # ...
           
        except Exception as e:
            self.get_logger().info(str(e))

    def handle_request(self, request, response):

        global banner1, banner2, llamado
    
        # Inicializa la respuesta del servicio
        banner1 = request.banner_a
        banner2 = request.banner_b
    
        #Se imprime la solicitud recibida
        respuesta = "Debo identificar el banner " + str(banner1) + ", y el banner " + str(banner2) + "."
        response.answer = respuesta

        llamado = True

        return response 
    

    #Metodo que realiza el recorrido del robot a cada banner
    def movimiento_a_banner(self):
         
        global banner1, banner2, llamado

        if llamado == True:
            self.apagar_timer()

            #Se mueve hacia el inicio de la prueba
            self.car_twist(1.0,0.0,0.0,1.1)
            self.car_twist(0.0,0.0,0.0,0.1)
            time.sleep(3)

            #Se mueve hacia el banner 1
            self.car_twist(0.0,0.0,-1.0,0.30)
            self.car_twist(0.0,0.0,0.0,0.1)

            time.sleep(5)

            #Revisa si debe hacer la prueba de vision
            if banner1 == 1 or banner2 == 1:
                time.sleep(2)
                frame1 = self.frame.copy()
                figura, texto, color = self.vision_computadora(frame1)
                banner1 = Banner()
                banner1.banner = 1
                banner1.figure = figura
                banner1.word = texto
                banner1.color = color
                self.pub_banner.publish(banner1)
                time.sleep(2)
            
            #Se mueve hacia el banner 2
            self.car_twist(0.0,0.0,1.0,0.5)
            self.car_twist(0.0,0.0,0.0,1.0)
            self.car_twist(1.0,0.0,0.0,0.5)
            self.car_twist(0.0,0.0,0.0,1.0)
            self.car_twist(0.0,0.0,1.0,0.5)
            self.car_twist(0.0,0.0,0.0,0.1)

            time.sleep(5)

            #Revisa si debe hacer la prueba de vision
            if banner1 == 2 or banner2 == 2:
                time.sleep(2)
                frame2 = self.frame.copy()
                figura, texto, color = self.vision_computadora(frame2)
                banner2 = Banner()
                banner2.banner = 2
                banner2.figure = figura
                banner2.word = texto
                banner2.color = color
                self.pub_banner.publish(banner2)
                time.sleep(2)

            #Se mueve hacia el banner 3
            self.car_twist(1.0,0.0,0.0,0.2)
            self.car_twist(0.0,0.0,0.0,1.0)
            self.car_twist(0.0,0.0,1.0,0.6)
            self.car_twist(0.0,0.0,0.0,1.0)
            self.car_twist(1.0,0.0,0.0,0.2)
            self.car_twist(0.0,0.0,0.0,0.1)
            time.sleep(5)

            #Revisa si debe hacer la prueba de vision
            if banner1 == 3 or banner2 == 3:
                time.sleep(2)
                frame3 = self.frame.copy()
                figura, texto, color = self.vision_computadora(frame3)
                banner3 = Banner()
                banner2.banner = 2
                banner3.figure = figura
                banner3.word = texto
                banner3.color = color
                self.pub_banner.publish(banner3)
                time.sleep(2)

    def vision_computadora(self, fotograma):

        # Capturar un fotograma de la cámara
        
        #cv2.imshow("Detección de figuras", fotograma)
        #cv2.waitKey(1)

            
        texto = self.detectar_palabras(fotograma)
        
        # Obtener la región de interés (ROI) del fotograma
        roi = fotograma[roi_y:roi_y+roi_height, roi_x:roi_x+roi_width]
        
        # Detectar figuras geométricas y círculos en la región de interés
        roi_con_figuras,figura = self.detectar_figuras(roi, figuras_detectadas,self.n)
            
        nomFigura = self.convertir_figura(figura)

        color = self.identificar_color(fotograma)[1]
            
        print(color, self.n, texto)
            
        # Dibujar un rectángulo que representa la región de interés en el fotograma completo
        cv2.rectangle(fotograma, (roi_x, roi_y), (roi_x+roi_width, roi_y+roi_height), (0, 0, 255), 2)
    
        # Mostrar el fotograma completo con la región de interés y las figuras detectadas
        cv2.imshow("Detección de figuras", fotograma)
        cv2.waitKey(1)

        return nomFigura, texto, color

    def convertir_figura(self,numero_lados):
        if numero_lados < 3 or numero_lados > 8:
            return "No se reconoce la figura"
        elif numero_lados == 3:
            return "Triángulo"
        elif numero_lados == 4:
            return "Cuadrado"
        elif numero_lados == 5:
            return "Pentágono"
        elif numero_lados == 6:
            return "Hexágono"
        elif numero_lados == 7:
            return "Heptágono"
        elif numero_lados == 8:
            return "Octágono"



    # Función para detectar diferentes figuras geométricas y círculos en una región de interés (ROI)
    def detectar_figuras(self, roi, figuras_detectadas,n):
        # Convertir la ROI a escala de grises
        gris = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    
        # Aplicar un umbral para obtener una imagen binaria
        _, umbral = cv2.threshold(gris, 127, 255, cv2.THRESH_BINARY_INV)
    
        # Encontrar los contornos en la imagen binaria
        contornos, _ = cv2.findContours(umbral, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
        # Obtener el tiempo actual
        tiempo_actual = time.time()
    
    
        # Iterar sobre los contornos y clasificar las figuras geométricas y círculos
        for contorno in contornos:
            perimetro = cv2.arcLength(contorno, True)
            aproximacion = cv2.approxPolyDP(contorno, 0.04 * perimetro, True)
        
            # Obtener el número de lados de la figura
            num_lados = len(aproximacion)
        
            # Dibujar las figuras geométricas detectadas
            if num_lados >= 3 and num_lados <= 7:
                cv2.drawContours(roi, [aproximacion], 0, (0, 255, 0), 2)  # Dibujar figura en verde
            
                # Verificar si la figura ha estado presente durante más de 10 segundos
                if num_lados not in figuras_detectadas or (tiempo_actual - figuras_detectadas[num_lados].tiempo_inicio) > 10:
                    # Crear una nueva instancia de Figura
                    figura = Figura(aproximacion, tiempo_actual)
                
                    # Guardar la figura en el diccionario de figuras detectadas
                    figuras_detectadas[num_lados] = figura
                
                    # Imprimir la figura
                    #print(f"Figura detectada: {num_lados} lados")
                    #print(id)
                    n = num_lados
        
            # Detectar círculos
            if num_lados > 7:
                (x, y), radio = cv2.minEnclosingCircle(aproximacion)
                centro = (int(x), int(y))
                radio = int(radio)
                cv2.circle(roi, centro, radio, (0, 0, 255), 2)  # Dibujar círculo en rojo

                # Verificar si el círculo ha estado presente durante más de 10 segundos
                if 'circulo' not in figuras_detectadas or (tiempo_actual - figuras_detectadas['circulo'].tiempo_inicio) > 10:
                    # Crear una nueva instancia de Figura
                    figura = Figura(aproximacion, tiempo_actual)

                    # Guardar la figura en el diccionario de figuras detectadas
                    figuras_detectadas['circulo'] = figura

                    # Imprimir la figura
                    #print("Círculo detectado")
                    #print(id)
                    n = 1
        

        return roi,n
    
    def identificar_color(self,frame):
    
        # Coordenadas de la región de interés (ROI) color
        roi_x1 = 0
        roi_y1 = 320
        roi_width1 = 640
        roi_height1 = 160
    
        # Definir la región de interés (ROI)
        roi = frame[roi_y1:roi_y1+roi_height1, roi_x1:roi_x1+roi_width1]
    
        # Convertir la ROI de BGR a HSV
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    
        # Definir los rangos de colores que quieres detectar
        lower_red = np.array([0, 100, 100])
        upper_red = np.array([10, 255, 255])
    
        lower_green = np.array([40, 100, 100])
        upper_green = np.array([70, 255, 255])
    
        lower_blue = np.array([90, 100, 100])
        upper_blue = np.array([130, 255, 255])
    
        lower_white = np.array([0, 0, 200])
        upper_white = np.array([180, 30, 255])
    
        lower_black = np.array([0, 0, 0])
        upper_black = np.array([180, 255, 30])
    
        lower_yellow = np.array([20, 100, 100])
        upper_yellow = np.array([40, 255, 255])
    
        # Crear máscaras para cada rango de colores
        mask_red = cv2.inRange(hsv, lower_red, upper_red)
        mask_green = cv2.inRange(hsv, lower_green, upper_green)
        mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
        mask_white = cv2.inRange(hsv, lower_white, upper_white)
        mask_black = cv2.inRange(hsv, lower_black, upper_black)
        mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
    
        # Aplicar las máscaras a la ROI para obtener los píxeles dentro de cada rango de colores
        result_red = cv2.bitwise_and(roi, roi, mask=mask_red)
        result_green = cv2.bitwise_and(roi, roi, mask=mask_green)
        result_blue = cv2.bitwise_and(roi, roi, mask=mask_blue)
        result_white = cv2.bitwise_and(roi, roi, mask=mask_white)
        result_black = cv2.bitwise_and(roi, roi, mask=mask_black)
        result_yellow = cv2.bitwise_and(roi, roi, mask=mask_yellow)
    
        # Contar los píxeles no negros en cada resultado
        count_red = cv2.countNonZero(mask_red)
        count_green = cv2.countNonZero(mask_green)
        count_blue = cv2.countNonZero(mask_blue)
        count_white = cv2.countNonZero(mask_white)
        count_black = cv2.countNonZero(mask_black)
        count_yellow = cv2.countNonZero(mask_yellow)
    
        # Crear un diccionario con los resultados
        resultados = {
            'Rojo': count_red,
            'Verde': count_green,
            'Azul': count_blue,
            'Blanco': count_white,
            'Negro': count_black,
            'Amarillo': count_yellow
        }
    
        # Encontrar el color con la mayor cantidad de píxeles
        color_maximo = max(resultados, key=resultados.get)
    
        # Mostrar las imágenes resultantes y la imagen original
        #cv2.imshow('Red', result_red)
        #cv2.imshow('Green', result_green)
        #cv2.imshow('Blue', result_blue)
        #cv2.imshow('White', result_white)
        #cv2.imshow('Black', result_black)
        #cv2.imshow('Yellow', result_yellow)
    
        # Dibujar un rectángulo que representa la región de interés en el fotograma completo
        cv2.rectangle(frame, (roi_x1, roi_y1), (roi_x1+roi_width1, roi_y1+roi_height1), (0, 255, 255), 2)
        #cv2.imshow('Original', frame)
        
        # Imprimir el color con la mayor cantidad de píxeles
        #print("El color predominante es:", color_maximo)
        
        # Esperar a que se presione la tecla 'q' para salir del programa
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return (False,color_maximo)
        
        return (True,color_maximo)


    def detectar_palabras(self, imagen):
        
        # Coordenadas de la región de interés (ROI)
        x_roi = 0  # Coordenada x superior izquierda
        y_roi = 160  # Coordenada y superior izquierda
        w_roi = 640  # Ancho de la región
        h_roi = 160  # Altura de la región
        
        # Recortar la imagen utilizando las coordenadas de la ROI
        roi = imagen[y_roi:y_roi+h_roi, x_roi:x_roi+w_roi]
        
        # Convertir la imagen de la ROI a escala de grises
        roi_gris = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

        # Aplicar OCR para extraer el texto de la ROI
        texto = pytesseract.image_to_string(roi_gris)
            
        # Obtener las coordenadas de las palabras encontradas por Tesseract
        cajas_palabras = pytesseract.image_to_boxes(roi_gris)
            
        # Dibujar los recuadros alrededor de las palabras en la imagen en vivo
        for caja in cajas_palabras.splitlines():
            caja = caja.split(' ')
            x, y, w, h = int(caja[1]), int(caja[2]), int(caja[3]), int(caja[4])
            cv2.rectangle(roi, (x, roi.shape[0] - y), (w, roi.shape[0] - h), (0, 255, 0), 2)
        
        return texto
    
    #Metodo que mueve el robot en una direccion con una velocidad y tiempo determinado
    def car_twist(self, x, y, z, tiempo):
        twist = Twist()
        twist.linear.x = x
        twist.linear.y = y
        twist.linear.z = z
        self.pub_carro_vel.publish(twist)
        time.sleep(tiempo)

    #Metodo que apaga el timer
    def apagar_timer(self):
        if self.timer is not None:
            self.timer.cancel()
            self.timer = None



def main(args=None):

    rclpy.init(args=args)
            
    perception_test = Perception_test()

    rclpy.spin(perception_test) 

    perception_test.destroy_node()    

    rclpy.shutdown()   


if __name__ == '__main__':

    main()