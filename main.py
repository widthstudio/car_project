from RobotCar import *
My_Car=Car(ENA,IN1,IN2,8,1,20000,0,ENB,IN3,IN4,8,2,20000,0)
while True:
	order=input('请输入命令:')
	print('\n')
	if order=='0':
		My_Car.led_all_on()
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