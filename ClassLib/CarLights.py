#定义绿灯、黄灯和红灯
#绿灯代表前大灯，前行
#红灯代表刹车灯，倒车，刹车
#黄灯代表转向灯，转向
#低电平亮灯
class CarLights(object):
	def __init__(self, Green_light, Red_light, Yellow_light):
		self.green_light=Green_light
		self.red_light=Red_light
		self.yellow_light=Yellow_light
	def yellow_light_on(self):
		self.yellow_light.value(1)
		print('yellow light on')
	def yellow_light_off(self):
		self.yellow_light.value(0)
		print('yellow light off')
	def red_light_on(self):
		self.red_light.value(1)
		print('red light on')
	def red_light_off(self):
		self.red_light.value(0)
		print('red light off')
	def green_light_on(self):
		self.green_light.value(1)
		print('green light on')
	def green_light_off(self):
		self.green_light.value(0)
		print('green light off')
	def all_lights_on(self):
		self.green_light.value(1)
		self.green_light.value(1)
		self.green_light.value(1)
		print('all lights on')
	def all_lights_off(self):
		self.green_light.value(0)
		self.green_light.value(0)
		self.green_light.value(0)
		print('all lights off')