from ClassLib.Wheels import Wheels 
from ClassLib.PWMTimer import PWMTimer
from pyb import Timer

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