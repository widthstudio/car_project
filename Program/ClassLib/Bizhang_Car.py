import pyb
from ClassLib.RobotCar import Car

class Bizhang_Car(Car):
	def __init__(self,ENr,IN1r,IN2r,timerr,channelr,freqr,pwprr,ENl,IN1l,IN2l,timerl,channell,freql,pwprl,green_light,red_light,yellow_light,servo,trig,echo):
		Car.__init__(self,ENr,IN1r,IN2r,timerr,channelr,freqr,pwprr,ENl,IN1l,IN2l,timerl,channell,freql,pwprl,green_light,red_light,yellow_light)
		self.servo=servo
		self.trig=trig		#超声波发送
		self.echo=echo		#超声波接收
		self.flag_turn = 0
		self.turn_list = [-90,90] #-90表示舵机右转，90表示左边
		
	#超声波测距函数	
	def Measure(self):		
		self.trig.value(1)	#产生Trig口所需要的高电平
		pyb.udelay(10)		#持续10us
		self.trig.value(0)
		ljh_start1=pyb.micros()
		while not self.echo.value() and pyb.micros()-ljh_start1<7000:#Echo口检测到高点平 等待7ms（约1.19m），超时跳过
			pass													
		ljh_start=pyb.micros()	#测量起始时间
		while self.echo.value() and pyb.micros()-ljh_start<7000:	#等待低电平的到来, 等待7ms，超时跳过
			pass
		ljh_end=pyb.micros()	#测量结束
		self.l=(ljh_end-ljh_start)*340.0/2/1000000		#计算距离的公式	
		return self.l
	
	
	#常用功能封装 旋转并测距 返回距离
	def Turn_and_Measure(self, angle=0):
		self.servo.angle(angle) #舵机朝向正前方，准备测正前方距离
		pyb.delay(300)		#舵机转动延时
		self.Measure()
		print(self.l)
		#self.servo.angle(0)	#回正
	
	
	
	#前方避障函数，传入速度、停车标志 参数
	#如果停车标志为 1则停车
	
	def Obstacle_Avoidance_Forward(self):
		self.Turn_and_Measure( angle=0 )
		if 0.1<self.l<0.5:				#如果正前方距离 0.1~0.8m
			self.Turn_and_Measure( angle=self.turn_list[self.flag_turn] )  #假定flag_turn = 0表示优先右转 ，测量右侧安全距离（猜-90表示右边）
			if self.l<0.4:	#如果右侧安全距离小于0.5m，说明有障碍物
				self.Turn_and_Measure( angle=self.turn_list[(self.flag_turn+1)%2] )  #测量另一侧安全距离
				if self.l<0.4:
					self.back_with_speed()
					pyb.delay(1000)
				else:
					if self.flag_turn:
						self.turn_right(4)
						pyb.delay(1000)   #右转90°时间
					else:
						self.turn_left(4)
						pyb.delay(800)	 #左转90°时间
					##self.flag_turn=(self.flag_turn+2)%2 转向优先级不变，这句就不写了
			else:
				if self.flag_turn:		
					self.turn_left(4)
					pyb.delay(800)	 #左转90°时间
				else:
					self.turn_right(4)	
					pyb.delay(1000)   #右转90°时间
				self.flag_turn=(self.flag_turn+1)%2  #下次转向改变
		elif self.l <0.1:  #如果前方安全距离小于0.1m，倒车
			self.back_with_speed()
			pyb.delay(1000)
		else:					##这句有必要吗，一开始就是直行的
			pass		
		
	#右侧避障函数
	def Obstacle_Avoidance_Right(self):
		self.Turn_and_Measure(-90)
		if self.l<0.25:
			self.turn_left(3)
			pyb.delay(500)
			self.forward_with_speed(2)
			pyb.delay(1300)
			self.turn_right(3)
			pyb.delay(800)
			
			
		#检测靠左墙体是否太近	
	def Obstacle_Avoidance_Left(self):
		self.Turn_and_Measure(+85)	
		if self.l<0.25:
			self.turn_right(3)
			pyb.delay(800)
			self.forward_with_speed(2)
			pyb.delay(1300)
			self.turn_left(3)
			pyb.delay(500)
			
	def bizhang(self,speedlevel=3,stop_flag=0):
		if stop_flag:  						#如果车辆停止标志位为 1 ，则直接退出避障函数
			return None
		self.forward_with_speed(speedlevel)	#前进
		self.Obstacle_Avoidance_Forward()
		
		self.forward_with_speed(speedlevel)	#前进
		self.Obstacle_Avoidance_Right()
		
		self.forward_with_speed(speedlevel)	#前进
		self.Obstacle_Avoidance_Left()	


def main():
	from ClassLib.RobotCar import Car
	from ClassLib.Obstacle_Avoidance_Car import Obstacle_Avoidance_Car
	from pyb import LED
	from pyb import Pin
	from pyb import Timer
	from pyb import UART
	from pyb import Servo

	ENA=Pin('Y1',Pin.OUT_PP)
	ENB=Pin('Y2',Pin.OUT_PP)

	IN1=Pin('Y3',Pin.OUT_PP)
	IN2=Pin('Y4',Pin.OUT_PP)
	IN3=Pin('Y5',Pin.OUT_PP)
	IN4=Pin('Y6',Pin.OUT_PP)

	ECHO=Pin('Y11',Pin.OUT_PP)
	TRIG=Pin('Y12',Pin.OUT_PP)

	My_Servo=Servo(1)

	red_light	= Pin(Pin.cpu.A13,Pin.OUT_PP)
	green_light	= Pin(Pin.cpu.A14,Pin.OUT_PP)
	yellow_light= Pin(Pin.cpu.A15,Pin.OUT_PP)

	uart=UART(1,115200)
	uart.write("I am ready")
	pyb.delay(10)

	My_Car=Obstacle_Avoidance_Car(ENA,IN1,IN2,8,1,20000,0,ENB,IN3,IN4,8,2,20000,0,green_light,red_light,yellow_light,My_Servo,TRIG,ECHO)

	while True:
		My_Car.Obstacle_Avoidance(speedlevel=3,stop_flag=0)
	
if __name__=='__main__':
	main()
			
	'''		
	
	def bizhang(self):
		self.forward_with_speed(3)	#全速前进	
		
		#检测前方障碍物时
		#转弯优先级右转高左转低
		if self.flag_turn%2==0:
			self.servo.angle(0) #舵机朝向正前方，准备测正前方距离
			pyb.delay(300)		#舵机转动延时
			self.voice()		#测量正前方距离
			if 0.1<self.l<0.8:	#如果正前方距离 0.1~0.8m
				self.servo.angle(-90) #测量
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
				print(2222)
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
			'''