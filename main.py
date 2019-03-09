from ClassLib.RobotCar import Car
from pyb import LED
from pyb import Pin
from pyb import Timer

ENA=Pin('Y1',Pin.OUT_PP)
ENB=Pin('Y2',Pin.OUT_PP)

IN1=Pin('Y3',Pin.OUT_PP)
IN2=Pin('Y4',Pin.OUT_PP)
IN3=Pin('Y5',Pin.OUT_PP)
IN4=Pin('Y6',Pin.OUT_PP)

red_light	= Pin(Pin.cpu.A13,Pin.OUT_PP)
green_light	= Pin(Pin.cpu.A14,Pin.OUT_PP)
yellow_light= Pin(Pin.cpu.A15,Pin.OUT_PP)


My_Car=Car(ENA,IN1,IN2,8,1,20000,0,ENB,IN3,IN4,8,2,20000,0,green_light,red_light,yellow_light)
while True:
	order=input('请输入命令:')
	print('\n')
	if order=='0':
		My_Car.lights.all_lights_on()
	elif order=='1':
		My_Car.forward_with_speed(pwpx=100)
	elif order=='2':
		My_Car.back_with_speed(pwpx=80)
	elif order=='3':
		My_Car.turn_left(level=2)
	elif order=='4':
		My_Car.stop()
	elif order=='5':
		My_Car.cutoff()
	order=' '
	print('\n -----------------------------------\n')