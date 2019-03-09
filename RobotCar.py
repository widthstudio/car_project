import pyb
from pyb import LED
from pyb import Pin
from pyb import Timer

ENA=Pin('Y1',Pin.OUT_PP)
ENB=Pin('Y2',Pin.OUT_PP)

IN1=Pin('Y3',Pin.OUT_PP)
IN2=Pin('Y4',Pin.OUT_PP)
IN3=Pin('Y5',Pin.OUT_PP)
IN4=Pin('Y6',Pin.OUT_PP)

red_light	=LED(1)
green_light	=LED(2)
yellow_light=LED(3)
blue_light	=LED(4)

#定义轮子类,实现前进、后退、刹车、等待（不控制）四种状态
class Wheels(object):
	def __init__(self,ENx,IN1x,IN2x):
		self.EN	= ENx
		self.IN1= IN1x
		self.IN2= IN2x
	def set_wheels(self,ENx,IN1x,IN2x):
		self.wheels.EN	= ENx
		self.wheels.IN1	= IN1x
		self.wheels.IN2	= IN2x
	def forward(self):
		self.EN.value(1)
		self.IN1.value(0)
		self.IN2.value(1)
	def back(self):
		self.EN.value(1)
		self.IN1.value(1)
		self.IN2.value(0)
	def stop(self):
		self.EN.value(1)
		self.IN1.value(0)
		self.IN2.value(0)
	def cutoff(self): #熄火
		self.EN.value(0)
		self.IN1.value(0)
		self.IN2.value(0)
		
#定义PWM定时器类
class PWMTimer(object):
	def __init__(self,timerx,channelx,pinx,freqx,pwpx):
		self.timer	 = Timer(timerx,freq=freqx)
		self.pwm = self.timer.channel(channelx, Timer.PWM, pin=pinx, pulse_width_percent=pwpx)
	#设置PWM波占空比，要求 60~100，否则取极限值
	def set_pwp(self,pwpx):
		if pwpx>100:
			pwpx=100
		elif pwpx<60:
			pwpx=60
		self.pwm.pulse_width_percent(pwpx)

#定义车侧类，继承 PWMTimer类和轮子类
class Carside(Wheels,PWMTimer):
	def __init__(self,ENx,IN1x,IN2x,timerx,channelx,freqx,pwpx):
		self.EN	 = ENx
		self.IN1 = IN1x
		self.IN2 = IN2x
		self.timer	 = Timer(timerx,freq=freqx)
		self.pwm = self.timer.channel(channelx, Timer.PWM, pin=self.EN, pulse_width_percent=pwpx)
	def forward_with_speed(self,pwpx):
		self.forward()
		self.set_pwp(pwpx)
	def back_with_speed(self,pwpx):
		self.back()
		self.set_pwp(pwpx)
				
#定义车类，调用车侧类
class  Car(object):
	def __init__(self,ENr,IN1r,IN2r,timerr,channelr,freqr,pwprr,ENl,IN1l,IN2l,timerl,channell,freql,pwprl):
		self.right = Carside(ENr, IN1r, IN2r, timerr, channelr, freqr, pwprr)
		self.left  = Carside(ENl, IN1l, IN2l, timerl, channell, freql, pwprl)
    #开灯
	def led_all_on(self):
		for i in [1,2,3,4]:
			pyb.LED(i).on()
		print('all lights on')
    #关灯
	def led_all_off(self):
		for i in [1,2,3,4]:
			pyb.LED(i).off()    
		print('all lights off')
    #前进绿灯
	def forward_with_speed(self,pwpx=100):  
		self.led_all_off()
		self.right.forward_with_speed(pwpx)
		self.left.forward_with_speed(pwpx)  
		green_light.on() 
		print('back with speed ',pwpx)
		print('green light')
		#倒车红灯
	def back_with_speed(self,pwpx=80): 
		self.led_all_off()
		self.right.back_with_speed(pwpx)
		self.left.back_with_speed(pwpx) 
		red_light.on() 
		print('back with speed ',pwpx)
		print('red light')
    #刹车红灯
	def stop(self): 
		self.led_all_off()
		self.right.stop()
		self.left.stop()
		red_light.on() 
		print('stop')
		print('red light')
    #熄火灭灯   
	def cutoff(self):
		self.led_all_off()
		self.right.cutoff()
		self.left.cutoff()
		print('cut off')
	#转弯黄灯亮，分三种程度，level取值1，2，3
	#1:微小偏转
	#2:中度偏转
	#3：大角度偏转，右轮刹车
	def turn_right(self,level=2):
		self.led_all_off()
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
		yellow_light.on()  
		print("yellow light")
		
	def turn_left(self,level=2):
		self.led_all_off()
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
		yellow_light.on()  
		print("yellow light")
        

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