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
		self.IN1.value(1)
		self.IN2.value(0)
	def back(self):
		self.EN.value(1)
		self.IN1.value(0)
		self.IN2.value(1)
	def stop(self):
		self.EN.value(1)
		self.IN1.value(0)
		self.IN2.value(0)
	def cutoff(self): #熄火
		self.EN.value(0)
		self.IN1.value(0)
		self.IN2.value(0)