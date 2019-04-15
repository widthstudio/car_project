import pyb
from pyb import Pin
from pyb import Servo
from ClassLib.RobotCar import Car

class bizhang_Car(Car):
	def __init__(self,ENr,IN1r,IN2r,timerr,channelr,freqr,pwprr,ENl,IN1l,IN2l,timerl,channell,freql,pwprl,green_light,red_light,yellow_light,servo,trig,echo,l=0,flag_turn=0):
		Car.__init__(self,ENr,IN1r,IN2r,timerr,channelr,freqr,pwprr,ENl,IN1l,IN2l,timerl,channell,freql,pwprl,green_light,red_light,yellow_light)
		self.servo=servo
		self.trig=trig
		self.echo=echo
		self.flag_turn=flag_turn
		self.l=l
		
	def voice(self):
		self.trig.value(1)#产生Trig口所需要的高电平
		pyb.udelay(10)#持续10us
		self.trig.value(0)
		ljh_start1=pyb.micros()
		while not self.echo.value() and pyb.micros()-ljh_start1<7000:#Echo口检测到高点平
			pass
		ljh_start=pyb.micros()#测量一个时间
		while self.echo.value() and pyb.micros()-ljh_start<7000:#等待低电平的到来
			pass
		ljh_end=pyb.micros()#再测量一个时间
		self.l=(ljh_end-ljh_start)*340.0/2000000#计算距离的公式	
		
	def bizhang(self):
		self.forward_with_speed(3)
		#检测前方障碍物时
		#转弯优先级右转高左转低
		
		if self.flag_turn%2==0:
			self.servo.angle(0)
			pyb.delay(300)
			self.voice()
			print(self.l)
			if 0.1<self.l<0.8:
				self.servo.angle(-90)
				pyb.delay(300)
				self.voice()
				if self.l<0.5:
					self.servo.angle(90)
					pyb.delay(300)
					self.voice()
					if self.l<0.5:
						self.back_with_speed()
						print(1111)
						pyb.delay(1000)
						self.forward_with_speed(3)
						#ljh_servo.angle(-79)
						#pyb.delay(zhuanjiao_delay)
						#print(l)
						#print(ljh_servo.angle())
					else:
						self.turn_left(3)
						pyb.delay(1120)
						self.forward_with_speed(3)
						self.flag_turn+=2
						#ljh_servo.angle(-79)
						#pyb.delay(zhuanjiao_delay)
				else:
					self.turn_right(3)
					pyb.delay(900)
					self.forward_with_speed(3)
					self.flag_turn+=1
					#ljh_servo.angle(-79)
					#pyb.delay(zhuanjiao_delay)
			elif self.l<0.1:
				self.back_with_speed()
				print(33333)
				pyb.delay(1000)
			else:
				self.forward_with_speed(3)
	
	
	
	
		#转弯优先级左转高右转低
		else:
			self.servo.angle(0)
			pyb.delay(300)
			self.voice()
			if 0.1<self.l<0.8:
				self.servo.angle(-90)
				pyb.delay(300)
				self.voice()
				if self.l<0.5:
					self.servo.angle(85)
					pyb.delay(300)
					self.voice()
					if self.l<0.5:
						self.back_with_speed()
						print(1111)
						pyb.delay(1000)
						self.forward_with_speed(3)
						#ljh_servo.angle(-79)
						#pyb.delay(zhuanjiao_delay)
						#print(l)
						#print(ljh_servo.angle())
					else:
						self.turn_right(3)
						pyb.delay(900)
						self.forward_with_speed(3)
						self.flag_turn+=2
						#ljh_servo.angle(-79)
						#pyb.delay(zhuanjiao_delay)
				else:
					self.turn_left(3)
					pyb.delay(1120)
					self.forward_with_speed(3)
					self.flag_turn+=1
					#ljh_servo.angle(-79)
					#pyb.delay(zhuanjiao_delay)
			elif self.l<0.1:
				self.back_with_speed()
				print(2222)
				pyb.delay(1000)
			else:
				self.forward_with_speed(3)
	
	
	
		#检测靠右墙体是否太近
		self.servo.angle(-90)
		pyb.delay(300)
		self.voice()
		if self.l<0.15:
			self.turn_left(3)
			pyb.delay(600)
			self.forward_with_speed(1)
			pyb.delay(700)
			self.turn_right(3)
			pyb.delay(500)
			self.forward_with_speed(3)
			#ljh_servo.angle(0)
			#pyb.delay(zhuanjiao_delay)
		else:
			self.forward_with_speed(3)
	
	
	
	
		#检测靠左墙体是否太近
		self.servo.angle(85)
		pyb.delay(300)
		self.voice()
		if self.l<0.15:
			self.turn_right(3)
			pyb.delay(500)
			self.forward_with_speed(1)
			pyb.delay(700)
			self.turn_left(3)
			pyb.delay(600)
			self.forward_with_speed(3)
			#ljh_servo.angle(0)
			#pyb.delay(zhuanjiao_delay)
		else:
			self.forward_with_speed(3)