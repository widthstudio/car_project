from ClassLib.RobotCar import Car
from ClassLib.Obstacle_Avoidance_Car import Obstacle_Avoidance_Car
from pyb import LED
from pyb import Pin
from pyb import Timer
from pyb import UART
from pyb import Servo

ENA=Pin('Y1',Pin.OUT_PP)
ENB=Pin('Y2',Pin.OUT_PP)

IN1=Pin('Y3',Pin.OUT_PP)
IN2=Pin('Y4',Pin.OUT_PP)
IN3=Pin('Y5',Pin.OUT_PP)
IN4=Pin('Y6',Pin.OUT_PP)

ECHO=Pin('Y11',Pin.IN)
TRIG=Pin('Y10',Pin.OUT_PP)

My_Servo=Servo(1)

red_light	= Pin(Pin.cpu.A13,Pin.OUT_PP)
green_light	= Pin(Pin.cpu.A14,Pin.OUT_PP)
yellow_light= Pin(Pin.cpu.A15,Pin.OUT_PP)

uart=UART(1,115200)
uart.write("I am ready")
pyb.delay(10)

My_Car=Obstacle_Avoidance_Car(ENA,IN1,IN2,8,1,20000,0,ENB,IN3,IN4,8,2,20000,0,green_light,red_light,yellow_light,My_Servo,TRIG,ECHO)

while True:
	My_Car.Obstacle_Avoidance(speedlevel=3,stop_flag=0)
	
	
	