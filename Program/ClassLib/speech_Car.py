import pyb
from pyb import LED
from pyb import Pin
from pyb import Timer
from pyb import UART
from ClassLib.RobotCar import Car

class speech_Car(Car):
	def __init__(self,ENr,IN1r,IN2r,timerr,channelr,freqr,pwprr,ENl,IN1l,IN2l,timerl,channell,freql,pwprl,green_light,red_light,yellow_light,uartx=1,baud_ratex=9600,mode=1):
		Car.__init__(self,ENr,IN1r,IN2r,timerr,channelr,freqr,pwprr,ENl,IN1l,IN2l,timerl,channell,freql,pwprl,green_light,red_light,yellow_light)
		self.ljh_uart=UART(uartx,baud_ratex)
		self.mode=mode
	def get_and_run(self):
		g=self.ljh_uart.read(self.ljh_uart.any())
		pyb.delay(10)
		print(g)
		pyb.delay(10)
		if g==b'0':
			self.mode=1 #刹车模式
		elif g==b'13':
			self.mode=2 #前进模式
		elif g==b'33':
			self.mode=3 #左转模式
		elif g==b'43':
			self.mode=4	#右转模式
		elif g==b'5':
			self.mode=5 #避障模式
		elif g==b'6':
			self.mode=6 #寻迹模式
		elif g==b'23':
			self.mode=7 #后退模式
		else:
			pass
		
		