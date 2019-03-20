import pyb
from pyb import LED
from pyb import Pin
from pyb import Timer
from pyb import UART
from ClassLib.Wheels import Wheels 
from ClassLib.PWMTimer import PWMTimer
from ClassLib.Car_side import Carside
from ClassLib.CarLights import CarLights
from ClassLib.RobotCar import Car



class  Bluetooth_Car(Car):
	def __init__(self,ENr,IN1r,IN2r,timerr,channelr,freqr,pwprr,ENl,IN1l,IN2l,timerl,channell,freql,pwprl,green_light,red_light,yellow_light,uartx,baud_ratex=115200):
		Car.__init__(self,ENr,IN1r,IN2r,timerr,channelr,freqr,pwprr,ENl,IN1l,IN2l,timerl,channell,freql,pwprl,green_light,red_light,yellow_light)
		self.bluetooth=UART(uartx,baud_ratex)
		self.bluetooth_received_command = 0		#接收到的蓝牙数据转换成数组的值
		self.bluetooth.write("I am ready!")
		print("I am ready!")
		pyb.delay(5) 							#略加延时（5ms）确保发送数据

	def bluetooth_receive_and_run(self):
		temp = self.bluetooth.read(self.bluetooth.any())
		print(temp)
		pyb.delay(5)							#略加延时（2ms）确保收到数据
		if temp.isdigit():						#判断收到的字符串是不是数字
			temp = int(temp)					#转换收到的信号为字典commands可以识别的数值信号
			if(self.command_process(temp)==0):  #执行指令并返回指令是否符合要求
				self.bluetooth.write('wrong_input!')
				print('wrong_input!')
			else:
				self.bluetooth.write('received!')
				print('received!')
		elif temp==b'':
			pass
		else:
			self.bluetooth.write('wrong_input!')
			print('wrong_input!')