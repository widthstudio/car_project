from ClassLib.RobotCar import Car
import pyb
from pyb import Pin

class xunji_Car(Car):
	def __init__(self,ENr,IN1r,IN2r,timerr,channelr,freqr,pwprr,ENl,IN1l,IN2l,timerl,channell,freql,pwprl,green_light,red_light,yellow_light,xunji_IN1,xunji_IN2,xunji_IN3,xunji_IN4):
		Car.__init__(self,ENr,IN1r,IN2r,timerr,channelr,freqr,pwprr,ENl,IN1l,IN2l,timerl,channell,freql,pwprl,green_light,red_light,yellow_light)
		self.xunji_IN1=xunji_IN1
		self.xunji_IN2=xunji_IN2
		self.xunji_IN3=xunji_IN3
		self.xunji_IN4=xunji_IN4
	def xunji(self):
		self.forward_with_speed(3)
		if self.xunji_IN4.value()==1:
			self.turn_right(4)
			pyb.delay(150)
		elif self.xunji_IN1.value()==1:
			self.turn_left(4)
			pyb.delay(150)
		else:
			pass