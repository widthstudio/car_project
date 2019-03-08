from pyb import Pin
from pyb import Timer

ENA=Pin('Y1',Pin.OUT_PP)
ENB=Pin('Y2',Pin.OUT_PP)

IN1=Pin('Y3',Pin.OUT_PP)
IN2=Pin('Y4',Pin.OUT_PP)
IN3=Pin('Y5',Pin.OUT_PP)
IN4=Pin('Y6',Pin.OUT_PP)



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
		pyb.LED(3).on() 
		print('back with speed ',pwpx)
		print('green light')
		#倒车红灯
	def back_with_speed(self,pwpx=80): 
		self.led_all_off()
		self.right.back_with_speed(pwpx)
		self.left.back_with_speed(pwpx) 
		pyb.LED(1).on() 
		print('back with speed ',pwpx)
		print('red light')
    #刹车红灯
	def stop(self): 
		self.led_all_off()
		self.right.stop()
		self.left.stop()
		pyb.LED(1).on() 
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
		pyb.LED(2).on()  
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
		pyb.LED(2).on()  
		print("yellow light")
        


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





















'''




		
#right side
	#设置右轮参数，输入 Pin对象
	def set_right(self,ENr,INr1,INr2):
		self.right.EN=ENr
		self.right.IN1=INr1
		self.right.IN2=INr2
	#设置右轮PWM时钟和通道
	# pwp 60~100
	#if pwp>100, pwp=100
	#if pwp<60,pwp=60
	def set_right_pwm_timer(self,timerr,channelr,freqr,pwpr):
		self.right_timer=Timer(timerr,freq=freqr) #10000hz
		if pwpr>100:
			pwpr=100
		elif pwpr<60:
			pwpr=60
		self.right_pwm_timer=self.right_timer.channel(channelr, Timer.PWM, pin=self.right.EN, pulse_width_percent=pwpr)		
	#设置右轮速度 pwp 60~100
	def set_right_speed(self,pwpr):
		if pwpr>100:
			pwpr=100
		elif pwpr<60:
			pwpr=60
		self.right_pwm_timer.pulse_width_percent(pwpr)
		
#left side 
	#设置左轮参数，输入 Pin对象
	def set_left(self,ENl,INl1,INl2):
		self.left.EN=ENl
		self.left.IN1=INl1
		self.left.IN2=INl2
	#设置左轮PWM时钟和通道
	# pwp 60~100
	#if pwp>100, pwp=100
	#if pwp<60,pwp=60
	def set_left_pwm_timer(self,timerl,channell,freql,pwpl):
		self.left_timer=Timer(timerl,freq=freql) #10000hz
		if pwpr>100:
			pwpr=100
		elif pwpr<60:
			pwpr=60
		self.left_pwm_timer=self.left_timer.channel(channell, Timer.PWM, pin=self.left.EN, pulse_width_percent=pwpl)	
	#设置左轮速度 pwp 60~100		
	def set_left_speed(self,pwpl):
		if pwpl>100:
			pwpl=100
		elif pwpl<60:
			pwpl=60
		self.left_pwm_timer.pulse_width_percent(pwpl)

	




ENA=Pin('Y1',Pin.OUT_PP)
IN1=Pin('Y2',Pin.OUT_PP)
IN2=Pin('Y3',Pin.OUT_PP)

ENA.value(0)
IN1.value(0)
IN2.value(0)


timer1=Timer(8,freq=10000) #10000hz
pwm_timer=timer1.channel(1,Timer.PWM,pin=ENA,pulse_width_percent=99)

BlueT=UART(1,115200)

def read_uart_bluet():
	BlueT_read_result=BlueT.read(BlueT.any())
	pyb.delay(10)
	return BlueT_read_result

	
a=99


def cb():
	global a
	a+=2
	a=a%102
	if a < 60 :
		a=60
	print(a)
	
#sw=Switch()
#sw.callback(cb)

def forward( speed ):
	pyb.LED(1).off()
	pyb.LED(2).off()
	pwm_timer.pulse_width_percent(speed%101)
	ENA.value(1)
	IN1.value(0)
	IN2.value(1)
	pyb.LED(3).on()
def back( speed ):
	pyb.LED(1).off()
	pyb.LED(3).off()
	pwm_timer.pulse_width_percent(speed%101)
	ENA.value(1)
	IN1.value(0)
	IN2.value(1)
	pyb.LED(2).on()
def stop():
	pyb.LED(2).off()
	pyb.LED(3).off()
	ENA.value(1)
	IN1.value(0)
	IN2.value(0)
	pyb.LED(1).on()	
def wait():
	ENA.value(0)

def move(direction=1,speed=100):
	if direction==1:
		forward(speed)
	elif direction==2:
		back(speed)
	elif direction==3:
		stop()
	else :
		wait()
	'''

order={
b'11':1100,
b'forward_harf':180,
b'forward_slow':170,
b'back_full':2100,
b'back_harf':280,
b'back_slow':270,
b'stop':30,
b'wait':40
}



	
	
	
	
	

	