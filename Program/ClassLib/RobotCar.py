
from ClassLib.Car_side import Car_side
from ClassLib.Car_Lights import Car_Lights

#定义车类，调用车侧类
class  Car(object):
	def __init__(self,ENr,IN1r,IN2r,timerr,channelr,freqr,pwprr,ENl,IN1l,IN2l,timerl,channell,freql,pwprl,green_light,red_light,yellow_light):
		self.right = Car_side(ENr, IN1r, IN2r, timerr, channelr, freqr, pwprr)
		self.left  = Car_side(ENl, IN1l, IN2l, timerl, channell, freql, pwprl)
		self.lights=Car_Lights(green_light,red_light,yellow_light)
		self.command_num=0
		self.commands = {
		#前进3档
		11:[1,1],12:[1,2],13:[1,3],
		#后退三档
		21:[2,1],22:[2,2],23:[2,3],
		#左转三档
		31:[3,1],32:[3,2],33:[3,3],
		#右转三档
		41:[4,1],42:[4,2],43:[4,3],
		#刹车
		0:[0],
		#自由熄火
		-1:[-1]
		}
		
    #前进绿灯

	def forward_with_speed(self,level=1):  
			
		self.lights.all_lights_off()
		if level ==1:
			self.right.forward_with_speed(91)
			self.left.forward_with_speed(100)
		
		elif level==2:
			self.right.forward_with_speed(85)
			self.left.forward_with_speed(90)

		elif level==3:
			self.right.forward_with_speed(73)
			self.left.forward_with_speed(80)
		
		print('forward with speed on level ',level)
		
		#倒车红灯
	def back_with_speed(self,level=1): 
		self.lights.all_lights_off()
		if level ==1:
			self.right.back_with_speed(100)
			self.left.back_with_speed(93)
		
		elif level==2:
			self.right.back_with_speed(90)
			self.left.back_with_speed(87)

		elif level==3:
			self.right.back_with_speed(80)
			self.left.back_with_speed(80)
		self.lights.red_light_on()
		print('back with speed on level ',level)
		#刹车红灯
	def stop(self): 
		self.lights.all_lights_off()
		self.right.stop()
		self.left.stop()
		self.lights.red_light_on()
		print('stop')
		#熄火灭灯   
	def cutoff(self):
		self.lights.all_lights_off()
		self.right.cutoff()
		self.left.cutoff()
		print('cut off')
	#转弯黄灯亮，分三种程度，level取值1，2，3
	#1:微小偏转
	#2:中度偏转
	#3：大角度偏转，右轮刹车
	def turn_right(self,level=2):
		self.lights.all_lights_off()
		if level==1:
			self.left.forward_with_speed(100)
			self.right.forward_with_speed(80)
			print("turn right on level 1")
		elif level==2:
			self.left.forward_with_speed(100)
			self.right.forward_with_speed(65)
			print("turn right on level 2")
		elif level==3:
			self.left.forward_with_speed(100)
			self.right.forward_with_speed(0)
			print("turn right on level ",level)
		elif level==4:
			self.left.forward_with_speed(80)
			self.right.back_with_speed(80)
			print("turn right on level ",level)
		self.lights.yellow_light_on()
		
	def turn_left(self,level=2):
		self.lights.all_lights_off()
		if level==1:
			self.left.forward_with_speed(85)
			self.right.forward_with_speed(100)
			print("turn left on level 1")
		elif level==2:
			self.left.forward_with_speed(70)
			self.right.forward_with_speed(100)
			print("turn left on level 2")
		elif level==3:
			self.right.forward_with_speed(100)
			self.left.forward_with_speed(0)
			print("turn left on level ",level)
		elif level==4:
			self.right.forward_with_speed(80)
			self.left.back_with_speed(80)
			print("turn left on level ",level)
		self.lights.yellow_light_on()
		
		
	#判断self.command_num 是否符合要求	
	def command_judge(self,temp_command_num):
		if temp_command_num in self.commands.keys():
			self.command_num=temp_command_num
			return True		#输入的指令在指令集里面
		else:
			return False	#输入的指令不在指令集里面
		
	
	#执行命令，不判断
	def command_execute(self,command_num):   #输入代表指令的数字（见self.commands），查字典，执行响应指令
		if self.commands[command_num][0]==-1:
			self.cutoff()
		elif self.commands[command_num][0]==0:
			self.stop()
		elif self.commands[command_num][0]==1:
			self.forward_with_speed(self.commands[command_num][1])
		elif self.commands[command_num][0]==2:
			self.back_with_speed(self.commands[command_num][1])
		elif self.commands[command_num][0]==3:
			self.turn_left(self.commands[command_num][1])
		elif self.commands[command_num][0]==4:
			self.turn_right(self.commands[command_num][1])
			
			
	#判断命令是否符合条件并执行
	def judge_and_execute(self):
		if self.command_judge(self.command_num):
			self.command_execute(self.command_num)
		else:
			pass
		
		

def main():
	My_Car=Car(ENA,IN1,IN2,8,1,20000,0,ENB,IN3,IN4,8,2,20000,0)
	while True:
		order=input('请输入命令:')
		print('\n')
		if order=='0':
			My_Car.led_all_on()
		elif order=='1':
			My_Car.forward_with_speed(pwpx=100)
		elif order=='2':
			My_Car.back_with_speed(pwpx=80)
		elif order=='3':
			My_Car.turn_left(level=2)
		elif order=='4':
			My_Car.stop()
		elif order=='5':
			My_Car.cutoff()
		order=' '
		print('\n -----------------------------------\n')
	
class  Bluetooth_Car(Car):
	def __init__(self,ENr,IN1r,IN2r,timerr,channelr,freqr,pwprr,ENl,IN1l,IN2l,timerl,channell,freql,pwprl,green_light,red_light,yellow_light,uartx,baud_ratex=115200):
		Car.__init__(self,ENr,IN1r,IN2r,timerr,channelr,freqr,pwprr,ENl,IN1l,IN2l,timerl,channell,freql,pwprl,green_light,red_light,yellow_light)
		self.bluetooth=UART(uartx,baud_ratex)
		self.bluetooth_received_command = 0		#接收到的蓝牙数据转换成数组的值
		self.bluetooth.write("I am ready")
		pyb.delay(5) 							#略加延时（5ms）确保发送数据

	def bluetooth_receive_and_run(self):
		temp = self.bluetooth.read(bluetooth.any())
		pyb.delay(2)							#略加延时（2ms）确保收到数据
		if temp.isdigit():						#判断收到的字符串是不是数字
			temp = int(temp)					#转换收到的信号为字典commands可以识别的数值信号
			if(self.command_process(temp)==0):  #执行指令并返回指令是否符合要求
				self.bluetooth.write('wrong_input!')
			else:
				self.bluetooth.write('received!')
		else:
			self.bluetooth.write('wrong_input!')

if __name__=="__main":
	main()