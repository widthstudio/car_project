import pyb
from pyb import Pin
from pyb import Timer
from pyb import UART
from pyb import Servo
from ClassLib.Multif_Car import Multif_Car




ENA=Pin('Y1',Pin.OUT_PP)
ENB=Pin('Y2',Pin.OUT_PP)

IN1=Pin('Y3',Pin.OUT_PP)
IN2=Pin('Y4',Pin.OUT_PP)
IN3=Pin('Y5',Pin.OUT_PP)
IN4=Pin('Y6',Pin.OUT_PP)

ECHO=Pin('Y11',Pin.IN)
TRIG=Pin('Y12',Pin.OUT_PP)

My_Servo=Servo(1)

red_light	= Pin(Pin.cpu.A13,Pin.OUT_PP)
green_light	= Pin(Pin.cpu.A14,Pin.OUT_PP)
yellow_light= Pin(Pin.cpu.A15,Pin.OUT_PP)

xunji_IN4=Pin('X22',Pin.IN)#右
xunji_IN3=Pin('X21',Pin.IN)#中
xunji_IN2=Pin('X20',Pin.IN)#中
xunji_IN1=Pin('X19',Pin.IN)#左

uart=UART(1,9600)
uart.write("I am ready")
pyb.delay(10)

My_Car=Multif_Car(ENA,IN1,IN2,8,1,20000,0,ENB,IN3,IN4,8,2,20000,0,green_light,red_light,yellow_light,xunji_IN1,xunji_IN2,xunji_IN3,xunji_IN4,My_Servo,TRIG,ECHO,1,9600)

while True:
	My_Car.bluetooth_receive_and_run()
	