import pyb
from pyb import LED
from pyb import Pin
from pyb import Timer
from pyb import UART
from ClassLib.RobotCar import Car



class  Bluetooth_Car(Car):
	def __init__(self,ENr,IN1r,IN2r,timerr,channelr,freqr,pwprr,ENl,IN1l,IN2l,timerl,channell,freql,pwprl,green_light,red_light,yellow_light,uartx,baud_ratex=9600):
		Car.__init__(self,ENr,IN1r,IN2r,timerr,channelr,freqr,pwprr,ENl,IN1l,IN2l,timerl,channell,freql,pwprl,green_light,red_light,yellow_light)
		self.bluetooth=UART(uartx,baud_ratex)
		self.bluetooth_received_command = 0		#接收到的蓝牙数据转换成数组的值
		self.command_string=''
		self.bluetooth.write("I am ready!")
		print("I am ready!")
		pyb.delay(5) 							#略加延时（5ms）确保发送数据
		
	def read_command_string_and_judge(self):
		#读取蓝牙信息
		#self.command_string=self.bluetooth.read(self.bluetooth.any())
		self.command_string=input("input:")
		pyb.delay(5)	
		print(self.command_string)
		#判断command_string是否符合指令格式 ，即是否是字典中的关键字数字
		if self.command_string.isdigit() :		#判断命令是不是数字格式，是就转换成int类型
			self.command_num=int(self.command_string)
			if self.command_judge():  				#判断数字是不是符合命令格式
				return 1
			else:
				print('wrong')
				return 0
		else:
			return 0
			
	def bluetooth_receive_and_run(self):
		if self.read_command_string_and_judge() :
			self.command_execute(self.command_num)
		else:
			pass
			
