import pyb
from pyb import LED
from pyb import Pin
from pyb import Timer
from ClassLib.Wheels import Wheels 
from ClassLib.PWMTimer import PWMTimer
from ClassLib.Car_side import Carside
from ClassLib.CarLights import CarLights

#定义车类，调用车侧类
class  Car(object):
	def __init__(self,ENr,IN1r,IN2r,timerr,channelr,freqr,pwprr,ENl,IN1l,IN2l,timerl,channell,freql,pwprl,red_light,yellow_light,green_light):
		self.right = Carside(ENr, IN1r, IN2r, timerr, channelr, freqr, pwprr)
		self.left  = Carside(ENl, IN1l, IN2l, timerl, channell, freql, pwprl)
		self.lights=CarLights(green_light,red_light,yellow_light)

    #前进绿灯

	def forward_with_speed(self,pwpx=100):  
		self.lights.all_lights_off()
		self.right.forward_with_speed(pwpx)
		self.left.forward_with_speed(pwpx)  
		self.lights.green_light_on()
		print('back with speed ',pwpx)
		#倒车红灯
	def back_with_speed(self,pwpx=80): 
		self.lights.all_lights_off()
		self.right.back_with_speed(pwpx)
		self.left.back_with_speed(pwpx) 
		self.lights.red_light_on()
		print('back with speed ',pwpx)
		print('red light')
		#刹车红灯
	def stop(self): 
		self.lights.all_lights_off()
		self.right.stop()
		self.left.stop()
		self.lights.red_light_on()
		print('stop')
		print('red light')
		#熄火灭灯   
	def cutoff(self):
		self.lights.all_lights_off()
		self.right.cutoff()
		self.left.cutoff()
		print('cut off')
	#转弯黄灯亮，分三种程度，level取值1，2，3
	#1:微小偏转
	#2:中度偏转
	#3：大角度偏转，右轮刹车
	def turn_right(self,level=2):
		self.lights.all_lights_off()
		if level==1:
			self.left.back_with_speed(100)
			self.right.back_with_speed(80)
			print("turn right on level 1")
		elif level==2:
			self.left.back_with_speed(100)
			self.right.back_with_speed(70)
			print("turn right on level 2")
		elif level==3:
			self.left.back_with_speed(100)
			self.right.stop()
			print("turn right on level ",level)
		self.lights.yellow_light_on()
		
	def turn_left(self,level=2):
		self.lights.all_lights_off()
		if level==1:
			self.left.back_with_speed(80)
			self.right.back_with_speed(100)
			print("turn right on level 1")
		elif level==2:
			self.left.back_with_speed(70)
			self.right.back_with_speed(100)
			print("turn right on level 2")
		elif level==3:
			self.right.back_with_speed(100)
			self.left.stop()
			print("turn left on level ",level)
		self.lights.yellow_light_on()
        

def main():
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



if __name__=="__main":
	main()