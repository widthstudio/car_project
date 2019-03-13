from ClassLib.Bluetooth_Car import Bluetooth_Car
from pyb import LED
from pyb import Pin
from pyb import Timer
from pyb import UART

ENA=Pin('Y1',Pin.OUT_PP)
ENB=Pin('Y2',Pin.OUT_PP)

IN1=Pin('Y3',Pin.OUT_PP)
IN2=Pin('Y4',Pin.OUT_PP)
IN3=Pin('Y5',Pin.OUT_PP)
IN4=Pin('Y6',Pin.OUT_PP)

red_light	= Pin(Pin.cpu.A13,Pin.OUT_PP)
green_light	= Pin(Pin.cpu.A14,Pin.OUT_PP)
yellow_light= Pin(Pin.cpu.A15,Pin.OUT_PP)


My_Car=Bluetooth_Car(ENA,IN1,IN2,8,1,20000,0,ENB,IN3,IN4,8,2,20000,0,green_light,red_light,yellow_light,1,115200)
while True:
	My_Car.bluetooth_receive_and_run()
	pyb.delay(100) #100ms收一次
	
	
	