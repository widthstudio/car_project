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